# HyperTwin: a home blood-pressure digital twin (research prototype)

**Pitch:** a small, patient-specific twin for hypertension. It starts from a patient's EHR, updates with each daily home reading plus sleep and steps, forecasts tomorrow's morning systolic BP, and explains the forecast.

> Synthetic data only. Not a diagnosis or treatment tool.

## Team and college/incubator
- Team name: arshin.kazi20
- Members: Arshin Kazi
- College / incubator: Mody University of Science and Technology

## Problem and target population
Home BP readings are sparse and noisy. Target use case: adults on home BP monitoring; predicted event is "next-morning SBP at or above 135 mmHg" (guidelines cite 135/85 mmHg as the home-BP diagnostic threshold for multi-day averages, so a single-morning threshold is an engineering proxy; see `RESEARCH.md`).

## Existing solutions and differentiation
See `RESEARCH.md`. Many public submissions found for this challenge focus on diabetes; this one targets hypertension with a state-space twin, data-quality gating and a decomposed explanation. No novelty claim is made. Sources and limits of the research are in `RESEARCH.md`.

## How the twin works
1. **EHR prior:** OLS from age, BMI, antihypertensive count, family history, last clinic SBP to the patient's baseline level.
2. **Sensor stream:** daily morning SBP/DBP, sleep, steps. Missing days and implausible values (SBP outside 70-250, DBP >= SBP) do not move the state.
3. **State:** Kalman local-level filter, updated one day at a time (no look-ahead; tested).
4. **Forecast:** Gaussian next-morning SBP and P(SBP >= target), with contributions (EHR prior, learned level, sleep, steps).
5. **Scenario:** what-if sleep/steps using learned associations (illustrative, not causal).

## Technical stack

- **Language:** Python
- **Dashboard:** Streamlit
- **Data processing:** NumPy, Pandas
- **Statistical modelling:** scikit-learn / Statsmodels (as used in the implementation)
- **Visualisation:** Plotly (if used in the implementation)
- **Testing:** pytest, Streamlit AppTest
- **Model:** OLS-based EHR prior and Kalman local-level state-space filter

See `requirements.txt` for the complete dependency list.

## Data
Fully synthetic and seeded (`src/generate_data.py`, seed 2026): 150 patients x 90 days. Sleep/steps effects are assumed, not clinical findings. `data/*.csv` is generated output.

## Architecture

- [Architecture and system design](ARCHITECTURE.md)

## Presentation

- [View or download the project presentation (PPTX)](PRESENTATION.pptx)

## Evaluation and actual results
**Split:** 150 synthetic patients; parameters (including baseline residual SDs) are fit on the first 90 patients only; the other 60 patients (disjoint) are the test set. Test is forward in time, 14-day warm-up, 4,024 predictions on days with a valid reading (event rate 21.7%). Run: `python -m src.evaluate` (writes `results.json`). Single seed, no confidence intervals.

**Headline (fair, no same-day information):** the twin forecasts using only past data, with next-day sleep/steps assumed equal to the patient's past average.

| Method | MAE (mmHg) | AUROC | Brier |
|---|---|---|---|
| HyperTwin (past-average covariates) | 4.25 | 0.937 | 0.075 |
| 7-day mean | 4.33 | 0.935 | 0.076 |
| Last valid reading | 5.44 | 0.904 | 0.099 |

**What-if/oracle setting** (same-day sleep/steps treated as known or planned), compared against an equally informed baseline:

| Method | MAE | AUROC | Brier |
|---|---|---|---|
| HyperTwin (same-day covariates) | 3.96 | 0.947 | 0.070 |
| 7-day adjusted mean + same-day covariates | 4.01 | 0.946 | 0.071 |

**Reading these honestly:** the twin clearly beats "last reading", but its edge over a 7-day mean is small (about 0.1 mmHg MAE, near-identical AUROC) and untested for significance. All data are synthetic, so results show agreement with our own generator, not clinical validity.

## Install and run
```
pip install -r requirements.txt
python -m src.generate_data
streamlit run app.py
```
Dashboard: choose a held-out patient, drag the replay slider, add an observation in the sidebar (risk updates), use the What-if tab.

## Tests
`python -m pytest -q`: 10 passed on 24 Oct 2026 (determinism, validity gate, state update, scenario direction, contributions sum, no look-ahead, no same-day covariate use in the realistic mode, eval split disjoint, fitted-sign check). App smoke-tested headlessly with Streamlit AppTest (no exceptions; adding a reading changed risk 6% to 20%). Not tested in a real browser.

## Limitations, safety, privacy, future work
No real patients, no clinical validation, simple Gaussian level model, no treatment effects. Future: real licensed home-BP data, covariate forecasting, calibration checks, clinician feedback.

## Demo video
[VIDEO LINK PENDING: not recorded.]

## License
This project is licensed under the MIT License. See the LICENSE file for details.
