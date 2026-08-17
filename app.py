import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# 1. Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gaming Analytics: D1 Retention Incident",
    page_icon="🎮",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .metric-card {
        background-color: #1E222D;
        padding: 18px;
        border-radius: 8px;
        border-left: 4px solid #74B9FF;
        margin-bottom: 15px;
    }
    .metric-title { font-size: 0.85rem; color: #A0A0A0; margin-bottom: 5px; }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #FFFFFF; }
    .insight-box {
        background-color: #1E222D;
        border-left: 4px solid #FDCB6E;
        padding: 18px;
        border-radius: 6px;
        margin-bottom: 25px;
    }
    .section-header {
        color: #74B9FF;
        border-bottom: 1px solid #2D3748;
        padding-bottom: 8px;
        margin-top: 35px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Generation
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

    tournaments = [
        "Quick Clash", "Neon Blitz", "Starlight Cup", "Shadow Dash", "Solar Strike",
        "Crystal Clash", "Titan Arena", "Cyber Duel", "Vortex Rush", "Dragon's Hoard"
    ]

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
                churn_r = 0.55 if xp_lvl < 10 else 0.18
            else:
                t_type = np.random.choice(list(base_econ.keys()))
                fee = base_econ[t_type]["fee"] + np.random.randint(-2, 3)
                win_r = base_econ[t_type]["win"]
                churn_r = 0.18

            is_win = 1 if np.random.rand() < win_r else 0

            matches.append({
                "match_id": f"m_{u_id}_{sess}", "user_id": u_id, "install_date": inst_date,
                "country": row["country"], "session_number": sess, "tournament_type": t_type,
                "xp_level": xp_lvl, "is_win": is_win, "entry_fee": fee
            })

            if t_type == "Dragon's Hoard" and is_win == 0 and xp_lvl < 10 and is_problem:
                break

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
    <b>🔍 Executive Incident Summary:</b><br>
    • <b>Incident Period:</b> On May 21st, D1 Retention dropped by <b>~5%</b> (from 58.2% to 53.2%).<br>
    • <b>Root Cause:</b> Early exposure to the high-stakes <i>Dragon's Hoard</i> tournament (250 coins entry fee, 32% win rate) depleted coin balances for early-stage players.<br>
    • <b>Action & Recovery:</b> On May 25th, early access was rebalanced. D1 Retention immediately recovered to baseline (58.5%).
</div>
""", unsafe_allow_html=True)

# Metric Row
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
st.markdown("<h3 class='section-header'>PART 1: Incident Investigation (May 1–24)</h3>", unsafe_allow_html=True)

matches_inv = filtered_matches[filtered_matches["install_date"] <= datetime(2026, 5, 24)]

# Graph 1: Investigation Retention
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
st.plotly_chart(fig1, use_container_width=True)

# Graph 2: Game Mode Distribution
st.subheader("2. Daily D1 Game Mode Distribution (Dragon's Hoard Appears May 21)")
d1_m_inv = matches_inv[matches_inv["session_number"] <= 3]
d1_s_inv = d1_m_inv.groupby(["install_date", "tournament_type"])["match_id"].count().reset_index()
d1_tot_inv = d1_s_inv.groupby("install_date")["match_id"].transform("sum")
d1_s_inv["share_pct"] = (d1_s_inv["match_id"] / d1_tot_inv) * 100

fig2 = px.area(d1_s_inv, x="install_date", y="share_pct", color="tournament_type", template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# Graph 3: Tournament Economy
st.subheader("3. Tournament Economy Breakdown (Entry Fee vs Win Rate Anomaly)")
econ = matches_inv.groupby("tournament_type").agg(
    fee=("entry_fee", "mean"), win_rate=("is_win", lambda x: x.mean() * 100), count=("match_id", "count")
).reset_index()
econ["label"] = econ.apply(lambda r: f"{r['tournament_type']}<br>({r['fee']:.0f} Coins, {r['win_rate']:.1f}%)", axis=1)

fig3 = px.scatter(econ, x="fee", y="win_rate", size="count", color="tournament_type", text="label", template="plotly_dark")
fig3.update_traces(textposition="top center")
fig3.update_xaxes(range=[0, 310])
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------------------------------
# PART 2: POST-FIX VALIDATION & RECOVERY (MAY 25 – MAY 31)
# -----------------------------------------------------------------------------
st.markdown("<h3 class='section-header'>PART 2: Post-Fix Validation & Retention Recovery</h3>", unsafe_allow_html=True)

# Graph 4: Full Retention View with Fix
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
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------------------------------------------
# PART 3: XP LEVEL THRESHOLD SIMULATION
# -----------------------------------------------------------------------------
st.markdown("<h3 class='section-header'>PART 3: Interactive XP Level Unlock Simulation</h3>", unsafe_allow_html=True)
st.markdown("Use the slider below to simulate setting the **Minimum XP Unlock Level** for *Dragon's Hoard* and observe the dynamic impact on Retention and Churn.")

# Dedicated Interactive Slider
xp_threshold = st.slider(
    "Set Minimum XP Unlock Level for Dragon's Hoard:",
    min_value=1, max_value=15, value=1, step=1,
    help="Move slider to Level 10 to see full recovery."
)

if xp_threshold < 10:
    st.info(f"⚠️ **Current Simulation (XP Level {xp_threshold}):** Low-XP players (1–9) are exposed to early coin depletion, causing a ~5% D1 Retention drop.")
else:
    st.success(f"✅ **Optimal Threshold Reached (XP Level {xp_threshold}+):** Dragon's Hoard is locked for early players. D1 Retention recovers completely!")

# Graph 5: Dynamic Simulated Retention Graph
st.subheader("5. Simulated D1 Retention Impact (Controlled by XP Slider)")
daily_ret_sim = filtered_matches.groupby("install_date").agg(total_users=("user_id", "nunique")).reset_index()

def calc_d1_sim(dt):
    if datetime(2026, 5, 21) <= dt < datetime(2026, 5, 25):
        return np.random.uniform(52.2, 53.8) if xp_threshold < 10 else np.random.uniform(57.8, 59.2)
    else:
        return np.random.uniform(57.1, 58.9)

daily_ret_sim["d1_retention"] = daily_ret_sim["install_date"].apply(calc_d1_sim)
daily_ret_sim["label"] = daily_ret_sim["d1_retention"].apply(lambda x: f"{x:.1f}%")

fig5 = px.line(daily_ret_sim, x="install_date", y="d1_retention", text="label", markers=True, template="plotly_dark")
fig5.update_traces(line_color="#74B9FF" if xp_threshold < 10 else "#55E6C1", line_width=2.5, textposition="top center")
fig5.update_yaxes(range=[0, 80])
st.plotly_chart(fig5, use_container_width=True)

# Graph 6: Dynamic Churn Rate by XP Level
st.subheader("6. Churn Rate in Dragon's Hoard by Player XP Level")
xp_imp = filtered_matches[filtered_matches["tournament_type"] == "Dragon's Hoard"].groupby("xp_level").agg(
    churn=("is_win", lambda x: (1 - x.mean()) * 100)
).reset_index()

xp_imp["status"] = xp_imp["xp_level"].apply(lambda x: "Safe / Unlocked" if x >= xp_threshold else "Blocked / High Churn")
xp_imp["label"] = xp_imp["churn"].apply(lambda x: f"{x:.1f}%")

fig6 = px.bar(
    xp_imp, x="xp_level", y="churn", text="label", color="status",
    color_discrete_map={"Blocked / High Churn": "#FF7675", "Safe / Unlocked": "#55E6C1"},
    template="plotly_dark",
    labels={"xp_level": "Player XP Level", "churn": "Churn Rate (%)"}
)
fig6.add_hline(y=20, line_dash="dash", line_color="#55E6C1", annotation_text="Safe Churn Baseline (~18%)")
fig6.update_xaxes(dtick=1)
st.plotly_chart(fig6, use_container_width=True)
