import itertools

import numpy as np
import pandas as pd

from src.randomization import (
    assign_treatment_stratified,
    estimate_weighted_ate_and_ci,
    fisher_pvalue,
    generate_potential_outcomes,
    neyman_se_stratified,
    stat_diff_in_means,
    stat_stratified,
    stat_studentized,
)


def test_generate_potential_outcomes_columns_and_counts():
    config = {
        "seed_population": 11,
        "N_by_stratum": {"A": 4, "B": 6},
        "tau_by_stratum": {"A": 0.2, "B": 0.4},
        "sd_y0_by_stratum": {"A": 1.0, "B": 1.0},
        "sd_noise_by_stratum": {"A": 1.0, "B": 1.0},
    }
    df = generate_potential_outcomes(config=config)
    assert list(df.columns) == ["unit_id", "g", "y0", "y1"]
    assert len(df) == 10
    assert (df["g"] == "A").sum() == 4
    assert (df["g"] == "B").sum() == 6


def test_assign_treatment_stratified_respects_n1_by_stratum():
    potential = pd.DataFrame(
        {
            "unit_id": np.arange(8),
            "g": ["A"] * 4 + ["B"] * 4,
            "y0": np.arange(8, dtype=float),
            "y1": np.arange(8, dtype=float) + 1.0,
        }
    )
    observed = assign_treatment_stratified(
        potential=potential,
        n1_by_stratum={"A": 1, "B": 3},
        seed=7,
    )
    assert list(observed.columns) == ["unit_id", "g", "z", "y"]
    assert observed.loc[observed["g"] == "A", "z"].sum() == 1
    assert observed.loc[observed["g"] == "B", "z"].sum() == 3


def test_statistics_values_on_fixed_data():
    data = pd.DataFrame(
        {
            "unit_id": [1, 2, 3, 4, 5, 6, 7, 8],
            "g": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "z": [1, 1, 0, 0, 1, 1, 0, 0],
            "y": [3.0, 5.0, 1.0, 3.0, 4.0, 6.0, 2.0, 4.0],
        }
    )
    diff = stat_diff_in_means(data)
    student = stat_studentized(data)
    strat = stat_stratified(data, {"A": 0.6, "B": 0.4})

    assert np.isclose(diff, 2.0)
    assert np.isclose(student, 2.0 / np.sqrt(2.0))
    assert np.isclose(strat, 2.0)


def test_fisher_pvalue_known_enumeration():
    data = pd.DataFrame(
        {
            "unit_id": [1, 2, 3, 4],
            "g": ["A", "A", "A", "A"],
            "z": [1, 1, 0, 0],
            "y": [1.0, 2.0, 3.0, 4.0],
        }
    )
    assignments = list(itertools.combinations([0, 1, 2, 3], 2))

    def rerandomize_fn(df: pd.DataFrame, seed: int) -> pd.DataFrame:
        treated = assignments[seed % len(assignments)]
        out = df.copy()
        out["z"] = 0
        out.loc[list(treated), "z"] = 1
        return out

    pvalue = fisher_pvalue(
        data=data,
        stat_fn=stat_diff_in_means,
        rerandomize_fn=rerandomize_fn,
        R=6,
        seed=0,
    )
    assert np.isclose(pvalue, 2.0 / 6.0)


def test_neyman_weighted_estimator_and_ci():
    data = pd.DataFrame(
        {
            "unit_id": [1, 2, 3, 4, 5, 6, 7, 8],
            "g": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "z": [1, 1, 0, 0, 1, 1, 0, 0],
            "y": [3.0, 5.0, 1.0, 3.0, 4.0, 6.0, 2.0, 4.0],
        }
    )
    lambdas = {"A": 0.6, "B": 0.4}
    se = neyman_se_stratified(data, lambdas)
    est = estimate_weighted_ate_and_ci(data, lambdas, alpha=0.05)

    expected_se = np.sqrt(1.04)
    assert np.isclose(se, expected_se)
    assert np.isclose(est["tau_hat"], 2.0)
    assert np.isclose(est["se_hat"], expected_se)
    assert est["ci_lower"] < est["tau_hat"] < est["ci_upper"]
