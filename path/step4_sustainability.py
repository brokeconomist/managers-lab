import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def run_step():
    st.header("🏢 Stage 4: Sustainability & Structural Break-Even")
    st.info("Calculating the scale required to cover all fixed obligations and debt service.")

    # 1. SYNC WITH SHARED CORE & PREVIOUS STAGES
    p = st.session_state.get('price', 100.0)
    vc = st.session_state.get('variable_cost', 60.0)
    unit_margin = p - vc
    current_vol = st.session_state.get('volume', 1000) / 12 # Monthly volume
    
    st.write(f"**🔗 Core Baseline:** Margin/Unit: **{unit_margin:,.2f} €**")

    st.divider()

    # 2. FIXED COSTS INPUTS
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Operating Costs")
        rent = st.number_input("Rent & Utilities (€)", value=1500.0)
        salaries = st.number_input("Salaries & Insurance (€)", value=4500.0)
        software = st.number_input("Software & Admin (€)", value=500.0)
        other_fixed = st.number_input("Other Fixed Costs (€)", value=500.0)
        
        total_monthly_fixed = rent + salaries + software + other_fixed
        st.metric("Total Monthly Fixed", f"{total_monthly_fixed:,.2f} €")

    with col2:
        st.subheader("Capital & Debt Obligations")
        loan_payment = st.number_input("Monthly Loan Repayment (€)", value=1000.0)
        taxes_buffer = st.slider("Tax Provision %", 0, 40, 22)
        
        total_monthly_burn = total_monthly_fixed + loan_payment

    # --- 3. CALCULATIONS (Πρέπει να είναι ΕΝΤΟΣ της συνάρτησης) ---
    monthly_revenue = current_vol * p
    monthly_variable_costs = current_vol * vc
    ebit = monthly_revenue - monthly_variable_costs - total_monthly_fixed
    
    # Break-even Calculations
    be_units = total_monthly_burn / unit_margin if unit_margin > 0 else 0
    safety_margin = ((current_vol - be_units) / current_vol) * 100 if current_vol > 0 else -100
    
    # Net Profit Logic
    tax_amount = (ebit * taxes_buffer / 100) if ebit > 0 else 0
    net_profit = ebit - loan_payment - tax_amount

    # --- 4. RESULTS DISPLAY ---
    st.divider()
    res1, res2 = st.columns(2)

    with res1:
        st.metric("EBIT (Operating Profit)", f"{ebit:,.2f} €")
        st.caption("Κέρδη από τη λειτουργία (Revenue - Expenses).")

    with res2:
        st.metric("Net Profit (Final)", f"{net_profit:,.2f} €", 
                  delta=f"-{loan_payment + tax_amount:,.2f} € (Obligations)", delta_color="inverse")
        st.caption("Καθαρό ποσό μετά από Δάνεια και Φόρους.")

    with st.expander("🔍 Γιατί διαφέρουν το EBIT και το Net Profit;"):
        st.write(f"""
        - **EBIT:** Η λειτουργική σου υγεία.
        - **Net Profit:** Τι μένει στην τσέπη. Αφαιρέθηκαν **{loan_payment:,.2f} €** για το δάνειο και **{tax_amount:,.2f} €** για φόρο ({taxes_buffer}%).
        """)

    # --- 5. BREAK-EVEN VISUALIZATION ---
    st.divider()
    st.subheader("Profitability Threshold Analysis")
    
    x_range = list(range(0, int(be_units * 2) if be_units > 0 else 100, 1))
    rev_y = [x * p for x in x_range]
    cost_y = [total_monthly_burn + (x * vc) for x in x_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=rev_y, name='Total Revenue', line=dict(color='#00CC96')))
    fig.add_trace(go.Scatter(x=x_range, y=cost_y, name='Total Costs', line=dict(color='#EF553B')))
    fig.add_vline(x=be_units, line_dash="dash", line_color="white", annotation_text="Break-Even Point")
    
    fig.update_layout(xaxis_title="Monthly Units", yaxis_title="Euros (€)", height=400, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # --- 6. STRATEGIC VERDICT ---
    if safety_margin < 0:
        st.error(f"🔴 **STRUCTURAL DEFICIT:** Current volume ({current_vol:.0f}/mo) is below break-even. Monthly Loss: {abs(net_profit):,.2f} €")
    elif safety_margin < 15:
        st.warning(f"🟡 **FRAGILE ZONE:** Safety Margin: {safety_margin:.1f}%. Vulnerable to market shocks.")
    else:
        st.success(f"🟢 **SUSTAINABLE SCALE:** Safety Margin: {safety_margin:.1f}%. Business is structurally sound.")

    st.divider()

    # --- 7. NAVIGATION ---
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Back to Unit Economics"):
            st.session_state.flow_step = 3
            st.rerun()
    with nav2:
        if st.button("Final Strategy & Stress Test (Stage 5) ➡️", type="primary"):
            st.session_state.flow_step = 5
            st.rerun()
