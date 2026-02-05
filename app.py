"""
ELBOW ZONE™ | STRATEGIC BEHAVIORAL INVESTMENT TERMINAL
World-Class Presentation UI — Maximum Readability

CONFIDENTIAL: Russell Barnett © 2026. The Elbow Interference Theory™.
"""

# Suppress all warnings (Python 3.9 + Google SDK + urllib3)
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, List, Any
import json

from config import TOOLTIPS, tip, DEFAULT_CATEGORY

# Import priors module for behavioral adjustments
try:
    from priors import (
        apply_priors_dict, ScoringContext, get_default_context,
        calculate_repeat_momentum, generate_assumptions_section,
        RawScores, AdjustedScores
    )
    PRIORS_AVAILABLE = True
except ImportError:
    PRIORS_AVAILABLE = False
    print("[PRIORS] Module not available - using raw scores only")

# Import hard_data module for deterministic constants and guardrails
try:
    from hard_data import get_hard_data, get_external_support_snippets
    HARD_DATA = get_hard_data()
    HARD_DATA_AVAILABLE = True
    print("[HARD_DATA] Module loaded successfully")
except ImportError:
    HARD_DATA = None
    HARD_DATA_AVAILABLE = False
    print("[HARD_DATA] Module not available")

from ai_services import (
    get_gemini_model,
    analyze_brand_with_ai,
    generate_strategic_synthesis,
    generate_rule_based_memo,
    GEMINI_AVAILABLE,
)
from brands import (
    Archetype,
    ARCHETYPES,
    BRAND_DATABASE,
    KNOWN_BRANDS,
    normalize_brand_name,
    hunt_brand,
)
from scoring import calculate_s_score, validate_rationale

# ═══════════════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Elbow Interference Evaluator™",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════════════
# MASSIVE FONT THEME
# ═══════════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* DEEP VIOLET GLASSMORPHISM - WCAG AA ACCESSIBLE                                  */
    /* All text: Pure White (#FFFFFF) or Pale Lavender (#E9D5FF)                       */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    /* GLOBAL BACKGROUND - Deep Violet Gradient */
    .stApp {
        background: linear-gradient(135deg, #2e1065 0%, #4c1d95 100%) !important;
        background-attachment: fixed !important;
    }
    .main {
        background: transparent !important;
    }
    
    /* Watermark - very subtle */
    .main::before {
        content: 'ELBOW INTERFERENCE™';
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%) rotate(-25deg);
        font-size: 8rem; font-weight: 900;
        color: rgba(255, 255, 255, 0.02);
        pointer-events: none; z-index: 0;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* GLOBAL TEXT RESET - FORCE HIGH CONTRAST                                         */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    /* EVERYTHING defaults to white */
    *, *::before, *::after {
        color: #FFFFFF;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* SIDEBAR - Dark with WHITE text                                                  */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    section[data-testid="stSidebar"] { 
        background: rgba(15, 10, 35, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(12px) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] strong {
        color: #FFFFFF !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #E9D5FF !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* TYPOGRAPHY - WCAG AA Compliant                                                  */
    /* Primary: #FFFFFF | Secondary: #E9D5FF | NEVER use grays                         */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    /* Headers - Bold White with text shadow */
    h1 { 
        font-size: 3.5rem !important; 
        font-weight: 900 !important; 
        color: #FFFFFF !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    h2 { 
        font-size: 2.5rem !important; 
        font-weight: 800 !important; 
        color: #FFFFFF !important; 
        margin-top: 2rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    h3 { 
        font-size: 1.8rem !important; 
        font-weight: 700 !important; 
        color: #FFFFFF !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    h4, h5 { 
        font-size: 1.4rem !important; 
        font-weight: 700 !important; 
        color: #E9D5FF !important;
    }
    
    /* Body text - Pale Lavender for readability */
    .main p, .main li, .main span { 
        font-size: 1.2rem !important; 
        line-height: 1.8 !important; 
        font-weight: 500 !important;
        color: #E9D5FF !important;
    }
    
    /* Labels - Pure White */
    .main label { 
        font-size: 1.2rem !important; 
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    
    .main .stMarkdown p { color: #E9D5FF !important; }
    .main .stMarkdown strong { color: #FFFFFF !important; font-weight: 800 !important; }
    .main .stMarkdown li { color: #E9D5FF !important; }
    
    /* Captions - Pale Lavender (NOT muted gray) */
    small, .stCaption, [data-testid="stCaptionContainer"] { 
        font-size: 1rem !important; 
        font-weight: 500 !important; 
        color: #E9D5FF !important; 
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* GLASSMORPHISM CARDS - Darker backgrounds for contrast                           */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    /* Expander */
    [data-testid="stExpander"] {
        background: rgba(0, 0, 0, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary *,
    .streamlit-expanderHeader,
    .streamlit-expanderHeader * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] *,
    .streamlit-expanderContent,
    .streamlit-expanderContent * { 
        color: #E9D5FF !important;
    }
    .streamlit-expanderContent strong { color: #FFFFFF !important; }
    
    /* Metrics - Glass Card */
    div[data-testid="stMetric"] { 
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important; 
        padding: 24px !important; 
    }
    div[data-testid="stMetric"] label { 
        font-size: 1.1rem !important; 
        font-weight: 700 !important; 
        text-transform: uppercase !important; 
        letter-spacing: 0.1em !important; 
        color: #E9D5FF !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { 
        font-family: 'JetBrains Mono', monospace !important; 
        font-size: 3rem !important; 
        font-weight: 800 !important; 
        color: #10b981 !important;
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] { 
        font-size: 1.2rem !important; 
        font-weight: 700 !important;
        color: #ec4899 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* INPUTS - DARK backgrounds (bg-black/30), WHITE text, white/40 placeholders      */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    /* Text Inputs */
    .stTextInput label { 
        font-size: 1.3rem !important; 
        font-weight: 700 !important; 
        color: #FFFFFF !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    .stTextInput input { 
        font-size: 1.2rem !important; 
        padding: 16px 20px !important; 
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
    }
    .stTextInput input::placeholder { 
        color: rgba(255, 255, 255, 0.4) !important;
        opacity: 1 !important;
    }
    .stTextInput input:focus { 
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.3) !important;
        outline: none !important;
    }
    
    /* Number Inputs */
    .stNumberInput label { 
        font-size: 1.1rem !important; 
        font-weight: 700 !important; 
        color: #FFFFFF !important;
    }
    .stNumberInput > div { 
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    .stNumberInput input { 
        font-size: 1.5rem !important; 
        font-weight: 800 !important;
        padding: 8px 4px !important; 
        text-align: center !important;
        width: 60px !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 8px !important;
        background: rgba(0, 0, 0, 0.4) !important;
        color: #FFFFFF !important;
    }
    .stNumberInput button {
        font-size: 1.1rem !important;
        min-width: 32px !important;
        height: 32px !important;
        background: #10b981 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
        margin: 0 4px !important;
    }
    .stNumberInput button:hover { background: #059669 !important; }
    .stNumberInput button svg { stroke: #FFFFFF !important; fill: #FFFFFF !important; }
    .stNumberInput button * { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; }
    
    /* Text Areas */
    .stTextArea label { 
        font-size: 1.2rem !important; 
        font-weight: 700 !important; 
        color: #FFFFFF !important;
    }
    .stTextArea textarea { 
        font-size: 1.1rem !important; 
        padding: 16px !important; 
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important; 
        color: #FFFFFF !important;
        min-height: 120px !important; 
    }
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Selectbox */
    .stSelectbox label { 
        font-size: 1.2rem !important; 
        font-weight: 700 !important; 
        color: #FFFFFF !important; 
    }
    .stSelectbox > div > div { 
        background: rgba(0, 0, 0, 0.4) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        min-height: 48px !important;
    }
    .stSelectbox [data-baseweb="select"] { background: transparent !important; }
    .stSelectbox [data-baseweb="select"] * { color: #FFFFFF !important; }
    .stSelectbox span, .stSelectbox div { color: #FFFFFF !important; }
    
    /* Dropdown menu - DARK background */
    div[data-baseweb="popover"], div[data-baseweb="popover"] * { 
        background: rgba(15, 10, 35, 0.98) !important; 
        color: #FFFFFF !important;
        backdrop-filter: blur(12px) !important;
    }
    div[data-baseweb="popover"] li { color: #FFFFFF !important; }
    div[data-baseweb="popover"] li:hover { background: rgba(16, 185, 129, 0.4) !important; }
    div[data-baseweb="menu"], div[data-baseweb="menu"] * { 
        background: rgba(15, 10, 35, 0.98) !important; 
        color: #FFFFFF !important;
    }
    [data-baseweb="list"], [data-baseweb="list"] * { 
        background: rgba(15, 10, 35, 0.98) !important; 
        color: #FFFFFF !important;
    }
    [data-baseweb="list-item"], [data-baseweb="list-item"] * { 
        background: transparent !important; 
        color: #FFFFFF !important;
    }
    [data-baseweb="list-item"]:hover { background: rgba(16, 185, 129, 0.4) !important; }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* ALERTS - High contrast text                                                     */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    .stAlert { 
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
    }
    .stAlert * { color: #FFFFFF !important; }
    .stAlert p { color: #FFFFFF !important; font-weight: 600 !important; }
    
    /* Success - Mint */
    [data-testid="stAlert"]:has(svg[data-testid="stNotificationContentSuccess"]) {
        background: rgba(16, 185, 129, 0.2) !important;
        border-left: 4px solid #10b981 !important;
    }
    
    /* Error */
    [data-testid="stAlert"]:has(svg[data-testid="stNotificationContentError"]) {
        background: rgba(239, 68, 68, 0.2) !important;
        border-left: 4px solid #ef4444 !important;
    }
    
    /* Info */
    [data-testid="stAlert"]:has(svg[data-testid="stNotificationContentInfo"]) {
        background: rgba(59, 130, 246, 0.2) !important;
        border-left: 4px solid #3b82f6 !important;
    }
    
    /* Warning */
    [data-testid="stAlert"]:has(svg[data-testid="stNotificationContentWarning"]) {
        background: rgba(236, 72, 153, 0.2) !important;
        border-left: 4px solid #ec4899 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* BUTTONS - Bright accents with white text                                        */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    .stButton button { 
        font-size: 1.1rem !important; 
        font-weight: 700 !important; 
        padding: 14px 24px !important; 
        border-radius: 12px !important;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        transition: all 0.2s ease !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* OTHER COMPONENTS                                                                */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    /* Dividers */
    hr { 
        margin: 24px 0 !important; 
        border: none !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* DataFrames */
    .stDataFrame { 
        background: rgba(0, 0, 0, 0.2) !important;
        border-radius: 12px !important;
    }
    .stDataFrame * { color: #FFFFFF !important; }
    
    /* Code blocks */
    code { 
        font-size: 1.1rem !important; 
        font-weight: 600 !important; 
        background: rgba(0, 0, 0, 0.3) !important; 
        color: #10b981 !important;
        padding: 4px 10px !important; 
        border-radius: 6px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* FILE UPLOADER - Glass Card Style (NO WHITE BACKGROUNDS)                         */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] > div,
    [data-testid="stFileUploader"] > div > div,
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploadDropzone"] > div {
        background: rgba(0, 0, 0, 0.4) !important;
        background-color: rgba(0, 0, 0, 0.4) !important;
        border-radius: 12px !important;
    }
    
    /* The actual drop zone */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(15, 10, 35, 0.6) !important;
        border: 2px dashed rgba(255, 255, 255, 0.25) !important;
        border-radius: 12px !important;
        padding: 24px !important;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #10b981 !important;
        background: rgba(16, 185, 129, 0.1) !important;
    }
    
    /* All text in file uploader - WHITE */
    [data-testid="stFileUploader"] *,
    [data-testid="stFileUploadDropzone"] * { 
        color: #FFFFFF !important; 
        background-color: transparent !important;
    }
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] small { 
        color: #E9D5FF !important; 
    }
    
    /* Browse button */
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploadDropzone"] button { 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background: #10b981 !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    /* CHARTS - Transparent Background, White Labels                                   */
    /* ═══════════════════════════════════════════════════════════════════════════════ */
    
    /* Remove white backgrounds from chart containers */
    [data-testid="stVegaLiteChart"],
    [data-testid="stVegaLiteChart"] > div,
    [data-testid="stArrowVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] > div,
    .vega-embed,
    .vega-embed > div,
    .vega-embed canvas,
    .marks {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Chart wrapper - glass card */
    [data-testid="stVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 16px !important;
    }
    
    /* Force Vega-Lite text to white */
    .vega-embed text,
    .vega-embed .role-axis-label,
    .vega-embed .role-legend-label,
    .vega-embed .role-title,
    .vega-embed .mark-text text {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }
    
    /* Axis lines and grid - light */
    .vega-embed .role-axis line,
    .vega-embed .role-axis path,
    .vega-embed line.role-grid {
        stroke: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Legend text */
    .vega-embed .role-legend text {
        fill: #E9D5FF !important;
    }
    
    /* Icons - White or Mint */
    svg { color: #FFFFFF !important; }
    svg:not(.vega-embed svg) { stroke: #FFFFFF !important; }
    .stAlert svg { color: #10b981 !important; stroke: #10b981 !important; }
    
    /* LOCKED STATE - Alert Red */
    .score-locked {
        background: rgba(239, 68, 68, 0.2) !important;
        border: 2px solid #ef4444 !important;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        50% { opacity: 0.8; box-shadow: 0 0 20px 5px rgba(239, 68, 68, 0.2); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
<script>document.addEventListener('contextmenu', e => e.preventDefault());</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════════════

if "brand1_archetype" not in st.session_state: st.session_state.brand1_archetype = None
if "brand2_archetype" not in st.session_state: st.session_state.brand2_archetype = None
if "rationale_b1" not in st.session_state: st.session_state.rationale_b1 = ""
if "rationale_b2" not in st.session_state: st.session_state.rationale_b2 = ""
if "ai_scores_b1" not in st.session_state: st.session_state.ai_scores_b1 = None
if "ai_scores_b2" not in st.session_state: st.session_state.ai_scores_b2 = None
if "last_brand1" not in st.session_state: st.session_state.last_brand1 = ""
if "last_brand2" not in st.session_state: st.session_state.last_brand2 = ""

# Priors context state (behavioral adjustments)
if "use_priors" not in st.session_state: st.session_state.use_priors = True
if "cohort" not in st.session_state: st.session_state.cohort = "mixed"
if "occasion" not in st.session_state: st.session_state.occasion = "evening"
if "macro_stress" not in st.session_state: st.session_state.macro_stress = True
if "promo_frequency_b1" not in st.session_state: st.session_state.promo_frequency_b1 = 0.0
if "promo_depth_b1" not in st.session_state: st.session_state.promo_depth_b1 = 0.0
if "promo_frequency_b2" not in st.session_state: st.session_state.promo_frequency_b2 = 0.0
if "promo_depth_b2" not in st.session_state: st.session_state.promo_depth_b2 = 0.0
if "ups_pw_13_b1" not in st.session_state: st.session_state.ups_pw_13_b1 = None
if "ups_pw_26_b1" not in st.session_state: st.session_state.ups_pw_26_b1 = None
if "ups_pw_13_b2" not in st.session_state: st.session_state.ups_pw_13_b2 = None
if "ups_pw_26_b2" not in st.session_state: st.session_state.ups_pw_26_b2 = None
if "adjustments_log_b1" not in st.session_state: st.session_state.adjustments_log_b1 = []
if "adjustments_log_b2" not in st.session_state: st.session_state.adjustments_log_b2 = []


def _infer_advanced_from_dataframe(df: pd.DataFrame) -> Tuple[Dict[str, Any], List[str]]:
    """
    Infer sidebar Advanced values (promo frequency/depth, velocity) from uploaded CSV/Excel.
    Returns (updates_dict, messages) where updates_dict has keys like promo_frequency_b1 (0-1),
    and messages are short strings for the UI.
    """
    updates = {}
    messages = []
    if df is None or df.empty:
        return updates, messages
    cols_lower = {str(c).lower(): c for c in df.columns}
    # Promo frequency: % weeks on deal, 0-1 scale (or 0-100 → /100). Broad patterns for varied docs.
    for pattern in ["promo freq", "promo frequency", "deal frequency", "weeks on deal", "% weeks", "promo_weeks", "deal_weeks", "tpr freq", "feature rate", "promo rate", "deal rate", "freq", "frequency", "weeks deal", "deal %", "promo %", "feature", "tpr"]:
        for key, col in cols_lower.items():
            if pattern in key:
                try:
                    s = pd.to_numeric(df[col].dropna(), errors="coerce")
                    s = s[s.notna()]
                    if len(s) == 0:
                        break
                    v = float(s.mean())
                    if v > 1:
                        v = v / 100.0
                    v = max(0.0, min(1.0, v))
                    updates["promo_frequency_b1"] = v
                    updates["promo_frequency_b2"] = v
                    messages.append(f"Promo Frequency (B1 & B2): {v:.0%} from column «{col}»")
                except Exception:
                    pass
                break
        if "promo_frequency_b1" in updates:
            break
    # Promo depth: % off, 0-1 scale. Broad patterns for varied docs.
    for pattern in ["promo depth", "deal depth", "% off", "discount", "avg discount", "average discount", "depth", "tpr depth", "off shelf", "discount depth", "off", "disc", "reduction", "lift", "deal off"]:
        for key, col in cols_lower.items():
            if pattern in key:
                try:
                    s = pd.to_numeric(df[col].dropna(), errors="coerce")
                    s = s[s.notna()]
                    if len(s) == 0:
                        break
                    v = float(s.mean())
                    if v > 1:
                        v = v / 100.0
                    v = max(0.0, min(1.0, v))
                    updates["promo_depth_b1"] = v
                    updates["promo_depth_b2"] = v
                    messages.append(f"Promo Depth (B1 & B2): {v:.0%} from column «{col}»")
                except Exception:
                    pass
                break
        if "promo_depth_b1" in updates:
            break
    # Velocity 13w / 26w: one column each for 13-week and 26-week (apply to both B1 and B2)
    for pattern_13 in ["13", "13wk", "13 wk", "latest", "current"]:
        for pattern_u in ["ups", "units", "velocity", "sales", "volume"]:
            for key, col in cols_lower.items():
                if pattern_13 in key and pattern_u in key:
                    try:
                        s = pd.to_numeric(df[col].dropna(), errors="coerce").dropna()
                        if len(s) > 0:
                            v = float(s.mean())
                            if v > 0:
                                updates["ups_pw_13_b1"] = v
                                updates["ups_pw_13_b2"] = v
                                messages.append(f"Velocity 13w (B1 & B2): {v:.1f} from «{col}»")
                                break
                    except Exception:
                        pass
            if "ups_pw_13_b1" in updates:
                break
        if "ups_pw_13_b1" in updates:
            break
    for pattern_26 in ["26", "26wk", "26 wk", "prior", "base", "52"]:
        for pattern_u in ["ups", "units", "velocity", "sales", "volume"]:
            for key, col in cols_lower.items():
                if pattern_26 in key and pattern_u in key:
                    try:
                        s = pd.to_numeric(df[col].dropna(), errors="coerce").dropna()
                        if len(s) > 0:
                            v = float(s.mean())
                            if v > 0:
                                updates["ups_pw_26_b1"] = v
                                updates["ups_pw_26_b2"] = v
                                messages.append(f"Velocity 26w (B1 & B2): {v:.1f} from «{col}»")
                                break
                    except Exception:
                        pass
            if "ups_pw_26_b1" in updates:
                break
        if "ups_pw_26_b1" in updates:
            break
    return updates, messages


def _value_from_column(df: pd.DataFrame, col_name: str, kind: str) -> Optional[float]:
    """Compute a single value from a dataframe column for Advanced fields. kind: 'promo_freq'|'promo_depth'|'velocity'."""
    if df is None or df.empty or not col_name or col_name not in df.columns:
        return None
    try:
        s = pd.to_numeric(df[col_name].dropna(), errors="coerce").dropna()
        if len(s) == 0:
            return None
        v = float(s.mean())
        if kind == "promo_freq" or kind == "promo_depth":
            if v > 1:
                v = v / 100.0
            return max(0.0, min(1.0, v))
        return v if v > 0 else None
    except Exception:
        return None


def _build_upload_context_for_report() -> str:
    """
    Build full context from any uploaded file (sales data or brand/consumer documents)
    for the final Investor Memo so the report explicitly uses this material.
    """
    parts = []
    _fname = st.session_state.get("_last_uploaded_file_name", "")
    _df = st.session_state.get("uploaded_data")
    _txt = st.session_state.get("uploaded_text")
    if not _fname and _df is None and not _txt:
        return ""
    if _fname:
        parts.append(f"Uploaded file: {_fname}")
    # Sales/tabular data: include structure and sample rows so the report can reference real numbers
    if _df is not None and hasattr(_df, "shape") and not _df.empty:
        parts.append(f"Sales/tabular data: {_df.shape[0]} rows × {_df.shape[1]} columns.")
        parts.append(f"Columns: {list(_df.columns)}")
        try:
            sample = _df.head(20)
            if len(_df.columns) > 15:
                sample = sample.iloc[:, :15]
            parts.append("Sample rows (use these figures where relevant in the report):")
            parts.append(sample.to_string(max_colwidth=35))
        except Exception:
            # Fallback: avoid huge to_dict() for wide dataframes; use shape + column names only
            parts.append(f"Sample omitted (table shape {_df.shape[0]}×{_df.shape[1]}; columns listed above).")
    # Documents (brand/consumer): include substantial extracted text so the report can cite context
    if _txt and isinstance(_txt, str) and _txt.strip():
        cap = 7000
        excerpt = _txt.strip()[:cap] + ("..." if len(_txt) > cap else "")
        parts.append("Document content (brand/consumer context — use in the report where relevant):")
        parts.append("---")
        parts.append(excerpt)
        parts.append("---")
    if not parts:
        return ""
    return "\n\n".join(parts)


# Check if Gemini is configured
_test_model = get_gemini_model()
AI_ENABLED = _test_model is not None
print(f"[STARTUP] AI_ENABLED = {AI_ENABLED}")

# ═══════════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.header("◈ Elbow Interference™")
    
    # Status indicator
    if AI_ENABLED:
        st.success("System Active")
    else:
        st.warning("Manual Mode")
    
    st.divider()
    
    # RESTART
    if st.button("🔄 Restart Analysis", width="stretch"):
        st.session_state.ai_scores_b1 = None
        st.session_state.ai_scores_b2 = None
        st.session_state.last_brand1 = ""
        st.session_state.last_brand2 = ""
        st.session_state['final_b1'] = {}
        st.session_state['final_b2'] = {}
        st.session_state.last_memo = None
        st.rerun()
    
    st.divider()
    
    # Data Upload - Multiple file types
    st.subheader("📊 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload Data", 
        type=["csv", "xlsx", "xls", "pdf", "docx", "doc", "pptx", "ppt", "txt"],
        help=tip("upload")
    )
    
    if uploaded_file:
        # On new file upload: restart analysis (clear AI cache + memo) but keep user overrides (final_b1, final_b2)
        _prev_name = st.session_state.get('_last_uploaded_file_name', '')
        if _prev_name != uploaded_file.name:
            st.session_state.ai_scores_b1 = None
            st.session_state.ai_scores_b2 = None
            st.session_state.last_brand1 = ""
            st.session_state.last_brand2 = ""
            st.session_state.last_memo = None
            st.session_state['_last_uploaded_file_name'] = uploaded_file.name
            # Do NOT clear final_b1 / final_b2 so overrides are preserved

        file_ext = uploaded_file.name.split('.')[-1].lower()
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        # Show processing status
        st.info(f"📄 **{uploaded_file.name}** ({file_size_mb:.1f} MB)")
        
        try:
            # CSV files
            if file_ext == 'csv':
                with st.spinner("⏳ Processing CSV..."):
                    df = pd.read_csv(uploaded_file)
                    st.session_state['uploaded_data'] = df
                    st.session_state['uploaded_text'] = None
                    st.session_state['file_loaded'] = True
                    # Auto-fill Advanced (sidebar) from detected promo/velocity columns
                    adv_updates, adv_messages = _infer_advanced_from_dataframe(df)
                    for k, v in adv_updates.items():
                        setattr(st.session_state, k, v)
                st.success(f"✅ **CSV loaded:** {len(df)} rows × {len(df.columns)} columns")
                if adv_messages:
                    st.caption("📌 **Advanced (auto-filled):** " + " | ".join(adv_messages))
                
                # Show column preview
                with st.expander("📋 Data Preview"):
                    try:
                        st.dataframe(df.head(10), width="stretch")
                    except Exception:
                        st.table(df.head(10))
                
                # Time series detection for CSV
                time_cols = [col for col in df.columns if any(x in col.lower() for x in ['52', '26', '13', '4', 'week', 'wk', 'latest'])]
                if time_cols:
                    selected_period = st.selectbox("Time Period", ["All Provided"] + time_cols, key="data_period")
                    st.session_state['selected_period'] = selected_period
            
            # Excel files
            elif file_ext in ['xlsx', 'xls']:
                with st.spinner("⏳ Processing Excel file... (large files may take a moment)"):
                    # Try to read with openpyxl for xlsx
                    if file_ext == 'xlsx':
                        df = pd.read_excel(uploaded_file, engine='openpyxl')
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Clean up mixed data types - convert all columns to strings for display
                    df_clean = df.copy()
                    for col in df_clean.columns:
                        df_clean[col] = df_clean[col].astype(str)
                    
                    st.session_state['uploaded_data'] = df
                    st.session_state['uploaded_text'] = None
                    st.session_state['file_loaded'] = True
                    # Auto-fill Advanced (sidebar) from detected promo/velocity columns
                    adv_updates, adv_messages = _infer_advanced_from_dataframe(df)
                    for k, v in adv_updates.items():
                        setattr(st.session_state, k, v)
                    
                st.success(f"✅ **Excel loaded:** {len(df)} rows × {len(df.columns)} columns")
                st.caption(f"Columns: {', '.join(df.columns[:5].tolist())}{'...' if len(df.columns) > 5 else ''}")
                if adv_messages:
                    st.caption("📌 **Advanced (auto-filled):** " + " | ".join(adv_messages))
                
                # Show column preview with cleaned data
                with st.expander("📋 Data Preview (first 10 rows)"):
                    try:
                        st.dataframe(df_clean.head(10), width="stretch")
                    except Exception:
                        st.table(df.head(10))
                
                # Time series detection for Excel
                time_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['52', '26', '13', '4', 'week', 'wk', 'latest'])]
                if time_cols:
                    selected_period = st.selectbox("Time Period", ["All Provided"] + time_cols, key="data_period")
                    st.session_state['selected_period'] = selected_period
            
            # PDF files
            elif file_ext == 'pdf':
                try:
                    import PyPDF2
                    with st.spinner("⏳ Extracting text from PDF..."):
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        text_content = ""
                        for page in pdf_reader.pages:
                            text_content += page.extract_text() + "\n"
                        st.session_state['uploaded_text'] = text_content
                        st.session_state['uploaded_data'] = None
                    st.success(f"✅ PDF extracted: {len(pdf_reader.pages)} pages, {len(text_content)} characters")
                    with st.expander("📋 Preview extracted text"):
                        st.text(text_content[:3000] + "..." if len(text_content) > 3000 else text_content)
                except ImportError:
                    st.error("📦 Missing library: `pip install PyPDF2`")
                except Exception as pdf_err:
                    st.error(f"PDF Error: {str(pdf_err)[:100]}")
            
            # Word documents
            elif file_ext in ['docx', 'doc']:
                try:
                    from docx import Document
                    with st.spinner("⏳ Extracting text from Word document..."):
                        doc = Document(uploaded_file)
                        text_content = "\n".join([para.text for para in doc.paragraphs])
                        st.session_state['uploaded_text'] = text_content
                        st.session_state['uploaded_data'] = None
                    st.success(f"✅ Word extracted: {len(doc.paragraphs)} paragraphs")
                    with st.expander("📋 Preview extracted text"):
                        st.text(text_content[:3000] + "..." if len(text_content) > 3000 else text_content)
                except ImportError:
                    st.error("📦 Missing library: `pip install python-docx`")
                except Exception as doc_err:
                    st.error(f"Word Error: {str(doc_err)[:100]}")
            
            # PowerPoint files
            elif file_ext in ['pptx', 'ppt']:
                try:
                    from pptx import Presentation
                    with st.spinner("⏳ Extracting text from PowerPoint..."):
                        prs = Presentation(uploaded_file)
                        text_content = ""
                        for slide in prs.slides:
                            for shape in slide.shapes:
                                if hasattr(shape, "text"):
                                    text_content += shape.text + "\n"
                        st.session_state['uploaded_text'] = text_content
                        st.session_state['uploaded_data'] = None
                    st.success(f"✅ PowerPoint extracted: {len(prs.slides)} slides")
                    with st.expander("📋 Preview extracted text"):
                        st.text(text_content[:3000] + "..." if len(text_content) > 3000 else text_content)
                except ImportError:
                    st.error("📦 Missing library: `pip install python-pptx`")
                except Exception as ppt_err:
                    st.error(f"PowerPoint Error: {str(ppt_err)[:100]}")
            
            # Plain text files
            elif file_ext == 'txt':
                with st.spinner("⏳ Loading text file..."):
                    text_content = uploaded_file.read().decode('utf-8')
                    st.session_state['uploaded_text'] = text_content
                    st.session_state['uploaded_data'] = None
                st.success(f"✅ Text loaded: {len(text_content)} characters")
                with st.expander("📋 Preview text"):
                    st.text(text_content[:3000] + "..." if len(text_content) > 3000 else text_content)
            
            else:
                st.warning(f"⚠️ Unsupported file type: {file_ext}")
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.session_state['file_loaded'] = False
            import traceback
            with st.expander("🔧 Error Details"):
                st.code(traceback.format_exc())
    
    # When we have tabular data, let user map any column to Advanced (works with any column names)
    _ud = st.session_state.get("uploaded_data")
    if _ud is not None and hasattr(_ud, "columns") and isinstance(_ud, pd.DataFrame):
        df_map = _ud
        col_options = ["— Don't map —"] + [str(c) for c in df_map.columns]
        with st.expander("🗺️ Map columns to Advanced", expanded=True):
            st.caption("Choose which column in your file is used for each Advanced field. Values are averaged and applied to both brands.")
            c_freq = st.selectbox("Promo Frequency (B1 & B2)", col_options, key="adv_map_promo_freq")
            if c_freq != "— Don't map —":
                val = _value_from_column(df_map, c_freq, "promo_freq")
                if val is not None:
                    st.session_state.promo_frequency_b1 = val
                    st.session_state.promo_frequency_b2 = val
                    st.caption(f"✓ Set to **{val:.0%}** (mean of «{c_freq}»)")
            c_depth = st.selectbox("Promo Depth (B1 & B2)", col_options, key="adv_map_promo_depth")
            if c_depth != "— Don't map —":
                val = _value_from_column(df_map, c_depth, "promo_depth")
                if val is not None:
                    st.session_state.promo_depth_b1 = val
                    st.session_state.promo_depth_b2 = val
                    st.caption(f"✓ Set to **{val:.0%}** (mean of «{c_depth}»)")
            c_13 = st.selectbox("Velocity 13w (B1 & B2)", col_options, key="adv_map_13w")
            if c_13 != "— Don't map —":
                val = _value_from_column(df_map, c_13, "velocity")
                if val is not None:
                    st.session_state.ups_pw_13_b1 = val
                    st.session_state.ups_pw_13_b2 = val
                    st.caption(f"✓ Set to **{val:.1f}** (mean of «{c_13}»)")
            c_26 = st.selectbox("Velocity 26w (B1 & B2)", col_options, key="adv_map_26w")
            if c_26 != "— Don't map —":
                val = _value_from_column(df_map, c_26, "velocity")
                if val is not None:
                    st.session_state.ups_pw_26_b1 = val
                    st.session_state.ups_pw_26_b2 = val
                    st.caption(f"✓ Set to **{val:.1f}** (mean of «{c_26}»)")
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════════════════
    # ADVANCED SETTINGS - BEHAVIORAL PRIORS
    # ═══════════════════════════════════════════════════════════════════════════════════════
    
    with st.expander("⚙️ Advanced Settings", expanded=False):
        st.markdown("**Behavioral Priors**")
        
        # Feature flag toggle
        st.session_state.use_priors = st.checkbox(
            "Apply Behavioral Priors",
            value=st.session_state.use_priors,
            help=tip("priors_toggle")
        )
        
        if st.session_state.use_priors and PRIORS_AVAILABLE:
            st.caption("Context affects scoring adjustments:")
            
            _cohort_opts = ["younger", "mixed", "older"]
            _cohort_val = getattr(st.session_state, "cohort", "mixed") or "mixed"
            _cohort_idx = _cohort_opts.index(_cohort_val) if _cohort_val in _cohort_opts else 1
            st.session_state.cohort = st.selectbox(
                "Target Cohort",
                options=_cohort_opts,
                index=_cohort_idx,
                help=tip("cohort")
            )
            _occ_opts = ["evening", "late_night", "daytime", "on_the_go"]
            _occ_val = getattr(st.session_state, "occasion", "evening") or "evening"
            _occ_idx = _occ_opts.index(_occ_val) if _occ_val in _occ_opts else 0
            st.session_state.occasion = st.selectbox(
                "Primary Occasion",
                options=_occ_opts,
                index=_occ_idx,
                help=tip("priors_occasion")
            )
            
            st.session_state.macro_stress = st.checkbox(
                "Macro Stress Active",
                value=st.session_state.macro_stress,
                help=tip("macro_stress")
            )
            
            st.divider()
            st.caption("**Promo Reliance (Brand 1)**")
            st.session_state.promo_frequency_b1 = st.slider(
                "Promo Frequency B1",
                0.0, 1.0, st.session_state.promo_frequency_b1,
                help=tip("promo_frequency")
            )
            st.session_state.promo_depth_b1 = st.slider(
                "Promo Depth B1",
                0.0, 1.0, st.session_state.promo_depth_b1,
                help=tip("promo_depth")
            )
            
            st.caption("**Promo Reliance (Brand 2)**")
            st.session_state.promo_frequency_b2 = st.slider(
                "Promo Frequency B2",
                0.0, 1.0, st.session_state.promo_frequency_b2,
                help=tip("promo_frequency")
            )
            st.session_state.promo_depth_b2 = st.slider(
                "Promo Depth B2",
                0.0, 1.0, st.session_state.promo_depth_b2,
                help=tip("promo_depth")
            )
        elif not PRIORS_AVAILABLE:
            st.warning("Priors module not loaded")
    
    st.divider()
    
    # FORMAT REFERENCE
    st.subheader("Format Reference")
    
    st.success("SINGLE-SERVE (Low Friction): Bars, bites, pouches. B=1, K=1")
    st.error("MULTI-SERVE (High Friction): Pints, tubs, bags. B=4, K=3")
    st.info("RITUAL DRINKS (Low Friction): Cans, bottles. F=5, B=1, K=1")
    
    st.divider()
    
    st.subheader("The Equation")
    st.markdown("""
<div style="background: rgba(0, 0, 0, 0.3); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.1);">
    <code style="color: #10b981 !important; font-size: 1.1rem; font-weight: 600;">S = (M×E×F) ÷ (B×K×C)</code>
</div>
    """, unsafe_allow_html=True)
    st.caption("Value Delivered ÷ Cost Extracted = Satisfaction")
    
    st.divider()
    
    st.caption("© Russell Barnett 2026")

# ═══════════════════════════════════════════════════════════════════════════════════════
# MAIN HEADER
# ═══════════════════════════════════════════════════════════════════════════════════════

st.markdown("# Elbow Interference Evaluator™")

# Compact Equation Banner - Glassmorphism
st.markdown("""
<div style="background: rgba(91, 33, 182, 0.35); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.15); padding: 24px 40px; border-radius: 16px; display: flex; align-items: center; justify-content: space-between; margin: 16px 0 24px 0;">
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.8rem; font-weight: 700; color: #10b981 !important;">S = (M × E × F) ÷ (B × K × C)</div>
    <div style="font-size: 1rem; color: #c4b5fd !important; text-align: right;">S = Satisfaction (enables persistence)</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════════════
# BRAND DISCOVERY - CLEAN: BRAND + FORMAT SEPARATE
# ═══════════════════════════════════════════════════════════════════════════════════════

st.markdown("## 🔍 Brand Discovery")

# Educational context
with st.expander("📖 How Scoring Works (Elbow Interference Theory™)", expanded=False):
    st.markdown("""
    **S = Satisfaction.** Value Delivered ÷ Cost Extracted = Satisfaction. Satisfaction enables persistence over time, but persistence is not the equation itself.

    **The Key Insight:** Products don't win by maximizing pleasure—they win by minimizing friction.
    
    **F (Familiarity)** — Does the consumer buy on autopilot?
    - **5** = Iconic legacy (Coke, Oreo, Lay's) — decades of habit
    - **3** = Growing brand or celebrity launch — still building ritual
    - **1** = Unknown/new — requires discovery
    
    **C (Cognitive)** — Does the brand make consumers THINK?
    - **1-2** = Autopilot purchase — grab without thinking
    - **3** = Some consideration — premium or health-adjacent
    - **4-5** = High cognitive load — celebrity brands, complex value props
    
    **Celebrity brands = Low F + High C** (the celebrity is familiar, but the PRODUCT is new and requires evaluation)
    
    **Format determines B and K:**
    - **Single-serve** = B=1, K=1 (package ends the occasion)
    - **Multi-serve** = B=4, K=3 (you decide when to stop)
    """)

# Default category when not set in session (used for priors context)
CATEGORY_OPTIONS = ["ice_cream", "chips", "candy", "soda", "energy", "yogurt", "bars", "other"]

# Format options - covers ALL orally consumed CPG
FORMAT_LIST = [
    "Pint / Tub (multi-serve)",
    "Bag / Pouch (multi-serve)", 
    "Box / Carton (multi-serve)",
    "Single-Serve Bar / Novelty",
    "Can / Bottle (single)",
]
FORMAT_TO_ARCHETYPE = {
    "Pint / Tub (multi-serve)": "bulk",
    "Bag / Pouch (multi-serve)": "bulk",
    "Box / Carton (multi-serve)": "bulk",
    "Single-Serve Bar / Novelty": "unitized",
    "Can / Bottle (single)": "ritual",
}

# Optional occasion context (free-text, separate from priors occasion enum)
occasion_free_text = st.text_input(
    "Occasion (optional)",
    placeholder="e.g., snacking, dessert, breakfast...",
    key="occasion_free_text",
    help=tip("occasion_free_text"),
)

st.markdown("---")

h1, h2 = st.columns(2)

with h1:
    st.markdown("### 🟢 BRAND 1 (Incumbent)")
    brand1_name = st.text_input(
        "Brand Name",
        placeholder="e.g., Serendipity, Dr. Bombay...",
        key="b1",
        help=tip("brand_name"),
    )
    brand1_format = st.selectbox(
        "Product Format", 
        options=["Pint / Tub (multi-serve)", "Bag / Pouch (multi-serve)", "Box / Carton (multi-serve)", "Single-Serve Bar / Novelty", "Can / Bottle (single)"],
        index=0, 
        key="b1_format",
        help=tip("format"),
    )
    st.caption(f"**Selected: {brand1_format}**")
    st.session_state.brand1_archetype = FORMAT_TO_ARCHETYPE[brand1_format]
    st.selectbox(
        "Category",
        options=CATEGORY_OPTIONS,
        index=0,
        key="brand1_category",
    )
    
    # Get format-based defaults
    arch1 = ARCHETYPES[FORMAT_TO_ARCHETYPE[brand1_format]]
    
    if brand1_name:
        # Normalize brand name for lookup (uses global KNOWN_BRANDS)
        brand_key = brand1_name.lower().strip()
        known_scores = KNOWN_BRANDS.get(brand_key)
        
        # Try known database first, then AI
        if known_scores:
            st.session_state.ai_scores_b1 = known_scores
            st.success(f"✓ **{brand1_name}** — F={known_scores['F']}, C={known_scores['C']}")
            with st.expander("Analysis", expanded=False):
                st.write(known_scores.get('reasoning', ''))
        elif AI_ENABLED and (st.session_state.ai_scores_b1 is None or st.session_state.last_brand1 != brand1_name):
            st.session_state.last_brand1 = brand1_name
            with st.spinner(f"Analyzing {brand1_name}..."):
                try:
                    ai_result = analyze_brand_with_ai(brand1_name)
                    if ai_result and "error" not in ai_result:
                        st.session_state.ai_scores_b1 = ai_result
                        st.success(f"✓ **{brand1_name}** — F={ai_result.get('F')}, C={ai_result.get('C')}")
                    else:
                        st.warning(f"⚠️ **{brand1_name}** not recognized — set scores manually")
                except Exception as e:
                    st.warning(f"⚠️ Set scores manually for {brand1_name}")
                    print(f"[AI ERROR B1]: {e}")
        elif st.session_state.ai_scores_b1:
            ai1 = st.session_state.ai_scores_b1
            st.success(f"✓ **{brand1_name}** — F={ai1.get('F')}, C={ai1.get('C')}")
        else:
            st.warning(f"⚠️ **{brand1_name}** — set scores manually below")
        
        ai1 = st.session_state.ai_scores_b1
        # Prefer saved overrides (final_b1) so upload restarts analysis but keeps your edits
        _fb1 = st.session_state.get('final_b1') or {}
        def _orig_b1(key: str, default):
            v = _fb1.get(key) if (_fb1 and key in _fb1) else (ai1.get(key, default) if ai1 else default)
            return max(1, min(5, int(round(v)))) if v is not None else default
        orig_M1 = _orig_b1('M', 4)
        orig_E1 = _orig_b1('E', 4)
        orig_F1 = _orig_b1('F', 3)
        orig_B1 = _orig_b1('B', arch1.B)
        orig_K1 = _orig_b1('K', arch1.K)
        orig_C1 = _orig_b1('C', 3)
        
        # === ALL 6 SCORE CONTROLS ===
        st.markdown("**ALL 6 METRICS** (adjust as needed)")
        
        # Row 1: M, E, F
        row1_c1, row1_c2, row1_c3 = st.columns(3)
        with row1_c1:
            b1_manual_M = st.number_input("M", min_value=1, max_value=5, value=orig_M1, key="b1_M", help=tip("M"))
            st.caption("Mouthfeel")
        with row1_c2:
            b1_manual_E = st.number_input("E", min_value=1, max_value=5, value=orig_E1, key="b1_E", help=tip("E"))
            st.caption("Emotion")
        with row1_c3:
            b1_manual_F = st.number_input("F ⭐", min_value=1, max_value=5, value=orig_F1, key="b1_F", help=tip("F"))
            st.caption("Familiarity")
        
        # Row 2: B, K, C
        row2_c1, row2_c2, row2_c3 = st.columns(3)
        with row2_c1:
            b1_manual_B = st.number_input("B", min_value=1, max_value=5, value=orig_B1, key="b1_B", help=tip("B"))
            st.caption("Bites")
        with row2_c2:
            b1_manual_K = st.number_input("K", min_value=1, max_value=5, value=orig_K1, key="b1_K", help=tip("K"))
            st.caption("Kinetic")
        with row2_c3:
            b1_manual_C = st.number_input("C ⭐", min_value=1, max_value=5, value=orig_C1, key="b1_C", help=tip("C"))
            st.caption("Cognitive")
        
        # Check for overrides - each needs individual justification
        b1_justifications = {}
        b1_missing_justifications = []
        
        if b1_manual_M != orig_M1:
            st.warning(f"⚠️ **M Override**: {orig_M1}→{b1_manual_M}")
            b1_justifications['M'] = st.text_input(f"Why M={b1_manual_M}?", key="b1_just_M", placeholder="Explain Mouthfeel change...", help=tip("override_rationale"))
            if len((b1_justifications.get('M') or '').strip()) < 10: b1_missing_justifications.append('M')
        
        if b1_manual_E != orig_E1:
            st.warning(f"⚠️ **E Override**: {orig_E1}→{b1_manual_E}")
            b1_justifications['E'] = st.text_input(f"Why E={b1_manual_E}?", key="b1_just_E", placeholder="Explain Emotion change...", help=tip("override_rationale"))
            if len((b1_justifications.get('E') or '').strip()) < 10: b1_missing_justifications.append('E')
        
        if b1_manual_F != orig_F1:
            st.warning(f"⚠️ **F Override**: {orig_F1}→{b1_manual_F}")
            b1_justifications['F'] = st.text_input(f"Why F={b1_manual_F}?", key="b1_just_F", placeholder="Explain Familiarity change...", help=tip("override_rationale"))
            if len((b1_justifications.get('F') or '').strip()) < 10: b1_missing_justifications.append('F')
        
        if b1_manual_B != orig_B1:
            st.warning(f"⚠️ **B Override**: {orig_B1}→{b1_manual_B}")
            b1_justifications['B'] = st.text_input(f"Why B={b1_manual_B}?", key="b1_just_B", placeholder="Explain Bites change...", help=tip("override_rationale"))
            if len((b1_justifications.get('B') or '').strip()) < 10: b1_missing_justifications.append('B')
        
        if b1_manual_K != orig_K1:
            st.warning(f"⚠️ **K Override**: {orig_K1}→{b1_manual_K}")
            b1_justifications['K'] = st.text_input(f"Why K={b1_manual_K}?", key="b1_just_K", placeholder="Explain Kinetic change...", help=tip("override_rationale"))
            if len((b1_justifications.get('K') or '').strip()) < 10: b1_missing_justifications.append('K')
        
        if b1_manual_C != orig_C1:
            st.warning(f"⚠️ **C Override**: {orig_C1}→{b1_manual_C}")
            b1_justifications['C'] = st.text_input(f"Why C={b1_manual_C}?", key="b1_just_C", placeholder="Explain Cognitive change...", help=tip("override_rationale"))
            if len((b1_justifications.get('C') or '').strip()) < 10: b1_missing_justifications.append('C')
        
        if b1_missing_justifications:
            st.error(f"❌ Justify: {', '.join(b1_missing_justifications)} (min 10 chars each)")
            st.session_state['b1_locked'] = True
        elif b1_justifications:
            st.success("✓ All overrides justified")
            st.session_state['b1_locked'] = False
        else:
            st.session_state['b1_locked'] = False
        
        b1_justification = " | ".join([f"{k}: {v}" for k, v in b1_justifications.items() if v])
        
        # Store final values
        final_scores_b1 = {
            'M': b1_manual_M, 'E': b1_manual_E, 'F': b1_manual_F,
            'B': b1_manual_B, 'K': b1_manual_K, 'C': b1_manual_C,
            'archetype': FORMAT_TO_ARCHETYPE[brand1_format],
            'reasoning': ai1.get('reasoning', 'Manual scoring') if ai1 else 'Manual scoring',
            'override_justification': b1_justification if b1_justifications else ''
        }
        st.session_state['final_b1'] = final_scores_b1

with h2:
    st.markdown("### 🟡 BRAND 2 (Challenger)")
    brand2_name = st.text_input(
        "Brand Name",
        placeholder="e.g., Dr. Bombay, Häagen-Dazs...",
        key="b2",
        help=tip("brand_name"),
    )
    brand2_format = st.selectbox(
        "Product Format", 
        options=["Pint / Tub (multi-serve)", "Bag / Pouch (multi-serve)", "Box / Carton (multi-serve)", "Single-Serve Bar / Novelty", "Can / Bottle (single)"],
        index=0, 
        key="b2_format",
        help=tip("format"),
    )
    st.caption(f"**Selected: {brand2_format}**")
    st.session_state.brand2_archetype = FORMAT_TO_ARCHETYPE[brand2_format]
    st.selectbox(
        "Category",
        options=CATEGORY_OPTIONS,
        index=0,
        key="brand2_category",
    )
    
    arch2 = ARCHETYPES[FORMAT_TO_ARCHETYPE[brand2_format]]
    
    if brand2_name:
        brand_key2 = brand2_name.lower().strip()
        known_scores2 = KNOWN_BRANDS.get(brand_key2)
        
        if known_scores2:
            st.session_state.ai_scores_b2 = known_scores2
            st.success(f"✓ **{brand2_name}** — F={known_scores2['F']}, C={known_scores2['C']}")
            with st.expander("Analysis", expanded=False):
                st.write(known_scores2.get('reasoning', ''))
        elif AI_ENABLED and (st.session_state.ai_scores_b2 is None or st.session_state.last_brand2 != brand2_name):
            st.session_state.last_brand2 = brand2_name
            with st.spinner(f"Analyzing {brand2_name}..."):
                try:
                    ai_result = analyze_brand_with_ai(brand2_name)
                    if ai_result and "error" not in ai_result:
                        st.session_state.ai_scores_b2 = ai_result
                        st.success(f"✓ **{brand2_name}** — F={ai_result.get('F')}, C={ai_result.get('C')}")
                    else:
                        st.warning(f"⚠️ **{brand2_name}** not recognized — set scores manually")
                except Exception as e:
                    st.warning(f"⚠️ Set scores manually for {brand2_name}")
                    print(f"[AI ERROR B2]: {e}")
        elif st.session_state.ai_scores_b2:
            ai2 = st.session_state.ai_scores_b2
            st.success(f"✓ **{brand2_name}** — F={ai2.get('F')}, C={ai2.get('C')}")
        else:
            st.warning(f"⚠️ **{brand2_name}** — set scores manually below")
        
        ai2 = st.session_state.ai_scores_b2
        # Prefer saved overrides (final_b2) so upload restarts analysis but keeps your edits
        _fb2 = st.session_state.get('final_b2') or {}
        def _orig_b2(key: str, default):
            v = _fb2.get(key) if (_fb2 and key in _fb2) else (ai2.get(key, default) if ai2 else default)
            return max(1, min(5, int(round(v)))) if v is not None else default
        orig_M2 = _orig_b2('M', 4)
        orig_E2 = _orig_b2('E', 4)
        orig_F2 = _orig_b2('F', 3)
        orig_B2 = _orig_b2('B', arch2.B)
        orig_K2 = _orig_b2('K', arch2.K)
        orig_C2 = _orig_b2('C', 3)
        
        st.markdown("**ALL 6 METRICS** (adjust as needed)")
        
        # Row 1: M, E, F
        r1_c1, r1_c2, r1_c3 = st.columns(3)
        with r1_c1:
            b2_manual_M = st.number_input("M", min_value=1, max_value=5, value=orig_M2, key="b2_M", help=tip("M"))
            st.caption("Mouthfeel")
        with r1_c2:
            b2_manual_E = st.number_input("E", min_value=1, max_value=5, value=orig_E2, key="b2_E", help=tip("E"))
            st.caption("Emotion")
        with r1_c3:
            b2_manual_F = st.number_input("F ⭐", min_value=1, max_value=5, value=orig_F2, key="b2_F", help=tip("F"))
            st.caption("Familiarity")
        
        # Row 2: B, K, C
        r2_c1, r2_c2, r2_c3 = st.columns(3)
        with r2_c1:
            b2_manual_B = st.number_input("B", min_value=1, max_value=5, value=orig_B2, key="b2_B", help=tip("B"))
            st.caption("Bites")
        with r2_c2:
            b2_manual_K = st.number_input("K", min_value=1, max_value=5, value=orig_K2, key="b2_K", help=tip("K"))
            st.caption("Kinetic")
        with r2_c3:
            b2_manual_C = st.number_input("C ⭐", min_value=1, max_value=5, value=orig_C2, key="b2_C", help=tip("C"))
            st.caption("Cognitive")
        
        # Check for overrides - each needs individual justification
        b2_justifications = {}
        b2_missing_justifications = []
        
        if b2_manual_M != orig_M2:
            st.warning(f"⚠️ **M Override**: {orig_M2}→{b2_manual_M}")
            b2_justifications['M'] = st.text_input(f"Why M={b2_manual_M}?", key="b2_just_M", placeholder="Explain Mouthfeel change...", help=tip("override_rationale"))
            if len((b2_justifications.get('M') or '').strip()) < 10: b2_missing_justifications.append('M')
        
        if b2_manual_E != orig_E2:
            st.warning(f"⚠️ **E Override**: {orig_E2}→{b2_manual_E}")
            b2_justifications['E'] = st.text_input(f"Why E={b2_manual_E}?", key="b2_just_E", placeholder="Explain Emotion change...", help=tip("override_rationale"))
            if len((b2_justifications.get('E') or '').strip()) < 10: b2_missing_justifications.append('E')
        
        if b2_manual_F != orig_F2:
            st.warning(f"⚠️ **F Override**: {orig_F2}→{b2_manual_F}")
            b2_justifications['F'] = st.text_input(f"Why F={b2_manual_F}?", key="b2_just_F", placeholder="Explain Familiarity change...", help=tip("override_rationale"))
            if len((b2_justifications.get('F') or '').strip()) < 10: b2_missing_justifications.append('F')
        
        if b2_manual_B != orig_B2:
            st.warning(f"⚠️ **B Override**: {orig_B2}→{b2_manual_B}")
            b2_justifications['B'] = st.text_input(f"Why B={b2_manual_B}?", key="b2_just_B", placeholder="Explain Bites change...", help=tip("override_rationale"))
            if len((b2_justifications.get('B') or '').strip()) < 10: b2_missing_justifications.append('B')
        
        if b2_manual_K != orig_K2:
            st.warning(f"⚠️ **K Override**: {orig_K2}→{b2_manual_K}")
            b2_justifications['K'] = st.text_input(f"Why K={b2_manual_K}?", key="b2_just_K", placeholder="Explain Kinetic change...", help=tip("override_rationale"))
            if len((b2_justifications.get('K') or '').strip()) < 10: b2_missing_justifications.append('K')
        
        if b2_manual_C != orig_C2:
            st.warning(f"⚠️ **C Override**: {orig_C2}→{b2_manual_C}")
            b2_justifications['C'] = st.text_input(f"Why C={b2_manual_C}?", key="b2_just_C", placeholder="Explain Cognitive change...", help=tip("override_rationale"))
            if len((b2_justifications.get('C') or '').strip()) < 10: b2_missing_justifications.append('C')
        
        if b2_missing_justifications:
            st.error(f"❌ Justify: {', '.join(b2_missing_justifications)} (min 10 chars each)")
            st.session_state['b2_locked'] = True
        elif b2_justifications:
            st.success("✓ All overrides justified")
            st.session_state['b2_locked'] = False
        else:
            st.session_state['b2_locked'] = False
        
        b2_justification = " | ".join([f"{k}: {v}" for k, v in b2_justifications.items() if v])
        
        # Store final values
        final_scores_b2 = {
            'M': b2_manual_M, 'E': b2_manual_E, 'F': b2_manual_F,
            'B': b2_manual_B, 'K': b2_manual_K, 'C': b2_manual_C,
            'archetype': FORMAT_TO_ARCHETYPE[brand2_format],
            'reasoning': ai2.get('reasoning', 'Manual scoring') if ai2 else 'Manual scoring',
            'override_justification': b2_justification if b2_justifications else ''
        }
        st.session_state['final_b2'] = final_scores_b2

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════════════
# THE STRUCTURAL COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════════════

st.markdown("## ⚔️ Structural Comparison")

# Get final scores from session state (user-adjusted values)
final1 = st.session_state.get('final_b1') or {}
final2 = st.session_state.get('final_b2') or {}
arch1 = ARCHETYPES[st.session_state.brand1_archetype or "bulk"]
arch2 = ARCHETYPES[st.session_state.brand2_archetype or "bulk"]

# Brand 1 final scores - use final values if available, else archetype defaults
b1_m = final1.get('M') if final1.get('M') else arch1.M
b1_e = final1.get('E') if final1.get('E') else arch1.E
b1_f = final1.get('F') if final1.get('F') else arch1.F
b1_b = final1.get('B') if final1.get('B') else arch1.B
b1_k = final1.get('K') if final1.get('K') else arch1.K
b1_c = final1.get('C') if final1.get('C') else arch1.C

# Brand 2 final scores - use final values if available, else archetype defaults
b2_m = final2.get('M') if final2.get('M') else arch2.M
b2_e = final2.get('E') if final2.get('E') else arch2.E
b2_f = final2.get('F') if final2.get('F') else arch2.F
b2_b = final2.get('B') if final2.get('B') else arch2.B
b2_k = final2.get('K') if final2.get('K') else arch2.K
b2_c = final2.get('C') if final2.get('C') else arch2.C

# ═══════════════════════════════════════════════════════════════════════════════════════
# APPLY BEHAVIORAL PRIORS (if enabled)
# ═══════════════════════════════════════════════════════════════════════════════════════

if PRIORS_AVAILABLE and st.session_state.get('use_priors', True):
    # Build context for Brand 1
    context_b1 = {
        "cohort": st.session_state.get('cohort', 'mixed'),
        "occasion": st.session_state.get('occasion', 'evening'),
        "macro_stress": st.session_state.get('macro_stress', True),
        "category": st.session_state.get('brand1_category', DEFAULT_CATEGORY),
        "promo_frequency": st.session_state.get('promo_frequency_b1', 0.0),
        "promo_depth": st.session_state.get('promo_depth_b1', 0.0),
        "ups_pw_13": st.session_state.get('ups_pw_13_b1'),
        "ups_pw_26": st.session_state.get('ups_pw_26_b1'),
        "format": brand1_format if brand1_format else "pint",
        "use_priors": True,
    }
    
    # Build context for Brand 2
    context_b2 = {
        "cohort": st.session_state.get('cohort', 'mixed'),
        "occasion": st.session_state.get('occasion', 'evening'),
        "macro_stress": st.session_state.get('macro_stress', True),
        "category": st.session_state.get('brand2_category', DEFAULT_CATEGORY),
        "promo_frequency": st.session_state.get('promo_frequency_b2', 0.0),
        "promo_depth": st.session_state.get('promo_depth_b2', 0.0),
        "ups_pw_13": st.session_state.get('ups_pw_13_b2'),
        "ups_pw_26": st.session_state.get('ups_pw_26_b2'),
        "format": brand2_format if brand2_format else "pint",
        "use_priors": True,
    }
    
    # Apply priors to Brand 1
    raw_b1 = {"M": b1_m, "E": b1_e, "F": b1_f, "B": b1_b, "K": b1_k, "C": b1_c}
    adjusted_b1, adjustments_b1 = apply_priors_dict(raw_b1, context_b1, hard_data=HARD_DATA)
    b1_m = adjusted_b1["M"]
    b1_e = adjusted_b1["E"]
    b1_f = adjusted_b1["F"]
    b1_b = adjusted_b1["B"]
    b1_k = adjusted_b1["K"]
    b1_c = adjusted_b1["C"]
    st.session_state.adjustments_log_b1 = adjustments_b1
    
    # Apply priors to Brand 2
    raw_b2 = {"M": b2_m, "E": b2_e, "F": b2_f, "B": b2_b, "K": b2_k, "C": b2_c}
    adjusted_b2, adjustments_b2 = apply_priors_dict(raw_b2, context_b2, hard_data=HARD_DATA)
    b2_m = adjusted_b2["M"]
    b2_e = adjusted_b2["E"]
    b2_f = adjusted_b2["F"]
    b2_b = adjusted_b2["B"]
    b2_k = adjusted_b2["K"]
    b2_c = adjusted_b2["C"]
    st.session_state.adjustments_log_b2 = adjustments_b2
    
    print(f"[PRIORS] B1 adjustments: {len(adjustments_b1)} applied")
    print(f"[PRIORS] B2 adjustments: {len(adjustments_b2)} applied")
else:
    st.session_state.adjustments_log_b1 = ["Priors disabled. Using raw inputs only."]
    st.session_state.adjustments_log_b2 = ["Priors disabled. Using raw inputs only."]

# Debug output for final scores (after priors)
print(f"[DEBUG] Final B1 scores (after priors): M={b1_m}, E={b1_e}, F={b1_f}, B={b1_b}, K={b1_k}, C={b1_c}")
print(f"[DEBUG] Final B2 scores (after priors): M={b2_m}, E={b2_e}, F={b2_f}, B={b2_b}, K={b2_k}, C={b2_c}")

# Calculate S-Scores when both brands are entered (show comparison even if overrides are locked)
b1_locked = st.session_state.get('b1_locked', False)
b2_locked = st.session_state.get('b2_locked', False)

s1 = calculate_s_score(b1_m, b1_e, b1_f, b1_b, b1_k, b1_c) if brand1_name else None
s2 = calculate_s_score(b2_m, b2_e, b2_f, b2_b, b2_k, b2_c) if brand2_name else None

print(f"[DEBUG] S1={s1}, S2={s2}")

# Side-by-side results
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {brand1_name or 'Brand 1'}")
    if st.session_state.brand1_archetype == "unitized":
        st.success(f"🟢 {arch1.short_name}")
    elif st.session_state.brand1_archetype == "bulk":
        st.error(f"🔴 {arch1.short_name}")
    else:
        st.info(f"🔵 {arch1.short_name}")
    
    if brand1_name:
        st.markdown(f"""
        | Var | Score | Meaning |
        |-----|-------|---------|
        | **M** | {b1_m} | Mouthfeel |
        | **E** | {b1_e} | Emotion |
        | **F** | {b1_f} | Familiarity |
        | **B** | {b1_b} | Bites |
        | **K** | {b1_k} | Kinetic |
        | **C** | {b1_c} | Cognitive |
        """)
        num1 = b1_m * b1_e * b1_f
        den1 = b1_b * b1_k * b1_c
        st.caption(f"Numerator: {num1} | Denominator: {den1}")
        if b1_locked:
            st.error("🔒 **LOCKED**: Provide override justification above")
        elif s1:
            st.metric("S-Score™", f"{s1:.2f}")
    else:
        st.info("Enter brand name above")

with col2:
    st.markdown(f"### {brand2_name or 'Brand 2'}")
    if st.session_state.brand2_archetype == "unitized":
        st.success(f"🟢 {arch2.short_name}")
    elif st.session_state.brand2_archetype == "bulk":
        st.error(f"🔴 {arch2.short_name}")
    else:
        st.info(f"🔵 {arch2.short_name}")
    
    if brand2_name:
        st.markdown(f"""
        | Var | Score | Meaning |
        |-----|-------|---------|
        | **M** | {b2_m} | Mouthfeel |
        | **E** | {b2_e} | Emotion |
        | **F** | {b2_f} | Familiarity |
        | **B** | {b2_b} | Bites |
        | **K** | {b2_k} | Kinetic |
        | **C** | {b2_c} | Cognitive |
        """)
        num2 = b2_m * b2_e * b2_f
        den2 = b2_b * b2_k * b2_c
        st.caption(f"Numerator: {num2} | Denominator: {den2}")
        if b2_locked:
            st.error("🔒 **LOCKED**: Provide override justification above")
        elif s2:
            delta = s2 - s1 if s1 else None
            st.metric("S-Score™", f"{s2:.2f}", delta=f"{delta:+.2f}" if delta else None)
    else:
        st.info("Enter brand name above")

# Get justifications from session state for memo generation
final1 = st.session_state.get('final_b1') or {}
final2 = st.session_state.get('final_b2') or {}
rat_b1 = final1.get('override_justification', '')
rat_b2 = final2.get('override_justification', '')
b1_amendments = bool(rat_b1)
b2_amendments = bool(rat_b2)


# When both brands are entered, show comparison and reports (scroll down if needed)
if brand1_name and brand2_name and (s1 is None or s2 is None):
    st.info("💡 **Tip:** Scroll up to fill in or adjust the 6 metrics (M, E, F, B, K, C) for each brand. S-Scores and reports appear below once both brands have scores.")

# ═══════════════════════════════════════════════════════════════════════════════════════
# BEHAVIORAL SIGNATURE - USING NATIVE STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════════════════

if s1 is not None and s2 is not None:
    st.divider()
    st.markdown("## 📊 Behavioral Signature Comparison")
    
    n1 = brand1_name or "Brand 1"
    n2 = brand2_name or "Brand 2"
    
    # Create comparison dataframe - ALL STRINGS to avoid pyarrow issues
    data = {
        "Variable": ["M · Mouthfeel", "E · Emotion", "F · Familiarity", "B · Bites", "K · Kinetic", "C · Cognitive", "S-SCORE™"],
        n1: [str(b1_m), str(b1_e), str(b1_f), str(b1_b), str(b1_k), str(b1_c), f"{s1:.2f}"],
        n2: [str(b2_m), str(b2_e), str(b2_f), str(b2_b), str(b2_k), str(b2_c), f"{s2:.2f}"],
        "Delta": [
            f"{b2_m - b1_m:+.2f}", f"{b2_e - b1_e:+.2f}", f"{b2_f - b1_f:+.2f}",
            f"{b2_b - b1_b:+.2f}", f"{b2_k - b1_k:+.2f}", f"{b2_c - b1_c:+.2f}",
            f"{s2 - s1:+.2f}"
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Display as table
    st.table(df)
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # VISUAL BAR CHART COMPARISON
    # ═══════════════════════════════════════════════════════════════════════════════════
    st.markdown("### 📈 Visual Score Comparison")
    
    chart_data = pd.DataFrame({
        "Variable": ["M", "E", "F", "B", "K", "C"],
        n1: [b1_m, b1_e, b1_f, b1_b, b1_k, b1_c],
        n2: [b2_m, b2_e, b2_f, b2_b, b2_k, b2_c]
    })
    
    # Custom chart with dark theme colors
    st.bar_chart(
        chart_data.set_index("Variable"), 
        height=350, 
        width="stretch",
        color=["#10b981", "#ec4899"]  # Mint green and Pink for brands
    )
    
    st.caption("📈 **Numerator (M, E, F)**: Higher = more value | 📉 **Denominator (B, K, C)**: Lower = less friction")
    
    # Numerator vs Denominator metrics
    st.markdown("### Numerator vs Denominator")
    
    bc1, bc2 = st.columns(2)
    with bc1:
        st.markdown(f"**{n1}**")
        num1 = b1_m * b1_e * b1_f
        den1 = b1_b * b1_k * b1_c
        st.metric("Numerator (M×E×F)", num1)
        st.metric("Denominator (B×K×C)", den1)
    
    with bc2:
        st.markdown(f"**{n2}**")
        num2 = b2_m * b2_e * b2_f
        den2 = b2_b * b2_k * b2_c
        st.metric("Numerator (M×E×F)", num2, delta=num2-num1)
        st.metric("Denominator (B×K×C)", den2, delta=den2-den1, delta_color="inverse")

# ═══════════════════════════════════════════════════════════════════════════════════════
# INVESTOR MEMO
# ═══════════════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown("## 📋 Investor Memo: Behavioral Structural Audit")

if s1 is not None and s2 is not None:
    delta = s2 - s1
    ratio = max(s1, s2) / min(s1, s2) if min(s1, s2) > 0 else float('inf')
    winner = brand1_name if s1 > s2 else brand2_name
    
    # Big metrics - Glassmorphism style
    st.markdown(f"""
    <div style="background: rgba(91, 33, 182, 0.35); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.15); padding: 32px; border-radius: 20px; margin: 24px 0;">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 0.9rem; color: #c4b5fd !important; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 8px;">
                    {brand1_name or 'Brand 1'} S-Score™
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 3.5rem; font-weight: 800; color: #10b981 !important;">
                    {s1:.2f}
                </div>
            </div>
            <div>
                <div style="font-size: 0.9rem; color: #c4b5fd !important; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 8px;">
                    {brand2_name or 'Brand 2'} S-Score™
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 3.5rem; font-weight: 800; color: #ec4899 !important;">
                    {s2:.2f}
                </div>
            </div>
            <div>
                <div style="font-size: 0.9rem; color: #c4b5fd !important; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 8px;">
                    Behavioral Advantage
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 3.5rem; font-weight: 800; color: #FFFFFF !important;">
                    {ratio:.1f}x
                </div>
                <div style="font-size: 0.9rem; color: #a78bfa !important; margin-top: 4px;">{winner} leads</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    n1 = brand1_name or "Brand 1"
    n2 = brand2_name or "Brand 2"
    
    # Initialize memo storage in session state
    if 'last_memo' not in st.session_state:
        st.session_state.last_memo = None
    
    scores1 = {'M': b1_m, 'E': b1_e, 'F': b1_f, 'B': b1_b, 'K': b1_k, 'C': b1_c}
    scores2 = {'M': b2_m, 'E': b2_e, 'F': b2_f, 'B': b2_b, 'K': b2_k, 'C': b2_c}
    
    # Build full upload context for memo: sales data and/or brand/consumer documents (so report uses all of it)
    _data_ctx = _build_upload_context_for_report()

    # Generate memo buttons
    col_ai, col_rule = st.columns(2)
    
    with col_ai:
        if AI_ENABLED:
            if st.button("📊 Elbow Interference Investor Report", type="primary", width="stretch"):
                with st.spinner("Generating analysis... (10-15 seconds)"):
                    try:
                        print(f"[MEMO] Attempting AI generation for {n1} vs {n2}")
                        ai_thesis = generate_strategic_synthesis(
                            n1, n2, s1, s2, scores1, scores2,
                            rat_b1 if b1_amendments else "",
                            rat_b2 if b2_amendments else "",
                            data_context=_data_ctx
                        )
                        if ai_thesis:
                            st.session_state.last_memo = ai_thesis
                            print(f"[MEMO] ✓ AI memo generated successfully")
                        else:
                            print(f"[MEMO] ✗ AI returned None, using fallback")
                            st.session_state.last_memo = generate_rule_based_memo(n1, n2, s1, s2, scores1, scores2)
                            st.warning("Using standard analysis")
                    except Exception as e:
                        print(f"[MEMO] ✗ Exception: {e}")
                        st.session_state.last_memo = generate_rule_based_memo(n1, n2, s1, s2, scores1, scores2)
                        st.warning("Using standard analysis")
        else:
            st.info("Use Quick Analysis")
    
    with col_rule:
        if st.button("📋 Quick Analysis", width="stretch"):
            st.session_state.last_memo = generate_rule_based_memo(n1, n2, s1, s2, scores1, scores2)
    
    # Display saved memo if exists
    if st.session_state.last_memo:
        st.markdown("---")
        st.markdown("### 📋 INVESTOR MEMO: BEHAVIORAL STRUCTURAL AUDIT")
        st.markdown(st.session_state.last_memo)
    
    st.divider()
    
    # Quick Summary Cards
    st.markdown("### Quick Structural Summary")
    
    sum1, sum2 = st.columns(2)
    
    with sum1:
        den1_avg = (b1_b + b1_k + b1_c) / 3
        if den1_avg <= 1.5:
            st.success(f"**{n1}**: Denominator Collapse ✓")
            st.caption("Structural Persistence — Format does the work")
        elif den1_avg <= 2.5:
            st.warning(f"**{n1}**: Partial Compression")
            st.caption("Mixed structure — Some marketing needed")
        else:
            st.error(f"**{n1}**: High Interference")
            st.caption("Purchased Velocity — Spend-dependent")
    
    with sum2:
        den2_avg = (b2_b + b2_k + b2_c) / 3
        if den2_avg <= 1.5:
            st.success(f"**{n2}**: Denominator Collapse ✓")
            st.caption("Structural Persistence — Format does the work")
        elif den2_avg <= 2.5:
            st.warning(f"**{n2}**: Partial Compression")
            st.caption("Mixed structure — Some marketing needed")
        else:
            st.error(f"**{n2}**: High Interference")
            st.caption("Purchased Velocity — Spend-dependent")
    
    # Analyst Amendment Notes
    if (b1_amendments and rat_b1.strip()) or (b2_amendments and rat_b2.strip()):
        st.divider()
        st.markdown("### Analyst Amendments")
        if b1_amendments and rat_b1.strip():
            st.info(f"**{n1}:** {rat_b1}")
        if b2_amendments and rat_b2.strip():
            st.info(f"**{n2}:** {rat_b2}")
    
    # ═══════════════════════════════════════════════════════════════════════════════════════
    # ASSUMPTIONS & ADJUSTMENTS (Priors Log)
    # ═══════════════════════════════════════════════════════════════════════════════════════
    
    if PRIORS_AVAILABLE and st.session_state.get('use_priors', True):
        st.divider()
        st.markdown("### ⚙️ Assumptions & Adjustments")
        
        with st.expander("View Prior Adjustments Applied", expanded=False):
            adj_col1, adj_col2 = st.columns(2)
            
            with adj_col1:
                st.markdown(f"**{n1} Adjustments:**")
                for adj in st.session_state.get('adjustments_log_b1', []):
                    st.caption(f"• {adj}")
            
            with adj_col2:
                st.markdown(f"**{n2} Adjustments:**")
                for adj in st.session_state.get('adjustments_log_b2', []):
                    st.caption(f"• {adj}")
            
            st.caption("---")
            st.caption(f"Context: cohort={st.session_state.get('cohort', 'mixed')}, "
                      f"occasion={st.session_state.get('occasion', 'evening')}, "
                      f"macro_stress={'Active' if st.session_state.get('macro_stress', True) else 'Inactive'}")
            
            # External Support (Hard Data)
            if HARD_DATA_AVAILABLE:
                st.markdown("---")
                st.markdown("**External Support (Hard Data)**")
                
                ext_col1, ext_col2 = st.columns(2)
                
                # Get category from context or default
                cat_b1 = st.session_state.get('brand1_category', DEFAULT_CATEGORY)
                cat_b2 = st.session_state.get('brand2_category', DEFAULT_CATEGORY)
                
                with ext_col1:
                    st.caption(f"**{n1}** ({cat_b1}):")
                    snippets_b1 = get_external_support_snippets(cat_b1)
                    for snippet in snippets_b1[:3]:  # Show top 3
                        st.caption(f"• {snippet}")
                
                with ext_col2:
                    st.caption(f"**{n2}** ({cat_b2}):")
                    snippets_b2 = get_external_support_snippets(cat_b2)
                    for snippet in snippets_b2[:3]:  # Show top 3
                        st.caption(f"• {snippet}")
                
                st.caption("---")
                st.caption("*Hard data is used as guardrails, not as score input.*")
    elif not st.session_state.get('use_priors', True):
        st.divider()
        st.caption("⚠️ **Priors disabled** — Raw inputs used without adjustment.")

else:
    st.warning("**Analysis Locked** — Provide rationale for all amendments to unlock Investor Report.")

# ═══════════════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown("""
<div style="text-align: center; padding: 48px 0; border-top: 4px solid #10B981;">
    <div style="font-size: 1.3rem; font-weight: 900; color: #DC2626; letter-spacing: 0.25em; margin-bottom: 16px;">⬥ CONFIDENTIAL ⬥</div>
    <div style="font-size: 1.4rem; font-weight: 700; color: #475569;">PROPRIETARY METHODOLOGY OF RUSSELL BARNETT</div>
    <div style="font-size: 1.2rem; color: #64748B; margin-top: 8px;">THE ELBOW INTERFERENCE THEORY™ · ALL RIGHTS RESERVED © 2026</div>
</div>
""", unsafe_allow_html=True)
