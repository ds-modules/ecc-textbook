"""A small legal-move scorer that students train in Python.

The fly network is not in this file. Pass in an activity matrix that the
browser widget has already transferred. Each row is one chess position.
Each column is one readout neuron.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

READOUT = 41692
N_MOVE = 33
MAX_FEATURES = 64
NARROW_METRIC = (
    "Stockfish top-move agreement is one narrow metric. "
    "It is not a complete chess-strength assessment."
)


class HeldOutError(ValueError):
    """Raised when a validation or test position is used to choose features or to fit."""


class MoveScorer:
    """One student model. Its weights are not shared with any other model."""

    def __init__(
        self,
        name,
        neuron_index,
        train_rows,
        validation_rows,
        test_rows,
        initial_weights=None,
    ):
        self.name = str(name)
        self.neuron_index = np.array(neuron_index, dtype=int).copy()
        self.train_rows = tuple(int(row) for row in train_rows)
        self.validation_rows = frozenset(int(row) for row in validation_rows)
        self.test_rows = frozenset(int(row) for row in test_rows)
        width = len(self.neuron_index)
        if initial_weights is None:
            self.weights = np.zeros((width, N_MOVE), dtype=np.float64)
        else:
            self.weights = np.array(initial_weights, dtype=np.float64).copy()
        self.initial_weights = self.weights.copy()
        self.center = np.zeros(width, dtype=np.float64)
        self.scale = np.ones(width, dtype=np.float64)
        self.history = []
        self.settings = {
            "n_features": int(len(self.neuron_index)),
            "train_rows": self.train_rows,
            "learning_rate": None,
            "n_rounds": 0,
            "fit_calls": 0,
        }

    @property
    def n_features(self):
        return int(len(self.neuron_index))

    @property
    def n_parameters(self):
        return int(self.weights.size)

    @property
    def weight_length(self):
        return float(np.linalg.norm(self.weights))

    def summary(self):
        return (
            f"{self.name}: {self.n_features} activity features, "
            f"{self.n_parameters} trainable numbers, "
            f"weight length {self.weight_length:.4f}. "
            f"Features were chosen from training rows {list(self.train_rows)} only. "
            f"{len(self.validation_rows)} validation rows and "
            f"{len(self.test_rows)} test rows are blocked."
        )


def _rows_for_split(examples, split_name):
    matches = examples.index[examples["split"].astype(str) == split_name]
    return [int(row) for row in matches]


def test_row_numbers(examples):
    """Fixed final test positions. Students do not choose these."""
    return _rows_for_split(examples, "test")


def validation_row_numbers(examples):
    """Fixed validation positions. Students do not choose these."""
    return _rows_for_split(examples, "validation")


def pool_row_numbers(examples):
    return _rows_for_split(examples, "pool")


def check_training_rows(train_rows, examples):
    """Reject validation and test rows before feature selection or fitting."""
    requested = [int(row) for row in train_rows]
    if not requested:
        raise ValueError("Choose at least one training row from the pool.")
    leaked = []
    for row in requested:
        split_name = None
        if row in set(validation_row_numbers(examples)):
            split_name = "validation"
        elif row in set(test_row_numbers(examples)):
            split_name = "test"
        if split_name is not None:
            leaked.append(f"{row} ({split_name})")
    if leaked:
        raise HeldOutError(
            "These rows are held out and cannot be used for feature selection "
            f"or fitting: {leaked}"
        )
    allowed = set(pool_row_numbers(examples))
    unknown = [row for row in requested if row not in allowed]
    if unknown:
        raise ValueError(f"These rows are not in the training pool: {unknown}")
    return requested


def move_features(uci):
    """Fixed description of a move. These 33 numbers are not trained."""
    files = "abcdefgh"
    start_file = files.index(uci[0])
    start_rank = int(uci[1]) - 1
    end_file = files.index(uci[2])
    end_rank = int(uci[3]) - 1
    features = np.zeros(N_MOVE, dtype=np.float64)
    features[start_file] = 1.0
    features[8 + start_rank] = 1.0
    features[16 + end_file] = 1.0
    features[24 + end_rank] = 1.0
    features[32] = 1.0
    return features


def _legal_moves(examples, row):
    return sorted(str(examples.loc[row, "legal_uci"]).split())


def _labels(examples):
    return examples["stockfish_uci"].astype(str).tolist()


def select_activity_features(activity, train_rows, n_features):
    """Keep the training-set neurons that vary the most.

    Validation and test rows are not read. n_features is the student's choice,
    capped so the lab stays on a small matrix.
    """
    n_features = int(n_features)
    if n_features < 1 or n_features > MAX_FEATURES:
        raise ValueError(
            f"Choose n_features from 1 to {MAX_FEATURES}. "
            f"The fly readout has {READOUT} neurons; this lab trains a small scorer."
        )
    rows = np.asarray(list(train_rows), dtype=int)
    variance = np.asarray(activity, dtype=np.float64)[rows].var(axis=0)
    order = np.argsort(-variance)
    chosen = [int(index) for index in order if variance[index] > 0][:n_features]
    if not chosen:
        raise ValueError("No readout neuron varied across these training rows.")
    return np.array(chosen, dtype=int)


def create_move_scorer(
    activity, examples, train_rows, n_features=16, name="scorer", like=None
):
    """Make a new scorer with its own weights.

    Feature columns are chosen from train_rows only. A validation or test row
    raises HeldOutError and does not create a model. Pass like= another scorer
    to copy that scorer's neurons and its original starting weights. Use that
    when the comparison changes learning rate or round count, and the feature
    count stays the same.
    """
    activity = np.asarray(activity)
    if activity.ndim != 2 or activity.shape[1] != READOUT:
        raise ValueError(
            f"activity must have shape (n_positions, {READOUT}). "
            "Load the fly network and call fly.get_activity() first."
        )
    if activity.shape[0] != len(examples):
        raise ValueError(
            f"activity has {activity.shape[0]} rows and the example table has {len(examples)}."
        )
    checked = check_training_rows(train_rows, examples)
    n_features = int(n_features)
    if like is not None:
        if n_features != int(like.settings["n_features"]):
            raise ValueError(
                "like= copies features from an existing model. "
                "Leave it out when you change n_features."
            )
        if tuple(checked) != tuple(like.train_rows):
            raise ValueError(
                "like= requires the same training rows as the model you are copying."
            )
        neuron_index = np.array(like.neuron_index, dtype=int).copy()
        initial_weights = np.array(like.initial_weights, dtype=np.float64).copy()
    else:
        neuron_index = select_activity_features(activity, checked, n_features)
        initial_weights = None
    return MoveScorer(
        name=name,
        neuron_index=neuron_index,
        train_rows=checked,
        validation_rows=validation_row_numbers(examples),
        test_rows=test_row_numbers(examples),
        initial_weights=initial_weights,
    )


def _prepared_features(model, activity, row):
    raw = np.asarray(activity, dtype=np.float64)[row, model.neuron_index]
    return (raw - model.center) / model.scale


def predict_move(model, activity, examples, row):
    """Highest-scoring legal move on this board. Ties use alphabetical order."""
    legal = _legal_moves(examples, row)
    values = _prepared_features(model, activity, row)
    phi = np.stack([move_features(move) for move in legal])
    scores = phi @ (model.weights.T @ values)
    choice = legal[int(np.argmax(scores))]
    return choice


def baseline_move(examples, row):
    """First legal move in alphabetical order. No fly activity and no training."""
    return _legal_moves(examples, row)[0]


def train_scorer(model, activity, examples, train_rows, learning_rate=0.5, n_rounds=5):
    """Update this model's weights. Held-out rows are refused. Other models are untouched.

    A second call continues from the current weights. reset_scorer starts over.
    """
    checked = check_training_rows(train_rows, examples)
    if set(checked) != set(model.train_rows):
        raise ValueError(
            "These training rows do not match the rows used to create this model. "
            "Create a new scorer for a different training set."
        )
    learning_rate = float(learning_rate)
    n_rounds = int(n_rounds)
    if learning_rate <= 0:
        raise ValueError("learning_rate must be greater than 0.")
    if n_rounds < 1 or n_rounds > 30:
        raise ValueError("n_rounds must be from 1 to 30.")

    activity = np.asarray(activity, dtype=np.float64)
    labels = _labels(examples)
    raw = activity[:, model.neuron_index]
    rows = np.asarray(checked, dtype=int)
    model.center = raw[rows].mean(axis=0)
    scale = raw[rows].std(axis=0)
    model.scale = np.where(scale < 1e-6, 1.0, scale)

    model.settings["fit_calls"] = int(model.settings["fit_calls"]) + 1
    model.settings["learning_rate"] = learning_rate
    for _ in range(n_rounds):
        round_index = len(model.history) + 1
        gradient = np.zeros_like(model.weights)
        loss = 0.0
        length_before = model.weight_length
        for row in checked:
            legal = _legal_moves(examples, row)
            phi = np.stack([move_features(move) for move in legal])
            values = _prepared_features(model, activity, row)
            scores = phi @ (model.weights.T @ values)
            shifted = scores - scores.max()
            probs = np.exp(shifted)
            probs /= probs.sum()
            target = legal.index(labels[row])
            loss += float(-np.log(probs[target] + 1e-12))
            residual = probs.copy()
            residual[target] -= 1.0
            gradient += np.outer(values, phi.T @ residual)
        gradient /= len(checked)
        model.weights = model.weights - learning_rate * gradient
        train_hits = sum(
            predict_move(model, activity, examples, row) == labels[row] for row in checked
        )
        model.history.append(
            {
                "round": round_index,
                "loss_before_step": loss / len(checked),
                "train_matches": train_hits,
                "train_total": len(checked),
                "weight_length_before": length_before,
                "weight_length": model.weight_length,
                "learning_rate": learning_rate,
            }
        )
    model.settings["n_rounds"] = int(model.settings["n_rounds"]) + n_rounds
    return list(model.history)


def reset_scorer(model):
    """Set this model's weights back to their original start. Leave every other model alone."""
    model.weights = np.array(model.initial_weights, dtype=np.float64).copy()
    model.center = np.zeros(model.initial_weights.shape[0], dtype=np.float64)
    model.scale = np.ones(model.initial_weights.shape[0], dtype=np.float64)
    model.history = []
    model.settings["learning_rate"] = None
    model.settings["n_rounds"] = 0
    model.settings["fit_calls"] = 0
    return model


def plot_training(model):
    """Training loss and training agreement. These plots do not include held-out rows."""
    import matplotlib.pyplot as plt

    if not model.history:
        raise ValueError("Train the model before plotting.")
    rounds = [item["round"] for item in model.history]
    losses = [item["loss_before_step"] for item in model.history]
    agreement = [
        item["train_matches"] / item["train_total"] for item in model.history
    ]
    figure, axes = plt.subplots(1, 2, figsize=(8, 3))
    axes[0].plot(rounds, losses, marker="o")
    axes[0].set_xlabel("Round")
    axes[0].set_ylabel("Training loss")
    axes[0].set_title("Training loss")
    axes[1].plot(rounds, agreement, marker="o")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].set_xlabel("Round")
    axes[1].set_ylabel("Share of training rows")
    axes[1].set_title("Training agreement")
    figure.tight_layout()
    return figure


def describe_comparison(first, second):
    """Say whether two trained models differ by exactly one stored setting."""
    compared = ("n_features", "learning_rate", "n_rounds")
    different = [
        name
        for name in compared
        if first.settings[name] != second.settings[name]
    ]
    problems = []
    if first.settings["train_rows"] != second.settings["train_rows"]:
        problems.append("the training rows differ")
    if first.settings["fit_calls"] != 1 or second.settings["fit_calls"] != 1:
        problems.append(
            "Train was run more than once on a model, so that run continued from existing weights"
        )
    if len(different) != 1:
        shown = ", ".join(different) if different else "none"
        problems.append(f"the number of changed settings is {len(different)} ({shown})")
    feature_change = different == ["n_features"]
    if not feature_change and len(different) == 1:
        if not np.array_equal(first.neuron_index, second.neuron_index):
            problems.append("the activity features differ")
        if not np.array_equal(first.initial_weights, second.initial_weights):
            problems.append("the initial weights differ")
    if problems:
        return "This is not a one-setting comparison from a fresh start. " + "; ".join(problems) + "."
    return f"Fair comparison: only {different[0]} differs."


def save_intact_state(model, activity):
    """Copy weights and activity before a connection change."""
    return {
        "weights": np.array(model.weights, dtype=np.float64).copy(),
        "activity": np.array(activity, dtype=np.float64).copy(),
    }


def describe_intervention(intact, model, activity_now, examples, rows):
    """Compare the current network with the activity and weights saved beforehand."""
    weights_unchanged = bool(np.allclose(model.weights, intact["weights"]))
    activity_unchanged = bool(np.allclose(activity_now, intact["activity"]))
    labels = _labels(examples)
    records = []
    changed = 0
    for row in [int(item) for item in rows]:
        before = predict_move(model, intact["activity"], examples, row)
        after = predict_move(model, activity_now, examples, row)
        if before != after:
            changed += 1
        records.append(
            {
                "index": row,
                "split": str(examples.loc[row, "split"]),
                "intact network": before,
                "current network": after,
                "Stockfish": labels[row],
                "prediction changed": "yes" if before != after else "no",
            }
        )
    intact_activity = np.asarray(intact["activity"])
    current_activity = np.asarray(activity_now)
    summary = {
        "weights_unchanged": weights_unchanged,
        "activity_unchanged": activity_unchanged,
        "row0_sum_intact": float(intact_activity[0].sum()),
        "row0_sum_current": float(current_activity[0].sum()),
        "predictions_changed": changed,
    }
    return pd.DataFrame.from_records(records), summary


def evaluate_scorer(model, activity, examples, rows):
    """Compare the baseline, this model, and the Stockfish move.

    `rows` may include the test set. Evaluation does not change weights and
    does not choose features.
    """
    labels = _labels(examples)
    records = []
    for row in [int(item) for item in rows]:
        legal = _legal_moves(examples, row)
        target = labels[row]
        baseline = baseline_move(examples, row)
        prediction = predict_move(model, activity, examples, row)
        records.append(
            {
                "index": row,
                "split": str(examples.loc[row, "split"]),
                "baseline": baseline,
                "baseline legal": "yes" if baseline in legal else "no",
                "your model": prediction,
                "your model legal": "yes" if prediction in legal else "no",
                "Stockfish": target,
                "Stockfish legal": "yes" if target in legal else "no",
                "agrees with Stockfish": "yes" if prediction == target else "no",
            }
        )
    table = pd.DataFrame.from_records(records)
    agreements = int((table["agrees with Stockfish"] == "yes").sum()) if len(table) else 0
    summary = {
        "model": model.name,
        "rows": int(len(table)),
        "agreements": agreements,
        "weight_length": model.weight_length,
        "n_parameters": model.n_parameters,
        "note": NARROW_METRIC,
    }
    return table, summary


def compare_scorers(models, activity, examples, rows):
    """One table for several models on the same positions. Weights stay as they are."""
    labels = _labels(examples)
    records = []
    for row in [int(item) for item in rows]:
        legal = _legal_moves(examples, row)
        record = {
            "index": row,
            "split": str(examples.loc[row, "split"]),
            "baseline": baseline_move(examples, row),
            "Stockfish": labels[row],
        }
        for model in models:
            prediction = predict_move(model, activity, examples, row)
            record[model.name] = prediction
            record[f"{model.name} legal"] = "yes" if prediction in legal else "no"
            record[f"{model.name} agrees"] = "yes" if prediction == labels[row] else "no"
        records.append(record)
    return pd.DataFrame.from_records(records)
