"""Shared data setup for Zillow exercises notebooks."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ZHVI_URL = (
    "https://files.zillowstatic.com/research/public_csvs/zhvi/"
    "Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
)
ZORI_URL = (
    "https://files.zillowstatic.com/research/public_csvs/zori/"
    "Metro_zori_uc_sfrcondomfr_sm_month.csv"
)


def _classify_market(value: float) -> str:
    if value >= 800000:
        return "Luxury"
    if value >= 500000:
        return "Premium"
    if value >= 300000:
        return "Mid-Range"
    return "Affordable"


def load_exercise_data(
    verbose: bool = True,
    use_cache: bool = True,
    force_refresh: bool = False,
) -> dict[str, pd.DataFrame]:
    """Build and return all DataFrames required by the exercises notebook."""
    cache_file = Path(__file__).resolve().parent / ".cache" / "zillow_exercise_data.pkl"

    if use_cache and not force_refresh and cache_file.exists():
        data = pd.read_pickle(cache_file)
        if verbose:
            print("⚡ Loaded cached Zillow exercise data")
            print(f"home_values: {data['home_values'].shape}")
            print(f"home_values_latest: {data['home_values_latest'].shape}")
            print(f"latest_home_values_copy: {data['latest_home_values_copy'].shape}")
            print(f"housing_combined: {data['housing_combined'].shape}")
        return data

    home_values_wide = pd.read_csv(ZHVI_URL)
    rent_values_wide = pd.read_csv(ZORI_URL)

    meta_cols = [
        "RegionID",
        "SizeRank",
        "RegionName",
        "RegionType",
        "StateName",
        "State",
        "City",
        "Metro",
        "CountyName",
    ]
    meta_cols = [c for c in meta_cols if c in home_values_wide.columns]

    home_date_cols = [c for c in home_values_wide.columns if c not in meta_cols]
    home_values = pd.melt(
        home_values_wide,
        id_vars=meta_cols,
        value_vars=home_date_cols,
        var_name="Date",
        value_name="HomeValue",
    )
    home_values["Date"] = pd.to_datetime(home_values["Date"])
    home_values = home_values.dropna(subset=["HomeValue"])
    home_values["Year"] = home_values["Date"].dt.year

    rent_meta_cols = [c for c in meta_cols if c in rent_values_wide.columns]
    rent_date_cols = [c for c in rent_values_wide.columns if c not in rent_meta_cols]
    rent_values = pd.melt(
        rent_values_wide,
        id_vars=rent_meta_cols,
        value_vars=rent_date_cols,
        var_name="Date",
        value_name="Rent",
    )
    rent_values["Date"] = pd.to_datetime(rent_values["Date"])
    rent_values = rent_values.dropna(subset=["Rent"])

    latest_date = home_values["Date"].max()
    home_values_latest = home_values[home_values["Date"] == latest_date].copy()

    latest_home_values_copy = home_values_latest.copy()
    latest_home_values_copy["MarketTier"] = latest_home_values_copy["HomeValue"].apply(_classify_market)

    latest_rent_values = rent_values[rent_values["Date"] == rent_values["Date"].max()][["RegionName", "Rent"]]
    housing_combined = home_values_latest.merge(latest_rent_values, on="RegionName", how="inner")
    housing_combined["Annual_Rent"] = housing_combined["Rent"] * 12
    housing_combined["Price_to_Rent"] = (housing_combined["HomeValue"] / housing_combined["Annual_Rent"]).round(1)
    housing_combined["Buy_vs_Rent"] = np.select(
        [
            housing_combined["Price_to_Rent"] < 15,
            housing_combined["Price_to_Rent"] > 20,
        ],
        ["Lean Buy", "Lean Rent"],
        default="Neutral",
    )

    data = {
        "home_values_wide": home_values_wide,
        "rent_values_wide": rent_values_wide,
        "home_values": home_values,
        "rent_values": rent_values,
        "home_values_latest": home_values_latest,
        "latest_home_values_copy": latest_home_values_copy,
        "housing_combined": housing_combined,
    }

    if use_cache:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        pd.to_pickle(data, cache_file)

    if verbose:
        print("✅ Setup complete: exercise variables are ready")
        print(f"home_values: {home_values.shape}")
        print(f"home_values_latest: {home_values_latest.shape}")
        print(f"latest_home_values_copy: {latest_home_values_copy.shape}")
        print(f"housing_combined: {housing_combined.shape}")

    return data
