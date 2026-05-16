"""Public data utilities for the intraday deviation factor demo.

This module intentionally supports only local sample/mock CSV files. It does
not contain private data vendors, real symbol mappings, or private paths.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = ["datetime", "open", "high", "low", "close", "volume"]


def read_intraday_csv(path: str | Path, symbol: str | None = None) -> pd.DataFrame:
    """Read a public demo OHLCV CSV and normalize common research columns."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["symbol"] = symbol or df.get("symbol", "DEMO")
    df["date"] = df["datetime"].dt.normalize()
    df["time"] = df["datetime"].dt.strftime("%H:%M")
    df["elapsed_minutes"] = (
        df["datetime"].dt.hour * 60
        + df["datetime"].dt.minute
        - int(df["datetime"].dt.hour.min()) * 60
    )
    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values(["symbol", "datetime"]).reset_index(drop=True)


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sample_path(name: str) -> Path:
    return project_root() / "sample_data" / name


def output_path(name: str) -> Path:
    out_dir = project_root() / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / name
