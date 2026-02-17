import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Calculation Engine (Analytical Logic)
def get_clv_data(purchases, price, cost, marketing, retention, discount, churn, realization, risk_p, cac):
    # CM per period
    cm = (purchases * (price - cost)) - marketing
    # Adjusted Discount Rate (Risk-Free + Risk Premium)
    adj_disc = discount + risk_p
    cum_npv = -cac
    data = []
    payback = None
    
    for t in range(1, int(retention) + 1):
        # Survival Probability
        survival = (1 - churn) ** t
        # Risk-Adjusted Discounted Cash Flow
        flow = (cm * realization * survival) / ((1 + adj_disc) ** t)
        cum_npv += flow
        data.append({"Year": t, "Cumulative_NPV": cum_npv})
        if cum_npv >= 0 and payback is None:
            payback = t
            
    return pd.DataFrame(data), cum_npv, payback

# 2. Main Interface Function
def show_clv_calculator():
    st.title("👥 Strategic CLV & Scenario Comparison")
    st.markdown("---")
    
    st.info("""
    **Analytical Framework:** This tool evaluates the Net Present Value (NPV) of a customer under two distinct scenarios. 
    It incorporates **Churn**, **Realization Rates**, and **Risk Premiums** to derive the 'Behavioral NPV'.
    """)

    # Input Columns for Scenario Comparison
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("📊 Scenario A (Current)")
        p_a = st.number_input("Expected Purchases/Year (A)", value=10.0, key="p_a")
        pr_a = st.number_input("Price per Purchase (A) $", value=100.0, key="pr_a")
        cac_a = st.number_input("Acquisition Cost (CAC) (A) $", value=150.0, key="cac_a")
        ch_a = st.number_input("Churn Rate (A) (e.g. 0.05)", value=0.05, key="ch_a")

    with col_input2:
        st.subheader("🚀 Scenario B (Optimized)")
        p_b = st.number_input("Expected Purchases/Year (B)", value=12.0, key="p_b")
        pr_b = st.number_input("Price per Purchase (B) $", value=110.0, key="pr_b")
        cac_b = st.number_input("Acquisition Cost (CAC) (B) $", value=150.0, key="cac_b")
        ch_b = st.number_input("Churn Rate (B) (e.g. 0.03)", value=0.03, key="ch_b")

    # Fixed Risk Variables
    with st.expander("⚠️ Underlying Risk Assumptions (Common to both)"):
        cost = st.number_input("Unit Cost $", value=60.0)
        mkt = st.number_input("Retention Marketing/Year $", value=20.0)
        disc = st.number_input("Base Discount Rate (e.g. 0.05)", value=0.08)
        real = st.number_input("Purchase Realization (e.g. 0.90)", value=0.85)
        risk_p = st.number_input("Customer Risk Premium", value=0.03)
        ret = st.slider("Retention Horizon (Years)", 1, 10, 5)

    if st.button("Execute Comparative Analysis"):
        # Calculate Data
        df_a, final_a, pb_a = get_clv_data(p_a, pr_a, cost, mkt, ret, disc, ch_a, real, risk_p, cac_a)
        df_b, final_b, pb_b = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)

        # 1. Visualization: NPV Timeline
        st.subheader("📉 Cumulative Risk-Adjusted NPV Timeline")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_a['Year'], y=df_a['Cumulative_NPV'], name='Scenario A', line=dict(color='#EF553B', dash='dash')))
        fig.add_trace(go.Scatter(x=df_b['Year'], y=df_b['Cumulative_NPV'], name='Scenario B', line=dict(color='#00CC96', width=4)))
        fig.add_hline(y=0, line_dash="dot", line_color="white")
        st.plotly_chart(fig, use_container_width=True)
        
        

        # 2. Executive Metrics Summary
        st.markdown("### 📋 Comparative Executive Summary")
        m1, m2, m3 = st.columns(3)
        
        value_gap = final_b - final_a
        m1.metric("Value Gap per Customer", f"${value_gap:,.2f}", f"{((final_b/final_a)-1)*100:.1f}% Improvement")
        
        ltv_cac_b = (final_b + cac_b) / cac_b if cac_b > 0 else 0
        m2.metric("LTV/CAC Ratio (Scenario B)", f"{ltv_cac_b:.2f}x")
        
        m3.metric("Break-Even (Scenario B)", f"Year {pb_b}" if pb_b else "N/A")
        
        

        # 3. Analytical Breakdown
        st.divider()
        col_text1, col_text2 = st.columns(2)
        
        with col_text1:
            st.subheader("💡 Strategic Insights")
            st.write(f"""
            - **Liquidity Exposure:** Scenario B reaches break-even in **Year {pb_b if pb_b else 'N/A'}**. 
            - **Efficiency Multiplier:** The model suggests that for every $1.00 spent on acquisition in Scenario B, the system realizes **${ltv_cac_b:,.2f}** in risk-adjusted value.
            """)

        with col_text2:
            st.subheader("⚠️ Risk Factors")
            st.write(f"""
            - **Churn Impact:** Moving from {ch_a*100}% to {ch_b*100}% churn accounts for a significant portion of the value retention.
            - **Realization Risk:** A realization rate of {real*100}% assumes that not all forecasted revenue will materialize due to market friction.
            """)

        # 4. Comparative Data Table
        st.subheader("📊 Detailed Metrics Comparison")
        st.table(pd.DataFrame({
            "Metric": ["Risk-Adjusted CLV (Behavioral NPV)", "Payback Period", "LTV/CAC Ratio"],
            "Scenario A": [f"${final_a:,.2f}", f"{pb_a} Years" if pb_a else "N/A", f"{(final_a+cac_a)/cac_a:.2f}x"],
            "Scenario B": [f"${final_b:,.2f}", f"{pb_b} Years" if pb_b else "N/A", f"{ltv_cac_b:.2f}x"]
        }))

if __name__ == "__main__":
    show_cl
