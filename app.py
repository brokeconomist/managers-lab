import streamlit as st

# 1. TOOL IMPORTS
try:
    from unit_cost_app import show_unit_cost_app
    from credit_days_calculator import show_credit_days_calculator
    from inventory_turnover_calculator import show_inventory_turnover_calculator
    from financial_resilience_app import show_resilience_map
    from qspm_two_strategies import show_qspm_tool
except ImportError as e:
    st.error(f"Missing component: {e}")

# --- SETTINGS & STYLE ---
st.set_page_config(page_title="Managers’ Lab", page_icon="🧪", layout="wide")

# Professional Tablet-First CSS
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; font-weight: 600; border: 1px solid #e0e0e0; }
    .stMetric { background-color: #ffffff; border: 1px solid #eee; padding: 15px; border-radius: 12px; }
    .sidebar .sidebar-content { background-color: #fcfcfc; }
    h1, h2, h3 { color: #1e293b; }
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
    st.subheader("📊 Operational Essentials")
    st.caption("Baseline metrics (Free Access)")
    if st.sidebar.button("Unit Cost Calculator"): 
        st.session_state.selected_tool = "UnitCost"
    if st.sidebar.button("Accounts Receivable (Credit)"): 
        st.session_state.selected_tool = "CreditDays"
    if st.sidebar.button("Inventory Velocity"): 
        st.session_state.selected_tool = "Inventory"
    
    st.divider()
    st.subheader("💎 Strategic Intelligence")
    st.caption("Advanced system diagnostics")
    
    res_label = "🛡️ Financial Resilience Map" if st.session_state.is_premium else "🔒 Financial Resilience Map"
    qspm_label = "🧭 Strategic Choice (QSPM)" if st.session_state.is_premium else "🔒 Strategic Choice (QSPM)"
    
    if st.sidebar.button(res_label): 
        st.session_state.selected_tool = "Resilience"
    if st.sidebar.button(qspm_label): 
        st.session_state.selected_tool = "QSPM"
    
    if not st.session_state.is_premium:
        st.info("Full Access: 7-Day Pass (€10)")
        if st.sidebar.button("🔓 Unlock Strategic Suite", type="primary"):
            st.session_state.is_premium = True
            st.rerun()

# --- MAIN DISPLAY LOGIC ---

if st.session_state.selected_tool == "Home":
    st.title("🧪 Managers’ Lab")
    st.markdown("""
    ### Systemic Decision Engineering
    
    Welcome to the Lab. This environment is designed to strip away intuition and replace it with **structural visibility**. 
    Every decision made here follows a cold, analytical path from operational cost to strategic survival.
    
    **Workflow:**
    1. **Operational Audit:** Use the 'Essentials' to verify margins and credit health.
    2. **Resilience Testing:** Unlock 'Strategic Intelligence' to map your system's breaking point under market shocks.
    """)

    
    
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Status", "Active")
    c2.metric("Environment", "Live Analysis")
    c3.metric("System Model", "365-Day Cycle")

elif st.session_state.selected_tool == "UnitCost":
    show_unit_cost_app()

elif st.session_state.selected_tool == "CreditDays":
    show_credit_days_calculator()

elif st.session_state.selected_tool == "Inventory":
    show_inventory_turnover_calculator()

elif st.session_state.selected_tool in ["Resilience", "QSPM"]:
    if not st.session_state.is_premium:
        st.title("🛡️ Strategic Intelligence Suite")
        st.markdown("""
        ### Premium Feature Restricted
        This module provides high-level diagnostics that analyze the **structural integrity** of your business. 
        
        **Unlock includes:**
        - **Resilience Mapping:** Visualizing your position in the survival/efficiency matrix.
        - **Stress Simulation:** Testing cash-flow stability against sudden revenue drops.
        - **Strategic Comparison:** Quantitative evaluation of competing business paths.
        
        **Pass Validity:** 7 Calendar Days  
        **Fee:** €10.00 (Single payment)
        """)
        
        if st.button("Activate 7-Day Strategic Access", type="primary"):
            st.session_state.is_premium = True
            st.rerun()
    else:
        if st.session_state.selected_tool == "Resilience":
            show_resilience_map()
        else:
            show_qspm_tool()

# FOOTER
st.divider()
st.caption("Managers’ Lab · Analytical Rigor · Strategic Survival · 2026")
