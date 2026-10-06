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

## Build-your-own-model lab

`ChessFly_train_readout_prototype.ipynb` is a separate guided lab. The playing notebook and its iframe stay as they are. This lab is not classroom-ready.

Students construct the scorer in small cells. The helpers live in `fly_scorer.py` (`create_move_scorer`, `train_scorer`, `evaluate_scorer`, `compare_scorers`, `reset_scorer`). Each call to `create_move_scorer` returns a new object with its own weights. `reset_scorer` zeros that object only. `model_v2` is created with `n_features` 8 while `model_v1` stays at 16. The browser widget is `fly_activity.py`. It only loads the network and transfers activity. Training is a Python cell.

The widget fetches the published worker and patches it in memory. The patch depends on exact strings in the minified file `worker-D5p9jH36.js`. It forces the JavaScript backend, because the published WebGPU path does not return the float state the decoder multiplies. It returns that float readout and accepts two extra messages, `ablate` and `restore`. If a published minified string no longer matches, the loader stops and does not invent a network. The patched JavaScript is not stored in this repository. Activity reaches Python as a base64 float32 trait. `fly.get_activity()` raises if that transfer has not happened. Do not tell students that Python computed the connectome.

The lab file is `data/lichess_lab.csv`: 60 verified white-to-move positions, 48 in the pool and 12 fixed as test. Provenance, the parquet byte ranges, the `i % 5 == 4` split, and the two castling rewrites (`e1h1` to `e1g1`, `e1a1` to `e1c1`) are in `data/README.md`. Feature selection and fitting both call `check_training_rows` and raise `HeldOutError` if a test index is included. Evaluation may read the test rows and does not update weights. Predictions are the highest-scoring legal move. An untrained scorer matches the alphabetical baseline. Stockfish top-move agreement is stated in the notebook as one narrow metric, not a complete chess-strength assessment.

The default student settings are 16 features, learning rate 0.5, and 5 rounds, on pool indexes 0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, and 13. That is 528 trainable numbers. `model_v2` uses 8 features (264 numbers) and the same rows, learning rate, and rounds. Connection ablation is the last optional section. The button turns off the **first 2,000,000 connections in stored order**, meaning the first 2,000,000 entries of the published weight array. That is not a named brain region or a verified circuit. The activity sum is a total of readout numbers, not a measure of intelligence or chess performance. Ablation replaces the activity matrix and does not refit the scorer.

Local Chrome run from a fresh kernel, 5 October 2026: Python printed activity shape `(60, 41692)`, all finite, after a 29.8 s browser load on the JavaScript backend (138,639 neurons, 15,091,983 connections). Activity is sent in groups of six rows so the handoff is real data, not one giant message. With 16 features, learning rate 0.5, and 5 rounds, the weight length moved from 0 to 1.9809, training agreement was 11/12, and test agreement was 0/12. Every displayed model move was legal. `model_v2` (8 features, 264 numbers) trained to weight length 1.7410 while `model_v1` stayed at 1.9809. Resetting `model_v2` returned it to 0 and left `model_v1` unchanged. A one-round pair at learning rates 0.1 and 1.0 produced weight lengths 0.189 and 1.890. Passing test index 4 to `create_move_scorer` raised `HeldOutError`. Ablation of the first 2,000,000 stored-order connections changed index 0's activity sum from 1151.96 to 1503.75 and did not change `model_v1`'s weights. Some test predictions changed. This has not been repeated on DataHub.

The six-row file `lichess_sample.csv` remains the earlier technical sample. A four-class layer cannot name its held-out moves `b2b4` and `d5b5`, and the rows API did not supply a repeated-move split. The lab does not use that file.

`anywidget` has to be installed in the student kernel. It is not part of the playing notebook. It was not tested on DataHub. The hub login page at `https://elcamino.cloudbank.2i2c.cloud/hub/login` responds and requires an approved account. This session had no hub login, and the notebook is not on the `main` branch DataHub pulls until it is pushed. Do not call the lab classroom-ready until Load, the Python training cells, and the stored-order ablation have been run on DataHub with `anywidget` importable in that kernel.

Permissions for this extra use: fetching and patching the GPL-3.0 worker in the browser does not put that program in the repo. Distributing the patched worker later would require the GPL-3.0 notice and source. The weight file remains `license: other`, with no grant text; training a new head on its activations is not discussed by the model card. The readout is derived from the FlyWire graph, so the card's CC BY-NC 4.0 statement applies. Do not commit the weights, the packed connectome, or a saved activity matrix. The upstream `LICENSE` text is still only a hash in the Space metadata.
