import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Calculation Engine
def get_clv_data(purchases, price, cost, marketing, retention, discount, churn, realization, risk_p, cac):
    cm = (purchases * (price - cost)) - marketing
    adj_disc = discount + risk_p
    cum_npv = -cac
    data = []
    payback = None
    
    for t in range(1, int(retention) + 1):
        survival = (1 - churn) ** t
        # Discounted Cash Flow Calculation
        flow = (cm * realization * survival) / ((1 + adj_disc) ** t)
        cum_npv += flow
        data.append({"Year": t, "Cumulative_NPV": cum_npv})
        if cum_npv >= 0 and payback is None:
            payback = t
    return pd.DataFrame(data), cum_npv, payback

# 2. Main Function (Imported by app.py)
def show_clv_calculator():
    st.title("👥 Strategic CLV & Scenario Comparison")
    st.markdown("---")
    
    # Model Explanation
    st.info("""
    **CLV Analysis:** We calculate the Net Present Value (NPV) of a customer, adjusted for uncertainty (**Risk-Adjusted**). 
    Compare **Scenario A (Current)** with **Scenario B (Target)** to identify the **Value Gap**.
    """)

    # Input Parameters in Columns
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("📊 Scenario A (Current)")
        p_a = st.number_input("Purchases/Year (A)", value=10.0, key="p_a")
        pr_a = st.number_input("Price per Purchase (A) $", value=100.0, key="pr_a")
        cac_a = st.number_input("Acquisition Cost (CAC) (A) $", value=150.0, key="cac_a")
        ch_a = st.number_input("Churn Rate (A) (e.g., 0.05)", value=0.05, key="ch_a")

    with col_input2:
        st.subheader("🚀 Scenario B (Target)")
        p_b = st.number_input("Purchases/Year (B)", value=10.0, key="p_b")
        pr_b = st.number_input("Price per Purchase (B) $", value=110.0, key="pr_b")
        cac_b = st.number_input("Acquisition Cost (CAC) (B) $", value=150.0, key="cac_b")
        ch_b = st.number_input("Churn Rate (B) (e.g., 0.03)", value=0.03, key="ch_b")

    # Risk Constants (Common for both scenarios)
    cost, mkt, disc, real, risk_p = 60.0, 20.0, 0.08, 0.90, 0.03
    ret = 5

    if st.button("Generate Strategic Analysis"):
        df_a, final_a, pb_a = get_clv_data(p_a, pr_a, cost, mkt, ret, disc, ch_a, real, risk_p, cac_a)
        df_b, final_b, pb_b = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)

        # 1. Timeline Chart
        st.subheader("📉 Cumulative Profitability Comparison (NPV)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_a['Year'], y=df_a['Cumulative_NPV'], name='Scenario A', line=dict(color='#EF553B', dash='dash')))
        fig.add_trace(go.Scatter(x=df_b['Year'], y=df_b['Cumulative_NPV'], name='Scenario B', line=dict(color='#00CC96', width=4)))
        fig.add_hline(y=0, line_dash="dot", line_color="white")
        st.plotly_chart(fig, use_container_width=True)
        
        

        # 2. Executive Metrics
        st.markdown("### 📋 Strategic Interpretation")
        m1, m2, m3 = st.columns(3)
        
        gap = final_b - final_a
        m1.metric("Value Gap per Customer", f"${gap:,.2f}", f"{((final_b/final_a)-1)*100:.1f}%")
        
        ltv_a = (final_a + cac_a) / cac_a if cac_a > 0 else 0
        ltv_b = (final_b + cac_b) / cac_b if cac_b > 0 else 0
        m2.metric("LTV/CAC (Scenario B)", f"{ltv_b:.2f}x")
        
        m3.metric("Payback (Scenario B)", f"{pb_b} Years" if pb_b else "N/A")
        
        

        # 3. Contextual Explanations
        with st.expander("🧐 What do these results mean?"):
            st.write(f"""
            - **Risk-Adjusted CLV:** This is the "cold" present value of the customer. In Scenario B, we estimate each customer is worth **${final_b:,.2f}** in net profit.
            - **Value Gap:** Represents the value "left on the table" in your current model (A) compared to the optimized target (B). 
            - **Payback Period:** In Scenario B, you recover the acquisition cost in Year **{pb_b}**. A shorter period reduces liquidity risk.
            """)

        # 4. Data Table
        st.subheader("📊 Comparative Metrics Table")
        st.table(pd.DataFrame({
            "Metric": ["Net Lifetime Value (Risk Adjusted)", "Payback Year", "LTV/CAC Ratio"],
            "Scenario A": [f"${final_a:,.2f}", pb_a if pb_a else "N/A", f"{ltv_a:.2f}x"],
            "Scenario B": [f"${final_b:,.2f}", pb_b if pb_b else "N/A", f"{ltv_b:.2f}x"]
        }))
