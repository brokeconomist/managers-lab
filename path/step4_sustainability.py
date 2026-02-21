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

    # 3. CALCULATIONS (The Cold Reality)
    # Accounting Break-even (Monthly Units)
    be_units = total_monthly_burn / unit_margin if unit_margin > 0 else 0
    
    # Financial Margin of Safety
    current_vol = st.session_state.get('volume', 1000) / 12 # Monthly volume
    safety_margin = ((current_vol - be_units) / current_vol) * 100 if current_vol > 0 else -100

    # 4. RESULTS
    st.divider()
    res1, res2, res3 = st.columns(3)
    
    with res1:
        st.metric("Break-Even Volume", f"{int(be_units)} Units / Mo")
        st.caption("Units needed just to cover costs")

    with res2:
        st.metric("Daily Sales Target", f"{be_units/30:.1f} Units")
        st.caption("Based on 30-day month")

    with res3:
        color = "normal" if safety_margin > 20 else "inverse"
        st.metric("Safety Margin", f"{safety_margin:.1f}%", delta=f"{safety_margin:.1f}%", delta_color=color)
        st.caption("Distance from the 'Danger Zone'")

    # 5. BREAK-EVEN VISUALIZATION
    st.divider()
    st.subheader("Profitability Threshold Analysis")
    
    # Generate data for the chart
    x_range = list(range(0, int(be_units * 2) if be_units > 0 else 100, 1))
    rev_y = [x * p for x in x_range]
    cost_y = [total_monthly_burn + (x * vc) for x in x_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=rev_y, name='Total Revenue', line=dict(color='#00CC96')))
    fig.add_trace(go.Scatter(x=x_range, y=cost_y, name='Total Costs (Fixed + Var)', line=dict(color='#EF553B')))
    
    fig.add_vline(x=be_units, line_dash="dash", line_color="white", annotation_text="Break-Even Point")
    
    fig.update_layout(xaxis_title="Monthly Units", yaxis_title="Euros (€)", height=450, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    

    # 6. STRATEGIC VERDICT
    if safety_margin < 0:
        st.error(f"🔴 **STRUCTURAL DEFICIT:** Your current volume ({current_vol:.0f} units/mo) is below the break-even point. You are losing {abs(current_vol - be_units) * unit_margin:,.2f} € every month.")
    elif safety_margin < 15:
        st.warning("🟡 **FRAGILE ZONE:** You are barely covering costs. Any slight drop in sales or increase in costs will push you into deficit.")
    else:
        st.success("🟢 **SUSTAINABLE SCALE:** Your business model has a healthy buffer to absorb shocks.")

    st.divider()

    # 7. NAVIGATION
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Back to Unit Economics"):
            st.session_state.flow_step = 3
            st.rerun()
    with nav2:
        if st.button("Final Strategy & Stress Test (Stage 5) ➡️", type="primary"):
            st.session_state.flow_step = 5
            st.rerun()
