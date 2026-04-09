from __future__ import annotations

import shutil
import subprocess
import warnings
from pathlib import Path

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import Audio, display


def load_table(derived_dir: Path, name: str) -> pd.DataFrame:
    parquet_path = derived_dir / f"{name}.parquet"
    csv_path = derived_dir / f"{name}.csv"
    if parquet_path.exists():
        try:
            return pd.read_parquet(parquet_path)
        except Exception:
            pass
    if csv_path.exists():
        return pd.read_csv(csv_path)
    raise FileNotFoundError(f"Missing {name}.parquet/.csv")


def load_tables(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    derived = base_dir / "data" / "derived"
    tracks = load_table(derived, "jazz_age_pd_tracks")
    examples = load_table(derived, "lick_examples")
    missing = [p for p in examples["clip_path"].tolist() if not (base_dir / str(p)).exists()]
    if missing:
        raise RuntimeError(f"Missing clip files: {len(missing)}")
    return tracks, examples


def _resolve_ffmpeg_exe() -> str:
    system = shutil.which("ffmpeg")
    if system:
        return system
    try:
        import imageio_ffmpeg  # type: ignore[import-untyped]

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        raise RuntimeError(
            "No ffmpeg executable found. On JupyterHub, run: pip install imageio-ffmpeg "
            "(see jazz-licks/requirements.txt), restart the kernel, and try again. "
            "Hub admins can instead install conda-forge package ffmpeg. "
            "Some platforms (e.g. certain ARM images) may need a system-provided ffmpeg."
        ) from e


def decode_audio_ffmpeg(path: Path, sr: int = 22050) -> tuple[np.ndarray, int]:
    ffmpeg_exe = _resolve_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        "-v",
        "error",
        "-i",
        str(path),
        "-f",
        "f32le",
        "-ac",
        "1",
        "-ar",
        str(sr),
        "pipe:1",
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0 or not proc.stdout:
        raise RuntimeError(f"ffmpeg decode failed for {path}")
    y = np.frombuffer(proc.stdout, dtype=np.float32)
    return y, sr


def _to_audio_widget(y: np.ndarray, sr: int) -> Audio:
    clip = np.clip(y, -1.0, 1.0)
    pcm = np.int16(clip * 32767)
    return Audio(data=pcm, rate=sr, autoplay=False)


def hz_to_midi(hz: float) -> float:
    return 69.0 + 12.0 * np.log2(max(hz, 1e-9) / 440.0)


def midi_to_note_name(midi: float) -> str:
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    m = int(np.round(midi))
    return f"{names[m % 12]}{(m // 12) - 1}"


def dominant_pitch_track(
    y: np.ndarray, sr: int, frame_sec: float = 0.046, hop_sec: float = 0.020
) -> tuple[np.ndarray, np.ndarray]:
    n_fft = max(512, int(frame_sec * sr))
    hop = max(128, int(hop_sec * sr))
    if len(y) < n_fft:
        return np.array([]), np.array([])
    window = np.hanning(n_fft)
    times: list[float] = []
    freqs: list[float] = []
    for start in range(0, len(y) - n_fft + 1, hop):
        frame = y[start : start + n_fft] * window
        spec = np.abs(np.fft.rfft(frame))
        bins = np.fft.rfftfreq(n_fft, d=1.0 / sr)
        mask = (bins >= 80.0) & (bins <= 1200.0)
        if not np.any(mask):
            continue
        local = spec[mask]
        b = bins[mask]
        peak = int(np.argmax(local))
        if local[peak] < 0.01:
            continue
        times.append((start + (n_fft // 2)) / sr)
        freqs.append(float(b[peak]))
    return np.array(times), np.array(freqs)


def synthesize_from_pitch(
    pitch_times: np.ndarray, pitch_freqs: np.ndarray, duration: float, sr: int = 22050
) -> np.ndarray:
    n = max(1, int(duration * sr))
    t = np.arange(n) / sr
    if len(pitch_times) == 0:
        return np.zeros(n, dtype=np.float32)
    f_track = np.interp(t, pitch_times, pitch_freqs, left=pitch_freqs[0], right=pitch_freqs[-1])
    phase = 2.0 * np.pi * np.cumsum(f_track) / sr
    tone = 0.75 * np.sin(phase) + 0.25 * np.sin(2.0 * phase)
    env = np.clip(np.hanning(max(8, n)), 0.0, 1.0)
    y = (tone * env).astype(np.float32)
    peak = float(np.max(np.abs(y)))
    if peak > 0:
        y = 0.85 * y / peak
    return y


def _build_selection_widgets(examples: pd.DataFrame) -> tuple[widgets.Dropdown, widgets.Dropdown]:
    opts = examples[["title", "artist"]].drop_duplicates().copy()
    opts["label"] = opts.apply(lambda r: f"{r['title']} — {r['artist']}", axis=1)
    song_dd = widgets.Dropdown(options=opts["label"].tolist(), description="Song")
    clip_dd = widgets.Dropdown(options=[], description="Snippet")
    return song_dd, clip_dd


def _selected_clip_row(examples: pd.DataFrame, song_label: str, clip_label: str | None) -> pd.Series | None:
    title, artist = song_label.split(" — ", 1)
    df = examples[(examples["title"] == title) & (examples["artist"] == artist)].copy()
    if df.empty:
        return None
    labels = [f"{r.snippet_type} ({r.start_sec:.1f}-{r.end_sec:.1f}s)" for _, r in df.iterrows()]
    if clip_label not in labels:
        return df.iloc[0]
    return df.iloc[labels.index(clip_label)]


def _refresh_clip_options(examples: pd.DataFrame, song_dd: widgets.Dropdown, clip_dd: widgets.Dropdown) -> None:
    title, artist = song_dd.value.split(" — ", 1)
    df = examples[(examples["title"] == title) & (examples["artist"] == artist)].copy()
    labels = [f"{r.snippet_type} ({r.start_sec:.1f}-{r.end_sec:.1f}s)" for _, r in df.iterrows()]
    clip_dd.options = labels
    if labels:
        clip_dd.value = labels[0]


def _wire_dropdowns(
    examples: pd.DataFrame, song_dd: widgets.Dropdown, clip_dd: widgets.Dropdown, render
) -> None:
    suspend = {"active": False}

    def on_song_change(_: object) -> None:
        old_clip = clip_dd.value
        suspend["active"] = True
        _refresh_clip_options(examples, song_dd, clip_dd)
        suspend["active"] = False
        # If clip value did not change, no clip event will fire, so render now.
        if clip_dd.value == old_clip:
            render()

    def on_clip_change(_: object) -> None:
        if not suspend["active"]:
            render()

    song_dd.observe(on_song_change, names="value")
    clip_dd.observe(on_clip_change, names="value")
    on_song_change(None)
    render()


def create_waveform_section(base_dir: Path, examples: pd.DataFrame) -> widgets.VBox:
    song_dd, clip_dd = _build_selection_widgets(examples)
    hint = widgets.Label(value="Choose a song/snippet, then use the audio player under the chart.")
    out = widgets.Output()

    def render(*_: object) -> None:
        with out:
            out.clear_output(wait=True)
            row = _selected_clip_row(examples, song_dd.value, clip_dd.value)
            if row is None:
                print("No clip available.")
                return
            y, sr = decode_audio_ffmpeg(base_dir / str(row["clip_path"]), sr=22050)
            t = np.arange(len(y)) / sr
            fig, ax = plt.subplots(1, 1, figsize=(10, 2.8))
            ax.plot(t, y, linewidth=0.7)
            ax.set_title("Waveform")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            plt.tight_layout()
            plt.show()
            plt.close(fig)
            display(_to_audio_widget(y, sr))

    _wire_dropdowns(examples, song_dd, clip_dd, render)
    return widgets.VBox([widgets.HBox([song_dd, clip_dd]), hint, out])


def create_spectrogram_section(base_dir: Path, examples: pd.DataFrame) -> widgets.VBox:
    song_dd, clip_dd = _build_selection_widgets(examples)
    hint = widgets.Label(value="Choose a song/snippet, then use the audio player under the chart.")
    out = widgets.Output()

    def render(*_: object) -> None:
        with out:
            out.clear_output(wait=True)
            row = _selected_clip_row(examples, song_dd.value, clip_dd.value)
            if row is None:
                print("No clip available.")
                return
            y, sr = decode_audio_ffmpeg(base_dir / str(row["clip_path"]), sr=22050)
            fig, ax = plt.subplots(1, 1, figsize=(10, 3.6))
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore", message="divide by zero encountered in log10", category=RuntimeWarning
                )
                ax.specgram(y, NFFT=1024, Fs=sr, noverlap=512)
            ax.set_title("Spectrogram")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Frequency (Hz)")
            plt.tight_layout()
            plt.show()
            plt.close(fig)
            display(_to_audio_widget(y, sr))

    _wire_dropdowns(examples, song_dd, clip_dd, render)
    return widgets.VBox([widgets.HBox([song_dd, clip_dd]), hint, out])


def create_notes_section(base_dir: Path, examples: pd.DataFrame) -> widgets.VBox:
    song_dd, clip_dd = _build_selection_widgets(examples)
    hint = widgets.Label(value="Use the two players under the plot to compare original audio and synthesized notes.")
    out = widgets.Output()

    def render(*_: object) -> None:
        with out:
            out.clear_output(wait=True)
            row = _selected_clip_row(examples, song_dd.value, clip_dd.value)
            if row is None:
                print("No clip available.")
                return
            y, sr = decode_audio_ffmpeg(base_dir / str(row["clip_path"]), sr=22050)
            pt, pf = dominant_pitch_track(y, sr)
            pm = np.array([hz_to_midi(v) for v in pf]) if len(pt) else np.array([])
            synth = synthesize_from_pitch(pt, pf, duration=(len(y) / sr), sr=sr)

            if len(pt) > 0 and len(pm) > 0:
                fig, ax = plt.subplots(1, 1, figsize=(10, 3.0))
                ax.plot(pt, pm, marker="o", markersize=2, linewidth=0.7)
                ax.set_title("Estimated dominant notes over time")
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("MIDI note")
                ticks = np.unique(np.round(np.linspace(np.floor(pm.min()), np.ceil(pm.max()), 7)).astype(int))
                ax.set_yticks(ticks)
                ax.set_yticklabels([midi_to_note_name(v) for v in ticks])
                plt.tight_layout()
                plt.show()
                plt.close(fig)
            else:
                print("No stable pitch estimate for this clip. You can still compare the audio below.")

            print("Original clip")
            display(_to_audio_widget(y, sr))
            print("Synthesized MIDI-like version (from detected pitch)")
            display(_to_audio_widget(synth, sr))

    _wire_dropdowns(examples, song_dd, clip_dd, render)
    return widgets.VBox([widgets.HBox([song_dd, clip_dd]), hint, out])
