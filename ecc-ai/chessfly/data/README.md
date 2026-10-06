# Chess position sample

`lichess_sample.csv` is a small excerpt of [Lichess/chess-position-evaluations](https://huggingface.co/datasets/Lichess/chess-position-evaluations), which is CC0. It was read on 5 October 2026 from the Hugging Face datasets rows API:

`https://datasets-server.huggingface.co/rows?dataset=Lichess/chess-position-evaluations&config=default&split=train`

The full training split has 988,851,570 rows and does not include a game identifier. These six rows are unique white-to-move positions from row indices 80000, 250000, 4000000, 9000001, 20000000, and 50000000. Nearby rows often repeat the same FEN with another engine line, so one row was kept for each FEN (the first row when the search depth was equal).

`stockfish_uci` is the first move in the dataset field `line`. `depth` and `cp` are the Stockfish search depth and centipawn evaluation from that row. `legal_uci` was checked with python-chess; every Stockfish move in this file is legal. The FEN strings are the four-field positions published in the dataset.

The `split` column was assigned before any classroom fitting: sort by `row_idx`, then the first four positions are `train` and the last two are `test`. Positions that share a game cannot be kept together, because this dataset does not publish a game id.

Each Stockfish move in this file appears once. A classifier whose outputs are only the four training move names cannot name `b2b4` or `d5b5`. Further rows from the datasets API, requested on 5 October 2026, were often rejected with HTTP 429 or 502. The extra rows that did arrive did not provide several distinct positions for every move in both the training split and the test split. No labels were invented to fill that gap. The training notebook therefore scores the legal moves of each board instead of classifying four fixed move names.

The FlyWire connectome, FlyNet weights, and neuron activities are not in this folder. The training notebook loads those from the published ChessFly site when a student presses Load. Activity is computed in the browser and is not saved here.

## Lab sample

`lichess_lab.csv` is the sample used by the guided training notebook. It has 60 unique white-to-move positions. It was built on 5 October 2026 from `data/data_0000.parquet` in the same CC0 dataset, using HTTP range requests of four parquet row groups. The rows API was not used. The full parquet file is about 2.2 GB and is not in this repository.

The footer of `data_0000.parquet` was read first. These row groups were then downloaded by byte range:

| Row group | Byte range (start inclusive, end exclusive) | Rows in the group |
| --- | --- | --- |
| 0 | 4–36,464,823 | 1,048,576 |
| 18 | 712,019,603–754,372,687 | 1,048,576 |
| 36 | 1,452,406,200–1,494,939,996 | 1,048,576 |
| 53 | 2,165,607,928–2,190,242,856 | 622,499 |

`row_idx` is the position in the full shard: row-group index times 1,048,576, plus the offset inside that group. `source_file` is `data/data_0000.parquet`. `row_group` records which of the four groups the row came from.

A row was kept when White is to move, `depth` is at least 15, `mate` is null, the FEN had not already been kept, and the first move of `line` is legal under python-chess 1.11.2. Fifteen positions were taken at even spacing across the unique FENs in each row group, for 60 rows. There are 53 distinct Stockfish moves.

Two Stockfish lines used chess960-style castling names. Those are the same castling moves as the standard names, and the ChessFly move list uses the standard names. They were rewritten and then checked again:

- row 178,456: `e1h1` rewritten to `e1g1`
- row 37,898,993: `e1a1` rewritten to `e1c1`

After that rewrite, every `stockfish_uci` is one of that row's `legal_uci` values. No promotion moves appear in these legal lists.

The `split` column was assigned before any fitting, from row order only. Sort by `row_idx`. In that ordered list, a 0-based position `i` is `test` when `i % 5 == 4`, and `pool` otherwise. That gives 12 test rows and 48 pool rows. The test indexes in the CSV, as a pandas index, are 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, and 59. The dataset still has no game id, so the spacing reduces clustering and does not guarantee that two positions come from different games. The six-row file above is unchanged and is too small for this lab.
