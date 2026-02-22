import streamlit as st
import pandas as pd

def run_step():
    st.header("🏢 Stage 4: Sustainability & Structural Break-Even")
    st.info("Analyzing how fixed costs and inventory carrying costs affect your final net profit.")

    def run_step():
    st.header("🏢 Stage 4: Sustainability & Structural Break-Even")

    # 1. DYNAMIC SYNC WITH STAGE 0 (The Fix)
    # Τραβάμε τα δεδομένα απευθείας από το session_state
    p = st.session_state.get('price', 100.0)
    vc = st.session_state.get('variable_cost', 60.0)
    q_annual = st.session_state.get('volume', 1000.0) # Αυτό αλλάζεις στο Stage 0
    
    # Μετατροπή σε μηνιαία βάση για το Break-Even
    q_monthly = q_annual / 12
    unit_margin = p - vc

    st.write(f"**🔗 Linked to Stage 0:** Annual Volume: {q_annual:,.0f} units | Current Monthly: {q_monthly:,.1f} units")

    # 2. FIXED COSTS (Αυτά παραμένουν manual inputs στο Stage 4)
    col1, col2 = st.columns(2)
    with col1:
        rent = st.number_input("Rent & Utilities (€)", value=1500.0)
        salaries = st.number_input("Salaries & Insurance (€)", value=4500.0)
    with col2:
        loan_payment = st.number_input("Monthly Loan Repayment (€)", value=1000.0)
        taxes_buffer = st.slider("Tax Provision %", 0, 40, 22)

    # 3. BREAK-EVEN CALCULATION
    # Το Break-Even πρέπει να καλύπτει Fixed Costs + Loan Payment
    total_monthly_obligations = rent + salaries + 500 + 500 + loan_payment # software/other fixed
    
    if unit_margin > 0:
        be_units_monthly = total_monthly_obligations / unit_margin
    else:
        be_units_monthly = 0

    # 4. RESULTS
    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("Current Monthly Volume", f"{q_monthly:,.1f} units")
    c2.metric("Break-Even Volume", f"{be_units_monthly:,.1f} units", 
              delta=f"{q_monthly - be_units_monthly:,.1f} vs Target", delta_color="normal")

    if q_monthly < be_units_monthly:
        st.error(f"🔴 **Deficit:** You need {be_units_monthly - q_monthly:,.1f} more units per month to break even.")
    else:
        st.success(f"🟢 **Surplus:** You are {q_monthly - be_units_monthly:,.1f} units above the survival threshold.")
    

    # 5. STRATEGIC SIGNAL
    st.divider()
    if liquidity_drain_monthly > (ebit * 0.15) and ebit > 0:
        st.warning(f"⚠️ **Efficiency Risk:** Slow-moving inventory costs consume { (liquidity_drain_monthly/ebit)*100:.1f}% of your operating profit. Your capital is not 'leaking', but it is 'stagnating' significantly.")
    elif ebit <= 0:
        st.error("🔴 **Structural Deficit:** Your unit margin cannot cover even your basic fixed costs, regardless of inventory speed.")

    # 6. NAVIGATION
    st.divider()
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Back to Unit Economics"):
            st.session_state.flow_step = 3
            st.rerun()
    with nav2:
        if st.button("Proceed to Final Strategy (Stage 5) ➡️", type="primary"):
            st.session_state.flow_step = 5
            st.rerun()
