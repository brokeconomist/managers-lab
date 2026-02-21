import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def run_step():
    st.header("📊 Stage 3: Unit Economics & CLV Analysis")
    st.info("Analyzing the structural health of your customer acquisition and lifetime value.")

    # 1. SYNC WITH SHARED CORE
    p = st.session_state.get('price', 100.0)
    vc = st.session_state.get('variable_cost', 60.0)
    unit_margin = p - vc
    
    st.write(f"**🔗 Core Baseline:** Margin/Unit: **{unit_margin:,.2f} €**")

    st.divider()

    # 2. INPUTS: CAC & CHURN
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Acquisition Logic")
        purch_per_year = st.number_input("Purchases per Year / Customer", value=4.0)
        cac = st.number_input("Customer Acquisition Cost (CAC) €", value=150.0)
        
    with col2:
        st.subheader("Retention Logic")
        churn_rate = st.slider("Annual Churn Rate (%)", 0, 100, 15)
        horizon = st.slider("Analysis Horizon (Years)", 1, 10, 5)

    # 3. CALCULATIONS (Cold Logic)
    # Annual Margin per customer
    annual_margin = unit_margin * purch_per_year
    
    # Simple CLV (Discounted simplified version for speed)
    discount_rate = 0.10 # 10% standard hurdle rate
    total_clv_npv = 0
    data = []
    
    for t in range(1, horizon + 1):
        survival = (1 - (churn_rate/100)) ** (t-1)
        flow = (annual_margin * survival) / ((1 + discount_rate) ** t)
        total_clv_npv += flow
        data.append({"Year": t, "Cumulative_NPV": total_clv_npv - cac})

    ltv_cac_ratio = total_clv_npv / cac if cac > 0 else 0

    # 4. RESULTS
    c1, c2, c3 = st.columns(3)
    c1.metric("NPV CLV", f"{total_clv_npv:,.2f} €")
    c2.metric("LTV / CAC Ratio", f"{ltv_cac_ratio:.2f}x")
    
    # Payback Month estimate
    payback_months = (cac / annual_margin) * 12 if annual_margin > 0 else 0
    c3.metric("CAC Payback", f"{payback_months:.1f} Months")

    st.divider()

    # 5. VISUALIZATION
    df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Cumulative_NPV'], name='Net Value per Customer', line=dict(color='#00CC96', width=4)))
    fig.add_hline(y=0, line_dash="dot", line_color="white")
    fig.update_layout(title="Customer Profitability Timeline (NPV)", xaxis_title="Years", yaxis_title="Net Value (€)", height=400)
    st.plotly_chart(fig, use_container_width=True)

    

    # 6. STRATEGIC VERDICT
    if ltv_cac_ratio < 1:
        st.error("🔴 **Value Destruction:** Your CAC is higher than the lifetime value. You are losing money on every customer acquired.")
    elif ltv_cac_ratio < 3:
        st.warning("🟡 **Fragile Economics:** You are profitable, but the margin is too thin to cover fixed costs and overhead. Scaling is risky.")
    else:
        st.success("🟢 **Efficient Engine:** High LTV/CAC ratio. This unit structure supports aggressive growth.")

    st.divider()

    # 7. NAVIGATION
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Back to Cash Cycle"):
            st.session_state.flow_step = 2
            st.rerun()
    with nav2:
        if st.button("Proceed to Sustainability (Stage 4) ➡️", type="primary"):
            st.session_state.flow_step = 4
            st.rerun()
