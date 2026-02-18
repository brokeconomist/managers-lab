import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------
# Calculation Engine
# -----------------------
def get_clv_data(purchases, price, cost, marketing, retention, discount, churn, realization, risk_p, cac):
    # Contribution Margin per period
    cm = (purchases * (price - cost)) - marketing
    # Risk-Adjusted Discount Rate
    adj_disc = discount + risk_p
    cum_npv = -cac
    data = []
    payback = None
    
    for t in range(1, int(retention) + 1):
        # Survival Probability (Retention)
        survival = (1 - churn) ** t
        # Discounted Cash Flow adjusted for realization and survival
        flow = (cm * realization * survival) / ((1 + adj_disc) ** t)
        cum_npv += flow
        data.append({"Year": t, "Cumulative_NPV": cum_npv})
        if cum_npv >= 0 and payback is None:
            payback = t
            
    return pd.DataFrame(data), cum_npv, payback

# -----------------------
# Main Interface Function
# -----------------------
def show_clv_calculator():
    st.header("👥 Executive CLV Scenario Simulator")
    st.write("Evaluate Customer Lifetime Value resilience using Discounted & Risk-Adjusted NPV modeling.")
    
    st.info("""
    **Analytical Framework:** This simulator compares a **Base Case** against a **Target/Stress Case** to quantify the value gap. 
    It incorporates churn probabilities and risk premiums to derive the 'Behavioral NPV'.
    """)

    # 1. Input Section
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("📊 Scenario A (Base)")
        p_a = st.number_input("Purchases / Year (A)", value=10.0, key="p_a")
        pr_a = st.number_input("Price / Purchase (A) $", value=100.0, key="pr_a")
        cac_a = st.number_input("Acquisition Cost (A) $", value=150.0, key="cac_a")
        ch_a = st.number_input("Churn Rate (A)", value=0.05, format="%.3f", key="ch_a")

    with col_input2:
        st.subheader("🚀 Scenario B (Target)")
        p_b = st.number_input("Purchases / Year (B)", value=12.0, key="p_b")
        pr_b = st.number_input("Price / Purchase (B) $", value=110.0, key="pr_b")
        cac_b = st.number_input("Acquisition Cost (B) $", value=150.0, key="cac_b")
        ch_b = st.number_input("Churn Rate (B)", value=0.03, format="%.3f", key="ch_b")

    with st.expander("⚠️ Underlying Risk & Cost Assumptions (Common)"):
        cost = st.number_input("Variable Cost per Purchase $", value=60.0)
        mkt = st.number_input("Retention Marketing / Year $", value=20.0)
        disc = st.number_input("Base Discount Rate (e.g., 0.08)", value=0.08)
        real = st.number_input("Purchase Realization Rate", value=0.85)
        risk_p = st.number_input("Customer Risk Premium", value=0.03)
        ret = st.slider("Analysis Horizon (Years)", 1, 15, 5)

    if st.button("Execute Strategic CLV Analysis"):
        # 2. Run Calculations
        df_a, final_a, pb_a = get_clv_data(p_a, pr_a, cost, mkt, ret, disc, ch_a, real, risk_p, cac_a)
        df_b, final_b, pb_b = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)
        
        # 3. Scenario Comparison Table
        st.divider()
        st.subheader("📊 Scenario Comparison")
        
        comparison_df = pd.DataFrame({
            "Metric": ["Risk-Adjusted CLV (NPV)", "Payback Period", "LTV/CAC Ratio", "Survival Prob. (End of Term)"],
            "Scenario A": [
                f"${final_a:,.2f}",
                f"{pb_a} Yrs" if pb_a else "N/A",
                f"{(final_a + cac_a)/cac_a:.2f}x" if cac_a > 0 else "N/A",
                f"{(1-ch_a)**ret:.1%}"
            ],
            "Scenario B": [
                f"${final_b:,.2f}",
                f"{pb_b} Yrs" if pb_b else "N/A",
                f"{(final_b + cac_b)/cac_b:.2f}x" if cac_b > 0 else "N/A",
                f"{(1-ch_b)**ret:.1%}"
            ]
        })
        st.table(comparison_df)

        # 4. Delta Variance Analysis
        c1, c2, c3 = st.columns(3)
        v_gap = final_b - final_a
        v_pct = (final_b / final_a - 1) * 100 if final_a != 0 else 0
        
        c1.metric("Value Gap (Δ CLV)", f"${v_gap:,.2f}", f"{v_pct:.1f}%")
        c2.metric("Efficiency Gain", f"{((final_b+cac_b)/cac_b - (final_a+cac_a)/cac_a):.2f}x")
        c3.metric("Retention Δ", f"{(ch_a - ch_b)*100:.1f} pts")

        # 5. Tornado Sensitivity Chart
        st.divider()
        st.subheader("🌪️ Value Driver Sensitivity (Impact on Gap)")
        
        impacts = {}
        # Isolate Price Effect
        _, v, _ = get_clv_data(p_b, pr_a, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)
        impacts["Price Strategy"] = final_b - v
        # Isolate Volume Effect
        _, v, _ = get_clv_data(p_a, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)
        impacts["Purchase Frequency"] = final_b - v
        # Isolate Churn Effect
        _, v, _ = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_a, real, risk_p, cac_b)
        impacts["Customer Retention"] = final_b - v
        # Isolate CAC Effect
        _, v, _ = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_a)
        impacts["Acquisition Efficiency"] = final_b - v

        sorted_impacts = dict(sorted(impacts.items(), key=lambda item: abs(item[1])))
        
        fig_tornado = go.Figure(go.Bar(
            y=list(sorted_impacts.keys()),
            x=list(sorted_impacts.values()),
            orientation='h',
            marker_color='#00CC96',
            text=[f"${v:,.2f}" for v in sorted_impacts.values()],
            textposition='auto',
        ))
        fig_tornado.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_tornado, use_container_width=True)
        

        # 6. Strategic Assessment
        st.divider()
        st.subheader("🧠 Strategic Assessment")
        top_driver = max(impacts, key=impacts.get)
        
        col_text1, col_text2 = st.columns(2)
        with col_text1:
            st.write(f"**Primary Leverage Point:** {top_driver}")
            st.write("Focusing resources on this variable provides the highest marginal utility for the business model.")
        
        with col_text2:
            if final_b < 0:
                st.error("🔴 UNVIABLE: Scenario B results in a negative NPV. The customer acquisition cost exceeds lifetime value.")
            elif (final_b + cac_b)/cac_b < 3.0:
                st.warning("🟠 MARGINAL: LTV/CAC ratio is below 3.0x. Scaling may be inefficient.")
            else:
                st.success("🟢 SCALABLE: Robust LTV/CAC ratio detected. Unit economics support aggressive growth.")

        # 7. NPV Timeline Visualization
        st.divider()
        st.subheader("📉 Cumulative Risk-Adjusted NPV Projection")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=df_a['Year'], y=df_a['Cumulative_NPV'], name='Scenario A', line=dict(color='#EF553B', dash='dash')))
        fig_line.add_trace(go.Scatter(x=df_b['Year'], y=df_b['Cumulative_NPV'], name='Scenario B', line=dict(color='#00CC96', width=4)))
        fig_line.add_hline(y=0, line_dash="dot", line_color="white")
        fig_line.update_layout(xaxis_title="Years", yaxis_title="Cumulative NPV ($)", height=500)
        st.plotly_chart(fig_line, use_container_width=True)
        

if __name__ == "__main__":
    show_clv_calculator()
