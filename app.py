import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# ---------------------------------------------------------
# Page Configuration & Rajasthan Royals Branding
# ---------------------------------------------------------
st.set_page_config(
    page_title="SupeRR Selector | Rajasthan Royals",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Rajasthan Royals Theme (Pink #EA1A85, Navy #1F2A6B, Gold #FFD700, Background #0A0F2E)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif !important;
        color: #FFFFFF !important;
    }
    
    /* Top Header Bar: Dark Navy (#0A0F2E) to match the dark theme */
    header[data-testid="stHeader"], .stApp > header {
        background-color: #0A0F2E !important;
    }
    
    .stApp {
        background-color: #0A0F2E !important;
        color: #FFFFFF !important;
    }

    /* Force pure white / light pink across all headings, labels and prose */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    p, span, div, li, label {
        color: #FFFFFF !important;
    }
    
    .rr-secondary {
        color: #FFD1E8 !important;
    }

    /* Top Header Banner */
    .rr-header {
        background: linear-gradient(135deg, #1F2A6B 0%, #0D1338 50%, #EA1A85 100%);
        padding: 24px 30px;
        border-radius: 14px;
        border-left: 6px solid #EA1A85;
        box-shadow: 0 10px 25px rgba(234, 26, 133, 0.25);
        margin-bottom: 25px;
    }
    
    .rr-title {
        font-size: 32px;
        font-weight: 900;
        color: #FFFFFF !important;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    
    .rr-tagline {
        color: #FFD700 !important;
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .rr-sub {
        color: #FFD1E8 !important;
        font-size: 14px;
        margin-top: 6px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #161D4D, #1A235A);
        border: 1px solid rgba(234, 26, 133, 0.35);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.35);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #EA1A85;
        box-shadow: 0 10px 22px rgba(234, 26, 133, 0.35);
    }
    .metric-label {
        font-size: 12px;
        color: #FFD1E8 !important;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 900;
        color: #FFFFFF !important;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 11.5px;
        color: #FFD700 !important;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Player Cards */
    .player-card {
        background: linear-gradient(145deg, #141B48, #18225C);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
        transition: all 0.3s ease;
    }
    .player-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 22px rgba(234, 26, 133, 0.3);
        border-color: rgba(234, 26, 133, 0.6);
    }
    .player-card.rank-1 {
        border: 2px solid #FFD700;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.25);
    }
    .player-card.rank-2 {
        border: 1.5px solid #EA1A85;
    }
    
    .badge-pink {
        background-color: #EA1A85;
        color: #FFFFFF !important;
        padding: 4px 9px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-navy {
        background-color: #1F2A6B;
        color: #FFD700 !important;
        border: 1px solid #FFD700;
        padding: 4px 9px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
    }
    
    .positive-stat {
        color: #10B981 !important;
        font-weight: 800;
    }
    .negative-stat {
        color: #EF4444 !important;
        font-weight: 800;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B1033 !important;
        border-right: 1px solid rgba(234, 26, 133, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Sidebar Button Navigation */
    section[data-testid="stSidebar"] div.stButton {
        margin-bottom: 6px !important;
    }

    section[data-testid="stSidebar"] div.stButton > button {
        width: 100% !important;
        border-radius: 10px !important;
        padding: 11px 16px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        text-align: left !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
    }

    /* Unselected Buttons: Dark navy translucent card with bright white text */
    section[data-testid="stSidebar"] div.stButton > button[kind="secondary"],
    section[data-testid="stSidebar"] div.stButton > button:not([kind="primary"]) {
        background: rgba(20, 27, 72, 0.65) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }

    section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover,
    section[data-testid="stSidebar"] div.stButton > button:not([kind="primary"]):hover {
        background: rgba(234, 26, 133, 0.25) !important;
        border-color: #EA1A85 !important;
        color: #FFFFFF !important;
        transform: translateX(4px) !important;
    }

    /* Selected Active Button: Rajasthan Royals Pink (#EA1A85) with Gold border */
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #EA1A85 0%, #B01062 100%) !important;
        color: #FFFFFF !important;
        border: 1.5px solid #FFD700 !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(234, 26, 133, 0.5) !important;
        transform: translateX(4px) !important;
    }

    section[data-testid="stSidebar"] div.stButton > button p {
        color: #FFFFFF !important;
        font-size: 13.5px !important;
        margin: 0 !important;
    }

    /* Streamlit Form Widgets: Selectbox, Radio */
    div[data-testid="stWidgetLabel"] label, 
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span {
        color: #FFD1E8 !important;
        font-weight: 700 !important;
        font-size: 13.5px !important;
    }

    div[data-baseweb="select"] {
        background-color: #141B48 !important;
        border: 1px solid rgba(234, 26, 133, 0.4) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="select"] * {
        background-color: #141B48 !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #141B48 !important;
        color: #FFFFFF !important;
        border: 1px solid #EA1A85 !important;
    }
    ul[role="listbox"] li {
        color: #FFFFFF !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #EA1A85 !important;
        color: #FFFFFF !important;
    }

    /* Radio buttons */
    div[data-testid="stRadio"] label p, div[data-testid="stRadio"] label span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Dataframe styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(234, 26, 133, 0.3) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loader (Using ONLY provided CSVs, Never Invent Numbers)
# ---------------------------------------------------------
@st.cache_data
def load_datasets():
    batters_df = pd.read_csv('final_batters.csv')
    bowlers_df = pd.read_csv('final_bowlers.csv')
    phase_df = pd.read_csv('phase_data.csv')
    return batters_df, bowlers_df, phase_df

try:
    batters, bowlers, phase_data = load_datasets()
except Exception as e:
    st.error(f"Error loading CSV datasets: {e}")
    st.stop()

# ---------------------------------------------------------
# Sidebar Navigation (Clean Layout, Logo, No Search, Button Nav)
# ---------------------------------------------------------
logo_path = os.path.join("assets", "rr_logo.png")
if os.path.exists(logo_path):
    _, col_logo, _ = st.sidebar.columns([1, 2, 1])
    with col_logo:
        st.image(logo_path, width=130)

st.sidebar.markdown("""
<div style='text-align: center; padding: 4px 0 10px 0;'>
    <h2 style='color: #EA1A85; margin: 0; font-weight: 900; letter-spacing: 1px;'>RAJASTHAN ROYALS</h2>
    <p style='color: #FFD700; font-size: 13px; font-weight: 800; letter-spacing: 2px; margin: 0;'>HALLA BOL! 👑</p>
    <p style='color: #FFD1E8; font-size: 11px; margin: 2px 0 0 0;'>SupeRR Selector Season 2</p>
</div>
<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 5px 0 12px 0;'>
""", unsafe_allow_html=True)

# Navigation using clean full-width rounded buttons with st.session_state
PAGES = [
    "👑 Overview & Hidden Gems",
    "🏏 Top 10 Batters",
    "🎯 Top 10 Bowlers",
    "⚡ Clutch Map",
    "⏳ Pressure Timeline",
    "⚔️ Player Head-to-Head",
    "📖 Methodology & Formulas"
]

if "selected_page" not in st.session_state:
    st.session_state.selected_page = PAGES[0]

for p in PAGES:
    is_active = (st.session_state.selected_page == p)
    btn_type = "primary" if is_active else "secondary"
    if st.sidebar.button(p, key=f"nav_btn_{p}", type=btn_type, width="stretch"):
        st.session_state.selected_page = p
        st.rerun()

menu = st.session_state.selected_page

st.sidebar.markdown("""
<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 20px 0 12px 0;'>
<div style='text-align: center; color: #FFD1E8; font-size: 11px; padding: 4px 6px;'>
    IPL 2022-2026 + T20I | Ball-by-ball pressure analysis
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Functions (Plotly Dark Theme)
# ---------------------------------------------------------
def apply_rr_theme(fig, title="", height=550):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0A0F2E",
        plot_bgcolor="#141B48",
        font=dict(color="#FFFFFF", family="Montserrat"),
        title=dict(text=title, font=dict(color="#FFFFFF", size=16, family="Montserrat")),
        legend=dict(font=dict(color="#FFFFFF", size=12, family="Montserrat")),
        hoverlabel=dict(
            bgcolor="#0F1538",
            font_color="#FFFFFF",
            font_size=12,
            bordercolor="#EA1A85",
            font_family="Montserrat"
        ),
        height=height
    )
    fig.update_xaxes(
        title_font=dict(color="#FFFFFF", size=13),
        tickfont=dict(color="#FFFFFF", size=11),
        gridcolor="rgba(255, 255, 255, 0.12)"
    )
    fig.update_yaxes(
        title_font=dict(color="#FFFFFF", size=13),
        tickfont=dict(color="#FFFFFF", size=11),
        gridcolor="rgba(255, 255, 255, 0.12)"
    )
    return fig

# ---------------------------------------------------------
# PAGE 1: OVERVIEW & HIDDEN GEMS
# ---------------------------------------------------------
if menu == "👑 Overview & Hidden Gems":
    st.markdown("""
    <div class='rr-header'>
        <div class='rr-tagline'>SupeRR Selector Season 2 • Rajasthan Royals Analytics</div>
        <div class='rr-title'>Identifying the Most Reliable Players Under Pressure</div>
        <div class='rr-sub'>Official pressure reliability index based on 200,961 standard T20 deliveries. Halla Bol!</div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Pressure Deliveries</div>
            <div class='metric-value'>91,435</div>
            <div class='metric-sub'>45.5% of all standard balls</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Wicket Rate Escalation</div>
            <div class='metric-value'>+50.0%</div>
            <div class='metric-sub'>6.51 vs 4.34 wkts/100b under pressure</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Top Clutch Batter</div>
            <div class='metric-value'>V. Sooryavanshi</div>
            <div class='metric-sub'>243.28 Pressure SR (Avg Rank: 1.00)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Top Clutch Bowler</div>
            <div class='metric-value'>A. Ghazanfar</div>
            <div class='metric-sub'>7.36 Pressure Econ (Avg Rank: 1.67)</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hidden Gems Section
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>💎 Hidden Gems & Tactical Auction Targets</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>Under-the-radar specialists identified by our pressure-robustness algorithms who deliver exceptional execution when games are on the line:</p>", unsafe_allow_html=True)
    
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("""
        <div class='player-card rank-1'>
            <span class='badge-pink'>RR FUTURE CORNERSTONE</span>
            <h3 style='color: #FFFFFF; margin-top: 8px; margin-bottom: 2px; font-weight: 800;'>Vaibhav Sooryavanshi</h3>
            <p style='color: #FFD700; font-weight: 700; font-size: 13px; margin: 0;'>Rajasthan Royals / India • Batter</p>
            <hr style='border-color: rgba(255,255,255,0.12); margin: 10px 0;'>
            <div style='font-size: 13px; color: #FFFFFF; line-height: 1.7;'>
                • <b>Pressure SR</b>: <span class='positive-stat'>243.28</span> (vs 210.39 normal)<br>
                • <b>Sample Size</b>: 251 Press Balls | 425 Base Balls<br>
                • <b>Clutch Elevation</b>: <span class='positive-stat'>+32.88 SR Delta</span><br>
                • <b>Verdict</b>: Generational power-hitting ceiling. Unflappable in early powerplay and high-RRR chases.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with g2:
        st.markdown("""
        <div class='player-card rank-2'>
            <span class='badge-navy'>SPIN MYSTERY TARGET</span>
            <h3 style='color: #FFFFFF; margin-top: 8px; margin-bottom: 2px; font-weight: 800;'>Allah Ghazanfar</h3>
            <p style='color: #FFD700; font-weight: 700; font-size: 13px; margin: 0;'>Afghanistan / MI • Mystery Spinner</p>
            <hr style='border-color: rgba(255,255,255,0.12); margin: 10px 0;'>
            <div style='font-size: 13px; color: #FFFFFF; line-height: 1.7;'>
                • <b>Pressure Economy</b>: <span class='positive-stat'>7.36</span> (vs 9.57 normal)<br>
                • <b>Sample Size</b>: 266 Press Balls | 195 Base Balls<br>
                • <b>Clutch Tightening</b>: <span class='positive-stat'>+2.21 Econ Saved</span><br>
                • <b>Verdict</b>: Phenomenal defensive mystery spin. Ranks #1 or #2 across all 3 pressure thresholds.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with g3:
        st.markdown("""
        <div class='player-card'>
            <span class='badge-pink'>MIDDLE-ORDER ACCELERATOR</span>
            <h3 style='color: #FFFFFF; margin-top: 8px; margin-bottom: 2px; font-weight: 800;'>Naman Dhir</h3>
            <p style='color: #FFD700; font-weight: 700; font-size: 13px; margin: 0;'>Mumbai Indians • Middle Order</p>
            <hr style='border-color: rgba(255,255,255,0.12); margin: 10px 0;'>
            <div style='font-size: 13px; color: #FFFFFF; line-height: 1.7;'>
                • <b>Pressure SR</b>: <span class='positive-stat'>187.80</span> (vs 149.64 normal)<br>
                • <b>Sample Size</b>: 296 Press Balls | 293 Base Balls<br>
                • <b>Clutch Elevation</b>: <span class='positive-stat'>+38.16 SR Delta</span><br>
                • <b>Verdict</b>: High-intent finisher who elevates strike rate aggressively in death overs without wasting balls.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 2: TOP 10 BATTERS (Clean Cards, No Filter Clutter)
# ---------------------------------------------------------
elif menu == "🏏 Top 10 Batters":
    st.markdown("""
    <div class='rr-header'>
        <div class='rr-tagline'>OFFICIAL RANKINGS • BATTING</div>
        <div class='rr-title'>Top 10 Batters Under Pressure</div>
        <div class='rr-sub'>Min. 200 Pressure Balls & 200 Baseline Balls • Capped Delta • Phase & Opponent Weighted</div>
    </div>
    """, unsafe_allow_html=True)
    
    for _, row in batters.iterrows():
        delta_sr = row['pressure_SR'] - row['baseline_SR']
        delta_color = "positive-stat" if delta_sr >= 0 else "negative-stat"
        delta_symbol = "▲" if delta_sr >= 0 else "▼"
        rank_class = "rank-1" if row['rank'] == 1 else ("rank-2" if row['rank'] == 2 else "")
        
        st.markdown(f"""
        <div class='player-card {rank_class}'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span class='badge-navy'>RANK #{row['rank']}</span>
                    <span class='badge-pink' style='margin-left: 6px;'>AVG RANK: {row['avg_rank']:.2f}</span>
                    <span style='color: #FFD1E8; font-size: 12px; margin-left: 8px;'>Qualified: {row['qualified_thresholds']} | Top 10: {row['thresholds_in_top10']}</span>
                    <h2 style='color: #FFFFFF; margin: 6px 0 2px 0; font-weight: 800;'>{row['player']}</h2>
                    <p style='color: #FFD700; font-size: 13px; font-weight: 700; margin: 0;'>{row['team']}</p>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 11px; color: #FFD1E8; font-weight: 700;'>PRESSURE RATING</div>
                    <div style='font-size: 32px; font-weight: 900; color: #EA1A85;'>{row['pressure_rating']:.1f}</div>
                    <div style='font-size: 11px; color: #FFFFFF;'>Press: <b>{row['pressure_balls']}b</b> | Base: <b>{row['baseline_balls']}b</b></div>
                    <div style='font-size: 10px; color: #FFD1E8;'>IPL: {row['ipl_balls']}b | T20I: {row['t20i_balls']}b</div>
                </div>
            </div>
            <hr style='border-color: rgba(255,255,255,0.08); margin: 12px 0;'>
            <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;'>
                <div style='background: rgba(10,14,42,0.6); padding: 8px; border-radius: 8px;'>
                    <span style='font-size: 11px; color: #FFD1E8;'>PRESSURE SR</span><br>
                    <span style='font-size: 18px; font-weight: 800; color: #FFFFFF;'>{row['pressure_SR']:.1f}</span>
                </div>
                <div style='background: rgba(10,14,42,0.6); padding: 8px; border-radius: 8px;'>
                    <span style='font-size: 11px; color: #FFD1E8;'>NORMAL SR</span><br>
                    <span style='font-size: 18px; font-weight: 800; color: #FFFFFF;'>{row['baseline_SR']:.1f}</span>
                </div>
                <div style='background: rgba(10,14,42,0.6); padding: 8px; border-radius: 8px;'>
                    <span style='font-size: 11px; color: #FFD1E8;'>CLUTCH DELTA (Δ)</span><br>
                    <span class='{delta_color}' style='font-size: 18px;'>{delta_symbol} {abs(delta_sr):.1f}</span>
                </div>
                <div style='background: rgba(10,14,42,0.6); padding: 8px; border-radius: 8px;'>
                    <span style='font-size: 11px; color: #FFD1E8;'>LEAGUE EXP SR</span><br>
                    <span style='font-size: 18px; font-weight: 800; color: #FFD700;'>{row['league_expected_SR']:.1f}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 3: TOP 10 BOWLERS (Clean Cards, No Filter Clutter)
# ---------------------------------------------------------
elif menu == "🎯 Top 10 Bowlers":
    st.markdown("""
    <div class='rr-header'>
        <div class='rr-tagline'>OFFICIAL RANKINGS • BOWLING</div>
        <div class='rr-title'>Top 10 Bowlers Under Pressure</div>
        <div class='rr-sub'>Min. 200 Pressure Balls & 150 Baseline Balls • Economy Primary (55%) • Hard Filter Enforced</div>
    </div>
    """, unsafe_allow_html=True)
    
    for _, row in bowlers.iterrows():
        delta_econ = row['baseline_economy'] - row['pressure_economy'] # positive is good
        delta_color = "positive-stat" if delta_econ >= 0 else "negative-stat"
        delta_symbol = "▼ Tightened" if delta_econ >= 0 else "▲ Leaked"
        rank_class = "rank-1" if row['rank'] == 1 else ("rank-2" if row['rank'] == 2 else "")
        
        st.markdown(f"""
        <div class='player-card {rank_class}'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span class='badge-navy'>RANK #{row['rank']}</span>
                    <span class='badge-pink' style='margin-left: 6px;'>{row['type'].upper()}</span>
                    <span class='badge-navy' style='margin-left: 6px;'>AVG RANK: {row['avg_rank']:.2f}</span>
                    <span style='color: #FFD1E8; font-size: 12px; margin-left: 8px;'>Qualified: {row['qualified_thresholds']} | Top 10: {row['thresholds_in_top10']}</span>
                    <h2 style='color: #FFFFFF; margin: 6px 0 2px 0; font-weight: 800;'>{row['player']}</h2>
                    <p style='color: #FFD700; font-size: 13px; font-weight: 700; margin: 0;'>{row['team']}</p>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 11px; color: #FFD1E8; font-weight: 700;'>PRESSURE RATING</div>
                    <div style='font-size: 32px; font-weight: 900; color: #EA1A85;'>{row['pressure_rating']:.1f}</div>
                    <div style='font-size: 11px; color: #FFFFFF;'>Press: <b>{row['pressure_balls']}b</b> | Base: <b>{row['baseline_balls']}b</b></div>
                    <div style='font-size: 10px; color: #FFD1E8;'>IPL: {row['ipl_balls']}b | T20I: {row['t20i_balls']}b</div>
                </div>
            </div>
            <hr style='border-color: rgba(255,255,255,0.08); margin: 12px 0;'>
            <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;'>
                <div style='background: rgba(10,14,42,0.6); padding: 8px; border-radius: 8px;'>
                    <span style='font-size: 11px; color: #FFD1E8;'>PRESSURE ECONOMY</span><br>
                    <span style='font-size: 18px; font-weight: 800; color: #FFFFFF;'>{row['pressure_economy']:.2f}</span>
                </div>
                <div style='background: rgba(10,14,42,0.6); padding: 8px; border-radius: 8px;'>
                    <span style='font-size: 11px; color: #FFD1E8;'>NORMAL ECONOMY</span><br>
                    <span style='font-size: 18px; font-weight: 800; color: #FFFFFF;'>{row['baseline_economy']:.2f}</span>
                </div>
                <div style='background: rgba(10,14,42,0.6); padding: 8px; border-radius: 8px;'>
                    <span style='font-size: 11px; color: #FFD1E8;'>CLUTCH DELTA (Δ)</span><br>
                    <span class='{delta_color}' style='font-size: 16px;'>{delta_symbol} {abs(delta_econ):.2f}</span>
                </div>
                <div style='background: rgba(10,14,42,0.6); padding: 8px; border-radius: 8px;'>
                    <span style='font-size: 11px; color: #FFD1E8;'>LEAGUE EXP ECON</span><br>
                    <span style='font-size: 18px; font-weight: 800; color: #FFD700;'>{row['league_expected_economy']:.2f}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 4: CLUTCH MAP (Clean Scatter Plots with Parity Line)
# ---------------------------------------------------------
elif menu == "⚡ Clutch Map":
    st.markdown("""
    <div class='rr-header'>
        <div class='rr-tagline'>DIAGNOSTIC VISUALIZATION</div>
        <div class='rr-title'>Clutch Map: Normal vs Pressure Performance</div>
        <div class='rr-sub'>Dotted diagonal line represents parity (y = x). Points above line (batters) or below line (bowlers) indicate superior clutch elevation.</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏏 Batters Clutch Scatter", "🎯 Bowlers Clutch Scatter"])
    
    with tab1:
        fig_b = go.Figure()
        
        # Parity Line
        min_sr = min(batters['baseline_SR'].min(), batters['pressure_SR'].min()) - 10
        max_sr = max(batters['baseline_SR'].max(), batters['pressure_SR'].max()) + 10
        fig_b.add_trace(go.Scatter(
            x=[min_sr, max_sr], y=[min_sr, max_sr],
            mode='lines', line=dict(color='rgba(255, 255, 255, 0.4)', dash='dash'),
            name='Parity Line (No Delta)',
            hoverinfo='skip'
        ))
        
        # All Scatter points
        custom_data_b = np.stack((
            batters['pressure_balls'],
            batters['baseline_balls'],
            batters['pressure_rating'],
            batters['rank'],
            batters['team']
        ), axis=-1)
        
        fig_b.add_trace(go.Scatter(
            x=batters['baseline_SR'],
            y=batters['pressure_SR'],
            mode='markers+text',
            text=batters['player'],
            textposition="top center",
            customdata=custom_data_b,
            marker=dict(
                size=batters['pressure_balls'] / 22,
                color=batters['pressure_rating'],
                colorscale=[[0, '#1F2A6B'], [0.5, '#EA1A85'], [1.0, '#FFD700']],
                showscale=True,
                colorbar=dict(
                    title=dict(text="Rating", font=dict(color="#FFFFFF", size=12)),
                    tickfont=dict(color="#FFFFFF"),
                    tickcolor="#FFFFFF"
                ),
                line=dict(color='rgba(255,255,255,0.3)', width=1)
            ),
            hovertemplate="<b>%{text}</b> (Rank #%{customdata[3]})<br>Team: %{customdata[4]}<br>Normal Baseline SR: %{x:.1f}<br>Pressure Strike Rate: %{y:.1f}<br>Pressure Deliveries: %{customdata[0]}b<br>Baseline Deliveries: %{customdata[1]}b<br>Official Pressure Rating: %{customdata[2]:.1f}<extra></extra>"
        ))
        
        apply_rr_theme(fig_b, "Batters: Normal SR vs Pressure SR (Above Diagonal = Clutch Elevation)", 600)
        fig_b.update_xaxes(title="Normal Baseline Strike Rate")
        fig_b.update_yaxes(title="Pressure Strike Rate")
        st.plotly_chart(fig_b, width="stretch")
        
    with tab2:
        fig_bw = go.Figure()
        
        min_ec = min(bowlers['baseline_economy'].min(), bowlers['pressure_economy'].min()) - 1
        max_ec = max(bowlers['baseline_economy'].max(), bowlers['pressure_economy'].max()) + 1
        fig_bw.add_trace(go.Scatter(
            x=[min_ec, max_ec], y=[min_ec, max_ec],
            mode='lines', line=dict(color='rgba(255, 255, 255, 0.4)', dash='dash'),
            name='Parity Line (No Delta)',
            hoverinfo='skip'
        ))
        
        custom_data_bw = np.stack((
            bowlers['pressure_balls'],
            bowlers['baseline_balls'],
            bowlers['pressure_rating'],
            bowlers['rank'],
            bowlers['team'],
            bowlers['type']
        ), axis=-1)
        
        fig_bw.add_trace(go.Scatter(
            x=bowlers['baseline_economy'],
            y=bowlers['pressure_economy'],
            mode='markers+text',
            text=bowlers['player'],
            textposition="top center",
            customdata=custom_data_bw,
            marker=dict(
                size=bowlers['pressure_balls'] / 16,
                color=bowlers['pressure_rating'],
                colorscale=[[0, '#1F2A6B'], [0.5, '#EA1A85'], [1.0, '#FFD700']],
                showscale=True,
                colorbar=dict(
                    title=dict(text="Rating", font=dict(color="#FFFFFF", size=12)),
                    tickfont=dict(color="#FFFFFF"),
                    tickcolor="#FFFFFF"
                ),
                line=dict(color='rgba(255,255,255,0.3)', width=1)
            ),
            hovertemplate="<b>%{text}</b> (Rank #%{customdata[3]})<br>Team: %{customdata[4]} • %{customdata[5]}<br>Normal Baseline Economy: %{x:.2f}<br>Pressure Economy: %{y:.2f}<br>Pressure Deliveries: %{customdata[0]}b<br>Baseline Deliveries: %{customdata[1]}b<br>Official Pressure Rating: %{customdata[2]:.1f}<extra></extra>"
        ))
        
        apply_rr_theme(fig_bw, "Bowlers: Normal Economy vs Pressure Economy (Below Diagonal = Clutch Tightening)", 600)
        fig_bw.update_xaxes(title="Normal Baseline Economy")
        fig_bw.update_yaxes(title="Pressure Economy")
        st.plotly_chart(fig_bw, width="stretch")

# ---------------------------------------------------------
# PAGE 5: PRESSURE TIMELINE (Clean Phase Volume Chart & Table)
# ---------------------------------------------------------
elif menu == "⏳ Pressure Timeline":
    st.markdown("""
    <div class='rr-header'>
        <div class='rr-tagline'>PHASE ANALYSIS</div>
        <div class='rr-title'>Pressure Timeline: Powerplay, Middle, Death</div>
        <div class='rr-sub'>Tracking how player volume and performance evolve across T20 game phases.</div>
    </div>
    """, unsafe_allow_html=True)
    
    role_choice = st.radio("Select Role", ["Batters", "Bowlers"], horizontal=True, key="timeline_role")
    
    if role_choice == "Batters":
        target_df = batters[['player_id', 'player', 'rank']].copy()
        role_phase = phase_data[phase_data['role'] == 'Batter'].merge(target_df, on='player_id', how='inner')
        player_order = batters['player'].tolist()
    else:
        target_df = bowlers[['player_id', 'player', 'rank']].copy()
        role_phase = phase_data[phase_data['role'] == 'Bowler'].merge(target_df, on='player_id', how='inner')
        player_order = bowlers['player'].tolist()
    
    # Volume by Phase Bar Chart
    fig_phase = px.bar(
        role_phase,
        x='player',
        y='pressure_balls',
        color='phase',
        title=f"{role_choice}: Pressure Deliveries by Match Phase (Final Top 10)",
        color_discrete_map={
            'Powerplay': '#FFD700',
            'Middle': '#1F2A6B',
            'Death': '#EA1A85'
        },
        category_orders={'player': player_order, 'phase': ['Powerplay', 'Middle', 'Death']},
        template="plotly_dark"
    )
    fig_phase.update_traces(
        hovertemplate="<b>%{x}</b><br>Phase: %{fullData.name}<br>Pressure Deliveries: %{y} balls<extra></extra>"
    )
    apply_rr_theme(fig_phase, f"{role_choice}: Pressure Deliveries by Match Phase", 520)
    fig_phase.update_layout(
        xaxis=dict(title="Player (Official Rank Order)", categoryorder='array', categoryarray=player_order),
        yaxis=dict(title="Pressure Deliveries Faced / Bowled"),
        legend=dict(title="Match Phase", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_phase, width="stretch")
    
    st.markdown("<h4 style='color: #FFD700; margin-top: 15px;'>Phase Data Breakdown (Top 10 Only)</h4>", unsafe_allow_html=True)
    st.dataframe(
        role_phase[['rank', 'player', 'phase', 'pressure_balls', 'pressure_runs', 'wickets_or_dismissals']].sort_values(['rank', 'phase']),
        width="stretch",
        hide_index=True
    )

# ---------------------------------------------------------
# PAGE 6: PLAYER HEAD-TO-HEAD (Clean Radar Comparison)
# ---------------------------------------------------------
elif menu == "⚔️ Player Head-to-Head":
    st.markdown("""
    <div class='rr-header'>
        <div class='rr-tagline'>COMPARATIVE SCOUTING</div>
        <div class='rr-title'>Player Head-to-Head Radar Comparison</div>
        <div class='rr-sub'>Multi-dimensional radar chart benchmarking key player attributes under pressure.</div>
    </div>
    """, unsafe_allow_html=True)
    
    role_pick = st.radio("Select Category", ["Batters", "Bowlers"], horizontal=True, key="h2h_role")
    
    if role_pick == "Batters":
        p_list = batters['player'].tolist()
        c1, c2 = st.columns(2)
        with c1:
            p1_name = st.selectbox("Select Player 1", p_list, index=0, key="h2h_p1_b")
        with c2:
            p2_name = st.selectbox("Select Player 2", p_list, index=1, key="h2h_p2_b")
            
        p1 = batters[batters['player'] == p1_name].iloc[0]
        p2 = batters[batters['player'] == p2_name].iloc[0]
        
        categories = ['Pressure Rating', 'Pressure SR', 'Normal SR', 'Clutch Delta SR', 'League Expected SR']
        
        def get_b_metrics(row):
            return [
                row['pressure_rating'],
                row['pressure_SR'] * 0.7,
                row['baseline_SR'] * 0.7,
                (row['pressure_SR'] - row['baseline_SR']) + 100,
                row['league_expected_SR'] * 0.7
            ]
            
        r1 = get_b_metrics(p1)
        r2 = get_b_metrics(p2)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=r1, theta=categories, fill='toself', name=p1_name, line_color='#EA1A85'))
        fig_radar.add_trace(go.Scatterpolar(r=r2, theta=categories, fill='toself', name=p2_name, line_color='#FFD700'))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[50, 160], color="#FFFFFF", gridcolor="rgba(255,255,255,0.15)"),
                angularaxis=dict(color="#FFFFFF")
            ),
            showlegend=True,
            legend=dict(font=dict(color="#FFFFFF", size=13)),
            template="plotly_dark",
            paper_bgcolor="#0A0F2E",
            height=500,
            margin=dict(l=40, r=40, t=30, b=30)
        )
        st.plotly_chart(fig_radar, width="stretch")
        
    else:
        p_list = bowlers['player'].tolist()
        c1, c2 = st.columns(2)
        with c1:
            p1_name = st.selectbox("Select Player 1", p_list, index=0, key="h2h_p1_bw")
        with c2:
            p2_name = st.selectbox("Select Player 2", p_list, index=1, key="h2h_p2_bw")
            
        p1 = bowlers[bowlers['player'] == p1_name].iloc[0]
        p2 = bowlers[bowlers['player'] == p2_name].iloc[0]
        
        categories = ['Pressure Rating', 'Economy Resistance', 'Wickets Scaled', 'T20I Experience', 'League Benchmark']
        
        def get_bw_metrics(row):
            return [
                row['pressure_rating'],
                (12.0 - row['pressure_economy']) * 12,
                row['wickets'] * 2.5,
                min(150, row['t20i_balls'] / 5),
                (12.0 - row['league_expected_economy']) * 12
            ]
            
        r1 = get_bw_metrics(p1)
        r2 = get_bw_metrics(p2)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=r1, theta=categories, fill='toself', name=p1_name, line_color='#EA1A85'))
        fig_radar.add_trace(go.Scatterpolar(r=r2, theta=categories, fill='toself', name=p2_name, line_color='#FFD700'))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[40, 150], color="#FFFFFF", gridcolor="rgba(255,255,255,0.15)"),
                angularaxis=dict(color="#FFFFFF")
            ),
            showlegend=True,
            legend=dict(font=dict(color="#FFFFFF", size=13)),
            template="plotly_dark",
            paper_bgcolor="#0A0F2E",
            height=500,
            margin=dict(l=40, r=40, t=30, b=30)
        )
        st.plotly_chart(fig_radar, width="stretch")

# ---------------------------------------------------------
# PAGE 7: METHODOLOGY & FORMULAS
# ---------------------------------------------------------
elif menu == "📖 Methodology & Formulas":
    st.markdown("""
    <div class='rr-header'>
        <div class='rr-tagline'>ANALYTICAL RIGOR & METHODOLOGICAL SPECIFICATION</div>
        <div class='rr-title'>Methodology, Mathematical Formulas & Validation</div>
        <div class='rr-sub'>Transparent, reproducible mathematical framework computed on 200,961 standard T20 deliveries. Halla Bol!</div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 1. Mathematical Formulas Display (Rendered with st.latex)
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>1. Exact Mathematical Rating Formulas</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>Each player's rating is computed without subjective weights, combining own baseline delta and peer league benchmarks:</p>", unsafe_allow_html=True)

    st.markdown("<h4 style='color: #EA1A85; margin-bottom: 2px;'>🏏 Batting Pressure Rating Formula</h4>", unsafe_allow_html=True)
    st.latex(r"\text{Pressure Rating}_{\text{Batter}} = 0.50 \times \left(100 + \min(35.0, \max(-50.0, \text{SR}_{\text{Press}} - \text{SR}_{\text{Base}}))\right) + 0.50 \times \left(\frac{\text{SR}_{\text{Adj}}}{\text{SR}_{\text{League}}} \times 100\right)")
    
    st.markdown("<p style='color: #FFD1E8; font-size: 13px;'>Where Bayesian shrinkage (k = 100 balls) regulates sample extremes toward league expected strike rate:</p>", unsafe_allow_html=True)
    st.latex(r"\text{SR}_{\text{Adj}} = \frac{n_p \times \text{SR}_{\text{Press}} + 100 \times \text{SR}_{\text{League}}}{n_p + 100}")

    st.markdown("<h4 style='color: #EA1A85; margin-top: 20px; margin-bottom: 2px;'>🎯 Bowling Pressure Rating Formula</h4>", unsafe_allow_html=True)
    st.latex(r"\text{Pressure Rating}_{\text{Bowler}} = 0.55 \times \text{Score}_{\text{Economy}} + 0.25 \times \text{Score}_{\text{WPB}} + 0.20 \times \text{Score}_{\text{Dot}}")
    
    st.markdown("<p style='color: #FFD1E8; font-size: 13px;'>With sub-component scores benchmarked against same-phase league expectations:</p>", unsafe_allow_html=True)
    st.latex(r"\text{Score}_{\text{Economy}} = \left(2.0 - \frac{\text{Econ}_{\text{Press}}}{\text{Econ}_{\text{League}}}\right) \times 100 \quad \left[\text{Hard Filter: } \text{Econ}_{\text{Press}} \le \text{Econ}_{\text{League}}\right]")
    st.latex(r"\text{Score}_{\text{WPB}} = \left(\frac{\text{WPB}_{\text{Press}}}{\text{WPB}_{\text{League}}}\right) \times 100 \qquad \text{Score}_{\text{Dot}} = \left(\frac{\text{Dot\%}_{\text{Press}}}{\text{Dot\%}_{\text{League}}}\right) \times 100")

    st.markdown("<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 25px 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. Percentage of Balls Labelled High Pressure
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>2. Percentage of Deliveries Under Pressure</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>Across all 200,961 standard match deliveries, pressure shares vary across sensitivity thresholds:</p>", unsafe_allow_html=True)

    p_df = pd.DataFrame([
        {
            "Threshold": "T1 (Moderate Pressure)",
            "Batting Deliveries": "109,474",
            "Batting Pressure %": "54.48%",
            "Bowling Deliveries": "109,242",
            "Bowling Pressure %": "54.36%"
        },
        {
            "Threshold": "T2 (Standard Baseline)",
            "Batting Deliveries": "91,435",
            "Batting Pressure %": "45.50%",
            "Bowling Deliveries": "95,557",
            "Bowling Pressure %": "47.55%"
        },
        {
            "Threshold": "T3 (Extreme Crunch)",
            "Batting Deliveries": "73,658",
            "Batting Pressure %": "36.65%",
            "Bowling Deliveries": "82,163",
            "Bowling Pressure %": "40.89%"
        }
    ])
    st.dataframe(p_df, width="stretch", hide_index=True)

    st.markdown("<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 25px 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. Pressure vs Normal Balls Empirical Comparison
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>3. Empirical Evidence: Pressure vs Normal Deliveries</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>Direct statistical comparison of 87,274 high-pressure balls faced vs 105,977 normal baseline balls faced (T2):</p>", unsafe_allow_html=True)

    comp_df = pd.DataFrame([
        {
            "Performance Metric": "Total Deliveries (Innings 1 & 2)",
            "High Pressure Balls": "91,435 balls (45.50%)",
            "Normal Baseline Balls": "109,526 balls (54.50%)",
            "Delta / Pressure Shift": "Total: 200,961 deliveries"
        },
        {
            "Performance Metric": "Faced Balls (Batting)",
            "High Pressure Balls": "87,274 balls",
            "Normal Baseline Balls": "105,977 balls",
            "Delta / Pressure Shift": "Excludes wides"
        },
        {
            "Performance Metric": "Legal Balls (Bowling)",
            "High Pressure Balls": "86,779 balls",
            "Normal Baseline Balls": "105,633 balls",
            "Delta / Pressure Shift": "Excludes wides & no-balls"
        },
        {
            "Performance Metric": "Run Rate (Runs per Over)",
            "High Pressure Balls": "8.89 rpo",
            "Normal Baseline Balls": "7.94 rpo",
            "Delta / Pressure Shift": "+0.95 rpo (+12.0% scoring lift)"
        },
        {
            "Performance Metric": "Batting Strike Rate",
            "High Pressure Balls": "148.18",
            "Normal Baseline Balls": "132.28",
            "Delta / Pressure Shift": "+15.90 SR (+12.0%)"
        },
        {
            "Performance Metric": "Wickets per 100 Legal Balls",
            "High Pressure Balls": "6.51 wkts / 100b",
            "Normal Baseline Balls": "4.34 wkts / 100b",
            "Delta / Pressure Shift": "+2.17 wkts / 100b (+50.0% hazard surge)"
        },
        {
            "Performance Metric": "Dismissals per 100 Faced Balls",
            "High Pressure Balls": "6.98%",
            "Normal Baseline Balls": "4.48%",
            "Delta / Pressure Shift": "+2.50% (+55.8% dismissal risk)"
        },
        {
            "Performance Metric": "Dot Ball Percentage",
            "High Pressure Balls": "35.23%",
            "Normal Baseline Balls": "38.61%",
            "Delta / Pressure Shift": "-3.38% (Fewer dot balls forced)"
        },
        {
            "Performance Metric": "Boundary Frequency (4s + 6s)",
            "High Pressure Balls": "19.97% (1 in 5.0 balls)",
            "Normal Baseline Balls": "17.61% (1 in 5.7 balls)",
            "Delta / Pressure Shift": "+2.36% (+13.4% boundary spike)"
        }
    ])
    st.dataframe(comp_df, width="stretch", hide_index=True)

    st.markdown("<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 25px 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 4. Exact Threshold Definition Matrix
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>4. Pressure Sensitivity Thresholds (T1, T2, T3)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>Objective situational triggers applied to partition deliveries into pressure vs baseline:</p>", unsafe_allow_html=True)

    th_matrix = pd.DataFrame([
        {
            "Threshold": "T1 (Moderate)",
            "Batting Triggers": "Inn 2 & RRR > 8.0  OR  Wickets in hand ≤ 4  OR  Overs 15–20  OR  Knock-out match",
            "Bowling Triggers": "Inn 2 Defending Overs 15–20  OR  Inn 2 & RRR ≤ 9.5  OR  Partnership ≥ 25  OR  Knock-out match",
            "Analytical Purpose": "Permissive envelope capturing early pressure onset & escalating chase pressure."
        },
        {
            "Threshold": "T2 (Standard)",
            "Batting Triggers": "Inn 2 & RRR > 9.0  OR  Wickets in hand ≤ 3  OR  Overs 16–20  OR  Knock-out match",
            "Bowling Triggers": "Inn 2 Defending Overs 16–20  OR  Inn 2 & RRR ≤ 9.0  OR  Partnership ≥ 30  OR  Knock-out match",
            "Analytical Purpose": "Primary production baseline balancing high leverage with robust sample sizes."
        },
        {
            "Threshold": "T3 (Extreme)",
            "Batting Triggers": "Inn 2 & RRR > 10.0  OR  Wickets in hand ≤ 2  OR  Overs 17–20  OR  Knock-out match",
            "Bowling Triggers": "Inn 2 Defending Overs 17–20  OR  Inn 2 & RRR ≤ 8.5  OR  Partnership ≥ 35  OR  Knock-out match",
            "Analytical Purpose": "Peak clutch crunch isolating final 3 overs and do-or-die crisis states."
        }
    ])
    st.dataframe(th_matrix, width="stretch", hide_index=True)

    st.markdown("<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 25px 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 5. Sample Size Rules & Cohort Qualification
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>5. Sample-Size Eligibility & Watch-List Counts</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>Strict volume gates prevent small-sample distortions while tracking emerging talents on the Watch List:</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='player-card' style='height: 100%;'>
            <span class='badge-pink'>BATTING VOLUME RULES</span>
            <h4 style='color: #FFFFFF; margin-top: 8px; font-weight: 800;'>Eligibility Requirements</h4>
            <ul style='color: #FFFFFF; font-size: 13.5px; line-height: 1.8;'>
                <li><b>≥ 200 Pressure Balls Faced</b></li>
                <li><b>≥ 200 Baseline Normal Balls Faced</b></li>
                <li><b>≥ 5 Pressure Innings Batted</b></li>
            </ul>
            <hr style='border-color: rgba(255,255,255,0.12); margin: 10px 0;'>
            <div style='font-size: 12.5px; color: #FFD1E8; line-height: 1.6;'>
                • <b>T1 Cohort</b>: 106 Qualified | 759 on Watch List<br>
                • <b>T2 Cohort</b>: 98 Qualified | 748 on Watch List<br>
                • <b>T3 Cohort</b>: 84 Qualified | 739 on Watch List
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='player-card' style='height: 100%;'>
            <span class='badge-navy'>BOWLING VOLUME RULES</span>
            <h4 style='color: #FFFFFF; margin-top: 8px; font-weight: 800;'>Eligibility Requirements</h4>
            <ul style='color: #FFFFFF; font-size: 13.5px; line-height: 1.8;'>
                <li><b>≥ 200 Pressure Legal Balls Bowled</b></li>
                <li><b>≥ 150 Baseline Normal Balls Bowled</b></li>
                <li><b>≥ 6 Pressure Spells Bowled</b></li>
                <li><b>≥ 2 Thresholds Qualified (T1, T2, T3)</b></li>
                <li><b>Hard Filter: Pressure Economy ≤ League Average</b></li>
            </ul>
            <hr style='border-color: rgba(255,255,255,0.12); margin: 10px 0;'>
            <div style='font-size: 12.5px; color: #FFD1E8; line-height: 1.6;'>
                • <b>T1 Cohort</b>: 147 Qualified | 483 on Watch List<br>
                • <b>T2 Cohort</b>: 140 Qualified | 483 on Watch List<br>
                • <b>T3 Cohort</b>: 120 Qualified | 493 on Watch List
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 25px 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 6. Shrinkage & T20I Opponent Strength Weights
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>6. Bayesian Shrinkage (k=100) & T20I Opponent Weighting</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>Regulating small-sample variance and accounting for quality-of-competition differences:</p>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background: rgba(31, 42, 107, 0.45); padding: 18px; border-radius: 12px; border-left: 4px solid #EA1A85; font-size: 13.5px; color: #FFFFFF; line-height: 1.8;'>
        <b style='color: #FFD700;'>1. Bayesian Shrinkage (k = 100 balls)</b>:<br>
        Strike rates and expectations are shrunken toward the specific match-phase and competition league average. A batter with 200 balls receives 67% empirical weight and 33% prior weight; a batter with 800 balls receives 89% empirical weight. This completely eliminates one-match flukes from topping the table.<br><br>
        <b style='color: #FFD700;'>2. Opponent Strength Weighting in T20Is</b>:<br>
        Deliveries faced against <b>Tier 1 Opponents</b> (Full Member ICC nations: India, Australia, England, South Africa, New Zealand, West Indies, Pakistan, Sri Lanka, Afghanistan, Bangladesh, and all IPL Franchises) are weighted at <b>1.0×</b>.<br>
        Deliveries faced against <b>Tier 2 Opponents</b> (Associate & Emerging nations) receive a discounted weight of <b>0.75×</b>.<br><br>
        <b style='color: #FFD1E8;'>Empirical Distribution in T20I Dataset:</b><br>
        • <b>Tier 1 Opponents</b>: <b style='color: #FFFFFF;'>84,149 balls (77.11%)</b><br>
        • <b>Tier 2 Opponents</b>: <b style='color: #FFFFFF;'>24,981 balls (22.89%)</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 25px 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 7. Robustness Validation Across Thresholds & IPL-Only
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>7. Robustness Check: Threshold Consistency & IPL-Only Overlap</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>How reliably do our Top 10 performers maintain elite status across sensitivity variations and IPL-only data?</p>", unsafe_allow_html=True)

    rob_col1, rob_col2 = st.columns(2)
    with rob_col1:
        st.markdown("<h4 style='color: #FFD700;'>Batters Robustness Audit</h4>", unsafe_allow_html=True)
        bat_rob_df = pd.DataFrame([
            {"Rank": row['rank'], "Player": row['player'], "Qual Thresholds": row['qualified_thresholds'], "Top 10 Finishes": row['thresholds_in_top10'], "IPL-Only Top 10": "✅ Yes (#1)" if row['player'] == "Vaibhav Sooryavanshi" else ("✅ Yes" if row['player'] in ["Shreyas Iyer", "Liam Livingstone", "Ryan Rickelton", "Naman Dhir"] else "No (T20I Heavy)")}
            for _, row in batters.iterrows()
        ])
        st.dataframe(bat_rob_df, width="stretch", hide_index=True)
        st.caption("5 of 10 batters directly overlap in the IPL-only Top 10. 8/10 qualified in all 3 thresholds.")

    with rob_col2:
        st.markdown("<h4 style='color: #FFD700;'>Bowlers Robustness Audit</h4>", unsafe_allow_html=True)
        bowl_rob_df = pd.DataFrame([
            {"Rank": row['rank'], "Player": row['player'], "Qual Thresholds": row['qualified_thresholds'], "Top 10 Finishes": row['thresholds_in_top10'], "IPL-Only Top 10": "✅ Yes (#2)" if row['player'] == "Josh Hazlewood" else ("✅ Yes (#1)" if row['player'] == "Prasidh Krishna" else ("✅ Yes (#3)" if row['player'] == "Noor Ahmad" else "No (Intl Elite)"))}
            for _, row in bowlers.iterrows()
        ])
        st.dataframe(bowl_rob_df, width="stretch", hide_index=True)
        st.caption("All 10 bowlers qualified in 3/3 thresholds. 3 overlap with the IPL-only top 10; others are world-class international frontline spinners.")

    st.markdown("<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 25px 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 8. Step-by-Step Worked Examples
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>8. Step-by-Step Worked Mathematical Examples</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD1E8; font-size: 14px;'>Trace the exact calculation from raw ball-by-ball deliveries to final rating:</p>", unsafe_allow_html=True)

    w1, w2 = st.columns(2)
    with w1:
        st.markdown("""
        <div class='player-card rank-1'>
            <span class='badge-pink'>BATTER WORKED EXAMPLE</span>
            <h3 style='color: #FFFFFF; margin: 6px 0 2px 0; font-weight: 800;'>Tim David (Rank #3)</h3>
            <p style='color: #FFD700; font-weight: 700; font-size: 13px; margin: 0;'>Australia / MI • Middle-Order Finisher</p>
            <hr style='border-color: rgba(255,255,255,0.12); margin: 10px 0;'>
            <div style='font-size: 12.5px; color: #FFFFFF; line-height: 1.8;'>
                <b style='color: #FFD700;'>Step 1: Raw Volume & Runs</b><br>
                • Pressure Balls Faced: <b>795 balls</b> (1,524 runs across 76 innings)<br>
                • Baseline Normal Balls: <b>431 balls</b> (652 runs)<br>
                • Match Types: 647 IPL balls | 579 T20I balls<br><br>
                <b style='color: #FFD700;'>Step 2: Strike Rate Calculation</b><br>
                • Raw Pressure SR: (1,524 / 795) × 100 = <b>191.71</b><br>
                • Baseline Normal SR: (652 / 431) × 100 = <b>151.29</b><br><br>
                <b style='color: #FFD700;'>Step 3: Component (a) - Own Baseline Delta</b><br>
                • Raw Delta: 191.71 - 151.29 = +40.42<br>
                • Capped Delta (max +35.0): <b>+35.00</b><br>
                • <code>Score A</code> = 100.0 + 35.00 = <b>135.00</b><br><br>
                <b style='color: #FFD700;'>Step 4: Component (b) - League Benchmark & Shrinkage</b><br>
                • Phase Split: 573 Death, 210 Middle, 12 Powerplay balls<br>
                • Weighted Opponent Balls: 786.5 balls (w_runs: 1,507.75)<br>
                • League Expected SR: <b>155.90</b><br>
                • Shrunk SR (k=100): (786.5 × 191.71 + 100 × 155.90) / (786.5 + 100) = <b>187.67</b><br>
                • <code>Score B</code> = (187.67 / 155.90) × 100 = <b>120.38</b><br><br>
                <b style='color: #FFD700;'>Step 5: Final Pressure Rating</b><br>
                • <code>Rating</code> = 0.50 × 135.00 + 0.50 × 120.38 = <b style='color: #EA1A85; font-size: 16px;'>127.7</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with w2:
        st.markdown("""
        <div class='player-card rank-2'>
            <span class='badge-navy'>BOWLER WORKED EXAMPLE</span>
            <h3 style='color: #FFFFFF; margin: 6px 0 2px 0; font-weight: 800;'>Allah Ghazanfar (Rank #1)</h3>
            <p style='color: #FFD700; font-weight: 700; font-size: 13px; margin: 0;'>Afghanistan / MI • Mystery Spinner</p>
            <hr style='border-color: rgba(255,255,255,0.12); margin: 10px 0;'>
            <div style='font-size: 12.5px; color: #FFFFFF; line-height: 1.8;'>
                <b style='color: #FFD700;'>Step 1: Raw Volume & Economy</b><br>
                • Pressure Legal Balls: <b>266 balls</b> (326 runs, 18 wkts, 127 dots in 20 spells)<br>
                • Baseline Legal Balls: <b>195 balls</b> (311 runs)<br>
                • Match Types: 233 IPL balls | 228 T20I balls<br><br>
                <b style='color: #FFD700;'>Step 2: Rates & League Benchmark</b><br>
                • Pressure Economy: 326 / (266 / 6) = <b>7.36 rpo</b><br>
                • Baseline Normal Economy: 311 / (195 / 6) = <b>9.57 rpo</b><br>
                • Tightening Delta: 9.57 - 7.36 = <b>+2.21 rpo</b><br>
                • League Expected Economy: <b>8.84 rpo</b><br>
                • Hard Filter Check: 7.36 ≤ 8.84? <b style='color: #10B981;'>PASS</b><br><br>
                <b style='color: #FFD700;'>Step 3: Component Scores</b><br>
                • <code>Economy Score (55%)</code>: (2.0 - 7.36 / 8.84) × 100 = <b>116.74</b><br>
                • <code>Wickets per Ball Score (25%)</code>: (0.0657 / 0.0573) × 100 = <b>114.66</b><br>
                • <code>Dot Ball % Score (20%)</code>: (47.74% / 38.50%) × 100 = <b>124.00</b><br><br>
                <b style='color: #FFD700;'>Step 4: Final Pressure Rating</b><br>
                • <code>Rating</code> = 0.55 × 116.74 + 0.25 × 114.66 + 0.20 × 124.00<br>
                • <code>Rating</code> = 64.21 + 28.67 + 24.80 = <b style='color: #EA1A85; font-size: 16px;'>118.3</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(234, 26, 133, 0.3); margin: 25px 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 9. Analytical Limitations Box
    # ---------------------------------------------------------
    st.markdown("<h3 style='color: #FFD700; font-weight: 800;'>9. Analytical Limitations & Caveats</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(239, 68, 68, 0.1); border: 1.5px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 20px; color: #FFFFFF; font-size: 13.5px; line-height: 1.8;'>
        <b style='color: #EF4444; font-size: 15px;'>CRITICAL DATA SCIENCE CAVEATS FOR SCOUTING & AUCTION TEAMS:</b>
        <ol style='margin-top: 10px; margin-bottom: 0; color: #FFFFFF;'>
            <li><b>Analyst Heuristics in Threshold Rules</b>: Operational pressure cutoffs (e.g., RRR > 9.0, overs 16–20) reflect domain consensus but remain analytical thresholds. Robust multi-threshold averaging (T1, T2, T3) was specifically built to counteract boundary sensitivity.</li>
            <li><b>Absence of Fielding & Chance Data</b>: Standard ball-by-ball records do not track dropped catches, misfields, run-out chances missed, or bowler-induced edges that fell safely. A bowler with low economy might have conceded chances that were grassed.</li>
            <li><b>T20I-Only & Asymmetric Schedules</b>: Certain frontline international bowlers (e.g. Sufiyan Muqeem, Mohammad Nawaz, Abrar Ahmed) do not participate in the IPL. These players have no IPL deliveries in the supplied dataset. Their ratings reflect elite T20I execution, discounted for associate fixtures.</li>
            <li><b>Youth Sample Disparity (Vaibhav Sooryavanshi)</b>: Vaibhav Sooryavanshi demonstrates highest pressure strike rate among ranked batters (243.28 pressure SR). However, his sample (251 pressure balls) is smaller than veterans like Tim David (795 pressure balls). In T3 extreme crunch, he narrowly missed the 200-ball threshold (qualifying in 2/3 thresholds).</li>
            <li><b>Exclusion of Indian Domestic Tournaments</b>: The dataset contains IPL and T20 International fixtures only. Domestic tournaments such as the Syed Mushtaq Ali Trophy (SMAT) and Vijay Hazare Trophy are not recorded, which would provide additional sample depth for emerging domestic stars.</li>
            <li><b>Delivery Volume & Thresholds</b>: A large share of all deliveries (45.5%) meets at least one pressure condition, so the three-threshold test is used to separate moderate from extreme pressure.</li>
            <li><b>Pipeline Verification</b>: Pressure labels and ratings were computed by one pipeline; ball counts were cross-checked against the raw ball_by_ball file.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
