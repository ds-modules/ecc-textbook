"""
One-off script to generate Excel_to_Pandas_Zillow_Instructor.ipynb from the student notebook.
Run from repo root: python excel_to_pandas_zillow/build_instructor_notebook.py
"""
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STUDENT = ROOT / "Excel_to_Pandas_Zillow.ipynb"
INSTRUCTOR = ROOT / "Excel_to_Pandas_Zillow_Instructor.ipynb"

EX1_SOLUTION = '''# Solution: Exercise 1 — State-Level Filtering and Aggregation

national_median = home_values_latest['HomeValue'].median()
print(f"National median home value: ${national_median:,.0f}")

tx_above_national = home_values_latest[
    (home_values_latest['StateName'] == 'TX') &
    (home_values_latest['HomeValue'] > national_median)
].sort_values('HomeValue', ascending=False)

print(f"\\nTexas metros above national median: {len(tx_above_national)}")
display(tx_above_national[['RegionName', 'HomeValue']])
'''

EX2_SOLUTION = '''# Solution: Exercise 2 — Pivot Table

top8_states = latest_home_values_copy['StateName'].value_counts().head(8).index

pivot_ex2 = latest_home_values_copy[latest_home_values_copy['StateName'].isin(top8_states)].pivot_table(
    values='HomeValue',
    index='StateName',
    columns='MarketTier',
    aggfunc='mean',
    fill_value=0,
    margins=True
).round(0)

print('Average home value by state and market tier:')
display(pivot_ex2)
'''

EX3_SOLUTION = '''# Solution: Exercise 3 — Year-Over-Year Growth Chart

annual_median = home_values.groupby('Year')['HomeValue'].median()
annual_growth = annual_median.pct_change() * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

annual_median.plot(ax=ax1, marker='o', linewidth=2, color='steelblue')
ax1.set_title('Annual Median Home Value (U.S., All Metros)', fontweight='bold')
ax1.set_ylabel('Home Value ($)')
ax1.grid(True, alpha=0.3)

annual_growth.plot(ax=ax2, marker='o', linewidth=2, color='green', label='YoY growth')
ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Zero growth')
ax2.set_title('Year-Over-Year Growth Rate (U.S., All Metros)', fontweight='bold')
ax2.set_ylabel('Growth Rate (%)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
'''

EX4_SOLUTION = '''# Solution: Exercise 4 — Buy vs. Rent Analysis

top6 = housing_combined['StateName'].value_counts().head(6).index
ex4_data = housing_combined[housing_combined['StateName'].isin(top6)]

tier_counts = (
    ex4_data.groupby(['StateName', 'Buy_vs_Rent'])
    .size()
    .unstack(fill_value=0)
)

plt.figure(figsize=(12, 6))
tier_counts.plot(kind='bar', width=0.8)
plt.title('Buy vs. Rent Signal by State', fontsize=14, fontweight='bold')
plt.xlabel('State')
plt.ylabel('Number of Metros')
plt.xticks(rotation=0)
plt.legend(title='Signal')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
'''


def to_source(s: str):
    """Split string into notebook source lines."""
    return [line + "\n" for line in s.rstrip().split("\n")] + ([] if s.endswith("\n") else [])


def main():
    with open(STUDENT, encoding="utf-8") as f:
        nb = json.load(f)

    # Title cell at top
    title_cell = {
        "cell_type": "markdown",
        "id": "instructor_title",
        "metadata": {},
        "source": ["# Excel to Pandas (Zillow) — **Instructor solutions**\n"],
    }
    nb["cells"].insert(0, title_cell)

    # Instructor banner — insert after title (now index 1)
    banner = {
        "cell_type": "markdown",
        "id": "instructor_banner",
        "metadata": {},
        "source": [
            "---\n",
            "## Instructor version\n",
            "\n",
            "**Not for distribution to students.** This notebook includes **full solutions** for all practice exercises. "
            "The student-facing notebook uses stubs and collapsible hints instead.\n",
            "\n",
            "---\n",
        ],
    }
    nb["cells"].insert(1, banner)  # after title

    # Cell indices shift by +1 after insert; exercises were at 93+ -> now 94+
    # Find cells by id after insert
    id_to_idx = {}
    for i, c in enumerate(nb["cells"]):
        cid = c.get("id")
        if cid:
            id_to_idx[cid] = i

    def replace_code_cell(cell_id, new_source_str):
        idx = id_to_idx.get(cell_id)
        if idx is None:
            raise SystemExit(f"Cell id not found: {cell_id}")
        nb["cells"][idx]["source"] = to_source(new_source_str)
        nb["cells"][idx]["outputs"] = []
        nb["cells"][idx]["execution_count"] = None

    replace_code_cell("ex1_solution", EX1_SOLUTION)

    # Replace hint markdown (ex1) with short note — find by content
    for i, c in enumerate(nb["cells"]):
        if c.get("cell_type") != "markdown":
            continue
        src = "".join(c.get("source", []))
        if "HINTS: See our staff solution outline" in src and "Solution: Exercise 1" in src:
            nb["cells"][i] = {
                "cell_type": "markdown",
                "id": "ex1_instructor_note",
                "metadata": {},
                "source": [
                    "*Exercise 1 solution is in the code cell above (no collapsible hint in instructor copy).*\n",
                ],
            }
            break

    replace_code_cell("ex2_solution", EX2_SOLUTION)

    # Remove duplicate solution cells (were immediately after stubs) — find by id
    for dup_id in ["3da83568", "8d77edbf", "a390ac23"]:
        for i, c in enumerate(nb["cells"]):
            if c.get("id") == dup_id:
                nb["cells"][i] = {
                    "cell_type": "markdown",
                    "id": c["id"] + "_removed",
                    "metadata": {},
                    "source": ["*Duplicate solution cell removed — see previous code cell.*\n"],
                }
                break

    replace_code_cell("ex3_solution", EX3_SOLUTION)
    replace_code_cell("ex4_solution", EX4_SOLUTION)

    # Optional: strip execution outputs from entire nb for smaller file (keep structure)
    # Uncomment if desired:
    # for c in nb["cells"]:
    #     if c.get("cell_type") == "code":
    #         c["outputs"] = []
    #         c["execution_count"] = None

    with open(INSTRUCTOR, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)

    print(f"Wrote {INSTRUCTOR}")


if __name__ == "__main__":
    main()
