# ReplayMobile

Offline bar-by-bar replay for 1-minute backtesting. One HTML file, runs in Android Chrome,
no internet needed once installed.

---

## 1. Get your data out of Tscreener (on the PC, once per refresh)

Your 1-minute bars live in `Tscreener-Production/tscreener/data/bars/minute/<SYMBOL>/<DATE>.parquet`.
`export_csv.py` turns them into CSV files this app can read.

**Where to run it:** any terminal (PowerShell is fine), from this folder.

```powershell
cd "D:\FUN projects\AI\Strategies\DAVID_SPARTAN\Tscreener-Production\ReplayMobile"
python export_csv.py
```

That writes one file per symbol into `ReplayMobile\csv\` — e.g. `csv\NVDA.csv`.
Only some symbols:

```powershell
python export_csv.py NVDA AAPL
```

It uses the same `pandas` the main project already has, so there is nothing to install.
Re-run it whenever the pipeline has pulled newer minute bars.

**The file name becomes the symbol name** in the app's dropdown.

### Using data from somewhere else
Any CSV works as long as the first line is a header containing
`time, open, high, low, close, volume` (any order; comma, semicolon or tab separated).
An optional `delta` column is used for the delta-volume pane. Without it, delta falls back
to ±volume by candle direction.

---

## 2. Put it on the phone

The phone needs to fetch the page once over http (a service worker can't install from a
`file://` page). From the **project root**, not this folder:

```powershell
cd "D:\FUN projects\AI\Strategies\DAVID_SPARTAN\Tscreener-Production"
python -m http.server 8080
```

Find the PC's LAN IP (`ipconfig` → IPv4 Address), then on the phone open:

```
http://<that-ip>:8080/ReplayMobile/
```

Chrome menu → **Add to Home screen**. From then on it opens offline, PC off.

## 3. Load the bars

Tap **CSV** and multi-select your files. Two ways to have them on the phone:

- **USB / Google Drive:** copy the `ReplayMobile\csv` folder to the phone's Downloads, then
  pick them from the file chooser.
- **Straight off the server:** while the `http.server` is running, browse to
  `http://<ip>:8080/ReplayMobile/csv/` on the phone and tap each file to download it, then
  load them from Downloads.

Bars go into IndexedDB on the phone. The PC is not needed again. Loading a symbol again
replaces its bars and **resets its session**.

---

## Controls

**Top bar** — ticker box (tap it to load CSVs; last entry in the list is "＋ Load CSV…") ·
timeframe (1m…1D) · drawing-tools dropdown (freehand, trend line, area box, clear) ·
indicators · stats · reset session · delete symbol.

**Indicators** — tap the wave icon. Volume and Delta volume are on by default and can be toggled off.
Add as many SMA / EMA / Bollinger Bands / Stochastic as you like and edit lengths live.
Your choices are remembered across symbols.

**Readout rows** — symbol/time/bar counter, then O H L C V Δ for the current bar,
then position, unrealised P/L, cash and equity, then live indicator values.

**Panes** — candles plus whichever indicator panes you have switched on. The equity curve now lives in Stats.

**Order pad** — BUY / SELL go in all-in at the current close. FLAT closes.
BUY STP / SELL STP drop a stop line near price; **drag it anywhere with your finger**.
A buy stop fires when a bar's high reaches it, a sell stop when a bar's low reaches it —
so it's an entry when you're flat and a stop-loss when you're in.

**Bottom bar** — `◀◀` back 10 · `◀` back 1 · `▶‖` autoplay · `▶` forward 1 ·
`⏭` run to the end and show stats. Everything moves one **1-minute** bar at a time;
higher timeframes build up progressively, so the right-hand candle is a forming one.

**Drawings are anchored to time and price**, not to screen position — mark an area on the
60m chart, drop to 1m, and it's still over the same bars.

**Going back truly rewinds**: trades, cash, position and the equity curve are restored to
how they were at that bar.

**RST** wipes trades, cash, equity and position and sends the cursor back to the start of
the session. Drawings survive.

## Stats

`STATS` (bar-chart icon) any time, or automatically at `⏭` / end of autoplay:

cash start → end, P/L and %, max drawdown, buy-&-hold P/L and drawdown over the exact same
replayed period, the difference against that benchmark, closed trades, win rate, profit
factor, average trade.

Starting cash is 10,000 and each entry is all-in (`floor(equity / price)` shares), so the
equity curve and the benchmark are directly comparable.

---

## Notes

Self-check: open `index.html?test` and look at the console (or run the same asserts under
node — see git history of this file).

`ponytail:` bars are stored as one array per symbol in IndexedDB. Fine to ~1–2M bars per
phone; chunk by day if loading gets slow. Fixed 80-bar window, no pinch-zoom yet.
