import streamlit as st

# 1. COMPREHENSIVE TOOL IMPORTS
try:
    from unit_cost_app import show_unit_cost_app
    from credit_days_calculator import show_credit_days_calculator
    from inventory_turnover_calculator import show_inventory_turnover_calculator
    from financial_resilience_app import show_resilience_map
    from qspm_two_strategies import show_qspm_tool
    from break_even_shift_calculator import show_break_even_shift_calculator
    from clv_calculator import show_clv_calculator
    from pricing_power_radar import show_pricing_power_radar
    from cash_cycle import run_cash_cycle_app
    from credit_policy_app import show_credit_policy_analysis
    from loan_vs_leasing_calculator import loan_vs_leasing_ui
    from cash_fragility_index import show_cash_fragility_index
    from loss_threshold import show_loss_threshold_before_price_cut
except ImportError as e:
    st.error(f"Missing component: {e}")

# --- SETTINGS & STYLE ---
st.set_page_config(page_title="Managers’ Lab", page_icon="🧪", layout="wide")

st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3.2em; font-weight: 600; margin-bottom: 8px; }
    .stMetric { background-color: #ffffff; border: 1px solid #eee; padding: 10px; border-radius: 10px; }
    h1, h2, h3 { color: #0f172a; }
    .sidebar .sidebar-content { background-color: #f8fafc; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "Home"
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧪 Managers’ Lab")
    
    if st.sidebar.button("🏠 Dashboard Home"):
        st.session_state.selected_tool = "Home"
    
    st.divider()
    
    # --- GROUP 1: OPERATIONAL ESSENTIALS (FREE) ---
    st.subheader("📊 Operational Essentials")
    st.caption("Standard Performance Metrics")
    
    # Dictionary to map button names to tool keys
    free_tools = {
        "Unit Cost Calculator": "UnitCost",
        "Accounts Receivable (Credit)": "CreditDays",
        "Inventory Velocity": "Inventory",
        "Break-Even Analysis": "BreakEven",
        "Cash Cycle Calculator": "CashCycle",
        "Loan vs Leasing": "LoanLeasing"
    }
    
    for label, key in free_tools.items():
        if st.sidebar.button(label): st.session_state.selected_tool = key

    st.divider()
    
    # --- GROUP 2: STRATEGIC INTELLIGENCE (PREMIUM) ---
    st.subheader("💎 Strategic Intelligence")
    st.caption("Systemic Risk & Choice Analysis")
    
    premium_tools = {
        "Financial Resilience Map": "Resilience",
        "Strategic Choice (QSPM)": "QSPM",
        "Pricing Power Radar": "PricingPower",
        "CLV & Customer Value": "CLV",
        "Cash Fragility Index": "Fragility",
        "Loss Threshold Analysis": "LossThreshold"
    }

    for label, key in premium_tools.items():
        display_label = label if st.session_state.is_premium else f"🔒 {label}"
        if st.sidebar.button(display_label):
            st.session_state.selected_tool = key

    if not st.session_state.is_premium:
        st.divider()
        st.warning("Strategic Suite Locked")
        if st.sidebar.button("🔓 Unlock 7-Day Pass (€10)", type="primary"):
            st.session_state.is_premium = True
            st.rerun()

# --- MAIN RENDER LOGIC ---

if st.session_state.selected_tool == "Home":
    st.title("🧪 Managers’ Lab")
    st.markdown("""
    ### Systemic Decision Engineering
    Analysis is structured in two tiers: **Operational Efficiency** and **Strategic Survival**.
    Calculations are based on a **365-day fiscal year** as per system constraints.
    """)

    

    c1, c2 = st.columns(2)
    with c1:
        st.info("💡 **Operational Tier:** Focus on margins, cash cycles, and unit economics. These are your baseline survival metrics.")
    with c2:
        st.success("🎯 **Strategic Tier:** Focus on risk absorption, pricing power, and alternative path comparisons.")

# --- ROUTING LOGIC ---

# FREE TOOLS
elif st.session_state.selected_tool == "UnitCost": show_unit_cost_app()
elif st.session_state.selected_tool == "CreditDays": show_credit_days_calculator()
elif st.session_state.selected_tool == "Inventory": show_inventory_turnover_calculator()
elif st.session_state.selected_tool == "BreakEven": show_break_even_shift_calculator()
elif st.session_state.selected_tool == "CashCycle": run_cash_cycle_app()
elif st.session_state.selected_tool == "LoanLeasing": loan_vs_leasing_ui()

# PREMIUM TOOLS (With Access Control)
elif st.session_state.selected_tool in premium_tools.values():
    if not st.session_state.is_premium:
        st.title("🛡️ Strategic Suite Restricted")
        st.markdown("""
        ### Access Required
        This module contains advanced diagnostic tools designed for structural business analysis.
        
        **Your current path requires visibility into:**
        - Systemic Resilience & Breaking Points
        - Pricing Power & Elasticity
        - High-Stakes Strategy Selection (QSPM)
        
        **One-time 7-day access: €10.00**
        """)
        if st.button("Activate Full Access"):
            st.session_state.is_premium = True
            st.rerun()
    else:
        # Actual tool calls
        if st.session_state.selected_tool == "Resilience": show_resilience_map()
        elif st.session_state.selected_tool == "QSPM": show_qspm_tool()
        elif st.session_state.selected_tool == "PricingPower": show_pricing_power_radar()
        elif st.session_state.selected_tool == "CLV": show_clv_calculator()
        elif st.session_state.selected_tool == "Fragility": show_cash_fragility_index()
        elif st.session_state.selected_tool == "LossThreshold": show_loss_threshold_before_price_cut()

# FOOTER
st.divider()
st.caption("Managers’ Lab · Professional Grade · 365-Day Logic")
