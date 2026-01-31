"""
ELBOW ZONE™ | Behavioral Audit Terminal
State-Machine Architecture

© 2026 Russell Barnett. The Elbow Interference Theory™. All Rights Reserved.
"""

import streamlit as st
from dataclasses import dataclass
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ELBOW ZONE™",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# DOMAIN MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ScoreSet:
    """Immutable container for the six behavioral variables."""
    M: int  # Mouthfeel
    E: int  # Emotion
    F: int  # Familiarity
    B: int  # Bites
    K: int  # Kinetic
    C: int  # Cognitive


@dataclass(frozen=True)
class Archetype:
    """Defines a structural archetype with baseline scores and theory."""
    name: str
    description: str
    scores: ScoreSet
    logic: str


# Archetype Constants
ARCHETYPES: dict[str, Archetype] = {
    "Unitized — Denominator Collapse": Archetype(
        name="Unitized — Denominator Collapse",
        description="Handhelds, bars, bites, pouches, single-serve",
        scores=ScoreSet(M=4, E=4, F=4, B=1, K=1, C=1),
        logic="Portion-bound format eliminates decision points. The Elbow finishes before the Head arrives."
    ),
    "Bulk — High Interference Risk": Archetype(
        name="Bulk — High Interference Risk",
        description="Pints, tubs, bags, multi-serve containers",
        scores=ScoreSet(M=5, E=4, F=5, B=4, K=3, C=3),
        logic="Open-ended format requires self-managed stopping. Each bite is a decision point."
    ),
    "Ritual — Habitual Flow": Archetype(
        name="Ritual — Habitual Flow",
        description="Cans, bottles, single-ritual beverages",
        scores=ScoreSet(M=3, E=3, F=5, B=2, K=1, C=1),
        logic="Ritual preservation through familiarity. Cognitive interference is structurally suppressed."
    ),
}

# Variable Metadata
VAR_META: dict[str, tuple[str, str]] = {
    "M": ("Mouthfeel", "Sensory resolution site — how it feels during consumption."),
    "E": ("Emotion", "Rises when expectation is violated and resolved in the body."),
    "F": ("Familiarity", "Comfort that suppresses interference — behavioral autopilot."),
    "B": ("Bites", "Decision count. More bites = more Head Zone risk."),
    "K": ("Kinetic", "Physical work required to continue consuming."),
    "C": ("Cognitive", "The interference point. When the Head arrives, the Elbow slows."),
}

# ═══════════════════════════════════════════════════════════════════════════════
# CORE LOGIC ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_s_score(m: int, e: int, f: int, b: int, k: int, c: int) -> float:
    """
    Calculate the Structural S-Score™.
    
    S = (M × E × F) ÷ (B × K × C)
    
    Numerator: Value Delivered (Mouthfeel × Emotion × Familiarity)
    Denominator: Cost Extracted (Bites × Kinetic × Cognitive)
    """
    numerator = m * e * f
    denominator = b * k * c
    return numerator / denominator


def scores_differ(baseline: ScoreSet, subject: ScoreSet) -> bool:
    """Check if any subject score differs from baseline."""
    return (
        baseline.M != subject.M or
        baseline.E != subject.E or
        baseline.F != subject.F or
        baseline.B != subject.B or
        baseline.K != subject.K or
        baseline.C != subject.C
    )


def validate_rationale(text: str, min_length: int = 25) -> bool:
    """Validate rationale meets minimum meaningful length."""
    return len(text.strip()) > min_length


def get_delta_display(baseline: int, subject: int) -> str:
    """Generate delta display string for amended values."""
    diff = subject - baseline
    if diff == 0:
        return ""
    sign = "+" if diff > 0 else ""
    return f"Δ {sign}{diff} from baseline ({baseline})"


# ═══════════════════════════════════════════════════════════════════════════════
# STATE MACHINE
# ═══════════════════════════════════════════════════════════════════════════════

def init_session_state(archetype: Archetype) -> None:
    """Initialize or reset session state to archetype defaults."""
    st.session_state.baseline = archetype.scores
    st.session_state.subject = ScoreSet(
        M=archetype.scores.M,
        E=archetype.scores.E,
        F=archetype.scores.F,
        B=archetype.scores.B,
        K=archetype.scores.K,
        C=archetype.scores.C,
    )
    st.session_state.rationale = ""
    st.session_state.current_archetype = archetype.name


def sync_archetype_change(selected: str) -> Archetype:
    """Handle archetype selection changes and reset state if needed."""
    archetype = ARCHETYPES[selected]
    
    # Reset state if archetype changed
    if st.session_state.get("current_archetype") != selected:
        init_session_state(archetype)
    
    return archetype


def compute_lock_state(baseline: ScoreSet, subject: ScoreSet, rationale: str) -> bool:
    """Determine if the Subject S-Score should be locked."""
    has_amendments = scores_differ(baseline, subject)
    has_valid_rationale = validate_rationale(rationale)
    
    # Locked if: amendments exist AND rationale is insufficient
    return has_amendments and not has_valid_rationale


# ═══════════════════════════════════════════════════════════════════════════════
# THEME
# ═══════════════════════════════════════════════════════════════════════════════

def inject_theme() -> None:
    """Inject institutional CSS theme."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
        
        .main { background: #FFFFFF; font-family: 'Inter', sans-serif; }
        .stApp { background: #FFFFFF; }
        
        section[data-testid="stSidebar"] {
            background: #FAFAFA;
            border-right: 1px solid #E5E7EB;
        }
        
        h1 { font-weight: 900 !important; font-size: 2.4rem !important; color: #0F172A !important; letter-spacing: -0.03em; }
        h2 { font-weight: 800 !important; font-size: 1.6rem !important; color: #1E293B !important; }
        h3 { font-weight: 700 !important; font-size: 1.2rem !important; color: #334155 !important; }
        
        .stSlider label { font-size: 18px !important; font-weight: 600 !important; color: #1E293B !important; }
        
        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 2px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px;
        }
        
        div[data-testid="stMetric"] label { font-size: 16px !important; font-weight: 700 !important; }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] { 
            font-family: 'JetBrains Mono', monospace !important; 
            font-size: 2.2rem !important; 
        }
        
        .equation-banner {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            color: #F8FAFC;
            padding: 28px 36px;
            border-radius: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.4rem;
            text-align: center;
            margin: 20px 0 28px 0;
            box-shadow: 0 8px 32px rgba(15, 23, 42, 0.15);
        }
        
        .column-header {
            font-size: 1rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 16px 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 16px;
        }
        
        .column-header.baseline { background: #F1F5F9; border: 2px solid #CBD5E1; color: #475569; }
        .column-header.subject { background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(52,211,153,0.05) 100%); border: 2px solid #10B981; color: #059669; }
        
        .delta-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #10B981;
            background: rgba(16,185,129,0.1);
            padding: 4px 10px;
            border-radius: 6px;
            margin-top: 4px;
            display: inline-block;
        }
        
        .locked-metric {
            background: linear-gradient(135deg, #64748B 0%, #94A3B8 100%);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            font-weight: 600;
        }
        
        .score-metric.advantage { border-color: #10B981 !important; }
        .score-metric.risk { border-color: #F87171 !important; }
        
        .stTextArea textarea {
            font-family: 'Inter', sans-serif !important;
            font-size: 15px !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 10px !important;
            padding: 14px !important;
        }
        
        .stTextArea textarea:focus { border-color: #10B981 !important; }
        
        .char-count { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #94A3B8; text-align: right; }
        .char-count.valid { color: #10B981; }
        
        .footer {
            font-size: 12px;
            color: #64748B;
            text-align: center;
            padding: 32px 0;
            border-top: 1px solid #E2E8F0;
            margin-top: 48px;
        }
        
        .watermark {
            position: fixed;
            bottom: 20px;
            right: 20px;
            font-size: 10px;
            font-weight: 800;
            color: rgba(148,163,184,0.3);
            letter-spacing: 0.2em;
            text-transform: uppercase;
            transform: rotate(-5deg);
            pointer-events: none;
        }
    </style>
    <div class="watermark">CONFIDENTIAL</div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def render_sidebar() -> str:
    """Render sidebar and return selected archetype key."""
    with st.sidebar:
        st.markdown("## ◈ ELBOW ZONE™")
        st.caption("Behavioral Audit Terminal")
        
        st.divider()
        
        # File Upload
        st.markdown("### 📊 Data Upload")
        uploaded = st.file_uploader(
            "Circana / MULO CSV",
            type=["csv"],
            help="Upload syndicated data to calibrate Presence vs Persistence"
        )
        
        if uploaded:
            st.success("✓ Data loaded")
        
        st.divider()
        
        # Archetype Selection
        st.markdown("### 🏗️ Structural Archetype")
        selected = st.selectbox(
            "Product Physics",
            options=list(ARCHETYPES.keys()),
            help="Sets the Baseline scores for the audit"
        )
        
        archetype = ARCHETYPES[selected]
        st.caption(archetype.description)
        
        with st.expander("Structural Logic"):
            st.write(archetype.logic)
        
        st.divider()
        
        # Variable Reference
        st.markdown("### 📖 Variables")
        with st.expander("Definitions"):
            for key, (name, desc) in VAR_META.items():
                st.markdown(f"**{key}** · {name}: {desc}")
        
        st.divider()
        
        st.markdown("""
        <div style='text-align:center; font-size:11px; color:#94A3B8;'>
            © 2026 Russell Barnett<br>
            The Elbow Interference Theory™
        </div>
        """, unsafe_allow_html=True)
    
    return selected


def render_slider_with_delta(
    label: str,
    key: str,
    baseline_value: int,
    help_text: str,
    disabled: bool = False
) -> int:
    """Render a slider with optional delta display."""
    value = st.slider(
        label,
        min_value=1,
        max_value=5,
        value=baseline_value,
        key=key,
        help=help_text,
        disabled=disabled
    )
    
    # Show delta if not disabled and value differs
    if not disabled:
        delta_text = get_delta_display(baseline_value, value)
        if delta_text:
            st.markdown(f'<span class="delta-badge">{delta_text}</span>', unsafe_allow_html=True)
    
    return value


def render_baseline_column(baseline: ScoreSet) -> float:
    """Render the Baseline column (read-only)."""
    st.markdown('<div class="column-header baseline">📊 BASELINE</div>', unsafe_allow_html=True)
    st.caption("Category structural norms (locked)")
    
    st.markdown("**NUMERATOR** — Value Delivered")
    render_slider_with_delta(f"M · {VAR_META['M'][0]}", "bl_m", baseline.M, VAR_META['M'][1], disabled=True)
    render_slider_with_delta(f"E · {VAR_META['E'][0]}", "bl_e", baseline.E, VAR_META['E'][1], disabled=True)
    render_slider_with_delta(f"F · {VAR_META['F'][0]}", "bl_f", baseline.F, VAR_META['F'][1], disabled=True)
    
    st.markdown("**DENOMINATOR** — Cost Extracted")
    render_slider_with_delta(f"B · {VAR_META['B'][0]}", "bl_b", baseline.B, VAR_META['B'][1], disabled=True)
    render_slider_with_delta(f"K · {VAR_META['K'][0]}", "bl_k", baseline.K, VAR_META['K'][1], disabled=True)
    render_slider_with_delta(f"C · {VAR_META['C'][0]}", "bl_c", baseline.C, VAR_META['C'][1], disabled=True)
    
    s_baseline = calculate_s_score(baseline.M, baseline.E, baseline.F, baseline.B, baseline.K, baseline.C)
    
    st.markdown("---")
    st.metric("Baseline S-Score™", f"{s_baseline:.2f}")
    
    return s_baseline


def render_subject_column(baseline: ScoreSet) -> tuple[ScoreSet, str]:
    """Render the Subject column (editable) and return current values + rationale."""
    st.markdown('<div class="column-header subject">🎯 SUBJECT</div>', unsafe_allow_html=True)
    st.caption("Adjust to model your Subject's structure")
    
    st.markdown("**NUMERATOR** — Value Delivered")
    m = render_slider_with_delta(f"M · {VAR_META['M'][0]}", "su_m", baseline.M, VAR_META['M'][1])
    e = render_slider_with_delta(f"E · {VAR_META['E'][0]}", "su_e", baseline.E, VAR_META['E'][1])
    f = render_slider_with_delta(f"F · {VAR_META['F'][0]}", "su_f", baseline.F, VAR_META['F'][1])
    
    st.markdown("**DENOMINATOR** — Cost Extracted")
    b = render_slider_with_delta(f"B · {VAR_META['B'][0]}", "su_b", baseline.B, VAR_META['B'][1])
    k = render_slider_with_delta(f"K · {VAR_META['K'][0]}", "su_k", baseline.K, VAR_META['K'][1])
    c = render_slider_with_delta(f"C · {VAR_META['C'][0]}", "su_c", baseline.C, VAR_META['C'][1])
    
    subject = ScoreSet(M=m, E=e, F=f, B=b, K=k, C=c)
    
    # Rationale input (only show if amendments exist)
    rationale = ""
    has_amendments = scores_differ(baseline, subject)
    
    if has_amendments:
        st.markdown("---")
        st.markdown("**📝 Strategic Rationale**")
        st.caption("Explain amendments to unlock the Subject S-Score (>25 chars)")
        
        rationale = st.text_area(
            "Rationale",
            value=st.session_state.get("rationale", ""),
            placeholder="Describe the structural reasoning behind your amendments...",
            label_visibility="collapsed",
            key="rationale_input"
        )
        st.session_state.rationale = rationale
        
        char_count = len(rationale.strip())
        is_valid = char_count > 25
        css_class = "char-count valid" if is_valid else "char-count"
        st.markdown(f'<div class="{css_class}">{char_count} / 25 characters</div>', unsafe_allow_html=True)
    
    return subject, rationale


def render_subject_score(
    subject: ScoreSet,
    s_baseline: float,
    is_locked: bool
) -> Optional[float]:
    """Render the Subject S-Score metric (locked or calculated)."""
    st.markdown("---")
    
    if is_locked:
        st.markdown("""
        <div class="locked-metric">
            JUSTIFICATION REQUIRED
        </div>
        """, unsafe_allow_html=True)
        return None
    
    s_subject = calculate_s_score(subject.M, subject.E, subject.F, subject.B, subject.K, subject.C)
    delta = s_subject - s_baseline
    
    st.metric("Subject S-Score™", f"{s_subject:.2f}", delta=round(delta, 2))
    
    return s_subject


def render_verdict(
    s_baseline: float,
    s_subject: Optional[float],
    subject: ScoreSet,
    rationale: str
) -> None:
    """Render the Strategic Verdict section."""
    st.markdown("---")
    st.markdown("## 📋 Strategic Verdict")
    
    if s_subject is None:
        st.warning("**Analysis Locked** — Provide strategic rationale for your amendments to unlock.")
        return
    
    delta = s_subject - s_baseline
    efficiency = ((s_subject / s_baseline) - 1) * 100 if s_baseline > 0 else 0
    
    # Summary Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Baseline", f"{s_baseline:.2f}")
    c2.metric("Subject", f"{s_subject:.2f}", delta=round(delta, 2))
    c3.metric("Efficiency", f"{efficiency:+.1f}%")
    
    st.markdown("---")
    st.markdown("### 🧠 AI Analyst Synthesis")
    
    # Verdict Logic (functional approach - no nested ifs)
    is_high_cognitive = subject.C >= 4
    is_structural_risk = delta < 0
    
    verdict_type, verdict_body = generate_verdict(
        s_baseline, s_subject, delta, subject, rationale,
        is_high_cognitive, is_structural_risk
    )
    
    st.markdown(verdict_body)
    
    # Persistence Status
    st.markdown("---")
    st.markdown("### Persistence Status")
    
    denom_avg = (subject.B + subject.K + subject.C) / 3
    persistence_achieved = denom_avg <= 1.5
    
    if persistence_achieved:
        st.success("✓ **Denominator Collapse Achieved** — Structural Persistence is built into the format.")
    else:
        st.warning("⚡ **Velocity is currently purchased** — Structural Persistence unproven until Denominator Collapse.")
    
    st.info("💡 *This signal measures Persistence (Repeat) not Presence (Trial).*")


def generate_verdict(
    s_baseline: float,
    s_subject: float,
    delta: float,
    subject: ScoreSet,
    rationale: str,
    is_high_cognitive: bool,
    is_structural_risk: bool
) -> tuple[str, str]:
    """Generate verdict text based on analysis state."""
    
    rationale_text = f'\n\n**Analyst Rationale:** *"{rationale}"*' if rationale.strip() else ""
    
    if is_high_cognitive:
        return ("analysis", f"""
⚠️ **FURTHER ANALYSIS REQUIRED**

High Cognitive Interference (C = {subject.C}) indicates the **Head Zone arrives before the occasion concludes**.

The consumer's automatic behavior (Elbow Zone) is interrupted by deliberate processing. 
This represents a structural barrier to repeat — each instance requires conscious re-evaluation.
{rationale_text}

*Recommendation: Investigate whether value justifies cognitive cost, or reposition to reduce Head Zone trigger.*
""")
    
    if is_structural_risk:
        return ("risk", f"""
🔴 **STRUCTURAL RISK DETECTED**

Subject S-Score ({s_subject:.2f}) trails Baseline ({s_baseline:.2f}) by **{abs(delta):.2f} points**.

The Subject's Denominator creates more interference points than category norm.
The Elbow slows earlier, allowing the Head to arrive and evaluate.

**Persistence:** Unproven. Without Denominator Collapse, velocity must be purchased through marketing.
{rationale_text}
""")
    
    return ("advantage", f"""
🟢 **STRUCTURAL ADVANTAGE CONFIRMED**

Subject S-Score ({s_subject:.2f}) exceeds Baseline ({s_baseline:.2f}) by **{delta:.2f} points**.

The Subject's physical structure supports automatic repeat behavior.
Consumption completes before cognitive interference triggers the Head Zone.

**Persistence:** Structurally embedded — the format does the work.
{rationale_text}
""")


def render_footer() -> None:
    """Render the footer."""
    st.markdown("""
    <div class="footer">
        <strong>ELBOW ZONE™</strong> | Behavioral Audit Terminal<br>
        © 2026 Russell Barnett. The Elbow Interference Theory™. All Rights Reserved.<br><br>
        <em>"When the Head arrives, the Elbow slows."</em>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Main application entry point."""
    
    # 1. Inject Theme
    inject_theme()
    
    # 2. Render Sidebar & Get Selected Archetype
    selected_archetype_key = render_sidebar()
    
    # 3. Sync State Machine with Archetype Selection
    archetype = sync_archetype_change(selected_archetype_key)
    baseline = archetype.scores
    
    # 4. Render Header
    st.markdown("# ELBOW ZONE™")
    st.caption("Strategic Behavioral Audit Terminal")
    
    # 5. Equation Banner
    st.markdown("""
    <div class="equation-banner">
        <div style="font-size: 0.9rem; opacity: 0.7; letter-spacing: 0.1em; margin-bottom: 8px;">
            THE SATISFACTION EQUATION
        </div>
        <div style="font-size: 1.8rem; font-weight: 600;">
            S = (M × E × F) ÷ (B × K × C)
        </div>
        <div style="font-size: 0.85rem; opacity: 0.6; margin-top: 8px;">
            Value Delivered ÷ Cost Extracted = Structural Persistence
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Active Archetype:** {archetype.name}")
    
    # 6. Dual-Column Layout
    col_baseline, col_subject = st.columns(2)
    
    with col_baseline:
        s_baseline = render_baseline_column(baseline)
    
    with col_subject:
        subject, rationale = render_subject_column(baseline)
        
        # Compute Lock State
        is_locked = compute_lock_state(baseline, subject, rationale)
        
        # Render Subject Score
        s_subject = render_subject_score(subject, s_baseline, is_locked)
    
    # 7. Strategic Verdict
    render_verdict(s_baseline, s_subject, subject, rationale)
    
    # 8. Footer
    render_footer()


# Entry Point
if __name__ == "__main__":
    main()
