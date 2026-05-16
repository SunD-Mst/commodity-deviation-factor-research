"""Public event-study helpers for the deviation factor demo."""

from __future__ import annotations

import pandas as pd


DEMO_THRESHOLDS = [0.75, 0.90]
DEMO_HOLDING_WINDOWS = [15, 30]


def build_event_summary(
    factor_df: pd.DataFrame,
    thresholds: list[float] | None = None,
    holding_windows: list[int] | None = None,
) -> pd.DataFrame:
    """Summarize later high-deviation frequency after demo threshold events.

    Public version note: these thresholds and holding windows are deliberately
    small demonstration values. Private research ranges and decision rules are
    not disclosed.
    """
    thresholds = thresholds or DEMO_THRESHOLDS
    holding_windows = holding_windows or DEMO_HOLDING_WINDOWS

    rows: list[dict] = []
    work = factor_df.dropna(subset=["deviation_pct"]).copy()
    for threshold in thresholds:
        for holding_window in holding_windows:
            event_rows = []
            for (_, date), day_df in work.groupby(["symbol", "date"], sort=True):
                day_df = day_df.sort_values("datetime").reset_index(drop=True)
                event_idx = day_df.index[day_df["deviation_pct"] >= threshold]
                if len(event_idx) == 0:
                    continue
                start = int(event_idx[0])
                future = day_df.iloc[start + 1 : start + 1 + max(1, holding_window // 15)]
                if future.empty:
                    continue
                event_rows.append(
                    {
                        "symbol": day_df.loc[start, "symbol"],
                        "date": date,
                        "future_max_pct": float(future["deviation_pct"].max()),
                    }
                )
            events = pd.DataFrame(event_rows)
            rows.append(
                {
                    "threshold": threshold,
                    "holding_window_minutes": holding_window,
                    "event_days": int(len(events)),
                    "demo_hit_rate": (
                        float((events["future_max_pct"] >= threshold).mean())
                        if not events.empty
                        else float("nan")
                    ),
                }
            )
    return pd.DataFrame(rows)

