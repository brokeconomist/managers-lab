import streamlit as st
import pandas as pd

def run_step():
    st.header("🏢 Stage 4: Sustainability & Structural Break-Even")
    st.info("Analyzing how fixed costs and inventory carrying costs affect your final net profit.")

    # 1. DYNAMIC SYNC WITH STAGE 0
    # Fetching values directly from session_state
    p = st.session_state.get('price', 100.0)
    vc = st.session_state.get('variable_cost', 60.0)
    q_annual = st.session_state.get('volume', 1000.0)
    
    # Inventory penalty from Stage 2
    liquidity_drain_annual = st.session_state.get('liquidity_drain', 0.0)
    liquidity_drain_monthly = liquidity_drain_annual / 12
    
    # Monthly conversion
    q_monthly = q_annual / 12
    unit_margin = p - vc

    st.write(f"**🔗 Linked to Stage 0:** Annual Volume: {q_annual:,.0f} units | Current Monthly: {q_monthly:,.1f} units")

    # 2. FIXED COSTS INPUTS
    st.subheader("Monthly Operating Obligations")
    col1, col2 = st.columns(2)
    with col1:
        rent = st.number_input("Rent & Utilities (€)", value=1500.0)
        salaries = st.number_input("Salaries & Insurance (€)", value=4500.0)
    with col2:
        loan_payment = st.number_input("Monthly Loan Repayment (€)", value=1000.0)
        other_fixed = st.number_input("Other Admin Costs (€)", value=500.0)

    # 3. CALCULATIONS
    total_monthly_fixed = rent + salaries + other_fixed
    # Operating profit before inventory penalty
    ebit = (unit_margin * q_monthly) - total_monthly_fixed
    
    # Break-Even must cover Fixed Costs + Loan Payments
    total_obligations = total_monthly_fixed + loan_payment
    
    if unit_margin > 0:
        be_units_monthly = total_obligations / unit_margin
    else:
        be_units_monthly = 0

    # Final Net Profit after inventory "Slow-Stock Penalty"
    final_net_profit = ebit - loan_payment - liquidity_drain_monthly

    # 4. RESULTS DISPLAY
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Monthly", f"{q_monthly:,.1f} units")
    c2.metric("Break-Even Needed", f"{be_units_monthly:,.1f} units")
    c3.metric("Final Net Profit", f"{final_net_profit:,.2f} €", delta=f"-{liquidity_drain_monthly:,.2f} Stock Penalty")

    

    # 5. STRATEGIC SIGNAL
    st.divider()
    if q_monthly < be_units_monthly:
        st.error(f"🔴 **Deficit:** You are underperforming by {be_units_monthly - q_monthly:,.1f} units/month to cover all obligations.")
    else:
        st.success(f"🟢 **Surplus:** You are {q_monthly - be_units_monthly:,.1f} units above the survival threshold.")

    if liquidity_drain_monthly > (ebit * 0.15) and ebit > 0:
        st.warning(f"⚠️ **Efficiency Risk:** Slow-moving stock costs consume {(liquidity_drain_monthly/ebit)*100:.1f}% of operating profit.")

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
