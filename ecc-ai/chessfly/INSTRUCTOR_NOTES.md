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
