from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd


def generate_potential_outcomes(config: dict) -> pd.DataFrame:
    """
    Return a DataFrame with columns: unit_id, g, y0, y1.
    """
    raise NotImplementedError("Implement generate_potential_outcomes().")


def assign_treatment_stratified(
    potential: pd.DataFrame,
    n1_by_stratum: dict[str, int],
    seed: int,
) -> pd.DataFrame:
    """
    Return observed data with columns: unit_id, g, z, y.
    """
    raise NotImplementedError("Implement assign_treatment_stratified().")


def stat_diff_in_means(data: pd.DataFrame) -> float:
    """
    Unweighted difference in means: E[y|z=1] - E[y|z=0].
    """
    raise NotImplementedError("Implement stat_diff_in_means().")


def stat_studentized(data: pd.DataFrame) -> float:
    """
    Studentized statistic:
      (mean_t - mean_c) / sqrt(s2_t / n_t + s2_c / n_c).
    """
    raise NotImplementedError("Implement stat_studentized().")


def stat_stratified(data: pd.DataFrame, lambda_by_stratum: dict[str, float]) -> float:
    """
    Weighted sum of stratum-specific differences in means.
    """
    raise NotImplementedError("Implement stat_stratified().")


def fisher_pvalue(
    data: pd.DataFrame,
    stat_fn: Callable[[pd.DataFrame], float],
    rerandomize_fn: Callable[[pd.DataFrame, int], pd.DataFrame],
    R: int,
    seed: int,
) -> float:
    """
    Two-sided Fisher randomization p-value based on rerandomization.
    """
    raise NotImplementedError("Implement fisher_pvalue().")


def neyman_se_stratified(data: pd.DataFrame, lambda_by_stratum: dict[str, float]) -> float:
    """
    Neyman-style conservative SE for weighted stratified estimator:
      sqrt(sum_g lambda_g^2 * (s2_tg / n_tg + s2_cg / n_cg)).
    """
    raise NotImplementedError("Implement neyman_se_stratified().")


def estimate_weighted_ate_and_ci(
    data: pd.DataFrame,
    lambda_by_stratum: dict[str, float],
    alpha: float,
) -> dict[str, float]:
    """
    Return dictionary with keys: tau_hat, se_hat, ci_lower, ci_upper.
    """
    raise NotImplementedError("Implement estimate_weighted_ate_and_ci().")
