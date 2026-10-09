"""A small chessboard picture for the lab. No extra chess library is required."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


def _placement(fen):
    ranks = []
    for field in fen.split()[0].split("/"):
        rank = []
        for char in field:
            if char.isdigit():
                rank.extend([""] * int(char))
            else:
                rank.append(char)
        ranks.append(rank)
    return ranks


def _square(uci_square):
    file_index = "abcdefgh".index(uci_square[0])
    row_index = 8 - int(uci_square[1])
    return row_index, file_index


def show_position(examples, index, activity, feature_index=None, prediction=None):
    """Draw one board, the reference move, and a short activity chart."""
    position = examples.loc[index]
    fen = str(position.fen)
    reference = str(position.stockfish_uci)
    ranks = _placement(fen)
    figure, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    board = axes[0]
    light = "#f0d9b5"
    dark = "#b58863"
    for row in range(8):
        for col in range(8):
            color = light if (row + col) % 2 == 0 else dark
            board.add_patch(Rectangle((col, 7 - row), 1, 1, facecolor=color, edgecolor="none"))
            piece = ranks[row][col]
            if piece:
                board.text(
                    col + 0.5,
                    7 - row + 0.5,
                    piece,
                    ha="center",
                    va="center",
                    fontsize=16,
                    fontweight="bold",
                    color="#1a1a1a" if piece.isupper() else "#222222",
                )
    _mark(board, reference, "#c9a227", 2.5)
    if prediction and prediction != reference:
        _mark(board, str(prediction), "#2b6cb0", 1.6)
    board.set_xlim(0, 8)
    board.set_ylim(0, 8)
    board.set_aspect("equal")
    board.set_xticks(np.arange(8) + 0.5)
    board.set_xticklabels(list("abcdefgh"))
    board.set_yticks(np.arange(8) + 0.5)
    board.set_yticklabels([str(rank) for rank in range(1, 9)])
    board.tick_params(length=0)
    title = f"index {index}: reference {reference}"
    if prediction:
        title += f", model {prediction}"
    board.set_title(title)

    row = np.asarray(activity, dtype=np.float64)[index]
    if feature_index is None:
        chosen = np.argsort(-row)[:12]
    else:
        chosen = np.asarray(feature_index, dtype=int)[:12]
    chart = axes[1]
    chart.bar(np.arange(len(chosen)), row[chosen], color="#2f6f4e")
    chart.set_xticks(np.arange(len(chosen)))
    chart.set_xticklabels([str(int(item)) for item in chosen], rotation=45, ha="right")
    chart.set_xlabel("Readout neuron")
    chart.set_ylabel("Activity")
    chart.set_title("A few activity features")
    figure.tight_layout()
    return figure


def _mark(board, uci, color, width):
    for square in (uci[:2], uci[2:4]):
        row, col = _square(square)
        board.add_patch(
            Rectangle(
                (col, 7 - row),
                1,
                1,
                fill=False,
                edgecolor=color,
                linewidth=width,
            )
        )
