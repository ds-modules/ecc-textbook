#!/usr/bin/env python3
"""Extract a small teaching sample from the large IndPenSim V3 time-series CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_V3 = REPO_ROOT / "Enzymes and DNA/Mendeley_data/100_Batches_IndPenSim_V3.csv"
DEFAULT_STATS = REPO_ROOT / "Enzymes and DNA/Mendeley_data/100_Batches_IndPenSim_Statistics.csv"
DEFAULT_OUTPUT = REPO_ROOT / "Enzymes and DNA/Mendeley_data/data/teaching_batches_timeseries.csv"

TEACHING_COLUMNS = [
    "Time (h)",
    "Substrate concentration(S:g/L)",
    "Dissolved oxygen concentration(DO2:mg/L)",
    "Penicillin concentration(P:g/L)",
    "pH(pH:pH)",
    "Temperature(T:K)",
    "carbon dioxide percent in off-gas(CO2outgas:%)",
    "Sugar feed rate(Fs:L/h)",
    "Aeration rate(Fg:L/h)",
    "Agitator RPM(RPM:RPM)",
    "Oxygen Uptake Rate(OUR:(g min^{-1}))",
    "Offline Biomass concentratio(X_offline:X(g L^{-1}))",
    "Fault reference(Fault_ref:Fault ref)",
    "Batch_Number",
]

# First 39 columns in V3 are process/metadata; column 40+ are Raman/spectroscopy.
V3_PROCESS_COLUMNS = [
    "Time (h)",
    "Aeration rate(Fg:L/h)",
    "Agitator RPM(RPM:RPM)",
    "Sugar feed rate(Fs:L/h)",
    "Acid flow rate(Fa:L/h)",
    "Base flow rate(Fb:L/h)",
    "Heating/cooling water flow rate(Fc:L/h)",
    "Heating water flow rate(Fh:L/h)",
    "Water for injection/dilution(Fw:L/h)",
    "Air head pressure(pressure:bar)",
    "Dumped broth flow(Fremoved:L/h)",
    "Substrate concentration(S:g/L)",
    "Dissolved oxygen concentration(DO2:mg/L)",
    "Penicillin concentration(P:g/L)",
    "Vessel Volume(V:L)",
    "Vessel Weight(Wt:Kg)",
    "pH(pH:pH)",
    "Temperature(T:K)",
    "Generated heat(Q:kJ)",
    "carbon dioxide percent in off-gas(CO2outgas:%)",
    "PAA flow(Fpaa:PAA flow (L/h))",
    "PAA concentration offline(PAA_offline:PAA (g L^{-1}))",
    "Oil flow(Foil:L/hr)",
    "NH_3 concentration off-line(NH3_offline:NH3 (g L^{-1}))",
    "Oxygen Uptake Rate(OUR:(g min^{-1}))",
    "Oxygen in percent in off-gas(O2:O2  (%))",
    "Offline Penicillin concentration(P_offline:P(g L^{-1}))",
    "Offline Biomass concentratio(X_offline:X(g L^{-1}))",
    "Carbon evolution rate(CER:g/h)",
    "Ammonia shots(NH3_shots:kgs)",
    "Viscosity(Viscosity_offline:centPoise)",
    "Fault reference(Fault_ref:Fault ref)",
    "0 - Recipe driven 1 - Operator controlled(Control_ref:Control ref)",
    "1- No Raman spec",
    " 1-Raman spec recorded",
    "2-PAT control(PAT_ref:PAT ref)",
    "Batch reference(Batch_ref:Batch ref)",
    "Batch ID",
    "Fault flag",
]


def default_batch_numbers(stats_path: Path) -> list[int]:
    """Pick one high-yield, low-yield, faulty, and normal batch."""
    stats = pd.read_csv(stats_path)
    yield_col = "Penicllin_yield_total (kg)"
    fault_col = "Fault ref(0-NoFault 1-Fault)"
    batch_col = "Batch ref"

    high = stats.sort_values(yield_col, ascending=False)
    low = stats.sort_values(yield_col, ascending=True)

    high_yield = int(high.iloc[0][batch_col])
    low_yield = int(low.iloc[0][batch_col])

    faulty = stats[stats[fault_col] == 1]
    faulty_batch = int(faulty.sort_values(yield_col, ascending=False).iloc[0][batch_col])

    normal = stats[(stats[fault_col] == 0) & (stats[batch_col] == 1)]
    normal_batch = int(normal.iloc[0][batch_col]) if not normal.empty else 1

    low_non_fault = stats[stats[fault_col] == 0].sort_values(yield_col, ascending=True)
    low_non_fault_batch = int(low_non_fault.iloc[0][batch_col])

    return sorted(set([normal_batch, high_yield, low_yield, faulty_batch, low_non_fault_batch]))


def extract_batches(
    v3_path: Path,
    output_path: Path,
    batch_numbers: list[int],
    chunksize: int = 50_000,
) -> None:
    time_col = "Time (h)"
    selected: list[pd.DataFrame] = []
    current_batch = 1
    previous_time: float | None = None
    current_rows: list[dict] = []

    reader = pd.read_csv(
        v3_path,
        usecols=V3_PROCESS_COLUMNS,
        chunksize=chunksize,
        low_memory=False,
    )

    def flush_batch() -> None:
        nonlocal current_rows, current_batch
        if not current_rows:
            return
        if current_batch in batch_numbers:
            batch_df = pd.DataFrame(current_rows)
            batch_df["Batch_Number"] = current_batch
            selected.append(batch_df)
        current_rows = []

    for chunk in reader:
        for _, row in chunk.iterrows():
            time_value = float(row[time_col])
            if previous_time is not None and time_value < previous_time - 0.05:
                flush_batch()
                current_batch += 1
            previous_time = time_value
            current_rows.append(row.to_dict())

    flush_batch()

    if not selected:
        raise RuntimeError("No rows extracted. Check batch numbers and input file.")

    result = pd.concat(selected, ignore_index=True)
    output_columns = [col for col in TEACHING_COLUMNS if col in result.columns]
    result = result[output_columns]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    print(f"Saved {len(result):,} rows across {result['Batch_Number'].nunique()} batches")
    print(f"Batch numbers: {sorted(result['Batch_Number'].unique())}")
    print(f"Output: {output_path} ({output_path.stat().st_size / 1024 / 1024:.2f} MB)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v3", type=Path, default=DEFAULT_V3)
    parser.add_argument("--stats", type=Path, default=DEFAULT_STATS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--batches",
        type=int,
        nargs="+",
        help="Batch numbers to include (default: auto-select from statistics file)",
    )
    args = parser.parse_args()

    if not args.v3.exists():
        raise FileNotFoundError(f"V3 file not found: {args.v3}")

    batch_numbers = args.batches or default_batch_numbers(args.stats)
    extract_batches(args.v3, args.output, batch_numbers)


if __name__ == "__main__":
    main()
