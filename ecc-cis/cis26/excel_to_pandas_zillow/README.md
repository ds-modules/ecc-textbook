# Excel to Pandas (Zillow)

| Notebook | Audience |
|----------|----------|
| `Excel_to_Pandas_Zillow.ipynb` | **Students** — exercise cells are stubs; solutions are in collapsible hints only. |
| `Excel_to_Pandas_Zillow_Instructor.ipynb` | **Instructors** — full solutions inline after each exercise prompt. |

## Regenerating the instructor copy

After editing the student notebook’s exercises, regenerate the instructor version:

```bash
python cis26/excel_to_pandas_zillow/build_instructor_notebook.py
```

Then re-apply any manual tweaks (e.g. title cell) if needed.

## Local module

`interact.py` must be on the path (same folder as the notebook, or add that folder to `sys.path`). See the import cell in the notebook.

## JupyterHub / nbgitpuller

Use links that open notebooks under **`cis26/excel_to_pandas_zillow/`** (the material moved out of a top-level `excel_to_pandas_zillow/` folder). If a sync fails because of leftover files from an old layout, remove any duplicate **`excel_to_pandas_zillow/`** tree under your clone or reset that repo folder per your hub’s instructions, then sync again.
