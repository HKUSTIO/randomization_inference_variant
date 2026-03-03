import json
from pathlib import Path


def test_output_files_exist_after_run():
    root = Path(__file__).resolve().parents[1]
    results = root / "output" / "results.json"
    observed = root / "cleaned" / "observed_data.csv"
    potential = root / "cleaned" / "potential_outcomes.csv"

    assert observed.exists(), "Missing cleaned/observed_data.csv. Run scripts/run_pipeline.py."
    assert potential.exists(), "Missing cleaned/potential_outcomes.csv. Run scripts/run_pipeline.py."
    assert results.exists(), "Missing output/results.json. Run scripts/run_pipeline.py."


def test_results_json_has_required_keys():
    root = Path(__file__).resolve().parents[1]
    results = json.loads((root / "output" / "results.json").read_text(encoding="utf-8"))
    required = {
        "fisher_diff_in_means_pvalue",
        "fisher_studentized_pvalue",
        "fisher_stratified_size_weighted_pvalue",
        "fisher_stratified_equal_weighted_pvalue",
        "neyman_size_weighted",
        "neyman_equal_weighted",
    }
    assert required.issubset(results.keys()), "results.json is missing required outputs."


def test_rendered_html_exists_and_contains_required_sections():
    root = Path(__file__).resolve().parents[1]
    html_path = root / "report" / "solution.html"
    assert html_path.exists(), "Missing report/solution.html. Render report/solution.qmd."

    html = html_path.read_text(encoding="utf-8")
    required_strings = [
        "Fisher p-value variants",
        "Neyman inference under different weights",
        "difference_in_means",
        "studentized",
        "size_weighted",
        "equal_weighted",
    ]
    for token in required_strings:
        assert token in html, f"report/solution.html does not contain `{token}`."
