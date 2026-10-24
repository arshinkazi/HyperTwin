# ARCHITECTURE
EHR (patients.csv) -> EHR prior (OLS) ---\
                                          +--> Kalman twin state (level, variance) -> forecast + risk -> Streamlit dashboard
Sensor stream (observations.csv) -> validity gate (range, DBP<SBP, missing) --/            ^
                                                                                  what-if sliders / new observation form
Diagram: `docs/architecture.pdf` (regenerate with `python docs/make_diagram.py`).
