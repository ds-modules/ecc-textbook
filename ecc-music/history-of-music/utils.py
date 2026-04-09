"""Load and visualize Spotify-style track analytics by genre (2015–2025 export).

Expects a parquet or CSV with columns like ``track_name``, ``artist_name``,
``release_date``, ``genre``, audio features, ``popularity``, ``explicit``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DEFAULT_SPOTIFY_STEM = "spotify_2015_2025_85k"

YEAR_MIN_DEFAULT = 2015
YEAR_MAX_DEFAULT = 2025

FEATURE_COLS_SPOTIFY_EXPORT = [
    "danceability",
    "energy",
    "instrumentalness",
    "tempo",
    "loudness",
]

CORE_FEATURE_COLS = ["energy", "danceability", "tempo", "loudness", "instrumentalness"]

DEFAULT_SPOTIFY_COLMAP: dict[str, str] = {
    "track_name": "track_name",
    "artist_name": "artist_name",
    "release_date": "release_date",
    "genre": "genre",
    "popularity": "popularity",
    "explicit": "explicit",
    **{k: k for k in FEATURE_COLS_SPOTIFY_EXPORT},
}


def load_table(path: str | Path) -> pd.DataFrame:
    p = Path(path)
    if p.suffix.lower() in {".parquet", ".pq"}:
        return pd.read_parquet(p)
    if p.suffix.lower() == ".csv":
        return pd.read_csv(p)
    raise ValueError(f"Unsupported file type: {p}")


def load_spotify(path: str | Path, colmap: Mapping[str, str] | None = None) -> pd.DataFrame:
    colmap = dict(DEFAULT_SPOTIFY_COLMAP if colmap is None else colmap)
    df = load_table(path)
    for logical, actual in colmap.items():
        if actual not in df.columns:
            raise KeyError(f"Spotify column '{actual}' ({logical}) not in file: {path}")
    return df


def spotify_to_song_table(spotify: pd.DataFrame, colmap: Mapping[str, str] | None = None) -> pd.DataFrame:
    """One row per track with columns ``Song``, ``Artist``, features, etc."""
    colmap = dict(DEFAULT_SPOTIFY_COLMAP if colmap is None else colmap)
    sp = spotify.copy()
    out = pd.DataFrame(
        {
            "Song": sp[colmap["track_name"]],
            "Artist": sp[colmap["artist_name"]],
            "genre": sp[colmap["genre"]],
            "popularity": pd.to_numeric(sp[colmap["popularity"]], errors="coerce"),
            "release_date": sp[colmap["release_date"]],
            "explicit": pd.to_numeric(sp[colmap["explicit"]], errors="coerce").fillna(0),
        }
    )
    for c in FEATURE_COLS_SPOTIFY_EXPORT:
        out[c] = pd.to_numeric(sp[colmap[c]], errors="coerce")
    return out


def load_prepared_spotify(
    path: str | Path,
    *,
    colmap: Mapping[str, str] | None = None,
    year_min: int = YEAR_MIN_DEFAULT,
    year_max: int = YEAR_MAX_DEFAULT,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Load Spotify export and return cleaned rows plus simple load stats."""
    raw = load_spotify(path, colmap)
    info: dict[str, Any] = {"rows_loaded": len(raw)}
    canon = spotify_to_song_table(raw, colmap)
    prepared = prepare_analysis_df(canon, year_min=year_min, year_max=year_max)
    info["rows_after_cleaning"] = len(prepared)
    return prepared, info


def prepare_analysis_df(
    df: pd.DataFrame,
    *,
    year_min: int = YEAR_MIN_DEFAULT,
    year_max: int = YEAR_MAX_DEFAULT,
) -> pd.DataFrame:
    """Parse release year, filter range, add popularity_scaled."""
    out = df.copy()
    out["release_date"] = pd.to_datetime(out["release_date"], errors="coerce")
    out = out.dropna(subset=["release_date"])
    out["year"] = out["release_date"].dt.year.astype(int)
    out = out[(out["year"] >= year_min) & (out["year"] <= year_max)].copy()

    for c in CORE_FEATURE_COLS:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    out["popularity"] = pd.to_numeric(out["popularity"], errors="coerce")
    out["explicit"] = pd.to_numeric(out["explicit"], errors="coerce").fillna(0).clip(0, 1)

    out["popularity_scaled"] = (out["popularity"] / 100.0).clip(0, 1)

    req = ["energy", "danceability", "tempo", "loudness", "instrumentalness", "genre"]
    out = out.dropna(subset=req)
    return out.reset_index(drop=True)


def genre_options(df: pd.DataFrame, genre_col: str = "genre", min_count: int = 200) -> list[str]:
    vc = df[genre_col].astype(str).value_counts()
    opts = vc[vc >= min_count].index.tolist()
    return sorted(opts)


def plot_mood_features_by_year(df: pd.DataFrame, *, title_suffix: str = "") -> go.Figure:
    feat_block = ["energy", "danceability", "instrumentalness", "popularity_scaled"]
    labels = {
        "energy": "Energy",
        "danceability": "Danceability",
        "instrumentalness": "Instrumentalness",
        "popularity_scaled": "Popularity (÷100)",
    }
    by_year = df.groupby("year", as_index=False)[feat_block].mean().sort_values("year")

    fig = go.Figure()
    for col in feat_block:
        fig.add_trace(
            go.Scatter(
                x=by_year["year"],
                y=by_year[col],
                name=labels[col],
                mode="lines+markers",
                hovertemplate="%{y:.3f}<extra></extra>",
            )
        )
    title = "Average audio features by release year"
    if title_suffix:
        title += f" — {title_suffix}"
    fig.update_layout(
        title=title,
        xaxis_title="Release year (from the data)",
        yaxis_title="Average score (0 = low, 1 = high on this scale)",
        hovermode="x unified",
        legend_title="Feature",
        height=520,
    )
    fig.update_xaxes(dtick=1)
    return fig


def plot_tempo_loudness_by_year(df: pd.DataFrame, *, title_suffix: str = "") -> go.Figure:
    by_year_tl = (
        df.groupby("year", as_index=False)
        .agg(tempo=("tempo", "mean"), loudness=("loudness", "mean"))
        .sort_values("year")
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Average tempo (BPM)", "Average loudness (Spotify-style scale)"),
        vertical_spacing=0.12,
    )
    fig.add_trace(
        go.Scatter(
            x=by_year_tl["year"],
            y=by_year_tl["tempo"],
            mode="lines+markers",
            name="Tempo",
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=by_year_tl["year"],
            y=by_year_tl["loudness"],
            mode="lines+markers",
            name="Loudness",
            showlegend=False,
        ),
        row=2,
        col=1,
    )
    fig.update_xaxes(title_text="Release year", row=2, col=1, dtick=1)
    fig.update_xaxes(dtick=1, row=1, col=1)
    fig.update_yaxes(title_text="BPM", row=1, col=1)
    fig.update_yaxes(title_text="dB (estimated)", row=2, col=1)
    t = "Tempo and loudness — yearly averages"
    if title_suffix:
        t += f" ({title_suffix})"
    fig.update_layout(title=t, height=640, hovermode="x unified")
    return fig


def plot_energy_danceability_scatter(df: pd.DataFrame, *, title_suffix: str = "") -> go.Figure:
    t = "Tracks: energy vs danceability"
    if title_suffix:
        t += f" ({title_suffix})"
    fig = px.scatter(
        df,
        x="energy",
        y="danceability",
        color="year",
        hover_data={"Song": True, "Artist": True, "year": True},
        title=t,
        labels={
            "energy": "Energy",
            "danceability": "Danceability",
            "year": "Release year",
        },
        color_continuous_scale="Viridis",
    )
    fig.update_traces(marker=dict(size=7, opacity=0.28))
    fig.update_layout(height=560, coloraxis_colorbar_title_text="Year")
    return fig


def plot_radar_by_year(df: pd.DataFrame, *, title_suffix: str = "") -> go.Figure:
    radar_feats = ["energy", "danceability", "instrumentalness", "explicit"]
    spoke_labels = ["Energy", "Danceability", "Instrumentalness", "Explicit (0–1)"]
    label_map = dict(zip(radar_feats, spoke_labels))

    by_year = df.groupby("year", as_index=False)[radar_feats].mean()
    long_radar = by_year.melt(id_vars=["year"], var_name="feature", value_name="value")
    long_radar["value"] = long_radar["value"].clip(0, 1)
    long_radar["Spoke"] = long_radar["feature"].map(label_map)

    title = "Average sound profile by release year — Play or drag the year slider"
    if title_suffix:
        title += f" ({title_suffix})"
    fig = px.line_polar(
        long_radar,
        r="value",
        theta="Spoke",
        animation_frame="year",
        line_close=True,
        range_r=[0, 1],
        title=title,
        category_orders={"Spoke": spoke_labels},
    )
    fig.update_layout(height=600, title_x=0.5)
    return fig


def year_counts_table(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("year", as_index=False)
        .size()
        .rename(columns={"size": "track_count"})
        .sort_values("year")
    )


def top_by_year_sample(
    df: pd.DataFrame,
    *,
    n: int = 3,
) -> pd.DataFrame:
    return (
        df.sort_values("popularity", ascending=False)
        .groupby("year", as_index=False)
        .head(n)[["year", "Song", "Artist", "popularity"]]
        .sort_values(["year", "popularity"], ascending=[True, False])
        .reset_index(drop=True)
    )
