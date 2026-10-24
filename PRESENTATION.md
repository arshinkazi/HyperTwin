# Slide source (12 slides). Built by `docs/deck/build.js` into `PRESENTATION.pptx` and `PRESENTATION.pdf`.
1. Title: HyperTwin, from isolated readings to a continuously updated patient state. Team placeholders.
2. Problem: one home reading is one noisy number (synthetic patient P090). Sources: ESH 2021 home BP position paper; AAFP summary of ISH guidelines.
3. Insight: historical EHR + new observations = patient state.
4. Solution: "HyperTwin is a research prototype that updates a patient-specific blood-pressure state from historical health information and home readings to forecast next-morning systolic BP risk."
5. Architecture: EHR prior, quality gate, Kalman patient state, forecast, dashboard (matches src/twin.py).
6. Clinician view: real dashboard screenshot.
7. New reading: 175/95 on P090 day 45 moves risk 6% to 53% (default 150/90 gives 6% to 20%). Illustrative, synthetic.
8. What-if: 9.5 h sleep and 10,000 steps after that reading: 135 to 131 mmHg, 53% to 21%. Illustrative, not a treatment effect.
9. Evaluation (synthetic; 4,024 predictions; 60 test / 90 training patients; one seed; no CIs): MAE 4.25 / 4.33 / 5.44, AUROC 0.937 / 0.935 / 0.904, Brier 0.075 / 0.076 / 0.099 for twin / 7-day mean / last reading. Small gain over 7-day mean, not shown significant.
10. What the prototype demonstrates (no first-of-its-kind claim).
11. Safety and limitations.
12. Conclusion, validation roadmap, team placeholders.
