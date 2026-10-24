# RESEARCH (time-boxed, accessed 24 Oct 2026)

**Scope and honesty note.** Research was limited to a few web searches. Guideline sources for the BP threshold were added in a second pass; the wider clinical literature was not reviewed, and the official Unstop listing was NOT opened directly. Everything below is either a quoted/paraphrased fact from a page I retrieved, or labelled as a hypothesis.

## What the landscape looks like (evidence retrieved)
Public GitHub repos for this same challenge, found via search:
| Repo | Focus (per its README) |
|---|---|
| Paras-so/Digital-Twin-Challenge-2026 | Type 2 diabetes, 120-min glucose forecast |
| parthpariwandh/Parth_Pariwandh_Jadavpur_University (GlycoTwin-IN) | T2D, 2-h post-meal hyperglycaemia, Bergman model |
| Thanatos9404/pratibimb | T2D, physiology + ML, EnKF |
| shashi-bhushan-27/digitalTwinChallenge | T2D, 2-h spike prediction |
| Jidnyasa-P/GlucoTwin | glucose twin |
| MananGilhotra/TwinPulse... (NightTwin) | night-time hypoglycaemia, type 1, children |
| aniketh-234/CardioTwin | cardiovascular |
| Kabirroy12345/Digital_Twin (PulmoTwin) | cardiopulmonary |
| Yashraja-cyber/dr-digital-twin | diabetic retinopathy |
| ShrushtiKakade/Digital_Twin | includes a hypertension-surge scenario among others |

**Observation (supported):** glucose/T2D is by far the most crowded choice among public submissions I found. Hypertension as the single, primary condition appeared less often in this sample (sample is small and search-biased).

## Organizer/academic framing (retrieved)
- IEEE ICHI 2026 Health Digital Twin workshop CFP: https://easychair.org/cfp/HDT-2026 emphasises data interoperability, model validity, explainability, and reproducibility/synthetic data practices.
- Aalborg Univ. Health Mission challenge page lists privacy and transparency as foundational for digital health twins: https://www.healthmission.aau.dk/challenges/digital-health-twins

These support (not prove) the design choices: explanations, validation against baselines, synthetic data disclosure.

## Datasets
No external dataset used. Data is generated (`src/generate_data.py`, seeded). A real-data version would need e.g. a licensed home-BP / wearable cohort; none verified here.

## Approaches compared (design-level, not literature-backed benchmarks)
1. Pure ML (gradient boosting on lagged features): flexible, weak on short per-patient series, opaque.
2. Mechanistic physiology (e.g. baroreflex/Windkessel): principled, but parameters need clinical data we lack.
3. **Chosen: EHR-informed state-space (Kalman) twin**: small, interpretable, updates online per patient, handles missing data natively.

## Gap addressed (hypothesis, not proven by sources)
Home BP readings are sparse and noisy; a per-patient state that starts from EHR priors, updates with each reading, rejects implausible values and explains forecasts is a feasible small twin. Claims that clinicians complain about false alarms or poor explanations for BP tools are NOT evidenced here.

## Authoritative sources for home BP and the 135 mmHg threshold (accessed 24 Oct 2026)
1. ESH Working Group, *Home blood pressure monitoring: methodology, clinical relevance and practical application* (2021 position paper). https://pmc.ncbi.nlm.nih.gov/articles/PMC9904446 : states 135/85 mmHg home BP as the ESC/ESH hypertension diagnostic threshold (corresponding to clinic 140/90), and that 130/80 may correspond to the ACC/AHA grade I threshold.
2. Unger et al. ISH guidelines summary, *American Family Physician* 2021. https://www.aafp.org/pubs/afp/issues/2021/0615/p763.html : home threshold 135/85 mmHg, hypertension diagnosed when home readings are consistently at or above it.
3. Brazilian hypertension guideline discussion (SciELO, *Arq Bras Cardiol*), https://www.scielo.br/j/abc/a/MSjFGpBGzQThLvFHdtfMrpy/?lang=en : the 2020 Brazilian guideline uses 130/80 mmHg for home BP, showing thresholds differ by guideline.
4. Overview of the 2023 ESH guidelines (secondary review), https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11263159/ : emphasises out-of-office (home, ambulatory) BP.

**Implication for this project:** 135 mmHg is a recognised home-BP threshold, but it is defined for averages over several days, not a single morning. Our target ("next morning SBP at or above 135") is therefore an engineering proxy for an adverse excursion, not a diagnostic criterion, and 130 is a defensible alternative (the dashboard lets you change the target). I cite these only for the threshold and for home BP monitoring being guideline-endorsed; I do not cite them for any claim about the model's accuracy.

## Evidence status of results
All model results are from synthetic data generated with assumed sleep/steps effects. They show the pipeline behaves correctly on its own generator. They are not clinical validation, and nothing here shows benefit for patients.

## Still to verify manually
- Official Unstop listing text, deadline (one peer README says 20 Oct 2026; you stated 24 Oct 7 PM IST) and video length (peer READMEs report both a 15-20 min form field and a minimum 20 min challenge text).
