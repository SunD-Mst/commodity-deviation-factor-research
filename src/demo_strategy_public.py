"""Simplified public strategy interface for demonstration only.

The functions in this module are placeholders. They are intentionally not the
private research rules and should not be treated as deployable trading logic.
"""

from __future__ import annotations

import pandas as pd


def example_signal(row: pd.Series, threshold: float = 0.75) -> bool:
    """Public example signal.

    公开版示例逻辑，真实研究规则未披露。
    """
    value = row.get("deviation_pct")
    return bool(pd.notna(value) and float(value) >= threshold)


def simplified_rule(day_df: pd.DataFrame) -> str:
    """Return a demo action label for a single day.

    公开版示例逻辑，真实研究规则未披露。
    """
    if day_df.empty or "deviation_pct" not in day_df.columns:
        return "no_action"
    if day_df["deviation_pct"].max(skipna=True) >= 0.75:
        return "demo_watch"
    return "no_action"


def demo_strategy(factor_df: pd.DataFrame) -> pd.DataFrame:
    """Run a lightweight demo strategy summary by day."""
    rows: list[dict] = []
    for (symbol, date), day_df in factor_df.groupby(["symbol", "date"], sort=True):
        action = simplified_rule(day_df)
        rows.append(
            {
                "symbol": symbol,
                "date": date,
                "demo_action": action,
                "max_demo_percentile": float(day_df["deviation_pct"].max(skipna=True)),
            }
        )
    return pd.DataFrame(rows)
