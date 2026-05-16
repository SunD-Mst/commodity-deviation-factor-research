# Commodity Intraday Deviation Factor Research (Public Demo)

This public version demonstrates a research workflow for intraday commodity futures deviation factors. It is designed for portfolio and interview review: the code is runnable, the research structure is complete, and sensitive trading details are intentionally simplified.

## Project Goal

Build a reproducible framework for studying whether opening-range deviation structure can describe later intraday volatility states.

The public repository focuses on research process rather than deployable trading rules:

- data loading and timestamp normalization
- opening-range reference construction
- ATR-normalized deviation factor calculation
- historical same-time percentile calculation
- event-study style validation
- multi-curve visualization
- simplified strategy research interface

## Research Question

Can the early-session deviation from the opening-range midpoint provide useful information about later intraday deviation behavior?

This public demo uses mock data and neutral example parameters. It should not be interpreted as a trading recommendation or as a disclosure of private research rules.

## Factor Definition

- `OR_mid`: midpoint of the opening range.
- `abs_deviation`: absolute distance between close and `OR_mid`, normalized by previous ATR.
- `deviation_pct`: historical same-time percentile of current `abs_deviation`, calculated with prior dates only.

## Research Workflow

1. Load sample intraday OHLCV data.
2. Build opening-range high, low, and midpoint.
3. Calculate prior ATR and normalized deviation.
4. Rebuild historical same-time percentiles without future leakage.
5. Run a small event study with demonstration thresholds.
6. Generate demo curves and a demo summary.
7. Run a simplified strategy interface with placeholder logic.

## Project Structure

```text
public_commodity_deviation_factor_research/
  README.md
  requirements.txt
  sample_data/
    sample_intraday_15m.csv
    sample_intraday_1m.csv
  src/
    quant_data_public.py
    factor_research_public.py
    event_study_public.py
    demo_strategy_public.py
  notebooks/
    public_factor_research_demo.ipynb
  outputs/
    .gitkeep
```

## How To Run

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the public demo:

```powershell
python src/factor_research_public.py
```

Expected demo outputs:

- `outputs/demo_factor_rows.csv`
- `outputs/demo_event_summary.csv`
- `outputs/demo_deviation_curve.png`
- `outputs/demo_strategy_summary.csv`

These outputs are generated from mock data and are only intended to demonstrate the research framework.

## Desensitization Notes

The public version does not include:

- real intraday market data
- full parameter search ranges
- private filter combinations
- effective strategy decision logic
- private research reports
- complete backtest trade logs
- complete event-result CSV files

The strategy module uses `simplified_rule()` and `demo_strategy()` as public placeholders. Comments in the code mark them as demonstration logic; private research rules are not disclosed.

## What This Demo Shows

This project is meant to show the engineering and research workflow behind a factor study:

- clean data interfaces
- leakage-aware historical features
- event-study design
- visualization pipeline
- basic strategy-prototyping interface
- risk-aware public communication
