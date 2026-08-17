import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# 1. Configuration & Dark Theme Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gaming Analytics: D1 Retention Incident",
    page_icon="🎮",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Metrics Styling */
    .metric-card {
        background-color: #1E222D;
        padding: 18px;
        border-radius: 8px;
        border-left: 4px solid #74B9FF;
        margin-bottom: 15px;
    }
    .metric-title { font-size: 0.85rem; color: #D0D0D0; margin-bottom: 5px; }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #FFFFFF; }
    
    /* Insight Box Styling */
    .insight-box {
        background-color: #1E222D;
        border-left: 4px solid #FDCB6E;
        padding: 18px;
        border-radius: 6px;
        margin-bottom: 25px;
        color: #F0F0F0;
    }
    
    /* Centered Section Headers */
    .section-header {
        color: #74B9FF;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        background-color: #161B22;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #2D3748;
        margin-top: 40px;
        margin-bottom: 25px;
    }
    
    /* Slider Text Brightness Fix */
    div[data-baseweb="slider"] { color: #FFFFFF !important; }
    .stMarkdown, p, span, label { color: #E0E0E0 !important; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Generation Function
# -----------------------------------------------------------------------------
@st.cache_data
def generate_data():
    np.random.seed(42)
    num_users = 7000
    start_date = datetime(2026, 5, 1)

    user_ids = [f"usr_{i:04d}" for i in range(1, num_users + 1)]
    install_dates = [start_date + timedelta(days=int(np.random.randint(0, 31))) for _ in range(num_users)]
    countries = np.random.choice(["US", "UK", "DE", "CA"], size=num_users, p=[0.5, 0.2, 0.15, 0.15])

    df_users = pd.DataFrame({"user_id": user_ids, "install_date": install_dates, "country": countries})

    base_econ = {
        "Quick Clash": {"fee": 15, "win": 0.52}, "Neon Blitz": {"fee": 25, "win": 0.48},
        "Starlight Cup": {"fee": 30, "win": 0.45}, "Shadow Dash": {"fee": 45, "win": 0.50},
        "Solar Strike": {"fee": 50, "win": 0.42}, "Crystal Clash": {"fee": 65, "win": 0.46},
        "Titan Arena": {"fee": 75, "win": 0.40}, "Cyber Duel": {"fee": 85, "win": 0.44},
        "Vortex Rush": {"fee": 90, "win": 0.41}
    }

    matches = []
    prob_start = datetime(2026, 5, 21)
    fix_date = datetime(2026, 5, 25)

    for idx, row in df_users.iterrows():
        u_id, inst_date = row["user_id"], row["install_date"]
        is_problem = prob_start <= inst_date < fix_date
        num_sessions = np.random.randint(1, 15)

        for sess in range(1, num_sessions + 1):
            match_time = inst_date + timedelta(days=sess-1, hours=int(np.random.randint(1, 12)))
            xp_lvl = min(15, sess)

            if is_problem and sess <= 5 and np.random.rand() < 0.12:
                t_type, fee, win_r = "Dragon's Hoard", 250, 0.32
            else:
                t_type = np.random.choice(list(base_econ.keys()))
                fee = base_econ[t_type]["fee"] + np.random.randint(-2, 3)
                win_r = base_econ[t_type]["win"]

            is_win = 1 if np.random.rand() < win_r else 0

            matches.append({
                "match_id": f"m_{u_id}_{sess}", "user_id": u_id, "install_date": inst_date,
                "country": row["country"], "session_number": sess, "tournament_type": t_type,
                "xp_level": xp_lvl, "is_win": is_win, "entry_fee": fee
            })

    return df_users, pd.DataFrame(matches)

df_users, df_matches = generate_data()

# -----------------------------------------------------------------------------
# 3. Sidebar Filters
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/controller.png", width=50)
st.sidebar.title("Dashboard Filters")

country_filter = st.sidebar.multiselect(
    "Filter Country", options=df_users["country"].unique(), default=df_users["country"].unique()
)

filtered_matches = df_matches[df_matches["country"].isin(country_filter)]

# -----------------------------------------------------------------------------
# 4. Header & Executive Summary
# -----------------------------------------------------------------------------
st.title("🎮 Product Analytics: D1 Retention Incident & Root Cause Analysis")
st.markdown("Investigation of **May 21st D1 Retention Drop**, Post-Fix Validation & XP Level Balancing.")

st.markdown("""
<div class="insight-box">
    <b style="color: #FDCB6E; font-size: 1.1rem;">🔍 Executive Incident Summary:</b><br>
    <span style="color: #E0E0E0;">
    • <b>Incident Period:</b> On May 21st, D1 Retention dropped by <b>~5%</b> (from 58.2% to 53.2%).<br>
    • <b>Root Cause:</b> Early exposure to the high-stakes <i>Dragon's Hoard</i> tournament (250 coins entry fee, 32% win rate) depleted coin balances for early-stage players.<br>
    • <b>Action & Recovery:</b> On May 25th, early access was rebalanced. D1 Retention immediately recovered to baseline (58.5%).
    </span>
</div>
""", unsafe_allow_html=True)

# Metrics Row
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">TOTAL USERS ANALYZED</div><div class="metric-value">{filtered_matches["user_id"].nunique():,}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><div class="metric-title">INCIDENT D1 RETENTION</div><div class="metric-value" style="color: #FF7675;">53.2%</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><div class="metric-title">POST-FIX D1 RETENTION</div><div class="metric-value" style="color: #55E6C1;">58.5%</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-card"><div class="metric-title">DRAGON\'S HOARD ENTRY FEE</div><div class="metric-value">250 Coins</div></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PART 1: INCIDENT INVESTIGATION (MAY 1 – MAY 24)
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>PART 1: Incident Investigation (May 1–24)</div>", unsafe_allow_html=True)

matches_inv = filtered_matches[filtered_matches["install_date"] <= datetime(2026, 5, 24)]

# Graph 1: Investigation Retention Trend
st.subheader("1. Daily D1 Retention Trend (Ongoing Drop Detected May 21)")
daily_ret_inv = matches_inv.groupby("install_date").agg(total_users=("user_id", "nunique")).reset_index()

def calc_d1_inv(dt):
    if dt >= datetime(2026, 5, 21):
        return np.random.uniform(52.2, 53.8)
    else:
        return np.random.uniform(57.1, 58.9)

daily_ret_inv["d1_retention"] = daily_ret_inv["install_date"].apply(calc_d1_inv)
daily_ret_inv["label"] = daily_ret_inv["d1_retention"].apply(lambda x: f"{x:.1f}%")

fig1 = px.line(daily_ret_inv, x="install_date", y="d1_retention", text="label", markers=True, template="plotly_dark")
fig1.update_traces(line_color="#74B9FF", line_width=2.5, textposition="top center")
fig1.update_yaxes(range=[0, 80])
fig1.update_layout(font=dict(color="#FFFFFF"))
st.plotly_chart(fig1, use_container_width=True)

# Graph 2: 100% Stacked Bar Plot (Matches Played Share)
st.subheader("2. Daily D1 Game Mode Distribution (100% Stacked Bar)")
d1_m_inv = matches_inv[matches_inv["session_number"] <= 3]
d1_s_inv = d1_m_inv.groupby(["install_date", "tournament_type"])["match_id"].count().reset_index()
d1_tot_inv = d1_s_inv.groupby("install_date")["match_id"].transform("sum")
d1_s_inv["share_pct"] = (d1_s_inv["match_id"] / d1_tot_inv) * 100

fig2 = px.bar(
    d1_s_inv, 
    x="install_date", 
    y="share_pct", 
    color="tournament_type",
    title="Daily Match Share per Tournament (%)",
    labels={"install_date": "Install Date", "share_pct": "Match Share (%)", "tournament_type": "Tournament"},
    template="plotly_dark"
)
fig2.update_layout(barmode="stack", font=dict(color="#FFFFFF"))
st.plotly_chart(fig2, use_container_width=True)

# Graph 3: Tournament Economy Scatter
st.subheader("3. Tournament Economy Breakdown (Entry Fee vs Win Rate Anomaly)")
econ = matches_inv.groupby("tournament_type").agg(
    fee=("entry_fee", "mean"), win_rate=("is_win", lambda x: x.mean() * 100), count=("match_id", "count")
).reset_index()
econ["label"] = econ.apply(lambda r: f"{r['tournament_type']}<br>({r['fee']:.0f} Coins, {r['win_rate']:.1f}%)", axis=1)

fig3 = px.scatter(econ, x="fee", y="win_rate", size="count", color="tournament_type", text="label", template="plotly_dark")
fig3.update_traces(textposition="top center")
fig3.update_xaxes(range=[0, 310])
fig3.update_layout(font=dict(color="#FFFFFF"))
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------------------------------
# PART 2: POST-FIX VALIDATION & RECOVERY (MAY 25 – MAY 31)
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>PART 2: Post-Fix Validation & Retention Recovery</div>", unsafe_allow_html=True)

st.subheader("4. Full D1 Retention View (Post-Fix Deployment on May 25)")
daily_ret_full = filtered_matches.groupby("install_date").agg(total_users=("user_id", "nunique")).reset_index()

def calc_d1_full(dt):
    if datetime(2026, 5, 21) <= dt < datetime(2026, 5, 25):
        return np.random.uniform(52.2, 53.8)
    elif dt >= datetime(2026, 5, 25):
        return np.random.uniform(57.8, 59.5)
    else:
        return np.random.uniform(57.1, 58.9)

daily_ret_full["d1_retention"] = daily_ret_full["install_date"].apply(calc_d1_full)
daily_ret_full["label"] = daily_ret_full["d1_retention"].apply(lambda x: f"{x:.1f}%")

fig4 = px.line(daily_ret_full, x="install_date", y="d1_retention", text="label", markers=True, template="plotly_dark")
fig4.update_traces(line_color="#55E6C1", line_width=2.5, textposition="top center")
fig4.add_vline(
    x=pd.Timestamp("2026-05-25").timestamp() * 1000, 
    line_dash="dash", line_color="#FF7675",
    annotation_text="Fix Deployed (May 25)", annotation_position="top left"
)
fig4.update_yaxes(range=[0, 80])
fig4.update_layout(font=dict(color="#FFFFFF"))
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------------------------------------------
# PART 3: XP LEVEL THRESHOLD SIMULATION (GRADUAL IMPACT)
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>PART 3: Interactive XP Level Unlock Simulation</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #B0B0B0; font-size: 1.1rem;'>Adjust the slider to observe how restricting Dragon's Hoard access to higher XP Levels gradually restores D1 Retention.</p>", unsafe_allow_html=True)

# Interactive XP Slider
xp_threshold = st.slider(
    "Set Minimum XP Unlock Level for Dragon's Hoard:",
    min_value=1, max_value=15, value=1, step=1
)

# Smooth Gradual Retention Curve Logic
# Retention gradually recovers as XP Threshold increases from 1 to 10
retention_gain = min(1.0, (xp_threshold - 1) / 9.0) # 0.0 at Level 1, 1.0 at Level 10+
simulated_retention_val = 53.2 + (5.3 * retention_gain)

if xp_threshold < 5:
    st.markdown(f"<div style='background-color:#2C1F21; border-left:4px solid #FF7675; padding:12px; border-radius:5px; color:#FFFFFF;'>⚠️ <b>Level {xp_threshold} Simulation:</b> Severe coin depletion for early players. D1 Retention is low (~{simulated_retention_val:.1f}%).</div>", unsafe_allow_html=True)
elif xp_threshold < 10:
    st.markdown(f"<div style='background-color:#2C2A1F; border-left:4px solid #FDCB6E; padding:12px; border-radius:5px; color:#FFFFFF;'>📈 <b>Level {xp_threshold} Simulation:</b> Partial recovery observed. D1 Retention improves to ~{simulated_retention_val:.1f}%.</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div style='background-color:#1F2C28; border-left:4px solid #55E6C1; padding:12px; border-radius:5px; color:#FFFFFF;'>✅ <b>Level {xp_threshold}+ Simulation:</b> Optimal threshold! D1 Retention fully normalized (~{simulated_retention_val:.1f}%).</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Graph 5: Gradual Dynamic Retention Graph
st.subheader("5. Simulated D1 Retention Impact (Dynamic Curve)")
daily_ret_sim = filtered_matches.groupby("install_date").agg(total_users=("user_id", "nunique")).reset_index()

def calc_d1_sim(dt):
    if datetime(2026, 5, 21) <= dt < datetime(2026, 5, 25):
        base_drop = np.random.uniform(52.2, 53.8)
        recovered_val = np.random.uniform(57.8, 59.2)
        return base_drop + ((recovered_val - base_drop) * retention_gain)
    else:
        return np.random.uniform(57.1, 58.9)

daily_ret_sim["d1_retention"] = daily_ret_sim["install_date"].apply(calc_d1_sim)
daily_ret_sim["label"] = daily_ret_sim["d1_retention"].apply(lambda x: f"{x:.1f}%")

fig5 = px.line(daily_ret_sim, x="install_date", y="d1_retention", text="label", markers=True, template="plotly_dark")
fig5.update_traces(
    line_color="#55E6C1" if xp_threshold >= 10 else ("#FDCB6E" if xp_threshold >= 5 else "#FF7675"),
    line_width=2.5, textposition="top center"
)
fig5.update_yaxes(range=[0, 80])
fig5.update_layout(font=dict(color="#FFFFFF"))
st.plotly_chart(fig5, use_container_width=True)

# Graph 6: Smooth Gradual Churn Rate per XP Level
st.subheader("6. Dragon's Hoard Churn Rate by Player XP Level")

# Realistic Gradual Churn Decay Across Levels 1 to 15
xp_levels = list(range(1, 16))
# Churn drops smoothly from ~58% at XP 1 down to ~18% at XP 10+
gradual_churns = [max(18.0, 58.0 - (i - 1) * 4.4) for i in xp_levels]

xp_df = pd.DataFrame({
    "xp_level": xp_levels,
    "churn": gradual_churns
})

xp_df["status"] = xp_df["xp_level"].apply(lambda x: "Unlocked / Safe" if x >= xp_threshold else "Locked / High Churn")
xp_df["label"] = xp_df["churn"].apply(lambda x: f"{x:.1f}%")

fig6 = px.bar(
    xp_df, x="xp_level", y="churn", text="label", color="status",
    color_discrete_map={"Locked / High Churn": "#FF7675", "Unlocked / Safe": "#55E6C1"},
    template="plotly_dark",
    labels={"xp_level": "Player XP Level", "churn": "Churn Rate (%)"}
)
fig6.add_hline(y=20, line_dash="dash", line_color="#55E6C1", annotation_text="Safe Churn Baseline (~18-20%)")
fig6.update_xaxes(dtick=1)
fig6.update_layout(font=dict(color="#FFFFFF"))
st.plotly_chart(fig6, use_container_width=True)
