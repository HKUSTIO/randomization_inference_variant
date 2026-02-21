import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.randomization import estimate_weighted_ate_and_ci, fisher_pvalue, stat_diff_in_means, stat_stratified, stat_studentized


def build_rerandomize_fn(n1_by_stratum: dict[str, int]):
    def rerandomize_fn(data: pd.DataFrame, seed: int) -> pd.DataFrame:
        rng = np.random.default_rng(seed)
        df = data.copy()
        df["z"] = 0
        for g, group in df.groupby("g"):
            idx = group.index.to_numpy()
            n1 = int(n1_by_stratum[g])
            treated_idx = rng.choice(idx, size=n1, replace=False)
            df.loc[treated_idx, "z"] = 1
        return df

    return rerandomize_fn


def main() -> None:
    config = json.loads((ROOT / "config" / "assignment.json").read_text(encoding="utf-8"))
    cleaned_dir = ROOT / "cleaned"
    output_dir = ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    observed = pd.read_csv(cleaned_dir / "observed_data.csv")

    n1_by_stratum = config["N1_by_stratum"]
    lambda_size = config["lambda_by_stratum"]["size_weighted"]
    lambda_equal = config["lambda_by_stratum"]["equal_weighted"]
    rerandomize_fn = build_rerandomize_fn(n1_by_stratum=n1_by_stratum)
    stat_strat_size = lambda df: stat_stratified(df, lambda_size)
    stat_strat_equal = lambda df: stat_stratified(df, lambda_equal)

    p_diff = fisher_pvalue(
        data=observed,
        stat_fn=stat_diff_in_means,
        rerandomize_fn=rerandomize_fn,
        R=config["R_fisher"],
        seed=config["seed_assignment"],
    )
    p_student = fisher_pvalue(
        data=observed,
        stat_fn=stat_studentized,
        rerandomize_fn=rerandomize_fn,
        R=config["R_fisher"],
        seed=config["seed_assignment"] + 1,
    )
    p_size = fisher_pvalue(
        data=observed,
        stat_fn=stat_strat_size,
        rerandomize_fn=rerandomize_fn,
        R=config["R_fisher"],
        seed=config["seed_assignment"] + 2,
    )
    p_equal = fisher_pvalue(
        data=observed,
        stat_fn=stat_strat_equal,
        rerandomize_fn=rerandomize_fn,
        R=config["R_fisher"],
        seed=config["seed_assignment"] + 3,
    )

    ci_size = estimate_weighted_ate_and_ci(
        data=observed,
        lambda_by_stratum=lambda_size,
        alpha=config["alpha"],
    )
    ci_equal = estimate_weighted_ate_and_ci(
        data=observed,
        lambda_by_stratum=lambda_equal,
        alpha=config["alpha"],
    )

    results = {
        "fisher_diff_in_means_pvalue": float(p_diff),
        "fisher_studentized_pvalue": float(p_student),
        "fisher_stratified_size_weighted_pvalue": float(p_size),
        "fisher_stratified_equal_weighted_pvalue": float(p_equal),
        "neyman_size_weighted": ci_size,
        "neyman_equal_weighted": ci_equal,
    }
    (output_dir / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
