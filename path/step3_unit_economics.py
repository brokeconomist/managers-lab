import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def run_step():
    st.header("📊 Stage 3: Unit Economics & CLV Analysis")
    st.info("Calculating Lifetime Value with dynamic retention margins.")

    # 1. DYNAMIC SYNC
    p = st.session_state.get('price', 100.0)
    vc = st.session_state.get('variable_cost', 60.0)
    initial_margin = p - vc
    
    # 2. INPUTS: CUSTOMER BEHAVIOR
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Purchase Dynamics")
        total_customers = st.number_input("Active Customer Base", min_value=1, value=500)
        purch_per_year = st.number_input("Purchases per Year", value=4.0)
        cac = st.number_input("Acquisition Cost (CAC) €", value=150.0)
        
    with col2:
        st.subheader("Retention Strategy")
        churn_rate = st.slider("Annual Churn Rate (%)", 0, 100, 15)
        # NEW: Discount applied to repeat purchases to keep customers
        retention_discount = st.slider("Retention Discount (%)", 0, 50, 5, 
                                       help="Discount offered to existing customers to encourage repeat orders.")
        horizon = st.slider("Analysis Horizon (Years)", 1, 10, 5)

    # 3. CALCULATIONS (Cold Logic)
    # The margin for the very first purchase
    first_purchase_margin = initial_margin
    # The margin for all subsequent purchases
    repeat_margin = (p * (1 - retention_discount/100)) - vc
    
    # Annual margin calculation: 1st purchase at full price (if t=1), rest at discount
    # For simplification in an annual model, we weigh the margins:
    weighted_annual_margin = first_purchase_margin + (repeat_margin * (purch_per_year - 1))
    
    discount_rate = 0.10
    total_clv_npv = 0
    data = []
    
    for t in range(1, horizon + 1):
        survival = (1 - (churn_rate/100)) ** (t-1)
        # We use the weighted annual margin (accounting for retention discounts)
        flow = (weighted_annual_margin * survival) / ((1 + discount_rate) ** t)
        total_clv_npv += flow
        data.append({"Year": t, "Cumulative_NPV": total_clv_npv - cac})

    ltv_cac_ratio = total_clv_npv / cac if cac > 0 else 0

    # 4. RESULTS
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Adjusted NPV CLV", f"{total_clv_npv:,.2f} €")
    c2.metric("LTV / CAC Ratio", f"{ltv_cac_ratio:.2f}x")
    
    # Payback estimate
    payback_months = (cac / weighted_annual_margin) * 12 if weighted_annual_margin > 0 else 0
    c3.metric("CAC Payback", f"{payback_months:.1f} Months")

    # 5. VISUALIZATION
    
    df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Cumulative_NPV'], 
                             name='Net Value per Customer', 
                             line=dict(color='#00CC96', width=4)))
    fig.add_hline(y=0, line_dash="dot", line_color="white")
    fig.update_layout(title="NPV Timeline (Including Retention Discounts)", 
                      xaxis_title="Years", yaxis_title="Net Value (€)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # 6. STRATEGIC SIGNAL
    if repeat_margin <= 0:
        st.error(f"❌ **Margin Collapse:** Your retention discount ({retention_discount}%) makes repeat purchases unprofitable (Margin: {repeat_margin:.2f} €).")
    elif ltv_cac_ratio < 3:
        st.warning("⚠️ **Efficiency Warning:** After accounting for retention costs, your LTV/CAC is below the safety threshold of 3.0x.")
    else:
        st.success("✅ **Robust Model:** Your unit economics remain strong even with customer incentives.")

    # 7. NAVIGATION
    st.divider()
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Back to Stage 2"):
            st.session_state.flow_step = 2
            st.rerun()
    with nav2:
        if st.button("Proceed to Stage 4 ➡️", type="primary"):
            st.session_state.flow_step = 4
            st.rerun()
