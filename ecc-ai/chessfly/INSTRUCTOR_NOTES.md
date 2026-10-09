# Instructor notes

This file is for the instructor. It is not part of the student notebook.

Students use the published ChessFly page, embedded from the internet. They record what they see. They do not train the model, and Python does not read the board.

## Lesson flow

About 30–45 minutes.

0. Warmup: what a computer would need before it could play chess. Accept pieces, rules, or examples of good moves. The later sections add the connectome, learned weights, and search.
1. Define connectome, architecture, trained weights, and inference. The diagram is chess position → encoder → connectome-based network → decoder → move scores → search. FlyWire supplies the connections and their signs. Developers added the encoder, strengths, decoder, chess labels, and search. ChessFly is the female FlyWire brain. The assigned Google article (Januszewski and Jain, 3 September 2026) is the male brain and nerve cord. Those are different maps.
2. Run the iframe. First load is about 148 MB in the browser. Ready state is the Brain tab naming neuron and connection counts. **New game** is under the Brain / Moves / About tabs. Students play White. Playing does not change weights.
3. Predict a reply and play once. Press New game and repeat that same opening, then press New game and try a different opening. Ask whether the replies repeat. A different reply does not, by itself, show learning during play. Read the Brain-tab line of positions evaluated and seconds, and record WebGPU or JS. Do not treat two different openings as a speed benchmark, and do not grade chess quality.
4. Students type those notes into a pandas table with three rows. Missing numbers stay `None`. Observed times are numbers such as `4.0`. If games 1 and 2 have replies, the cell says whether those replies match. If their times match, it says so. If the times differ, it prints both numbers and does not call one game slower. Empty times skip that sentence.
5. The student paragraph leads with fixed wiring and adjustable numbers trained on millions of chess examples. The examples are Stockfish-generated move and position evaluations for about 4.4 million Lichess positions. An optional note names the encoder, per-connection strength, gain, threshold, and decoder. The displayed move also depends on search. Students performed inference. WebGPU means the browser used the computer's graphics processor. JS fallback means the same calculations ran in ordinary browser code. Students record which label they saw.
6. Two reflections: what was added beyond the wiring, and what a chess game does not show about a living fly. The About tab already labels Fixed, Learned, and Search, so students may quote it. Look for encoder, strengths, decoder, chess examples, or search. For the cognition question, look for evidence the demo does not provide: recordings or behavior from a living fly, more than one animal, or a test the model was not trained on.

One local test, after the white move e4, got a black pawn from c7 to c5. The page reported 517 positions evaluated in 4.0 seconds on WebGPU. Other runs can differ. Do not grade against that move.

## Embedding

The code cell iframes `https://mlabonne-chessfly.static.hf.space/`. The page, worker, packed connectome, and `flynet.safetensors` load in the student's browser from that host. The notebook is not offline.

`https://huggingface.co/spaces/mlabonne/chessfly` sends `X-Frame-Options: DENY`, so that URL is not the iframe. The static host is the direct-open fallback.

In local JupyterLab 4.6.4, a saved iframe output was blank until the cell ran in that session. After the run, the iframe had no sandbox attribute. The worker accepts `init` and `evaluate` only.

File sizes: `data/connectome.bin.gz` 47,051,343 bytes, `data/neurons.bin.gz` 1,442,541 bytes, `data/flynet.safetensors` 99,572,154 bytes.

The Brain tab shows either `neurons, connections, WebGPU` or `JS fallback`, or `N positions evaluated, X.X s on WebGPU` or `JS`. During a search the brain view can say `search, N positions in one pass`. A bar beside the board is a win-probability display. Students are not asked to interpret it as a chess grade.

`curl` can show a sandbox content-security policy on the static host. Chrome document responses used for the local test did not include that policy, and the app ran.

## Permissions

**App.** The Space card says GPL-3.0 because the page includes chessground. This notebook does not copy that program. GPL-3.0's distribution conditions apply if someone later commits that JavaScript here: keep the license notice and make the corresponding source available.

**Weights.** The model card says `license: other`. There is no separate license file. The weight file is requested from the public Space at runtime and is not stored in this repository. Copying it into the repository is not covered by a stated license.

**Connectome.** FlyWire's public-release guidelines say the public data is under CC BY-NC 4.0. The model card says those non-commercial terms apply to anything derived from the graph. The packed connectome stays on the Space. The Space metadata hashes an upstream `LICENSE` file and does not include its text, so any extra author-release terms are still unread.

**Labels.** Lichess/chess-position-evaluations is CC0. This notebook does not ship those positions.

**Photograph.** The leg in the demo is by GorissM, CC BY-SA 2.0, via Wikimedia Commons.

## DataHub

A live run on El Camino DataHub is still outstanding. The hub login page responds. This session had no hub login, and the notebook is not on the `main` branch DataHub pulls until it is pushed. Still to check there: framing of `mlabonne-chessfly.static.hf.space`, a student download of about 148 MB, and WebGPU versus the JS fallback.

`jupyter-server-proxy` was not part of the local test, and this repository does not configure a hub proxy.

## Combined introductory lab

`Build_Your_Own_ChessFly_Model.ipynb` is the student notebook. It keeps the hosted ChessFly iframe and then builds the legal-move scorer. `ChessFly_DataHub_prototype.ipynb` and `ChessFly_train_readout_prototype.ipynb` stay in the folder until this combined notebook has been checked on DataHub. The combined notebook is not classroom-ready.

The hosted game and the training widget each request the published files. Shared browser caching was not verified, so students may see two downloads. The game can report WebGPU. The training widget forces the JavaScript backend so the float readout can be returned. Do not describe that widget as a WebGPU run.

Helpers: `fly_activity.py` loads the network and transfers activity in groups of six rows. `fly.get_activity()` raises with a load instruction if Python has not received the matrix. `fly_scorer.py` holds `create_move_scorer`, `train_scorer`, `plot_training`, `evaluate_scorer`, `describe_comparison`, `reset_scorer`, `save_intact_state`, and `describe_intervention`. `fly_board.py` draws a board from the FEN with matplotlib. Each `create_move_scorer` call returns a new object. `like=` copies another model's neurons and its original starting weights when the feature count is unchanged. `train_scorer` records `settings` on that object: feature count, training rows, learning rate, round count, and how many times Train has been called since the last reset. A second Train call continues from the current weights. `describe_comparison` reports a fair comparison only when the saved settings differ in exactly one of feature count, learning rate, and round count, both models were trained once, and a learning-rate or round-count change started from the same features and the same initial weights.

`data/lichess_lab.csv` has 60 positions: 36 pool, 12 validation (`i % 5 == 3`), and 12 test (`i % 5 == 4`), assigned from row order before fitting. Feature selection and fitting raise `HeldOutError` for validation and test indexes. Model comparison uses the validation rows. The test rows are evaluated in one later cell. Ablation compares predictions on the validation rows against activity and weights saved before the button press.

The earlier local fit on indexes 0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, and 13 matched 11 of 12 training targets and 0 of 12 test targets. Indexes 3, 8, and 13 are now validation rows, so that list is refused. The notebook states that result as a generalization problem. It is not a chess ranking.

Local Chrome run of the combined notebook’s default list, 5 October 2026, fresh kernel: training rows `[0, 1, 2, 5, 6, 7, 10, 11, 12, 15, 16, 17]`, 16 features, learning rate 0.5, 5 rounds. Activity shape `(60, 41692)`, JavaScript backend, 138,639 neurons, 15,091,983 connections, 40.4 s to load and run every position. Training agreement stayed 11/12. Validation agreement was 2/12. The one final test was 0/12 for both `model_v1` and the 8-feature `model_v2`. Every displayed move was legal. `model_v1` weight length after training was 2.1888; `model_v2` was 1.9500 and returned to 0 after reset while `model_v1` stayed 2.1888. A one-round learning-rate pair from identical initial weights went from length 0.188 at rate 0.1 to 1.88 at rate 1.0. Test index 4 raised `HeldOutError`. Ablation of the first 2,000,000 stored-order connections changed index 0’s activity sum from 1151.96 to 1503.75, left scorer weights fixed, and changed 7 of 12 validation predictions. Restore matched the saved activity and returned those predictions to the intact-network moves. DataHub was not part of this run.

Browser plumbing for the widget: the patch depends on exact strings in the minified file `worker-D5p9jH36.js`. It forces the JavaScript backend, because the published WebGPU path does not return the float state the decoder multiplies. It returns that float readout and accepts `ablate` and `restore`. If a published string no longer matches, the loader stops and does not invent a network. The patched JavaScript is not stored in this repository. Activity reaches Python as base64 float32 traits, six positions at a time. `anywidget` must be installed in the student kernel. It was not tested on DataHub. The hub login page at `https://elcamino.cloudbank.2i2c.cloud/hub/login` responds and requires an approved account. This session had no hub login, and the notebook is not on the `main` branch DataHub pulls until it is pushed. Do not call the lab classroom-ready until the iframe, Load, the training cells, and the stored-order ablation and restore have been run on DataHub with `anywidget` importable in that kernel.

Permissions: fetching and patching the GPL-3.0 worker in the browser does not put that program in the repo. Distributing the patched worker later would require the GPL-3.0 notice and source. The weight file remains `license: other`, with no grant text; training a new head on its activations is not discussed by the model card. The readout is derived from the FlyWire graph, so the card's CC BY-NC 4.0 statement applies. Do not commit the weights, the packed connectome, or a saved activity matrix. The upstream `LICENSE` text is still only a hash in the Space metadata. The connectome is the female FlyWire reconstruction. The assigned Google article is the male fly dataset. Do not treat them as the same map.

## Earlier notebooks

`ChessFly_DataHub_prototype.ipynb` is the earlier playing lesson, including the observation table. `ChessFly_train_readout_prototype.ipynb` is the earlier training lesson, written before the validation split. Neither is the DataHub launch notebook. The six-row file `lichess_sample.csv` remains the first technical sample. A four-class layer cannot name its held-out moves `b2b4` and `d5b5`. The combined lab does not use that file.

Local Chrome run of the earlier 12-row fit, 5 October 2026: activity shape `(60, 41692)`, JavaScript backend, 138,639 neurons, 15,091,983 connections, about 29.8 s to load and run every position. Training agreement 11/12, test agreement 0/12, every displayed model move legal. Ablation changed index 0's activity sum from 1151.96 to 1503.75 and left the scorer weights fixed.
