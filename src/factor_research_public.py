"""Public intraday deviation factor research demo.

This file keeps the research framework runnable while using mock data and
demonstration parameters. Sensitive private rules and private parameter
search spaces are intentionally not included.
"""

from __future__ import annotations

import matplotlib
from pathlib import Path

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from event_study_public import build_event_summary
from demo_strategy_public import demo_strategy
from quant_data_public import output_path, read_intraday_csv, sample_path


DEMO_CONFIG = {
    "opening_minutes": 30,
    "atr_window_days": 2,
    "thresholds": [0.75, 0.90],
    "holding_windows": [15, 30],
}


def compute_opening_range(df: pd.DataFrame, opening_minutes: int = 30) -> pd.DataFrame:
    opening_rows = df[df["elapsed_minutes"] < opening_minutes]
    grouped = opening_rows.groupby(["symbol", "date"], as_index=False).agg(
        OR_high=("high", "max"),
        OR_low=("low", "min"),
    )
    grouped["OR_mid"] = (grouped["OR_high"] + grouped["OR_low"]) / 2
    return grouped


def add_atr(df: pd.DataFrame, window_days: int = 2) -> pd.DataFrame:
    daily = df.groupby(["symbol", "date"], as_index=False).agg(
        daily_high=("high", "max"),
        daily_low=("low", "min"),
        daily_close=("close", "last"),
    )
    daily["daily_range"] = daily["daily_high"] - daily["daily_low"]
    daily["prev_atr"] = (
        daily.groupby("symbol")["daily_range"]
        .transform(lambda s: s.shift(1).rolling(window_days, min_periods=1).mean())
    )
    return df.merge(daily[["symbol", "date", "prev_atr"]], on=["symbol", "date"], how="left")


def add_deviation_factor(df: pd.DataFrame) -> pd.DataFrame:
    opening_range = compute_opening_range(df, DEMO_CONFIG["opening_minutes"])
    work = df.merge(opening_range, on=["symbol", "date"], how="left")
    work = add_atr(work, DEMO_CONFIG["atr_window_days"])
    work["abs_deviation"] = (work["close"] - work["OR_mid"]).abs() / work["prev_atr"]
    return work


def add_historical_percentile(df: pd.DataFrame) -> pd.DataFrame:
    """Add same-time historical percentile using prior dates only."""
    rows: list[pd.DataFrame] = []
    for symbol, symbol_df in df.groupby("symbol", sort=False):
        symbol_df = symbol_df.sort_values("datetime").copy()
        pct_values = []
        for _, row in symbol_df.iterrows():
            history = symbol_df[
                (symbol_df["date"] < row["date"])
                & (symbol_df["time"] == row["time"])
                & symbol_df["abs_deviation"].notna()
            ]["abs_deviation"]
            if history.empty or pd.isna(row["abs_deviation"]):
                pct_values.append(np.nan)
            else:
                pct_values.append(float((history <= row["abs_deviation"]).mean()))
        symbol_df["deviation_pct"] = pct_values
        rows.append(symbol_df)
    return pd.concat(rows, ignore_index=True)


def build_factor_frame(csv_path: str | Path) -> pd.DataFrame:
    raw = read_intraday_csv(csv_path)
    factor_df = add_deviation_factor(raw)
    factor_df = add_historical_percentile(factor_df)
    return factor_df


def plot_demo_curve(factor_df: pd.DataFrame) -> None:
    curve = (
        factor_df.dropna(subset=["deviation_pct"])
        .groupby("elapsed_minutes", as_index=False)["deviation_pct"]
        .mean()
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(curve["elapsed_minutes"], curve["deviation_pct"], marker="o", linewidth=1.5)
    ax.set_title("Demo Mean Same-Time Percentile Curve")
    ax.set_xlabel("Elapsed minutes")
    ax.set_ylabel("Mean percentile")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path("demo_deviation_curve.png"), dpi=140)
    plt.close(fig)


def run_public_demo() -> dict[str, pd.DataFrame]:
    factor_df = build_factor_frame(sample_path("sample_intraday_15m.csv"))
    event_summary = build_event_summary(
        factor_df,
        thresholds=DEMO_CONFIG["thresholds"],
        holding_windows=DEMO_CONFIG["holding_windows"],
    )
    strategy_summary = demo_strategy(factor_df.dropna(subset=["deviation_pct"]))

    factor_df.to_csv(output_path("demo_factor_rows.csv"), index=False)
    event_summary.to_csv(output_path("demo_event_summary.csv"), index=False)
    strategy_summary.to_csv(output_path("demo_strategy_summary.csv"), index=False)
    plot_demo_curve(factor_df)
    return {
        "factor_df": factor_df,
        "event_summary": event_summary,
        "strategy_summary": strategy_summary,
    }


if __name__ == "__main__":
    result = run_public_demo()
    print("Demo factor rows:", len(result["factor_df"]))
    print("Demo event summary:")
    print(result["event_summary"].to_string(index=False))
    print("Demo strategy summary:")
    print(result["strategy_summary"].head().to_string(index=False))
