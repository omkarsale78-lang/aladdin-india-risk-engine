import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests

st.set_page_config(
    page_title="AladdinIndia Risk Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, * {
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: #000000 !important;
}
.stApp, .stApp > * {
    background-color: #f2f4f7 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f2f4f7 !important;
}
p, span, div, label, input, button, td, th {
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.main .block-container { padding: 0 !important; max-width: 100% !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #dde3ea !important;
    border-top: 3px solid #e8630a !important;
    padding: 16px !important;
    border-radius: 0 !important;
}
[data-testid="metric-container"] label {
    font-size: 9px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #6b8299 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] > div {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 24px !important;
    font-weight: 300 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

h1, h2, h3 {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
    color: #000000 !important;
}
.stDataFrame { border: 1px solid #dde3ea !important; }
hr { border-color: #dde3ea !important; margin: 12px 0 !important; }

/* Download / primary buttons */
[data-testid="stDownloadButton"] button {
    background: #e8630a !important;
    color: #fff !important;
    border: none !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    border-radius: 0 !important;
    font-weight: 500 !important;
    width: 100% !important;
}

/* Sliders */
.stSlider > div > div > div { background: #e8630a !important; }

/* Expanders */
div[data-testid="stExpander"] {
    border: 1px solid #dde3ea !important;
    border-radius: 0 !important;
    background: #fff !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1px dashed #e8630a !important;
    border-radius: 4px !important;
    padding: 8px !important;
}
[data-testid="stFileUploader"] * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Hide sidebar */
section[data-testid="stSidebar"] { display: none !important; }

/* AI insight box */
.ai-insight-box {
    background: #0d1f2d;
    border-left: 3px solid #e8630a;
    padding: 16px 20px;
    margin: 8px 0;
    border-radius: 0;
}
.ai-insight-box .ai-label {
    font-size: 9px;
    letter-spacing: 2px;
    color: #e8630a !important;
    -webkit-text-fill-color: #e8630a !important;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.ai-insight-box .ai-text {
    font-size: 13px;
    color: #aec6d8 !important;
    -webkit-text-fill-color: #aec6d8 !important;
    line-height: 1.6;
}
.ai-insight-box .ai-footer {
    margin-top: 10px;
    font-size: 11px;
    color: #4a6580 !important;
    -webkit-text-fill-color: #4a6580 !important;
}
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#0d1f2d;padding:0 24px;height:56px;display:flex;
align-items:center;justify-content:space-between;border-bottom:2px solid #e8630a;'>
  <div style='display:flex;align-items:center;gap:14px;'>
    <div style='background:#e8630a;width:32px;height:32px;display:flex;
    align-items:center;justify-content:center;font-weight:600;font-size:13px;color:#fff;'>AI</div>
    <div>
      <div style='font-size:16px;font-weight:600;color:#fff;'>
        Aladdin<span style='color:#e8630a;'>India</span>
      </div>
      <div style='font-size:9px;color:#4a6580;letter-spacing:2px;'>RISK INTELLIGENCE PLATFORM</div>
    </div>
  </div>
  <div style='display:flex;gap:10px;align-items:center;'>
    <div style='display:flex;gap:20px;margin-right:20px;'>
      <span style='font-size:11px;color:#fff;border-bottom:2px solid #e8630a;padding-bottom:2px;'>Overview</span>
      <span style='font-size:11px;color:#4a6580;'>Portfolio</span>
      <span style='font-size:11px;color:#4a6580;'>Stress Testing</span>
      <span style='font-size:11px;color:#4a6580;'>Compliance</span>
    </div>
    <span style='background:#1e3a52;color:#4a6580;font-size:9px;padding:4px 10px;
    letter-spacing:1px;border:1px solid #1e3a52;'>SAMPLE DATA</span>
    <span style='background:#0f2637;color:#4a6580;font-size:9px;padding:4px 10px;
    letter-spacing:1px;border:1px solid #1e3a52;'>NSE · BSE</span>
  </div>
</div>
<div style='background:#0f2637;padding:0 24px;height:36px;display:flex;
align-items:center;justify-content:space-between;border-bottom:1px solid #1e3a52;margin-bottom:20px;'>
  <div style='font-size:10px;color:#4a6580;'>
    Portfolio Overview / <span style='color:#aec6d8;'>Risk Dashboard</span>
  </div>
  <div style='display:flex;gap:20px;'>
    <span style='font-size:10px;font-family:IBM Plex Mono,monospace;'>
      <span style='color:#4a6580;'>NIFTY </span>
      <span style='color:#2ecc71;'>22,847 ▲1.2%</span>
    </span>
    <span style='font-size:10px;font-family:IBM Plex Mono,monospace;'>
      <span style='color:#4a6580;'>VIX </span>
      <span style='color:#e74c3c;'>13.4 ▼0.5</span>
    </span>
    <span style='font-size:10px;font-family:IBM Plex Mono,monospace;'>
      <span style='color:#4a6580;'>INR/USD </span>
      <span style='color:#aec6d8;'>83.42</span>
    </span>
    <span style='font-size:9px;color:#2a4055;'>(indicative — connect live feed for production)</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CONSTANTS ────────────────────────────────────────────────────────────────
RISK_FREE_RATE = 0.045   # 4.5% RBI effective rate
N_SIMULATIONS  = 2000    # raise to 10000 for production
ANNUAL_DRIFT   = 0.12    # 12% expected annual return for Nifty large-cap basket

PORTFOLIO = {
    "RELIANCE": 0.20, "TCS":      0.18, "HDFCBANK": 0.16,
    "INFY":     0.14, "WIPRO":    0.12, "ICICIBANK": 0.11,
    "OTHERS":   0.09
}
STOCK_VOLS = [0.24, 0.19, 0.21, 0.22, 0.25, 0.28, 0.30]
SECTORS = {
    "RELIANCE": "Energy",  "TCS":      "IT",      "HDFCBANK":  "Banking",
    "INFY":     "IT",      "WIPRO":    "IT",       "ICICIBANK": "Banking",
    "OTHERS":   "Mixed"
}
ADTV = {
    "RELIANCE": 1200, "TCS": 800, "HDFCBANK": 1500,
    "INFY": 600, "WIPRO": 300, "ICICIBANK": 900, "OTHERS": 200
}
VALID_SYMBOLS = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "WIPRO", "ICICIBANK",
    "HDFC", "BAJFINANCE", "AXISBANK", "MARUTI", "TATAMOTORS",
    "LT", "SUNPHARMA", "TITAN", "ADANIENT", "OTHERS"
]

# ── CSV VALIDATION ────────────────────────────────────────────────────────────
def validate_portfolio(df):
    errors, warnings = [], []
    for col in ["Stock", "Weight"]:
        if col not in df.columns:
            errors.append(f"Missing column '{col}' — CSV must have Stock and Weight columns.")
    if errors:
        return errors, warnings
    try:
        df["Weight"] = pd.to_numeric(df["Weight"], errors="raise")
    except Exception:
        errors.append("Weight column must be numeric (e.g. 0.20 or 20 for 20%).")
        return errors, warnings
    if df["Weight"].max() > 1.5:
        df["Weight"] = df["Weight"] / 100
    total = df["Weight"].sum()
    if total < 0.95:
        errors.append(f"Weights sum to {total*100:.1f}% — must be >= 95%.")
    elif total > 1.05:
        errors.append(f"Weights sum to {total*100:.1f}% — must be <= 105%.")
    if len(df) < 2:
        errors.append("Portfolio needs at least 2 stocks.")
    if len(df) > 20:
        warnings.append("More than 20 stocks — simulation may be slow.")
    unknown = [s for s in df["Stock"].str.upper() if s not in VALID_SYMBOLS]
    if unknown:
        warnings.append(f"Unrecognised symbols (fallback vol 25%): {', '.join(unknown)}")
    if (df["Weight"] < 0).any():
        errors.append("Negative weights found — all weights must be positive.")
    breaching = df[df["Weight"] > 0.10]["Stock"].tolist()
    if breaching:
        warnings.append(f"SEBI single-stock >10% limit: {', '.join(breaching)}")
    return errors, warnings


def load_portfolio_from_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [c.strip().title() for c in df.columns]
        df["Stock"] = df["Stock"].str.strip().str.upper()
        errors, warnings = validate_portfolio(df)
        if errors:
            for e in errors:
                st.error(f"Error: {e}")
            return None, None
        for w in warnings:
            st.warning(f"Warning: {w}")
        df["Weight"] = df["Weight"] / df["Weight"].sum()
        portfolio = dict(zip(df["Stock"], df["Weight"].round(4)))
        vol_map = dict(zip(list(PORTFOLIO.keys()), STOCK_VOLS))
        vols = [vol_map.get(s, 0.25) for s in portfolio]
        return portfolio, vols
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        return None, None


# ── MONTE CARLO ───────────────────────────────────────────────────────────────
@st.cache_data
def generate_returns(wt, vt):
    np.random.seed(42)
    w  = np.array(wt)
    vd = np.array(vt) / np.sqrt(252)
    n  = len(w)
    corr = np.full((n, n), 0.45)
    np.fill_diagonal(corr, 1.0)
    cov = np.outer(vd, vd) * corr
    eigvals = np.linalg.eigvalsh(cov)
    if eigvals.min() < 1e-10:
        cov += np.eye(n) * 1e-8
    L  = np.linalg.cholesky(cov)
    z  = np.random.standard_normal((N_SIMULATIONS, n))
    cr = z @ L.T + (ANNUAL_DRIFT / 252)   # add daily drift
    return cr @ w, cr


# ── ACTIVE PORTFOLIO (session or default) ─────────────────────────────────────
if "portfolio" in st.session_state and "vols" in st.session_state:
    active_portfolio = st.session_state["portfolio"]
    active_vols      = st.session_state["vols"]
else:
    active_portfolio = PORTFOLIO
    active_vols      = STOCK_VOLS

weights_arr = np.array(list(active_portfolio.values()))
vols_arr    = np.array(active_vols)
returns, stock_returns = generate_returns(tuple(weights_arr), tuple(vols_arr))

var_95 = np.percentile(returns, 5)
var_99 = np.percentile(returns, 1)
vol    = returns.std() * np.sqrt(252)
sharpe = (returns.mean() * 252 - RISK_FREE_RATE) / vol

mkt  = stock_returns.mean(axis=1)
beta = np.cov(returns, mkt)[0, 1] / np.var(mkt)

cov_m = np.outer(vols_arr, vols_arr) * 0.45
np.fill_diagonal(cov_m, vols_arr ** 2)
pv   = np.sqrt(weights_arr @ cov_m @ weights_arr)
mctr = weights_arr * (cov_m @ weights_arr) / pv * 100

sw = {}
for s, wt in active_portfolio.items():
    sw[SECTORS.get(s, "Mixed")] = sw.get(SECTORS.get(s, "Mixed"), 0) + wt

# ── AI ENGINE ─────────────────────────────────────────────────────────────────
def build_risk_prompt(portfolio, sectors, vols, metrics, sector_weights):
    lines = []
    for i, (s, w) in enumerate(portfolio.items()):
        lines.append(f"  {s} ({sectors.get(s,'Mixed')}): {w*100:.0f}% weight, {vols[i]*100:.0f}% vol")
    sector_str = ", ".join(f"{sec} {wt*100:.0f}%" for sec, wt in sector_weights.items())
    return f"""You are a mathematical risk analytics tool for a SEBI-registered PMS firm.
Analyse this portfolio and produce a 3-point risk briefing.
Output raw analytical observations only — do NOT make buy/sell/trim recommendations.
Summarise mathematical risk concentrations, sector exposures, and tail risk only.

PORTFOLIO:
{chr(10).join(lines)}

COMPUTED RISK METRICS:
- 95% VaR (daily): {metrics['var_95']*100:.2f}%
- 99% VaR (daily): {metrics['var_99']*100:.2f}%
- Annual Volatility: {metrics['vol']*100:.1f}%
- Sharpe Ratio: {metrics['sharpe']:.2f}
- Portfolio Beta: {metrics['beta']:.2f}
- Sector weights: {sector_str}

FORMAT:
RISK 1: [concentration or tail risk observation with numbers]
RISK 2: [sector or beta exposure observation]
RISK 3: [volatility or correlation observation]

Under 80 words total. No preamble, no advice, no sign-off."""


def call_claude(prompt, api_key):
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model":      "claude-haiku-4-5-20251001",
                "max_tokens": 200,
                "messages":   [{"role": "user", "content": prompt}],
            },
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"].strip()
    except requests.exceptions.Timeout:
        return "Request timed out — try again."
    except requests.exceptions.HTTPError:
        if resp.status_code == 401:
            return "Invalid API key — check your Anthropic key."
        if resp.status_code == 429:
            return "Rate limited — wait a moment and retry."
        return f"API error {resp.status_code}"
    except Exception as e:
        return f"Unexpected error: {e}"


# ── TOP METRICS ───────────────────────────────────────────────────────────────
st.markdown("<div style='padding:0 24px;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:9px;letter-spacing:2.5px;color:#6b8299;"
    "text-transform:uppercase;margin:0 0 10px 0;'>Risk Metrics — Nifty 50 Basket</p>",
    unsafe_allow_html=True
)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("95% VaR Daily",
          f"{var_95 * 100:.2f}%",
          "Worst-case daily loss (95% confidence)",
          delta_color="off")
c2.metric("99% VaR Daily",
          f"{var_99 * 100:.2f}%",
          "Worst-case daily loss (99% confidence)",
          delta_color="off")
c3.metric("Annual Volatility",
          f"{vol * 100:.1f}%",
          "vs Nifty benchmark 14.2%",
          delta_color="off")
c4.metric("Sharpe Ratio",     f"{sharpe:.2f}",  "Benchmark: 0.98")
c5.metric("Portfolio Beta",   f"{beta:.2f}",    "vs Nifty 50")

st.markdown("<br>", unsafe_allow_html=True)

# ── CSV UPLOAD ────────────────────────────────────────────────────────────────
st.markdown(
    "<p style='font-size:9px;letter-spacing:2.5px;color:#6b8299;"
    "text-transform:uppercase;margin:0 0 10px 0;'>Upload Portfolio (CSV)</p>",
    unsafe_allow_html=True
)
with st.expander("Upload your own holdings CSV", expanded=False):
    st.markdown(
        "<div style='background:#fff8f0;border-left:3px solid #e8630a;"
        "padding:10px 14px;font-size:11px;color:#4a6580;margin-bottom:12px;'>"
        "Your portfolio data is processed in-memory only and never stored, "
        "logged, or used for model training."
        "</div>",
        unsafe_allow_html=True
    )
    st.caption("Two columns required: Stock (NSE symbol) and Weight (decimal 0.20 or percent 20)")
    sample_csv = "Stock,Weight\nRELIANCE,20\nTCS,18\nHDFCBANK,16\nINFY,14\nWIPRO,12\nICICIBANK,11\nOTHERS,9"
    st.download_button("Download sample CSV", sample_csv, "sample_portfolio.csv", "text/csv")
    uploaded = st.file_uploader("Upload holdings CSV", type=["csv"], label_visibility="collapsed")
    if uploaded:
        parsed_portfolio, parsed_vols = load_portfolio_from_csv(uploaded)
        if parsed_portfolio:
            st.success(f"Loaded {len(parsed_portfolio)} stocks — all metrics updated.")
            st.session_state["portfolio"] = parsed_portfolio
            st.session_state["vols"]      = parsed_vols
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── AI RISK BRIEFING ──────────────────────────────────────────────────────────
st.markdown(
    "<p style='font-size:9px;letter-spacing:2.5px;color:#6b8299;"
    "text-transform:uppercase;margin:0 0 10px 0;'>AI Risk Briefing</p>",
    unsafe_allow_html=True
)
with st.expander("Generate Client-Ready SEBI Compliance Briefing", expanded=True):
    api_col, btn_col = st.columns([3, 1])
    with api_col:
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            help="Never stored — used only for this session."
        )
    with btn_col:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("Analyse Portfolio", use_container_width=True)

    if generate_btn:
        if not api_key or not api_key.startswith("sk-ant-"):
            st.error("Enter a valid Anthropic API key (starts with sk-ant-).")
        else:
            with st.spinner("Running analysis..."):
                metrics_dict = {
                    "var_95": var_95, "var_99": var_99,
                    "vol":    vol,    "sharpe": sharpe, "beta": beta
                }
                prompt  = build_risk_prompt(active_portfolio, SECTORS, active_vols, metrics_dict, sw)
                insight = call_claude(prompt, api_key)
            st.markdown(f"""
<div class='ai-insight-box'>
  <div class='ai-label'>Risk Briefing · {pd.Timestamp.now().strftime('%d %b %Y %H:%M')} · For informational purposes only</div>
  <div class='ai-text'>{insight}</div>
  <div class='ai-footer'>Mathematical analysis only — not investment advice · Claude Haiku · Monte Carlo N={N_SIMULATIONS}</div>
</div>""", unsafe_allow_html=True)
    else:
        st.caption(
            "Generates a mathematical risk concentration summary based on computed metrics. "
            "Not investment advice."
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── STRESS TEST ───────────────────────────────────────────────────────────────
st.markdown(
    "<p style='font-size:9px;letter-spacing:2.5px;color:#6b8299;"
    "text-transform:uppercase;margin:0 0 10px 0;'>Stress Test Simulator</p>",
    unsafe_allow_html=True
)
col_sl, col_sc = st.columns([1, 2])

with col_sl:
    crash  = st.slider("Nifty Crash (%)",    5,   50,  30)
    beta_s = st.slider("Portfolio Beta",      0.5, 1.5, round(float(beta), 2))
    corr_s = st.slider("Market Correlation",  0.3, 0.95, 0.65)
    loss   = crash * beta_s * corr_s
    st.metric("Estimated Portfolio Loss", f"-{loss:.1f}%", delta_color="off")
    st.caption("Loss = Nifty Crash × Beta × Correlation. Recovery time is scenario-dependent.")

with col_sc:
    it_w = sum(wt for s, wt in active_portfolio.items() if SECTORS.get(s, "Mixed") == "IT")
    bk_w = sum(wt for s, wt in active_portfolio.items() if SECTORS.get(s, "Mixed") == "Banking")
    scenarios = {
        "Nifty crash -30%":    -crash * beta_s * corr_s,
        "IT selloff -20%":     -(20 * it_w * 1.15 * 0.85),
        "Banking crisis -25%": -(25 * bk_w * 1.05 * 0.90),
        "RBI +200bps":         -(crash * 0.4 * corr_s),
        "Bull rally +20%":     +(20 * beta_s * corr_s * 0.9),
        "COVID crash -34%":    -(34 * beta_s * corr_s),
    }
    fig_s = go.Figure(go.Bar(
        x=list(scenarios.values()),
        y=list(scenarios.keys()),
        orientation='h',
        marker_color=['#c0392b' if v < 0 else '#1a7a4a' for v in scenarios.values()],
        marker_line_width=0,
        text=[f"{v:.1f}%" for v in scenarios.values()],
        textposition='outside',
        textfont=dict(size=10, color='#6b8299', family='IBM Plex Mono')
    ))
    fig_s.update_layout(
        height=220, margin=dict(l=0, r=60, t=8, b=0),
        paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
        font=dict(color='#6b8299', size=10, family='IBM Plex Mono'),
        xaxis=dict(gridcolor='#f0f2f5', zeroline=True,
                   zerolinecolor='#dde3ea', title="Portfolio Impact (%)"),
        yaxis=dict(gridcolor='#f0f2f5'),
    )
    st.plotly_chart(fig_s, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── HOLDINGS + DISTRIBUTION ───────────────────────────────────────────────────
st.markdown(
    "<p style='font-size:9px;letter-spacing:2.5px;color:#6b8299;"
    "text-transform:uppercase;margin:0 0 10px 0;'>Holdings & Analytics</p>",
    unsafe_allow_html=True
)
col_h, col_v = st.columns(2)

with col_h:
    hdf = pd.DataFrame({
        "Stock":  list(active_portfolio.keys()),
        "Sector": [SECTORS.get(s, "Mixed") for s in active_portfolio],
        "Weight": [f"{v * 100:.0f}%" for v in active_portfolio.values()],
        "Vol":    [f"{v * 100:.0f}%" for v in active_vols],
        "MCTR":   [f"{rc:.2f}%" for rc in mctr],
    })
    st.dataframe(hdf, hide_index=True, use_container_width=True, height=250)
    st.caption("MCTR = Marginal Contribution to Risk (w_i x (Sw)_i / o_p)")

with col_v:
    fig_v = go.Figure()
    fig_v.add_trace(go.Histogram(
        x=returns * 100, nbinsx=50,
        marker_color='#1a4a7a', opacity=0.6
    ))
    fig_v.add_vline(x=var_95 * 100, line_dash="dash", line_color="#e8630a",
                    line_width=1.5, annotation_text="95% VaR",
                    annotation_font_color="#e8630a", annotation_font_size=10)
    fig_v.add_vline(x=var_99 * 100, line_dash="dot",  line_color="#c0392b",
                    line_width=1.5, annotation_text="99% VaR",
                    annotation_font_color="#c0392b", annotation_font_size=10)
    fig_v.update_layout(
        height=250, margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
        font=dict(color='#6b8299', size=10, family='IBM Plex Mono'),
        xaxis=dict(gridcolor='#f0f2f5', title="Daily Return (%)"),
        yaxis=dict(gridcolor='#f0f2f5', title="Frequency"),
        showlegend=False,
    )
    st.plotly_chart(fig_v, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── SECTOR · COMPLIANCE · LIQUIDITY ──────────────────────────────────────────
st.markdown(
    "<p style='font-size:9px;letter-spacing:2.5px;color:#6b8299;"
    "text-transform:uppercase;margin:0 0 10px 0;'>Sector · Compliance · Liquidity</p>",
    unsafe_allow_html=True
)
col_sec, col_sebi, col_liq = st.columns(3)

with col_sec:
    prudence = st.slider("Sector Prudence Limit (%)", 25, 50, 35)
    for sec, wt in sorted(sw.items(), key=lambda x: -x[1]):
        pct   = wt * 100
        over  = pct > prudence
        color = "#c0392b" if over else "#1a4a7a"
        warn  = " !" if over else ""
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;font-size:11px;"
            f"margin-bottom:3px;color:#4a6580;'>"
            f"<span>{sec}{warn}</span>"
            f"<span style='font-family:IBM Plex Mono,monospace;color:{color};'>{pct:.0f}%</span>"
            f"</div>"
            f"<div style='background:#f0f2f5;height:4px;margin-bottom:8px;'>"
            f"<div style='width:{min(pct,100):.0f}%;height:4px;background:{color};'></div>"
            f"</div>",
            unsafe_allow_html=True
        )
    if any(wt * 100 > prudence for wt in sw.values()):
        st.warning(f"Sector exceeds {prudence}% prudence limit")
    else:
        st.success("All sectors within limits")

with col_sebi:
    breaching       = [s for s, v in active_portfolio.items() if v > 0.10]
    single_stock_ok = len(breaching) == 0
    sector_ok       = not any(wt * 100 > prudence for wt in sw.values())
    breach_note     = f" ({', '.join(breaching)} breach)" if breaching else ""
    checks = [
        (f"Single stock < 10% AUM{breach_note}", single_stock_ok, "computed"),
        ("Sector < prudence limit",               sector_ok,       "computed"),
        ("Derivatives exposure",                  None,            "manual"),
        ("Unlisted < 10%",                        None,            "manual"),
        ("Monthly disclosure filed",              None,            "manual"),
        ("KYC — all clients",                     None,            "manual"),
    ]
    for name, ok, source in checks:
        if source == "manual":
            color, bg, status = "#6b8299", "#f5f6f8", "MANUAL"
        elif ok:
            color, bg, status = "#1a7a4a", "#e8f5ee", "PASS"
        else:
            color, bg, status = "#c47d0a", "#fff8e8", "REVIEW"
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;align-items:center;"
            f"padding:8px 0;border-bottom:1px solid #f5f6f8;font-size:11px;'>"
            f"<span style='color:#4a6580;'>{name}</span>"
            f"<span style='background:{bg};color:{color};font-size:9px;"
            f"padding:3px 8px;letter-spacing:0.5px;font-weight:500;'>{status}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    st.caption("MANUAL = requires external data. Connect SEBI portal for production.")

with col_liq:
    aum = st.number_input("Portfolio AUM (Rs Crore)", 1, 10000, 100)
    ldf = pd.DataFrame([{
        "Stock":        s,
        "Position RsCr": round(aum * wt, 1),
        "Days to Exit": round((aum * wt) / ADTV.get(s, 200), 2)
    } for s, wt in active_portfolio.items()])
    st.dataframe(ldf, hide_index=True, use_container_width=True, height=220)
    il = ldf[ldf["Days to Exit"] > 1]
    if not il.empty:
        st.warning(f"{len(il)} positions need more than 1 day to exit")
    else:
        st.success("All positions liquid in 1 day")

st.markdown("<br>", unsafe_allow_html=True)

# ── WHAT-IF OPTIMIZER ─────────────────────────────────────────────────────────
it_w_pct = sw.get("IT", 0) * 100

with st.expander("What-If Optimizer — Reduce IT Concentration"):
    shift_pct = st.slider(
        "Shift from IT to Others (%)", 0, max(int(it_w_pct - 5), 1), 5,
        help="Moves weight from IT stocks to OTHERS and recomputes risk analytically."
    )
    new_weights = weights_arr.copy()
    it_indices  = [i for i, s in enumerate(active_portfolio) if SECTORS.get(s, "Mixed") == "IT"]
    oth_keys    = list(active_portfolio.keys())
    oth_index   = oth_keys.index("OTHERS") if "OTHERS" in oth_keys else len(oth_keys) - 1
    shift_each  = (shift_pct / 100) / max(len(it_indices), 1)
    for idx in it_indices:
        new_weights[idx] = max(new_weights[idx] - shift_each, 0)
    new_weights[oth_index] += shift_pct / 100
    new_weights /= new_weights.sum()

    new_pv    = np.sqrt(new_weights @ cov_m @ new_weights)
    new_vol   = new_pv * np.sqrt(252)
    new_var95 = var_95 * (new_vol / vol)

    o1, o2 = st.columns(2)
    with o1:
        st.markdown("**Current Portfolio**")
        st.metric("IT Concentration", f"{it_w_pct:.0f}%")
        st.metric("Annual Vol",        f"{vol * 100:.1f}%")
        st.metric("95% VaR",           f"{var_95 * 100:.2f}%")
    with o2:
        st.markdown("**Rebalanced Portfolio**")
        delta_vol = (new_vol - vol) * 100
        delta_var = (new_var95 - var_95) * 100
        st.metric("IT Concentration", f"{it_w_pct - shift_pct:.0f}%",
                  f"-{shift_pct:.0f}%", delta_color="inverse")
        st.metric("Annual Vol",       f"{new_vol * 100:.1f}%",
                  f"{delta_vol:.2f}%", delta_color="inverse")
        st.metric("95% VaR",          f"{new_var95 * 100:.2f}%",
                  f"{delta_var:.2f}%", delta_color="inverse")
    if shift_pct > 0:
        st.info(
            f"Shifting {shift_pct:.0f}% from IT reduces annual vol by "
            f"{abs(delta_vol):.2f}% and VaR by {abs(delta_var):.2f}%."
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── EXPORT ────────────────────────────────────────────────────────────────────
report_df = pd.DataFrame({
    "Metric": ["95% VaR (Daily)", "99% VaR (Daily)", "Annual Volatility",
               "Sharpe Ratio", "Portfolio Beta", "IT Weight",
               "Risk-Free Rate", "Simulations", "Annual Drift Assumption"],
    "Value":  [f"{var_95 * 100:.2f}%", f"{var_99 * 100:.2f}%",
               f"{vol * 100:.1f}%",    f"{sharpe:.2f}",
               f"{beta:.2f}",          f"{it_w_pct:.0f}%",
               f"{RISK_FREE_RATE*100:.1f}%", str(N_SIMULATIONS),
               f"{ANNUAL_DRIFT*100:.0f}%"],
})
st.download_button(
    "EXPORT RISK REPORT (CSV)",
    report_df.to_csv(index=False),
    "aladdin_india_risk_report.csv",
    "text/csv",
    use_container_width=True
)

st.markdown(f"""
<div style='background:#0d1f2d;padding:10px 24px;display:flex;
justify-content:space-between;font-size:9px;color:#2a4055;
letter-spacing:1px;margin-top:20px;border-top:1px solid #1e3a52;'>
    <span>ALADDIN INDIA · RISK ENGINE v0.5</span>
    <span>NSE · SEBI PMS · MONTE CARLO N={N_SIMULATIONS} · Mathematical analysis only</span>
    <span>2026 ALADDIN INDIA TECHNOLOGIES</span>
</div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
