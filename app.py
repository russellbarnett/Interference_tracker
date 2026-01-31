import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════════
# ELBOW ZONE™ | BEHAVIORAL AUDIT TERMINAL
# © 2026 Russell Barnett. The Elbow Interference Theory™. All Rights Reserved.
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ELBOW ZONE™ | Behavioral Audit Terminal",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# GALLERY WHITE INSTITUTIONAL THEME
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    /* Gallery White Base */
    .main {
        background: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #FFFFFF;
    }
    
    /* Subtle Grid Pattern */
    .main::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            linear-gradient(rgba(226, 232, 240, 0.4) 1px, transparent 1px),
            linear-gradient(90deg, rgba(226, 232, 240, 0.4) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* Sidebar - Clean White */
    section[data-testid="stSidebar"] {
        background: #FAFAFA;
        border-right: 1px solid #E5E7EB;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #111827 !important;
    }
    
    /* Typography - Large & Bold */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        font-size: 2.8rem !important;
        color: #0F172A !important;
        letter-spacing: -0.04em;
        line-height: 1.1;
    }
    
    h2 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        color: #1E293B !important;
        letter-spacing: -0.02em;
    }
    
    h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        color: #334155 !important;
    }
    
    /* Slider Labels - Bold 20px */
    .stSlider label {
        font-family: 'Inter', sans-serif !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #1E293B !important;
    }
    
    .stSlider p {
        font-size: 14px !important;
        color: #64748B !important;
    }
    
    /* Equation Banner */
    .equation-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
        padding: 32px 40px;
        border-radius: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.6rem;
        text-align: center;
        margin: 24px 0 32px 0;
        box-shadow: 0 12px 40px rgba(15, 23, 42, 0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .equation-banner .equation {
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin: 16px 0;
    }
    
    .equation-banner .subtitle {
        font-size: 1rem;
        opacity: 0.7;
        font-family: 'Inter', sans-serif;
    }
    
    /* Column Headers */
    .column-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        color: #0F172A;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 20px 24px;
        background: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .column-header.baseline {
        border-color: #CBD5E1;
        background: #F1F5F9;
    }
    
    .column-header.subject {
        border-color: #10B981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(52, 211, 153, 0.04) 100%);
    }
    
    /* Score Display - 1.5x Scale */
    .score-box {
        padding: 28px 36px;
        border-radius: 16px;
        text-align: center;
        margin-top: 24px;
    }
    
    .score-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.6rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    .score-label {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    /* Elbow Zone - Emerald */
    .elbow-zone {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        color: white;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
    }
    
    /* Head Zone - Soft Coral */
    .head-zone {
        background: linear-gradient(135deg, #DC2626 0%, #F87171 100%);
        color: white;
        box-shadow: 0 8px 32px rgba(248, 113, 113, 0.3);
    }
    
    /* Locked State */
    .locked-score {
        background: linear-gradient(135deg, #475569 0%, #64748B 100%);
        color: white;
        box-shadow: 0 8px 32px rgba(71, 85, 105, 0.25);
    }
    
    .locked-score .score-value {
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    
    /* Ghost Value Label */
    .ghost-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #94A3B8;
        background: #F1F5F9;
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
        margin: 4px 0 12px 0;
        border: 1px solid #E2E8F0;
    }
    
    /* Amendment Indicator */
    .amended-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 6px 12px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    
    /* Strategic Rationale Box */
    .stTextArea textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        min-height: 120px !important;
        background: #FAFAFA !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.12) !important;
        background: #FFFFFF !important;
    }
    
    /* Verdict Box */
    .verdict-box {
        background: #FAFAFA;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 28px 32px;
        margin-top: 24px;
    }
    
    .verdict-box.advantage {
        border-color: #10B981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.06) 0%, rgba(255,255,255,1) 100%);
    }
    
    .verdict-box.risk {
        border-color: #F87171;
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.06) 0%, rgba(255,255,255,1) 100%);
    }
    
    .verdict-box.analysis {
        border-color: #F59E0B;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.06) 0%, rgba(255,255,255,1) 100%);
    }
    
    /* Metrics - 1.5x Scale */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    
    div[data-testid="stMetric"] label {
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #374151 !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Section Dividers */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #E2E8F0 50%, transparent 100%);
        margin: 40px 0;
    }
    
    /* Footer */
    .footer {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #64748B;
        text-align: center;
        padding: 40px 0 24px 0;
        border-top: 1px solid #E2E8F0;
        margin-top: 56px;
    }
    
    /* Confidential Watermark */
    .watermark {
        position: fixed;
        bottom: 24px;
        right: 24px;
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 800;
        color: rgba(148, 163, 184, 0.35);
        letter-spacing: 0.2em;
        text-transform: uppercase;
        transform: rotate(-5deg);
        pointer-events: none;
        z-index: 1000;
    }
    
    /* Warning State */
    .rationale-warning {
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.03) 100%);
        border-left: 4px solid #F59E0B;
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        font-size: 15px;
        color: #92400E;
        margin: 16px 0;
    }
    
    /* Character Counter */
    .char-counter {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #94A3B8;
        text-align: right;
        margin-top: 8px;
    }
    
    .char-counter.valid {
        color: #10B981;
    }
</style>
<div class="watermark">CONFIDENTIAL</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PRODUCT PHYSICS ARCHETYPES
# ═══════════════════════════════════════════════════════════════════════════════
PRODUCT_PHYSICS = {
    "Unitized — Denominator Collapse": {
        "description": "Handhelds, bars, bites, pouches, single-serve portions",
        "scores": {"M": 4, "E": 4, "F": 4, "B": 1, "K": 1, "C": 1},
        "logic": "The physical structure eliminates decision points. Portion-bound format means the Elbow finishes the job before the Head can arrive."
    },
    "Bulk — High Interference Risk": {
        "description": "Pints, tubs, bags, multi-serve containers",
        "scores": {"M": 5, "E": 4, "F": 5, "B": 4, "K": 3, "C": 3},
        "logic": "Open-ended format requires self-managed stopping. Each bite is a new decision point where the Head can interrupt the Elbow."
    },
    "Ritual — Habitual Flow": {
        "description": "Cans, bottles, single-ritual beverages",
        "scores": {"M": 3, "E": 3, "F": 5, "B": 2, "K": 1, "C": 1},
        "logic": "Ritual preservation through extreme familiarity. The behavior is so automatic that cognitive interference is structurally suppressed."
    }
}

VAR_INFO = {
    "M": ("Mouthfeel", "How the product feels during consumption — the site of sensory resolution."),
    "E": ("Emotion", "Rises when expectation is violated and resolved immediately in the body."),
    "F": ("Familiarity", "Comfort that suppresses interference — the behavioral autopilot."),
    "B": ("Bites", "Decision count. More bites = more chances for the Head to arrive."),
    "K": ("Kinetic", "Physical work required to continue consuming."),
    "C": ("Cognitive", "The interference point. When the Head arrives, the Elbow slows.")
}

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
if "rationale" not in st.session_state:
    st.session_state.rationale = ""

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — INSTITUTIONAL DATA FEED
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ◈ ELBOW ZONE™")
    st.caption("Behavioral Audit Terminal")
    
    st.markdown("---")
    
    # Data Upload
    st.markdown("### 📊 Circana / MULO Data")
    uploaded_file = st.file_uploader(
        "Upload syndicated data",
        type=["csv"],
        help="Drop Circana or MULO CSV to calibrate Presence vs. Persistence metrics"
    )
    
    if uploaded_file:
        st.success("✓ Presence data loaded")
    else:
        st.info("Structural analysis mode (no external data)")
    
    st.markdown("---")
    
    # Product Physics Selector
    st.markdown("### 🏗️ Product Physics")
    selected_physics = st.selectbox(
        "Select structural archetype",
        list(PRODUCT_PHYSICS.keys()),
        help="This sets the Baseline scores based on the physical form factor"
    )
    
    physics = PRODUCT_PHYSICS[selected_physics]
    st.caption(physics["description"])
    
    with st.expander("View Structural Logic"):
        st.write(physics["logic"])
    
    st.markdown("---")
    
    # Variable Reference
    st.markdown("### 📖 Variable Definitions")
    with st.expander("Expand Reference"):
        for key, (name, desc) in VAR_INFO.items():
            st.markdown(f"**{key} ({name})**: {desc}")
    
    st.markdown("---")
    
    # Copyright
    st.markdown("""
    <div style='text-align: center; font-size: 11px; color: #94A3B8; padding: 12px 0;'>
        © 2026 Russell Barnett<br>
        The Elbow Interference Theory™<br>
        All Rights Reserved
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TERMINAL
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("# ELBOW ZONE™")
st.caption("Strategic Behavioral Audit Terminal")

# Equation Banner
st.markdown("""
<div class="equation-banner">
    <div style="font-size: 1rem; font-weight: 600; letter-spacing: 0.1em; opacity: 0.7; margin-bottom: 8px;">
        THE SATISFACTION EQUATION
    </div>
    <div class="equation">
        S = (M × E × F) ÷ (B × K × C)
    </div>
    <div class="subtitle">
        Value Delivered ÷ Cost Extracted = Structural Persistence
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"**Active Physics:** {selected_physics}")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DUAL-COLUMN AUDIT
# ═══════════════════════════════════════════════════════════════════════════════

col_baseline, col_subject = st.columns(2)

baseline = physics["scores"]
amendments_made = False

with col_baseline:
    st.markdown('<div class="column-header baseline">📊 BASELINE — The Law</div>', unsafe_allow_html=True)
    st.caption("Category structural norms (locked to Product Physics)")
    
    st.markdown("##### NUMERATOR — Value Delivered")
    
    base_m = st.slider(
        f"M · {VAR_INFO['M'][0]}", 1, 5, baseline["M"],
        key="base_m", disabled=True, help=VAR_INFO["M"][1]
    )
    base_e = st.slider(
        f"E · {VAR_INFO['E'][0]}", 1, 5, baseline["E"],
        key="base_e", disabled=True, help=VAR_INFO["E"][1]
    )
    base_f = st.slider(
        f"F · {VAR_INFO['F'][0]}", 1, 5, baseline["F"],
        key="base_f", disabled=True, help=VAR_INFO["F"][1]
    )
    
    st.markdown("##### DENOMINATOR — Cost Extracted")
    
    base_b = st.slider(
        f"B · {VAR_INFO['B'][0]}", 1, 5, baseline["B"],
        key="base_b", disabled=True, help=VAR_INFO["B"][1]
    )
    base_k = st.slider(
        f"K · {VAR_INFO['K'][0]}", 1, 5, baseline["K"],
        key="base_k", disabled=True, help=VAR_INFO["K"][1]
    )
    base_c = st.slider(
        f"C · {VAR_INFO['C'][0]}", 1, 5, baseline["C"],
        key="base_c", disabled=True, help=VAR_INFO["C"][1]
    )
    
    # Calculate Baseline S-Score
    s_baseline = (base_m * base_e * base_f) / (base_b * base_k * base_c)
    
    st.markdown(f"""
    <div class="score-box elbow-zone">
        <div class="score-value">{s_baseline:.2f}</div>
        <div class="score-label">Baseline S-Score™</div>
    </div>
    """, unsafe_allow_html=True)

with col_subject:
    st.markdown('<div class="column-header subject">🎯 SUBJECT — The Amendment</div>', unsafe_allow_html=True)
    st.caption("Adjust scores to model your Subject's structural reality")
    
    st.markdown("##### NUMERATOR — Value Delivered")
    
    # M
    subj_m = st.slider(
        f"M · {VAR_INFO['M'][0]}", 1, 5, baseline["M"],
        key="subj_m", help=VAR_INFO["M"][1]
    )
    if subj_m != baseline["M"]:
        amendments_made = True
        st.markdown(f'<span class="amended-badge">AMENDED</span> <span class="ghost-value">Baseline: {baseline["M"]}</span>', unsafe_allow_html=True)
    
    # E
    subj_e = st.slider(
        f"E · {VAR_INFO['E'][0]}", 1, 5, baseline["E"],
        key="subj_e", help=VAR_INFO["E"][1]
    )
    if subj_e != baseline["E"]:
        amendments_made = True
        st.markdown(f'<span class="amended-badge">AMENDED</span> <span class="ghost-value">Baseline: {baseline["E"]}</span>', unsafe_allow_html=True)
    
    # F
    subj_f = st.slider(
        f"F · {VAR_INFO['F'][0]}", 1, 5, baseline["F"],
        key="subj_f", help=VAR_INFO["F"][1]
    )
    if subj_f != baseline["F"]:
        amendments_made = True
        st.markdown(f'<span class="amended-badge">AMENDED</span> <span class="ghost-value">Baseline: {baseline["F"]}</span>', unsafe_allow_html=True)
    
    st.markdown("##### DENOMINATOR — Cost Extracted")
    
    # B
    subj_b = st.slider(
        f"B · {VAR_INFO['B'][0]}", 1, 5, baseline["B"],
        key="subj_b", help=VAR_INFO["B"][1]
    )
    if subj_b != baseline["B"]:
        amendments_made = True
        st.markdown(f'<span class="amended-badge">AMENDED</span> <span class="ghost-value">Baseline: {baseline["B"]}</span>', unsafe_allow_html=True)
    
    # K
    subj_k = st.slider(
        f"K · {VAR_INFO['K'][0]}", 1, 5, baseline["K"],
        key="subj_k", help=VAR_INFO["K"][1]
    )
    if subj_k != baseline["K"]:
        amendments_made = True
        st.markdown(f'<span class="amended-badge">AMENDED</span> <span class="ghost-value">Baseline: {baseline["K"]}</span>', unsafe_allow_html=True)
    
    # C
    subj_c = st.slider(
        f"C · {VAR_INFO['C'][0]}", 1, 5, baseline["C"],
        key="subj_c", help=VAR_INFO["C"][1]
    )
    if subj_c != baseline["C"]:
        amendments_made = True
        st.markdown(f'<span class="amended-badge">AMENDED</span> <span class="ghost-value">Baseline: {baseline["C"]}</span>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # JUSTIFICATION GATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    if amendments_made:
        st.markdown("---")
        st.markdown("##### 📝 Strategic Rationale")
        st.caption("Explain the structural reasoning behind your amendments (minimum 25 characters)")
        
        rationale = st.text_area(
            "Strategic Rationale",
            value=st.session_state.rationale,
            placeholder="Describe why the Subject differs from the category baseline...\n\nExample: 'Premium price point creates cognitive friction at point-of-sale, but novel mochi texture delivers immediate sensory resolution that suppresses post-purchase doubt.'",
            label_visibility="collapsed",
            key="rationale_input"
        )
        st.session_state.rationale = rationale
        
        # Character count
        char_count = len(rationale.strip())
        is_valid = char_count >= 25
        
        counter_class = "char-counter valid" if is_valid else "char-counter"
        st.markdown(f'<div class="{counter_class}">{char_count} / 25 characters</div>', unsafe_allow_html=True)
        
        if not is_valid:
            st.markdown("""
            <div class="rationale-warning">
                ⚠️ <strong>Rationale Required</strong> — Provide at least 25 characters of strategic reasoning to unlock the Subject S-Score.
            </div>
            """, unsafe_allow_html=True)
    else:
        is_valid = True
        rationale = ""
    
    # Calculate or Lock Subject S-Score
    if amendments_made and not is_valid:
        st.markdown(f"""
        <div class="score-box locked-score">
            <div class="score-value">[LOCKED: RATIONALE REQUIRED]</div>
            <div class="score-label">Subject S-Score™</div>
        </div>
        """, unsafe_allow_html=True)
        s_subject = None
    else:
        s_subject = (subj_m * subj_e * subj_f) / (subj_b * subj_k * subj_c)
        
        if s_subject >= s_baseline:
            zone_class = "elbow-zone"
        else:
            zone_class = "head-zone"
        
        st.markdown(f"""
        <div class="score-box {zone_class}">
            <div class="score-value">{s_subject:.2f}</div>
            <div class="score-label">Subject S-Score™</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# STRATEGIC VERDICT
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown("## 📋 Strategic Verdict")

if s_subject is not None:
    delta = s_subject - s_baseline
    
    # Metrics Row
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric("Baseline S-Score™", f"{s_baseline:.2f}")
    with m2:
        st.metric("Subject S-Score™", f"{s_subject:.2f}", delta=round(delta, 2))
    with m3:
        efficiency = ((s_subject / s_baseline) - 1) * 100 if s_baseline > 0 else 0
        st.metric("Efficiency Gap", f"{efficiency:+.1f}%")
    
    st.markdown("---")
    
    # AI Analyst Synthesis
    st.markdown("### 🧠 AI Analyst Synthesis")
    
    # Determine verdict type and generate analysis
    if subj_c >= 4:
        verdict_class = "analysis"
        verdict_header = "⚠️ FURTHER ANALYSIS REQUIRED"
        
        verdict_body = f"""
**High Cognitive Interference Detected** (C = {subj_c})

The Subject exhibits elevated cognitive load in the Denominator, indicating the **Head Zone arrives before the occasion naturally concludes**. 
This represents a structural barrier to repeat behavior—each consumption instance requires conscious re-evaluation.

**Elbow → Head Transition:** The consumer's automatic behavior (Elbow Zone) is interrupted by deliberate processing (Head Zone). 
The structural advantage of the category baseline is compromised by this cognitive friction.
"""
        if amendments_made and rationale:
            verdict_body += f"\n**Analyst Rationale:** *\"{rationale}\"*"
        
        verdict_body += """

**Recommendation:** Investigate whether the value proposition justifies the cognitive cost, or whether repositioning can reduce the Head Zone trigger point.
"""
    
    elif delta < 0:
        verdict_class = "risk"
        verdict_header = "🔴 STRUCTURAL RISK DETECTED"
        
        verdict_body = f"""
**Subject Fails to Match Category Efficiency**

The Subject S-Score ({s_subject:.2f}) trails the Baseline ({s_baseline:.2f}) by **{abs(delta):.2f} points**, 
indicating higher behavioral cost relative to value delivered.

**Head Zone Analysis:** The Subject's Denominator creates more interference points than the category norm. 
The Elbow slows earlier in the consumption occasion, allowing the Head to arrive and evaluate.

**Structural Persistence:** Currently **unproven**. Without Denominator Collapse, velocity must be purchased through 
marketing, distribution, and promotion rather than earned through repeat structure.
"""
        if amendments_made and rationale:
            verdict_body += f"\n**Analyst Rationale:** *\"{rationale}\"*"
    
    else:
        verdict_class = "advantage"
        verdict_header = "🟢 STRUCTURAL ADVANTAGE CONFIRMED"
        
        verdict_body = f"""
**Subject Demonstrates Superior Repeat Efficiency**

The Subject S-Score ({s_subject:.2f}) exceeds the Baseline ({s_baseline:.2f}) by **{delta:.2f} points**, 
indicating lower behavioral cost relative to value delivered.

**Elbow Zone Dominance:** The Subject's physical structure supports automatic repeat behavior. 
The consumption occasion completes before cognitive interference can trigger the Head Zone.

**Structural Persistence:** The format does the work. Repeat behavior is **structurally embedded** rather than 
requiring continuous external activation.
"""
        if amendments_made and rationale:
            verdict_body += f"\n**Analyst Rationale:** *\"{rationale}\"*"
    
    st.markdown(f'<div class="verdict-box {verdict_class}">', unsafe_allow_html=True)
    st.markdown(f"#### {verdict_header}")
    st.markdown(verdict_body)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Persistence Commentary
    st.markdown("---")
    st.markdown("### Persistence Status")
    
    denom_avg = (subj_b + subj_k + subj_c) / 3
    
    if denom_avg <= 1.5:
        st.success("✓ **Denominator Collapse Achieved** — Structural Persistence is built into the format. The Elbow finishes the job.")
    else:
        st.warning("⚡ **Velocity is currently purchased; Structural Persistence is unproven** until Denominator Collapse is achieved.")
    
    st.info("💡 *This signal measures Persistence (Repeat) not Presence (Trial). A lack of data is not a lack of structure—look at the Denominator.*")

else:
    st.warning("**Verdict Locked** — Complete the Strategic Rationale for your amendments to unlock the AI Analyst Synthesis.")

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="footer">
    <strong>ELBOW ZONE™</strong> | Behavioral Audit Terminal<br>
    © 2026 Russell Barnett. The Elbow Interference Theory™. All Rights Reserved.<br><br>
    <em>"When the Head arrives, the Elbow slows. Structure the Denominator, and the behavior sustains itself."</em>
</div>
""", unsafe_allow_html=True)
