# Instructor notes

This file is for the instructor. It is not part of the student notebook.

Students play the published ChessFly demo inside the notebook. They do not train it. There is no stand-in network in the student flow.

## What students do

1. Read that a network built on fruit-fly wiring was already trained on chess examples.
2. Distinguish training (numbers change from examples) from inference (numbers stay fixed while the network answers).
3. Run the iframe cell. They play White. The network plays Black.
4. Predict a reply before moving, play several moves and record one observation, then say what the developers had to add besides the wiring.
5. Say what a game establishes about AI, and what further evidence a claim about animal cognition would need.

The student notebook does not give the answers. One local test, after e4, got a black pawn from c7 to c5, with the page reporting 517 positions evaluated in 4.0 seconds on WebGPU. Other sessions can show a different reply. Do not grade students against that one move.

## What to look for

**Beyond the wiring.** The FlyWire connections and their signs stay fixed. The published training changed an encoder from the board into 10,855 visual neurons, one positive gain on each connection, a gain and threshold per neuron and step, and a decoder into a move and a win probability. The labels were Stockfish-annotated Lichess positions (about 4.4 million; the dataset is CC0). The page also runs a depth-3 search on top of each forward pass. A strong answer names learned pieces or chess labels, not only "a computer" or "the rules of chess."

**Ethics.** A game shows that this trained model can choose legal chess moves. It does not show that a living fly plays chess, that the activity matches recordings from a fly, or that the animal learned this task. Look for a request for evidence the demo does not provide: behavior or recordings from living flies, more than one animal, or a test the model was not trained on.

## How the board is embedded

The code cell displays an iframe to `https://mlabonne-chessfly.static.hf.space/`. That is the published static Space. The page, the inference worker, the packed connectome, and `flynet.safetensors` are loaded by the student's browser from that host.

`https://huggingface.co/spaces/mlabonne/chessfly` sends `X-Frame-Options: DENY`, so the notebook does not iframe that URL. The same app is the direct-open link printed above the iframe and linked in the student notebook.

In local JupyterLab 4.6.4, a saved iframe output was stripped until the cell was run in that session. After the run, the iframe had no sandbox attribute. The browser then downloaded about 148 MB and reported WebGPU. The worker messages are `init` and `evaluate` only.

File sizes on the Space: `data/connectome.bin.gz` 47,051,343 bytes, `data/neurons.bin.gz` 1,442,541 bytes, `data/flynet.safetensors` 99,572,154 bytes.

The kernel does not run the forward pass. Internet is required in the browser, including the Hugging Face file host the Space redirects to. One local load stalled with no progress, and an earlier one reported a network error. Later loads finished, including the completed reply above.

The JavaScript fallback inside the worker was not used in the local test, because WebGPU was available.

## Permissions

**App.** The Space card says GPL-3.0 because the page includes chessground. This course notebook does not copy that program. It links to the hosted copy. GPL-3.0's distribution conditions apply if someone later commits that JavaScript to this repository: keep the license notice and make the corresponding source available.

**Weights.** The model card says `license: other`. The model repository has no separate license file. The notebook loads `flynet.safetensors` from the public Space at runtime and does not store it here. Copying the weight file into this repository is not covered by a stated license.

**Connectome.** FlyWire's public-release guidelines say the public data is under CC BY-NC 4.0. The model card says those non-commercial terms apply to anything derived from the graph. The packed connectome stays on the Space. The Space metadata records a SHA-256 for an upstream `LICENSE` file and does not include the file text, so any extra author-release terms are still unread.

**Labels.** Lichess/chess-position-evaluations is CC0. This notebook does not ship those positions.

**Photograph.** The leg in the demo is by GorissM, CC BY-SA 2.0, via Wikimedia Commons. It is part of their page, not a file in this repository.

## DataHub

A live run on El Camino DataHub is still outstanding. The hub login page responds, and this session had no hub login. The notebook is also not on the `main` branch that DataHub pulls until it is pushed. Still to check on the hub: whether the hub content security policy allows framing `mlabonne-chessfly.static.hf.space`, whether student browsers can download about 148 MB, and whether those browsers have WebGPU.

`jupyter-server-proxy` was not installed in the local test environment, and this repository does not configure a hub proxy. A 2i2c static-site service would require a hub administrator.
