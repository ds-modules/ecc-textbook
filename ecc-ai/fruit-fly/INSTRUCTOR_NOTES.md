# Instructor notes

This file is for the instructor. It is not part of the student notebook.

The student activity is a perceptron. It is separate from the six-neuron MaleCNS excerpt. The real map has loops and no labeled correct responses, so it is shown beside the model and is not the thing being trained.

## What students should see

Untrained weights are loom = 0, odor = 0, bias = 0. Every prediction is **stay**, because the score is 0 and the model jumps only when the score is above 0.

After **Reset**, then **Train** for 8 rounds:

| Example set | Wrong predictions each round | Weights afterward | Held-out row | Held-out prediction |
|---|---|---|---|---|
| `loom` | 1, 1, 0, 0, 0, 0, 0, 0 | loom = 1, odor = 0, bias = 0 | loom 1, odor 2, correct jump | jump |
| `odor` | 1, 1, 0, 0, 0, 0, 0, 0 | loom = 0, odor = 1, bias = 0 | loom 2, odor 1, correct jump | jump |
| `either` | 1, 2, 1, 0, 0, 0, 0, 0 | loom = 1, odor = 1, bias = 0 | loom 1, odor 2, correct jump | jump |
| `custom`, if left unchanged | same as `loom` | same as `loom` | same as `loom` | jump |

`either` gets slightly worse for one round, then reaches zero wrong training predictions. That is expected for this update rule.

The unchanged `custom` list matches `loom`.

One edited list is not a case of impossible feedback. Change only the training row loom = 1, odor = 0 from jump (1) to stay (0). Every training pair of signals is still unique, so no two rows have the same inputs and opposite labels. The held-out row stays loom = 1, odor = 2, correct jump.

Training rows in that edit:

| loom | odor | correct response |
|---|---|---|
| 0 | 0 | stay (0) |
| 0 | 1 | stay (0) |
| 0 | 2 | stay (0) |
| 1 | 0 | stay (0) |
| 1 | 1 | jump (1) |
| 2 | 0 | jump (1) |
| 2 | 1 | jump (1) |
| 2 | 2 | jump (1) |

With learning rate 1, eight rounds are not enough: wrong predictions are 1, 3, 3, 2, 2, 3, 2, 2, and the weights are loom = 3, odor = 2, bias = -2. Eleven rounds at learning rate 1 reach zero training mistakes. The weights are then loom = 3, odor = 1, bias = -3, and the held-out prediction is jump. Learning rate 0.2 also reaches zero training mistakes, on round 7, with weights loom = 0.4, odor = 0.2, bias = -0.4. Say that eight rounds were not enough. Do not say this list is impossible to satisfy.

Impossible feedback is the narrower case: two rows with the same loom signal, the same odor signal, and opposite correct responses. No weights can get both of those rows right.

The **Check and train** controls run this check. They start with the edited row, 8 rounds, and learning rate 1, and the printed line is that this run did not reach zero training mistakes. Set Rounds to 11, or Learning rate to 0.2, and press the button again to reach zero mistakes. **Add opposite label** inserts a second loom = 1, odor = 0 row with the other response. The printout names those two rows and says no weights can make both correct. If `ipywidgets` is missing, the same cell runs `flip_stay = True`, `add_opposite = False`, `n_rounds = 8`, and `learning_rate = 1`.

The code path trains `loom`, then resets and trains `odor`, then resets and trains the editable `custom` list. Buttons call the same functions. **Reset** clears weights. **Train** adds rounds and does not clear old rounds unless Reset was pressed. **Test** does not change weights.

If `ipywidgets` is missing, the button cell prints a short message. The code cells above it are the full activity.

## What to say out loud

- Left figure: measured synapse counts from MaleCNS v1.0. They do not change during training.
- Right figure: perceptron weights. They start at 0 and change only when feedback is not 0.
- Feedback is correct response minus prediction. Changing `correct_response` changes that feedback.
- This is not a fly, not a chess-playing fly model, and not a result checked against fly behavior experiments.

## Reflect, in brief

Students should be able to say that the computer learned weights for the invented examples, that the map contributed the six neurons and 16 synapse counts, and that the examples, the jump/stay rule, and the perceptron were supplied for class. A medical-use answer should name something that still has to be checked, such as who wrote the examples or how the model does on a case it was not trained on.

## Data

Do not replace the CSV files with the full connectome. Provenance and the CC BY 4.0 attribution are in `data/README.md`.
