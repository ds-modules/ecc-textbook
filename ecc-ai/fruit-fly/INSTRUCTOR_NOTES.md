# Instructor notes

This file is for the instructor. It is not part of the student notebook.

Students predict, then train and test a perceptron, then see one picture of the MaleCNS excerpt. The map is not the network being trained.

## What students should see

Untrained weights are loom = 0, odor = 0, bias = 0. Every prediction is **stay**, because the score is 0 and the model jumps only when the score is above 0.

The first run uses the `loom` examples for 8 rounds.

| Example set | Wrong predictions each round | Weights afterward | Held-out row | Held-out prediction |
|---|---|---|---|---|
| `loom` | 1, 1, 0, 0, 0, 0, 0, 0 | loom = 1, odor = 0, bias = 0 | loom 1, odor 2, correct jump | jump |
| `odor` | 1, 1, 0, 0, 0, 0, 0, 0 | loom = 0, odor = 1, bias = 0 | loom 2, odor 1, correct jump | jump |
| `either` | 1, 2, 1, 0, 0, 0, 0, 0 | loom = 1, odor = 1, bias = 0 | loom 1, odor 2, correct jump | jump |

`either` gets slightly worse for one round, then reaches zero wrong training predictions.

The controls on the training cell are the only widget. **Reset** clears the weights. **Train** adds rounds. **Test** does not change the weights. Students should press Reset before training a new example set. If `ipywidgets` is missing, the same cell trains `loom` for 8 rounds. They can edit `set_name` and `n_rounds` in that fallback and run the cell again.

The map picture uses short labels. In the files the neurons are `DNp01(GF)`, `TTMn`, and `PSI`. Arrows show measured synapse counts of at least 10. The largest is giant fiber R to motor R, count 70. Learned weights from `loom` are 1, 0, and 0. Those are not synapse counts.

## Closing question

Look for an answer that asks for evidence the class examples do not provide: recordings or behavior from a living fly, more than one animal, or a test the model was not trained on. The wiring diagram alone does not show how the fly responds.

## Data

Do not replace the CSV files with the full connectome. Provenance and the CC BY 4.0 attribution are in `data/README.md`.
