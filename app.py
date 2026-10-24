import numpy as np, pandas as pd, streamlit as st, plotly.graph_objects as go
from src.generate_data import generate
from src.twin import fit_params, Twin, valid_sbp, zvec, TARGET

st.set_page_config(page_title="HyperTwin", layout="wide")

@st.cache_data
def load():
    p, o = generate(); return p, o

@st.cache_resource
def params(_p, _o):
    n = int(.6 * len(_p)); return fit_params(_p.iloc[:n], _o)

pts, obs = load(); prm = params(pts, obs)
test_ids = list(pts.patient_id[int(.6 * len(pts)):])  # held-out patients (not used to fit)

st.title("HyperTwin: home blood-pressure digital twin")
st.warning("Research prototype on SYNTHETIC data. Not a diagnosis or treatment recommendation. "
           "Effects of sleep and steps are illustrative assumptions.")

pid = st.sidebar.selectbox("Patient (held-out synthetic)", test_ids)
ehr = pts.set_index("patient_id").loc[pid]
full = obs[obs.patient_id == pid].sort_values("timestamp").reset_index(drop=True)
day = st.sidebar.slider("Replay: twin knows data up to day", 15, len(full), 45)
target = st.sidebar.number_input("Morning SBP target (mmHg)", 110, 160, int(TARGET))

key = f"extra_{pid}_{day}"
extra = st.session_state.setdefault(key, [])
with st.sidebar.form("add"):
    st.subheader("Add a new observation")
    c_sbp = st.number_input("Morning SBP", 30, 320, 150); c_dbp = st.number_input("Morning DBP", 20, 200, 90)
    c_sl = st.number_input("Sleep last night (h)", 0.0, 14.0, 6.0, 0.5); c_st = st.number_input("Steps yesterday", 0, 40000, 4000, 500)
    if st.form_submit_button("Send to twin"):
        extra.append(dict(sbp=c_sbp, dbp=c_dbp, sleep_h=c_sl, steps=c_st))
if st.sidebar.button("Clear added observations"): extra.clear()

past = full.iloc[:day]
tw = Twin(prm, ehr); mean_hist = []
for r in past.itertuples():
    tw.update(r.sbp, r.dbp, r.sleep_h, r.steps); mean_hist.append((tw.mean, np.sqrt(tw.var)))
tw_before = Twin(prm, ehr)
for r in past.itertuples(): tw_before.update(r.sbp, r.dbp, r.sleep_h, r.steps)
z_next = zvec(float(past.sleep_h.mean()), float(past.steps.mean()))
risk_before = tw_before.risk(z_next, target)
for e in extra: tw.update(e["sbp"], e["dbp"], e["sleep_h"], e["steps"])

tab1, tab2, tab3 = st.tabs(["Twin and forecast", "What-if scenario", "Data and provenance"])
with tab1:
    c1, c2, c3 = st.columns(3)
    m, sd = tw.forecast(z_next); risk = tw.risk(z_next, target)
    c1.metric(f"P(next-morning SBP >= {target})", f"{risk:.0%}", f"{(risk - risk_before):+.0%} after added obs" if extra else None, delta_color="inverse")
    c2.metric("Forecast next-morning SBP", f"{m:.0f} mmHg", f"90% interval {m-1.645*sd:.0f} to {m+1.645*sd:.0f}", delta_color="off")
    c3.metric("Twin baseline level", f"{tw.mean:.0f} mmHg", f"EHR prior {tw.prior_mean:.0f}", delta_color="off")
    ts = past.timestamp; fig = go.Figure()
    ok = [valid_sbp(s, d) for s, d in zip(past.sbp, past.dbp)]
    fig.add_scatter(x=ts[ok], y=past.sbp[ok], mode="markers", name="Valid home SBP", marker=dict(color="#1f6f8b"))
    bad = [(not o_) and np.isfinite(s) for o_, s in zip(ok, past.sbp)]
    if any(bad): fig.add_scatter(x=ts[bad], y=np.clip(past.sbp[bad], 40, 250), mode="markers", name="Rejected (implausible)", marker=dict(color="#c0392b", symbol="x", size=10))
    mu = np.array([a for a, _ in mean_hist]); s_ = np.array([b for _, b in mean_hist])
    fig.add_scatter(x=ts, y=mu, name="Twin level", line=dict(color="#222", width=2))
    fig.add_scatter(x=list(ts) + list(ts[::-1]), y=list(mu + 1.645 * s_) + list((mu - 1.645 * s_)[::-1]), fill="toself", name="90% band", line=dict(width=0), fillcolor="rgba(34,34,34,.12)")
    nxt = ts.iloc[-1] + pd.Timedelta(days=1)
    fig.add_scatter(x=[nxt], y=[m], mode="markers", name="Forecast", marker=dict(color="#e67e22", size=12, symbol="diamond"), error_y=dict(type="data", array=[1.645 * sd]))
    fig.add_hline(y=target, line_dash="dash", line_color="#c0392b", annotation_text=f"target {target}")
    fig.update_layout(height=420, yaxis_title="Systolic BP (mmHg)", xaxis_title="Date (morning reading)", margin=dict(t=20))
    st.plotly_chart(fig, width="stretch")
    st.subheader("Why this forecast (mmHg contributions)")
    cont = tw.contributions(z_next)
    st.plotly_chart(go.Figure(go.Bar(x=list(cont.values()), y=list(cont.keys()), orientation="h", marker_color="#1f6f8b")).update_layout(height=260, margin=dict(t=10)), width="stretch")
    st.caption("Forecast assumes next-day sleep and steps equal this patient's average so far. Added observations update the twin state immediately.")
with tab2:
    st.write("Counterfactual using the model's learned sleep/steps associations. Illustrative, not a treatment effect.")
    a, b = st.columns(2)
    sl = a.slider("Planned sleep (h)", 4.0, 9.5, float(round(past.sleep_h.mean(), 1)), 0.5)
    stp = b.slider("Planned steps", 1000, 15000, int(past.steps.mean()), 500)
    m2, sd2 = tw.forecast(zvec(sl, stp)); r2 = tw.risk(zvec(sl, stp), target)
    st.table(pd.DataFrame({"Baseline (recent average)": [f"{m:.0f}", f"{risk:.0%}"], "Scenario": [f"{m2:.0f}", f"{r2:.0%}"]}, index=["Forecast SBP (mmHg)", f"P(SBP >= {target})"]))
with tab3:
    st.subheader("Historical EHR (synthetic)")
    st.dataframe(ehr.drop(["source"]).astype(str).to_frame("value"))
    st.subheader("Sensor stream quality")
    d1, d2, d3 = st.columns(3); d1.metric("Valid readings used", tw.n_obs); d2.metric("Rejected implausible", tw.rejected); d3.metric("Missing days", tw.missing)
    st.dataframe(past.drop(columns=["true_sbp_hidden", "source"]).tail(10))
    st.caption("All data synthetic (seeded generator, src/generate_data.py). Twin parameters fitted on the first 60% of patients only; patients shown here are held out.")
