import streamlit as st
import plotly.graph_objects as go

def run_step():
    st.header("📉 Stage 1: Break-Even Analysis")
    st.info("Calculates the minimum volume needed to cover all variable and fixed costs.")

    # 1. DYNAMIC SYNC WITH STAGE 0
    # We fetch the latest values directly from session_state to ensure updates flow through
    price = st.session_state.get('price', 0.0)
    variable_cost = st.session_state.get('variable_cost', 0.0)
    current_annual_volume = st.session_state.get('volume', 0.0)
    
    # 2. DATA INTEGRITY CHECK
    if price <= 0 or current_annual_volume <= 0:
        st.error("⚠️ Data Missing: Please return to Stage 0 (Calibration) to set Price and Volume.")
        if st.button("⬅️ Back to Stage 0"):
            st.session_state.flow_step = 0
            st.rerun()
        return

    st.write(f"**🔗 Linked to Stage 0:** Price: {price:,.2f} € | Unit VC: {variable_cost:,.2f} €")

    st.divider()

    # 3. FIXED COSTS INPUTS
    st.subheader("Annual Fixed Costs")
    col1, col2 = st.columns(2)
    with col1:
        # Defaulting to 50k if not set, but storing it for future steps
        fixed_costs = st.number_input("Total Annual Fixed Costs (€)", 
                                      min_value=0.0, 
                                      value=st.session_state.get('fixed_costs', 50000.0),
                                      step=1000.0)
        st.session_state.fixed_costs = fixed_costs

    # 4. BREAK-EVEN CALCULATIONS
    unit_contribution = price - variable_cost
    
    if unit_contribution > 0:
        be_units = fixed_costs / unit_contribution
        be_revenue = be_units * price
        # Margin of Safety: How far current volume is above break-even
        safety_margin = ((current_annual_volume - be_units) / current_annual_volume * 100)
    else:
        be_units = 0
        be_revenue = 0
