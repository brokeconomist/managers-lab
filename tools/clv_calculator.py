import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------
# Calculation Engine
# -----------------------
def get_clv_data(purchases, price, cost, marketing, retention, discount, churn, realization, risk_p, cac):
    cm = (purchases * (price - cost)) - marketing
    adj_disc = discount + risk_p
    cum_npv = -cac
    data = []
    payback = None
    
    for t in range(1, int(retention) + 1):
        survival = (1 - churn) ** t
        flow = (cm * realization * survival) / ((1 + adj_disc) ** t)
        cum_npv += flow
        data.append({"Year": t, "Cumulative_NPV": cum_npv})
        if cum_npv >= 0 and payback is None:
            payback = t
            
    return pd.DataFrame(data), cum_npv, payback


# -----------------------
# Main Interface
# -----------------------
def show_clv_calculator():
    st.header("👥 Executive CLV Scenario Simulator")
    st.write("Evaluate Customer Lifetime Value resilience using Discounted & Risk-Adjusted NPV modeling.")
    
    st.info("""
    Compare a **Base Case** vs a **Target Scenario** and identify which structure creates superior lifetime value.
    """)

    # -----------------------
    # Inputs
    # -----------------------
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("📊 Scenario A (Base)")
        p_a = st.number_input("Purchases / Year (A)", value=10.0)
        pr_a = st.number_input("Price / Purchase (A) $", value=100.0)
        cac_a = st.number_input("Acquisition Cost (A) $", value=150.0)
        ch_a = st.number_input("Churn Rate (A)", value=0.05, format="%.3f")

    with col_input2:
        st.subheader("🚀 Scenario B (Target)")
        p_b = st.number_input("Purchases / Year (B)", value=12.0)
        pr_b = st.number_input("Price / Purchase (B) $", value=110.0)
        cac_b = st.number_input("Acquisition Cost (B) $", value=150.0)
        ch_b = st.number_input("Churn Rate (B)", value=0.03, format="%.3f")

    with st.expander("⚠️ Common Structural Assumptions"):
        cost = st.number_input("Variable Cost per Purchase $", value=60.0)
        mkt = st.number_input("Retention Marketing / Year $", value=20.0)
        disc = st.number_input("Base Discount Rate", value=0.08)
        real = st.number_input("Purchase Realization Rate", value=0.85)
        risk_p = st.number_input("Customer Risk Premium", value=0.03)
        ret = st.slider("Analysis Horizon (Years)", 1, 15, 5)

    # -----------------------
    # Execution
    # -----------------------
    if st.button("Execute Strategic CLV Analysis"):

        df_a, final_a, pb_a = get_clv_data(p_a, pr_a, cost, mkt, ret, disc, ch_a, real, risk_p, cac_a)
        df_b, final_b, pb_b = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)

        # -----------------------
        # Comparison Table
        # -----------------------
        st.divider()
        st.subheader("📊 Scenario Comparison")
        
        comparison_df = pd.DataFrame({
            "Metric": ["Risk-Adjusted CLV (NPV)", "Payback Period", "LTV/CAC Ratio"],
            "Scenario A": [
                f"${final_a:,.2f}",
                f"{pb_a} Yrs" if pb_a else "N/A",
                f"{(final_a + cac_a)/cac_a:.2f}x" if cac_a > 0 else "N/A"
            ],
            "Scenario B": [
                f"${final_b:,.2f}",
                f"{pb_b} Yrs" if pb_b else "N/A",
                f"{(final_b + cac_b)/cac_b:.2f}x" if cac_b > 0 else "N/A"
            ]
        })
        st.table(comparison_df)

        # -----------------------
        # Best Scenario Detection
        # -----------------------
        st.divider()
        st.subheader("🏆 Executive Outcome Ranking")

        scenarios = {
            "Scenario A": final_a,
            "Scenario B": final_b
        }

        best_scenario = max(scenarios, key=scenarios.get)

        ranking_df = pd.DataFrame({
            "Scenario": scenarios.keys(),
            "Risk-Adjusted CLV ($)": scenarios.values()
        }).sort_values(by="Risk-Adjusted CLV ($)", ascending=False)

        st.dataframe(ranking_df, use_container_width=True)

        if final_a != final_b:
            value_gap = abs(final_b - final_a)
            pct_gap = (value_gap / abs(final_a)) * 100 if final_a != 0 else 0

            st.success(f"Top Performer: {best_scenario}")
            st.write(f"Value Advantage: ${value_gap:,.2f} ({pct_gap:.1f}%)")

        else:
            st.info("Both scenarios generate identical value.")

        # -----------------------
        # Strategic Assessment
        # -----------------------
        st.divider()
        st.subheader("🧠 Strategic Assessment")

        ltv_cac_b = (final_b + cac_b) / cac_b if cac_b > 0 else 0

        if final_b < 0:
            st.error("🔴 UNVIABLE: Negative NPV. Customer destroys value.")
        elif ltv_cac_b < 3.0:
            st.warning("🟠 MARGINAL: LTV/CAC below 3.0x. Scaling may be inefficient.")
        else:
            st.success("🟢 SCALABLE: Unit economics support growth.")

        # -----------------------
        # Strategic Signal
        # -----------------------
        st.divider()
        st.subheader("📌 Strategic Signal")

        if final_b > final_a:
            st.success("Recommendation: Transition toward Scenario B structure.")
        elif final_b < final_a:
            st.warning("Recommendation: Maintain Scenario A.")
        else:
            st.info("No structural difference detected.")

        # -----------------------
        # NPV Timeline
        # -----------------------
        st.divider()
        st.subheader("📉 Cumulative Risk-Adjusted NPV Projection")

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_a['Year'], 
            y=df_a['Cumulative_NPV'], 
            name='Scenario A',
            line=dict(color='#EF553B', dash='dash')
        ))

        fig_line.add_trace(go.Scatter(
            x=df_b['Year'], 
            y=df_b['Cumulative_NPV'], 
            name='Scenario B',
            line=dict(color='#00CC96', width=4)
        ))

        fig_line.add_hline(y=0)
        fig_line.update_layout(
            xaxis_title="Years",
            yaxis_title="Cumulative NPV ($)",
            height=500
        )

        st.plotly_chart(fig_line, use_container_width=True)


if __name__ == "__main__":
    show_clv_calculator()
