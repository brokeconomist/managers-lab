import streamlit as st
import pandas as pd

def run_step():
    st.header("🏢 Stage 4: Sustainability & Structural Break-Even")
    st.info("Analyzing how fixed costs and inventory carrying costs affect your final net profit.")

    # 1. SYNC WITH PREVIOUS STAGES
    p = st.session_state.get('price', 0.0)
    vc = st.session_state.get('variable_cost', 0.0)
    # Monthly volume from annual calibration
    q_monthly = st.session_state.get('volume', 0.0) / 12
    unit_margin = p - vc
    
    # Retrieval of the Liquidity Drain (Carrying Cost) calculated in Stage 2
    # This represents the cost of capital tied up for longer than healthy periods.
    liquidity_drain_annual = st.session_state.get('liquidity_drain', 0.0)
    liquidity_drain_monthly = liquidity_drain_annual / 12

    # 2. FIXED COSTS INPUTS
    st.subheader("Monthly Operating Obligations")
    col1, col2 = st.columns(2)
    
    with col1:
        rent = st.number_input("Rent & Utilities (€)", value=1500.0)
        salaries = st.number_input("Salaries & Insurance (€)", value=4500.0)
        
    with col2:
        software = st.number_input("Software & Admin (€)", value=500.0)
        loan_payment = st.number_input("Monthly Loan Repayment (€)", value=1000.0)

    # 3. CALCULATIONS (Cold Analytical Logic)
    total_fixed_costs = rent + salaries + software
    ebit = (unit_margin * q_monthly) - total_fixed_costs
    
    # Net Profit Calculation
    # We treat the slow-moving stock penalty as an operational expense (Carrying Cost)
    # rather than a structural deficit.
    net_profit_before_drain = ebit - loan_payment
    final_net_profit = net_profit_before_drain - liquidity_drain_monthly

    # 4. RESULTS DISPLAY
    st.divider()
    res1, res2, res3 = st.columns(3)
    
    with res1:
        st.metric("EBIT (Operating)", f"{ebit:,.2f} €")
        st.caption("Operational health before financial costs.")

    with res2:
        # This is your Slow-Moving Penalty
        st.metric("Slow-Stock Penalty", f"-{liquidity_drain_monthly:,.2f} €", delta="Carrying Cost", delta_color="inverse")
        st.caption("The cost of 'frozen' capital over time.")
    
    with res3:
        st.metric("Final Net Profit", f"{final_net_profit:,.2f} €")
        st.caption("Actual cash remaining in your pocket.")

    

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
