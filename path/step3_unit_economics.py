import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def run_step():
    st.header("📊 Stage 3: Unit Economics & CLV Analysis")
    st.info("Analyzing the structural health of your customer acquisition and lifetime value.")

    # 1. DYNAMIC SYNC WITH CORE BASELINE
    p = st.session_state.get('price', 100.0)
    vc = st.session_state.get('variable_cost', 60.0)
    # Using 'fixed_cost' singular as discovered in Stage 0
    annual_fixed_costs = st.session_state.get('fixed_cost', 50000.0)
    unit_margin = p - vc
    
    st.write(f"**🔗 Core Baseline:** Margin/Unit: **{unit_margin:,.2f} €** | Annual Fixed Costs: **{annual_fixed_costs:,.2f} €**")

    st.divider()

    # 2. INPUTS: CUSTOMER BASE & ACQUISITION
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Customer Base & Acquisition")
        # Added Average Number of Customers
        total_customers = st.number_input("Average Active Customers", min_value=1, value=500)
        purch_per_year = st.number_input("Purchases per Year / Customer", value=4.0)
        cac = st.number_input("Customer Acquisition Cost (CAC) €", value=150.0)
        
    with col2:
        st.subheader("Retention & Timeframe")
        churn_rate = st.slider("Annual Churn Rate (%)", 0, 100, 15)
        horizon = st.slider("Analysis Horizon (Years)", 1, 10, 5)
        discount_rate = st.slider("Hurdle Rate / Discount (%)", 0, 25, 10) / 100

    # 3. CALCULATIONS (Cold Analytical Logic)
    annual_margin_per_customer = unit_margin * purch_per_year
    
    total_clv_npv = 0
    data = []
    
    for t in range(1, horizon + 1):
        # Probability of customer still being active
        survival = (1 - (churn_rate/100)) ** (t-1)
        # Net Present Value of that year's cash flow
        flow = (annual_margin_per_customer * survival) / ((1 + discount_rate) ** t)
        total_clv_npv += flow
        data.append({
            "Year": t, 
            "NPV_per_Customer": total_clv_npv - cac,
            "Total_Base_Value": (total_clv_npv - cac) * total_customers
        })

    ltv_cac_ratio = total_clv_npv / cac if cac > 0 else 0
    customer_equity = (total_clv_npv - cac) * total_customers

    # 4. RESULTS (Metrics)
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Individual NPV CLV", f"{total_clv_npv:,.2f} €")
    c2.metric("LTV / CAC Ratio", f"{ltv_cac_ratio:.2f}x")
    
    # Payback estimate based on annual margin
    payback_months = (cac / annual_margin_per_customer) * 12 if annual_margin_per_customer > 0 else 0
    c3.metric("CAC Payback", f"{payback_months:.1f} Months")

    # NEW: Customer Equity Metric
    st.metric("Total Customer Equity (Base Value)", f"{customer_equity:,.2f} €", 
              help="Total discounted profit from your current customer base over the horizon.")

    # 5. VISUALIZATION
    
    df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['NPV_per_Customer'], 
                             name='Net Value per Customer', 
                             line=dict(color='#00CC96', width=4)))
    fig.add_hline(y=0, line_dash="dot", line_color="white")
    fig.update_layout(title="Cumulative Net Value per Customer (NPV)", 
                      xaxis_title="Years", yaxis_title="Euros (€)", height=400, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # 6. STRATEGIC VERDICT (Cold Insight)
    if ltv_cac_ratio < 1:
        st.error("🔴 **Value Destruction:** CAC exceeds CLV. Each new customer results in a net loss.")
    elif ltv_cac_ratio < 3:
        st.warning("🟡 **Fragile Economics:** Profitable but thin. High risk of failure if fixed costs increase.")
    else:
        st.success("🟢 **Efficient Engine:** Strong unit economics. This structure supports scaling.")

    # Cold Check vs Fixed Costs
    annual_base_profit = annual_margin_per_customer * total_customers
    if annual_base_profit < annual_fixed_costs:
        st.error(f"⚠️ **Structural Gap:** Your annual margin from {total_customers} customers ({annual_base_profit:,.0f} €) does not cover your Fixed Costs ({annual_fixed_costs:,.0f} €).")

    # 7. NAVIGATION
    st.divider()
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Back to Cash Cycle"):
            st.session_state.flow_step = 2
            st.rerun()
    with nav2:
        if st.button("Proceed to Stage 4 ➡️", type="primary"):
            st.session_state.flow_step = 4
            st.rerun()
