import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.randomization import assign_treatment_stratified, generate_potential_outcomes


def main() -> None:
    config = json.loads((ROOT / "config" / "assignment.json").read_text(encoding="utf-8"))
    cleaned_dir = ROOT / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    potential = generate_potential_outcomes(config)
    observed = assign_treatment_stratified(
        potential=potential,
        n1_by_stratum=config["N1_by_stratum"],
        seed=config["seed_assignment"],
    )

    potential.to_csv(cleaned_dir / "potential_outcomes.csv", index=False)
    observed.to_csv(cleaned_dir / "observed_data.csv", index=False)


if __name__ == "__main__":
    main()
