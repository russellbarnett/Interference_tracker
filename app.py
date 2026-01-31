import streamlit as st
import pandas as pd

# ═══════════════════════════════════════════════════════════════════════════════
# 1. ENLIGHTENED LABORATORY THEME
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="ELBOW ZONE™ Terminal", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500;600;700&display=swap');
    
    .main { background-color: #F8F9FA; color: #212529; font-family: 'Inter', sans-serif; }
    
    /* ENLARGED FONTS */
    .stSlider label { font-size: 18px !important; font-weight: 600 !important; color: #374151 !important; }
    .stTextInput label { font-size: 16px !important; font-weight: 600 !important; color: #374151 !important; }
    .stTextArea label { font-size: 16px !important; font-weight: 600 !important; }
    .stSelectbox label { font-size: 16px !important; font-weight: 600 !important; }
    div[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #dee2e6; }
    h1 { font-size: 32px !important; }
    h2 { font-size: 26px !important; }
    h3 { font-size: 22px !important; }
    p, .stMarkdown { font-size: 16px !important; }
    
    /* Equation Banner */
    .equation-banner {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 2px solid #3B82F6;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .equation-title {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #1E40AF;
        margin-bottom: 0.75rem;
    }
    .equation-text {
        font-family: 'Roboto Mono', monospace;
        font-size: 20px;
        color: #1E3A8A;
    }
    .equation-labels {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #3B82F6;
        margin-top: 0.75rem;
    }
    
    /* Archetype Card */
    .archetype-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.75rem 0;
    }
    .archetype-detected {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 2px solid #10B981;
    }
    .archetype-label {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #065F46;
    }
    .archetype-seeds {
        font-family: 'Roboto Mono', monospace;
        font-size: 14px;
        color: #059669;
        margin-top: 0.5rem;
    }
    
    /* Column Headers */
    .column-header {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 1.25rem;
        text-align: center;
    }
    .incumbent-header {
        background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
        color: #374151;
        border: 2px solid #9CA3AF;
    }
    .subject-header {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        color: #065F46;
        border: 2px solid #10B981;
    }
    
    /* Baseline Ghost Label */
    .baseline-ghost {
        font-family: 'Roboto Mono', monospace;
        font-size: 13px;
        color: #9CA3AF;
        background: #F3F4F6;
        padding: 4px 10px;
        border-radius: 6px;
        margin-left: 8px;
    }
    
    /* Amendment States */
    .amendment-unlocked {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        font-weight: 700;
        color: #059669;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .justification-required {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border: 2px solid #F59E0B;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }
    .warning-text {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: #92400E;
    }
    
    /* S-Score Cards */
    .sscore-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.75rem;
        text-align: center;
        margin: 1.25rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .sscore-incumbent { border-top: 5px solid #6B7280; }
    .sscore-subject { border-top: 5px solid #10B981; }
    .sscore-locked { border-top: 5px solid #F59E0B; }
    
    .sscore-value {
        font-family: 'Roboto Mono', monospace;
        font-size: 56px;
        font-weight: 700;
    }
    .sscore-value-incumbent { color: #374151; }
    .sscore-value-subject { color: #059669; }
    .sscore-value-locked { color: #F59E0B; }
    
    .sscore-label {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6B7280;
        margin-top: 0.5rem;
    }
    
    /* AI Terminal */
    .ai-terminal {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 2px solid #10B981;
        border-radius: 12px;
        padding: 1.75rem;
        margin: 1.75rem 0;
    }
    .ai-terminal-header {
        font-family: 'Roboto Mono', monospace;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: #065F46;
        text-transform: uppercase;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(16, 185, 129, 0.3);
    }
    .ai-terminal-content {
        font-family: 'Inter', sans-serif;
        font-size: 17px;
        line-height: 1.8;
        color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. UNIVERSAL ARCHETYPE ENGINE - Structure Seeds
# ═══════════════════════════════════════════════════════════════════════════════

STRUCTURE_SEEDS = {
    "Unitized / Portion-Bound": {
        "description": "Bars, Bites, Pouches, Single-Serve",
        "seeds": {"B": 1, "K": 1, "C": 2, "M": 4, "E": 4, "F": 3},
        "logic": "Denominator Collapse — portion-bound format eliminates decision points"
    },
    "Open-Ended / Bulk": {
        "description": "Bags of Chips, Tubs, Multi-Serve, Pints",
        "seeds": {"B": 5, "K": 3, "C": 3, "M": 5, "E": 4, "F": 5},
        "logic": "High Interference Risk — self-managed stopping creates Head Zone exposure"
    },
    "Ritual-Based": {
        "description": "Cans, Bottles, Beverages",
        "seeds": {"B": 1, "K": 1, "C": 1, "M": 3, "E": 4, "F": 5},
        "logic": "Ritual Preservation — familiar motion suppresses cognitive interference"
    }
}

def categorize_brand(brand_name: str, df: pd.DataFrame = None) -> str:
    """
    Dynamic Brand Lookup:
    1. Check CSV for category if available
    2. Fall back to keyword-based categorization
    """
    brand_lower = brand_name.lower()
    
    # Check CSV first
    if df is not None and not df.empty:
        # Look for brand/product columns
        for col in ['Brand', 'brand', 'Product', 'product', 'Name', 'name']:
            if col in df.columns:
                matches = df[df[col].astype(str).str.lower().str.contains(brand_lower, na=False)]
                if not matches.empty:
                    # Check for category column
                    for cat_col in ['Category', 'category', 'Type', 'type', 'Structure', 'structure']:
                        if cat_col in df.columns:
                            category = matches.iloc[0][cat_col]
                            if 'unit' in str(category).lower() or 'portion' in str(category).lower() or 'bar' in str(category).lower():
                                return "Unitized / Portion-Bound"
                            elif 'bulk' in str(category).lower() or 'bag' in str(category).lower() or 'tub' in str(category).lower():
                                return "Open-Ended / Bulk"
                            elif 'bev' in str(category).lower() or 'drink' in str(category).lower() or 'can' in str(category).lower():
                                return "Ritual-Based"
    
    # Keyword-based categorization (LLM simulation)
    unitized_keywords = ['mochi', 'bite', 'bar', 'snack', 'pouch', 'pack', 'piece', 'truffle', 'ball', 'pop', 'cookie', 'cracker']
    bulk_keywords = ['pint', 'tub', 'bag', 'chip', 'ice cream', 'legacy', 'family', 'share', 'multi']
    ritual_keywords = ['soda', 'pop', 'drink', 'water', 'juice', 'tea', 'coffee', 'can', 'bottle', 'sparkling', 'refreshment']
    
    for kw in unitized_keywords:
        if kw in brand_lower:
            return "Unitized / Portion-Bound"
    
    for kw in bulk_keywords:
        if kw in brand_lower:
            return "Open-Ended / Bulk"
    
    for kw in ritual_keywords:
        if kw in brand_lower:
            return "Ritual-Based"
    
    return "Open-Ended / Bulk"  # Default

# ═══════════════════════════════════════════════════════════════════════════════
# 3. SIDEBAR - DATA UPLOAD & STRUCTURE SELECTOR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.title("ELBOW ZONE™")
    st.markdown("### Universal Hunter Engine")
    
    st.divider()
    
    st.header("Institutional Data Feed")
    uploaded_file = st.file_uploader("Drop Circana/MULO CSV here", type=["csv"])
    
    df_uploaded = None
    if uploaded_file:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            st.success(f"✓ Loaded {len(df_uploaded)} rows")
            st.dataframe(df_uploaded.head(3), use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.divider()
    
    st.markdown("### Product Structure")
    structure_override = st.selectbox(
        "Manual Override (Optional)",
        options=["Auto-Detect"] + list(STRUCTURE_SEEDS.keys()),
        help="Select a structure to override auto-detection, or leave on Auto-Detect"
    )
    
    st.divider()
    st.info("© 2026 Russell Barnett. The Elbow Interference Theory™")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. HEADER & EQUATION BANNER
# ═══════════════════════════════════════════════════════════════════════════════

st.title("Strategic Behavioral Audit")

# EQUATION BANNER - Visual Reminder
st.markdown('''
<div class="equation-banner">
    <div class="equation-title">The Satisfaction Equation</div>
    <div class="equation-text">S = (M × E × F) ÷ (B × K × C)</div>
    <div class="equation-labels">
        <strong>Value Delivered</strong> (Numerator): Mouthfeel × Emotion × Familiarity<br>
        <strong>Cost Extracted</strong> (Denominator): Bites × Kinetic × Cognitive
    </div>
</div>
''', unsafe_allow_html=True)

st.caption("The S-Score™ is a relative metric. It measures persistence ONLY in the context of this head-to-head comparison.")

# Initialize session state
if 'justifications' not in st.session_state:
    st.session_state.justifications = {}

# Variable tooltips
TOOLTIPS = {
    'M': "MOUTHFEEL: How the product feels in the mouth during consumption. The primary site of embodied resolution.",
    'E': "EMOTION: The feeling created during consumption. Rises when expectation is violated and resolved immediately (Managed Violation).",
    'F': "FAMILIARITY: Comfort that suppresses interference. The elbow already knows the motion.",
    'B': "BITES: The number of decisions made before the occasion ends. More bites = more Head Zone risk.",
    'K': "KINETIC: The physical work required to continue consuming. Scooping, unwrapping, repositioning.",
    'C': "COGNITIVE: The interference point. High when a product asks the consumer to think—the Head Zone arrival."
}

# ═══════════════════════════════════════════════════════════════════════════════
# 5. DUAL-COLUMN SCORING AUDIT
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()

col_incumbent, col_subject = st.columns(2)

# ─────────────────────────────────────────────────────────────────────────────
# COLUMN 1: THE HABIT (Incumbent) - Fully Editable Baseline
# ─────────────────────────────────────────────────────────────────────────────

with col_incumbent:
    st.markdown('<div class="column-header incumbent-header">THE HABIT (Incumbent)</div>', unsafe_allow_html=True)
    st.caption("Set the baseline comparison. This defines the competitive benchmark.")
    
    brand_inc = st.text_input("Incumbent Brand", "Legacy Pint", key="brand_inc")
    
    # Auto-detect or use override
    if structure_override == "Auto-Detect":
        detected_structure_inc = categorize_brand(brand_inc, df_uploaded)
    else:
        detected_structure_inc = structure_override
    
    seeds_inc = STRUCTURE_SEEDS[detected_structure_inc]
    
    st.markdown(f'''
    <div class="archetype-card archetype-detected">
        <div class="archetype-label">Archetype: {detected_structure_inc}</div>
        <div class="archetype-seeds">{seeds_inc["logic"]}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("**NUMERATOR (Value Delivered)**")
    M_inc = st.slider("Mouthfeel (M)", 1, 5, seeds_inc["seeds"]["M"], key="M_inc", help=TOOLTIPS['M'])
    E_inc = st.slider("Emotion (E)", 1, 5, seeds_inc["seeds"]["E"], key="E_inc", help=TOOLTIPS['E'])
    F_inc = st.slider("Familiarity (F)", 1, 5, seeds_inc["seeds"]["F"], key="F_inc", help=TOOLTIPS['F'])
    
    st.markdown("**DENOMINATOR (Cost Extracted)**")
    B_inc = st.slider("Bites (B)", 1, 5, seeds_inc["seeds"]["B"], key="B_inc", help=TOOLTIPS['B'])
    K_inc = st.slider("Kinetic (K)", 1, 5, seeds_inc["seeds"]["K"], key="K_inc", help=TOOLTIPS['K'])
    C_inc = st.slider("Cognitive (C)", 1, 5, seeds_inc["seeds"]["C"], key="C_inc", help=TOOLTIPS['C'])
    
    # Calculate Incumbent S-Score
    num_inc = M_inc * E_inc * F_inc
    den_inc = B_inc * K_inc * C_inc
    s_inc = num_inc / den_inc
    
    st.markdown(f'''
    <div class="sscore-card sscore-incumbent">
        <div class="sscore-label">Incumbent S-Score</div>
        <div class="sscore-value sscore-value-incumbent">{s_inc:.2f}</div>
        <div style="font-size: 13px; color: #6B7280; margin-top: 8px;">
            ({M_inc}×{E_inc}×{F_inc}) ÷ ({B_inc}×{K_inc}×{C_inc})
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# COLUMN 2: THE SUBJECT (Amendment) - Mirror of Column 1, Locked Until Justified
# ─────────────────────────────────────────────────────────────────────────────

with col_subject:
    st.markdown('<div class="column-header subject-header">THE SUBJECT (Amendment)</div>', unsafe_allow_html=True)
    st.caption("Override baseline with strategic intelligence. 15+ character justification required.")
    
    brand_subj = st.text_input("Subject Brand", "My/Mochi", key="brand_subj")
    
    # Auto-detect structure for subject
    if structure_override == "Auto-Detect":
        detected_structure_subj = categorize_brand(brand_subj, df_uploaded)
    else:
        detected_structure_subj = structure_override
    
    seeds_subj = STRUCTURE_SEEDS[detected_structure_subj]
    
    st.markdown(f'''
    <div class="archetype-card archetype-detected">
        <div class="archetype-label">Archetype: {detected_structure_subj}</div>
        <div class="archetype-seeds">{seeds_subj["logic"]}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Track valid amendments
    valid_amendments = {}
    MIN_JUSTIFICATION_LENGTH = 15
    
    st.markdown("**NUMERATOR (Value Delivered)**")
    
    # M - Mouthfeel (Mirror Column 1)
    st.markdown(f'Mouthfeel (M) <span class="baseline-ghost">Baseline: {M_inc}</span>', unsafe_allow_html=True)
    M_subj = st.slider("Mouthfeel (M)", 1, 5, M_inc, key="M_subj", help=TOOLTIPS['M'], label_visibility="collapsed")
    if M_subj != M_inc:
        just_M = st.text_input("↳ Strategic Rationale for M:", key="just_M", 
                               placeholder=f"Min {MIN_JUSTIFICATION_LENGTH} characters required...")
        clean_just = just_M.strip() if just_M else ""
        if len(clean_just) >= MIN_JUSTIFICATION_LENGTH:
            st.markdown('<div class="amendment-unlocked">✓ AMENDMENT UNLOCKED</div>', unsafe_allow_html=True)
            valid_amendments['M'] = True
            st.session_state.justifications['M'] = clean_just
        else:
            st.markdown(f'''
            <div class="justification-required">
                <div class="warning-text">⚠️ Justification Required ({len(clean_just)}/{MIN_JUSTIFICATION_LENGTH} chars)</div>
            </div>
            ''', unsafe_allow_html=True)
            valid_amendments['M'] = False
    else:
        valid_amendments['M'] = True
        st.session_state.justifications.pop('M', None)
    
    # E - Emotion
    st.markdown(f'Emotion (E) <span class="baseline-ghost">Baseline: {E_inc}</span>', unsafe_allow_html=True)
    E_subj = st.slider("Emotion (E)", 1, 5, E_inc, key="E_subj", help=TOOLTIPS['E'], label_visibility="collapsed")
    if E_subj != E_inc:
        just_E = st.text_input("↳ Strategic Rationale for E:", key="just_E",
                               placeholder=f"Min {MIN_JUSTIFICATION_LENGTH} characters required...")
        clean_just = just_E.strip() if just_E else ""
        if len(clean_just) >= MIN_JUSTIFICATION_LENGTH:
            st.markdown('<div class="amendment-unlocked">✓ AMENDMENT UNLOCKED</div>', unsafe_allow_html=True)
            valid_amendments['E'] = True
            st.session_state.justifications['E'] = clean_just
        else:
            st.markdown(f'''
            <div class="justification-required">
                <div class="warning-text">⚠️ Justification Required ({len(clean_just)}/{MIN_JUSTIFICATION_LENGTH} chars)</div>
            </div>
            ''', unsafe_allow_html=True)
            valid_amendments['E'] = False
    else:
        valid_amendments['E'] = True
        st.session_state.justifications.pop('E', None)
    
    # F - Familiarity
    st.markdown(f'Familiarity (F) <span class="baseline-ghost">Baseline: {F_inc}</span>', unsafe_allow_html=True)
    F_subj = st.slider("Familiarity (F)", 1, 5, F_inc, key="F_subj", help=TOOLTIPS['F'], label_visibility="collapsed")
    if F_subj != F_inc:
        just_F = st.text_input("↳ Strategic Rationale for F:", key="just_F",
                               placeholder=f"Min {MIN_JUSTIFICATION_LENGTH} characters required...")
        clean_just = just_F.strip() if just_F else ""
        if len(clean_just) >= MIN_JUSTIFICATION_LENGTH:
            st.markdown('<div class="amendment-unlocked">✓ AMENDMENT UNLOCKED</div>', unsafe_allow_html=True)
            valid_amendments['F'] = True
            st.session_state.justifications['F'] = clean_just
        else:
            st.markdown(f'''
            <div class="justification-required">
                <div class="warning-text">⚠️ Justification Required ({len(clean_just)}/{MIN_JUSTIFICATION_LENGTH} chars)</div>
            </div>
            ''', unsafe_allow_html=True)
            valid_amendments['F'] = False
    else:
        valid_amendments['F'] = True
        st.session_state.justifications.pop('F', None)
    
    st.markdown("**DENOMINATOR (Cost Extracted)**")
    
    # B - Bites
    st.markdown(f'Bites (B) <span class="baseline-ghost">Baseline: {B_inc}</span>', unsafe_allow_html=True)
    B_subj = st.slider("Bites (B)", 1, 5, B_inc, key="B_subj", help=TOOLTIPS['B'], label_visibility="collapsed")
    if B_subj != B_inc:
        just_B = st.text_input("↳ Strategic Rationale for B:", key="just_B",
                               placeholder=f"Min {MIN_JUSTIFICATION_LENGTH} characters required...")
        clean_just = just_B.strip() if just_B else ""
        if len(clean_just) >= MIN_JUSTIFICATION_LENGTH:
            st.markdown('<div class="amendment-unlocked">✓ AMENDMENT UNLOCKED</div>', unsafe_allow_html=True)
            valid_amendments['B'] = True
            st.session_state.justifications['B'] = clean_just
        else:
            st.markdown(f'''
            <div class="justification-required">
                <div class="warning-text">⚠️ Justification Required ({len(clean_just)}/{MIN_JUSTIFICATION_LENGTH} chars)</div>
            </div>
            ''', unsafe_allow_html=True)
            valid_amendments['B'] = False
    else:
        valid_amendments['B'] = True
        st.session_state.justifications.pop('B', None)
    
    # K - Kinetic
    st.markdown(f'Kinetic (K) <span class="baseline-ghost">Baseline: {K_inc}</span>', unsafe_allow_html=True)
    K_subj = st.slider("Kinetic (K)", 1, 5, K_inc, key="K_subj", help=TOOLTIPS['K'], label_visibility="collapsed")
    if K_subj != K_inc:
        just_K = st.text_input("↳ Strategic Rationale for K:", key="just_K",
                               placeholder=f"Min {MIN_JUSTIFICATION_LENGTH} characters required...")
        clean_just = just_K.strip() if just_K else ""
        if len(clean_just) >= MIN_JUSTIFICATION_LENGTH:
            st.markdown('<div class="amendment-unlocked">✓ AMENDMENT UNLOCKED</div>', unsafe_allow_html=True)
            valid_amendments['K'] = True
            st.session_state.justifications['K'] = clean_just
        else:
            st.markdown(f'''
            <div class="justification-required">
                <div class="warning-text">⚠️ Justification Required ({len(clean_just)}/{MIN_JUSTIFICATION_LENGTH} chars)</div>
            </div>
            ''', unsafe_allow_html=True)
            valid_amendments['K'] = False
    else:
        valid_amendments['K'] = True
        st.session_state.justifications.pop('K', None)
    
    # C - Cognitive
    st.markdown(f'Cognitive (C) <span class="baseline-ghost">Baseline: {C_inc}</span>', unsafe_allow_html=True)
    C_subj = st.slider("Cognitive (C)", 1, 5, C_inc, key="C_subj", help=TOOLTIPS['C'], label_visibility="collapsed")
    if C_subj != C_inc:
        just_C = st.text_input("↳ Strategic Rationale for C:", key="just_C",
                               placeholder=f"Min {MIN_JUSTIFICATION_LENGTH} characters required...")
        clean_just = just_C.strip() if just_C else ""
        if len(clean_just) >= MIN_JUSTIFICATION_LENGTH:
            st.markdown('<div class="amendment-unlocked">✓ AMENDMENT UNLOCKED</div>', unsafe_allow_html=True)
            valid_amendments['C'] = True
            st.session_state.justifications['C'] = clean_just
        else:
            st.markdown(f'''
            <div class="justification-required">
                <div class="warning-text">⚠️ Justification Required ({len(clean_just)}/{MIN_JUSTIFICATION_LENGTH} chars)</div>
            </div>
            ''', unsafe_allow_html=True)
            valid_amendments['C'] = False
    else:
        valid_amendments['C'] = True
        st.session_state.justifications.pop('C', None)
    
    # ─────────────────────────────────────────────────────────────────────────
    # LOCK LOGIC: S-Score shows "?" until all amendments are valid
    # ─────────────────────────────────────────────────────────────────────────
    
    all_valid = all(valid_amendments.values())
    
    if all_valid:
        num_subj = M_subj * E_subj * F_subj
        den_subj = B_subj * K_subj * C_subj
        s_subj = num_subj / den_subj
        
        st.markdown(f'''
        <div class="sscore-card sscore-subject">
            <div class="sscore-label">Subject S-Score</div>
            <div class="sscore-value sscore-value-subject">{s_subj:.2f}</div>
            <div style="font-size: 13px; color: #059669; margin-top: 8px;">
                ({M_subj}×{E_subj}×{F_subj}) ÷ ({B_subj}×{K_subj}×{C_subj})
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        s_subj = None  # Locked
        
        st.markdown('''
        <div class="sscore-card sscore-locked">
            <div class="sscore-label">Subject S-Score</div>
            <div class="sscore-value sscore-value-locked">?</div>
            <div style="font-size: 13px; color: #92400E; margin-top: 8px;">
                Complete all justifications to unlock
            </div>
        </div>
        ''', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. DELTA ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()
st.subheader("Delta Analysis")

if all_valid and s_subj is not None:
    delta = s_subj - s_inc
    pct_delta = ((s_subj - s_inc) / s_inc) * 100 if s_inc > 0 else 0
    
    res1, res2, res3 = st.columns(3)
    res1.metric(f"{brand_inc} (Incumbent)", f"{s_inc:.2f}")
    res2.metric(f"{brand_subj} (Subject)", f"{s_subj:.2f}", delta=round(delta, 2))
    res3.metric("Efficiency Gap", f"{pct_delta:+.0f}%")
else:
    st.warning("⚠️ **Delta Analysis Locked** — Complete all required justifications (15+ chars each) to unlock comparison.")
    delta = 0

st.info("**Reminder:** The S-Score™ measures **Cost Extracted vs Value Delivered** in this specific competitive context.")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. AI ANALYST VERDICT
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()
st.subheader("AI Analyst Verdict")

active_justifications = {k: v for k, v in st.session_state.justifications.items() if v}
justification_summary = ""
if active_justifications:
    justification_summary = "**Expert Amendments:** " + " | ".join([f"{k}: {v}" for k, v in active_justifications.items()])

user_notes = st.text_area("Additional Analyst Notes:", 
                          placeholder="e.g., Price friction at $7.99 is forcing the Head Zone to arrive prematurely...",
                          height=100)

if st.button("Synthesize Investment Memo", type="primary", disabled=not all_valid):
    if all_valid and s_subj is not None:
        if delta > 0:
            verdict_type = "STRUCTURAL ADVANTAGE"
            verdict_detail = f"**{brand_subj}** ({detected_structure_subj}) demonstrates superior repeat efficiency vs **{brand_inc}** ({detected_structure_inc}). The S-Score delta of +{delta:.2f} indicates the Elbow completes its motion before the Head arrives."
        elif delta < 0:
            verdict_type = "STRUCTURAL RISK"
            verdict_detail = f"**{brand_subj}** ({detected_structure_subj}) faces structural headwinds against **{brand_inc}** ({detected_structure_inc}). The S-Score deficit of {abs(delta):.2f} suggests the Cost Extracted exceeds Value Delivered, inviting the Head Zone too early."
        else:
            verdict_type = "STRUCTURAL PARITY"
            verdict_detail = f"**{brand_subj}** and **{brand_inc}** show equivalent structural persistence. Differentiation will be determined by execution, not format architecture."
        
        memo_parts = [verdict_detail]
        if justification_summary:
            memo_parts.append(justification_summary)
        if user_notes:
            memo_parts.append(f"**Analyst Intelligence:** {user_notes}")
        
        full_memo = "\n\n".join(memo_parts)
        
        st.markdown(f'''
        <div class="ai-terminal">
            <div class="ai-terminal-header">🔬 AI Strategic Memo · {verdict_type}</div>
            <div class="ai-terminal-content">{full_memo}</div>
        </div>
        ''', unsafe_allow_html=True)
