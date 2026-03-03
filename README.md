# Randomization Inference Variant Exercise

This GitHub Classroom assignment asks you to build variants of Fisher randomization inference and Neyman inference for stratified experiments with an explicit data pipeline:
input -> cleaned -> output.

## Learning goals

- Implement Fisher randomization p-values with multiple statistics.
- Compare weighted stratified estimators under different weight schemes.
- Compute Neyman-style conservative standard errors and confidence intervals.
- Produce a reproducible report in Quarto HTML.

## Project structure

```text
randomization_inference_variant/
├── .github/workflows/classroom.yml
├── config/
│   └── assignment.json
├── input/
├── cleaned/
│   ├── potential_outcomes.csv      # created by cleaning stage
│   └── observed_data.csv           # created by cleaning stage
├── output/
│   └── results.json                # created by analysis stage
├── report/
│   └── solution.qmd
├── scripts/
│   ├── run_cleaning.py
│   ├── run_analysis.py
│   ├── run_pipeline.py
│   └── run_assignment.py
├── src/
│   ├── __init__.py
│   └── randomization.py
├── pyproject.toml
└── README.md
```

## Your tasks

All parameters and hyperparameters are defined in `config/assignment.json`. Use that file as the single source of truth for simulation and inference settings. Do not hard-code constants in code files.

Implement the required functions in `src/randomization.py`:

1. `generate_potential_outcomes`
2. `assign_treatment_stratified`
3. `stat_diff_in_means`
4. `stat_studentized`
5. `stat_stratified`
6. `fisher_pvalue`
7. `neyman_se_stratified`
8. `estimate_weighted_ate_and_ci`

Function-level requirements:

- `generate_potential_outcomes(config)`
  - Use values in `config/assignment.json`.
  - Generate finite-population potential outcomes by stratum.
  - Return columns exactly: `unit_id`, `g`, `y0`, `y1`.

- `assign_treatment_stratified(potential, n1_by_stratum, seed)`
  - Randomize treatment within each stratum.
  - Enforce exact treated counts per stratum from `n1_by_stratum`.
  - Build observed outcome with
  $$
  y_i = z_i y_i(1) + (1-z_i)y_i(0).
  $$
  - Return columns exactly: `unit_id`, `g`, `z`, `y`.

- `stat_diff_in_means(data)`
  - Compute
  $$
  \bar{y}_1 - \bar{y}_0.
  $$
  - Return a scalar float.

- `stat_studentized(data)`
  - Use `stat_diff_in_means` as numerator.
  - Divide by a standard-error-style denominator based on treatment/control sample variances.
  - Use:
  $$
  T_{stud}
  =
  \frac{\bar{y}_1-\bar{y}_0}
  {\sqrt{\frac{s_1^2}{n_1}+\frac{s_0^2}{n_0}}}.
  $$
  - Follow the assignment convention consistently for all runs.

- `stat_stratified(data, lambda_by_stratum)`
  - Compute within-stratum effects and aggregate with weights
  $$
  \sum_g \lambda_g(\bar{y}_{1g}-\bar{y}_{0g}).
  $$

- `fisher_pvalue(data, stat_fn, rerandomize_fn, R, seed)`
  - Compute observed statistic.
  - Rerandomize assignment `R` times with `rerandomize_fn`.
  - Return two-sided randomization p-value using absolute statistics.

- `neyman_se_stratified(data, lambda_by_stratum)`
  - Compute conservative weighted Neyman SE based on stratum-level sample variances.
  - Use:
  $$
  \widehat{\mathrm{SE}}_{Neyman}
  =
  \sqrt{
    \sum_{g}
    \lambda_{g}^{2}
    \left(
      \frac{s_{1g}^{2}}{n_{1g}}
      +
      \frac{s_{0g}^{2}}{n_{0g}}
    \right)
  }.
  $$

- `estimate_weighted_ate_and_ci(data, lambda_by_stratum, alpha)`
  - Return dictionary with keys exactly:
    - `tau_hat`
    - `se_hat`
    - `ci_lower`
    - `ci_upper`
  - Use two-sided normal critical value with `alpha`.

Then complete the report in `report/solution.qmd` by running the pipeline script and presenting:

- Fisher p-value with difference-in-means statistic.
- Fisher p-value with studentized statistic.
- Fisher p-value with stratified statistic under size weights and equal weights.
- Neyman estimate and confidence interval under both weight schemes.

## Workflow

Accept the assignment through the GitHub Classroom link provided by the instructor. This creates a private repository under the course organization with the starter code. Clone it to your local machine:

```bash
git clone https://github.com/HKUSTIO/<your-repo-name>.git
cd <your-repo-name>
```

Install dependencies with `uv`:

```bash
uv sync
```

Work on the assignment locally. Implement the required functions in `src/randomization.py`, run the pipeline, and render the report:

```bash
uv run python scripts/run_pipeline.py
uv run quarto render report/solution.qmd
```

The pipeline has two stages. The cleaning stage (`scripts/run_cleaning.py`) maps `input` to `cleaned`. The analysis stage (`scripts/run_analysis.py`) maps `cleaned` to `output`. The script `scripts/run_pipeline.py` executes both stages in order.

When you are ready, commit your changes and push to GitHub:

```bash
git add -A
git commit -m "your message"
git push
```

Every push to the `main` branch triggers the autograding workflow on GitHub Actions. The workflow runs hidden test suites against your code and produces a score out of 100 points, split into two components: core inference functions (60 points) and rendered report and outputs (40 points).

To see your score, go to your repository on GitHub, click the Actions tab, and open the latest "Autograding Tests" run. The score table appears in the run summary at the top of the page. You can also see the score on the GitHub Classroom dashboard.

You may push as many times as you like before the deadline. Each push triggers a new grading run, and the latest score is the one recorded. There is no penalty for multiple submissions.

## Grading policy

This assignment is graded only on artifacts you can revise and resubmit by pushing additional commits.

Grading focuses on two components. Core implementation correctness (60 points) covers the required functions in `src/randomization.py`: the functions run and return outputs in the required format, formulas and estimators are implemented correctly, and the pipeline behavior is reproducible under the configured seeds. Report and output completeness (40 points) covers the data pipeline integrity, the rendered report, and the output files: `scripts/run_cleaning.py` writes required files into `cleaned/`, `scripts/run_analysis.py` reads from `cleaned/` and writes required files into `output/`, `report/solution.html` renders successfully from `report/solution.qmd`, and required Fisher and Neyman variant results are present.

Items that are hard to fix after history is pushed are not grading targets. For example, grading does not rely on commit-message wording, number of commits, or other immutable repository-history details.
