"""Export Tscreener 1m parquet bars -> one CSV per symbol for ReplayMobile.

  python export_csv.py            # all symbols
  python export_csv.py AAPL NVDA  # only these
Output: ReplayMobile/csv/<SYM>.csv  (time,open,high,low,close,volume)
"""
import sys, glob, os
import pandas as pd

SRC = os.path.join(os.path.dirname(__file__), "..", "tscreener", "data", "bars", "minute")
OUT = os.path.join(os.path.dirname(__file__), "csv")
os.makedirs(OUT, exist_ok=True)

want = [s.upper() for s in sys.argv[1:]]
syms = [d for d in sorted(os.listdir(SRC)) if os.path.isdir(os.path.join(SRC, d))]
if want:
    syms = [s for s in syms if s in want]

for sym in syms:
    files = sorted(glob.glob(os.path.join(SRC, sym, "*.parquet")))
    if not files:
        continue
    df = pd.concat([pd.read_parquet(f) for f in files]).sort_index()
    df = df[~df.index.duplicated()]
    out = pd.DataFrame({
        "time": df.index.tz_convert("America/New_York").strftime("%Y-%m-%d %H:%M"),
        "open": df.Open, "high": df.High, "low": df.Low,
        "close": df.Close, "volume": df.Volume,
    })
    p = os.path.join(OUT, f"{sym}.csv")
    out.to_csv(p, index=False)
    print(f"{sym}: {len(out)} bars, {len(files)} days -> {p}")
