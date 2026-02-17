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
        flow = (cm * realization * survival) / ((1 + adj_disc) ** t)
        cum_npv += flow
        data.append({"Year": t, "Cumulative_NPV": cum_npv})
        if cum_npv >= 0 and payback is None:
            payback = t
            
    return pd.DataFrame(data), cum_npv, payback

# 2. Main Interface Function
def show_clv_calculator():
    st.title("👥 Strategic CLV & Sensitivity Analysis")
    st.markdown("---")
    
    st.info("""
    **Analytical Framework:** This tool evaluates the Net Present Value (NPV) of a customer and identifies which strategic levers 
    (Price, Volume, or Retention) drive the most value using a **Tornado Sensitivity Analysis**.
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
        st.subheader("🚀 Scenario B (Target)")
        p_b = st.number_input("Expected Purchases/Year (B)", value=12.0, key="p_b")
        pr_b = st.number_input("Price per Purchase (B) $", value=110.0, key="pr_b")
        cac_b = st.number_input("Acquisition Cost (CAC) (B) $", value=150.0, key="cac_b")
        ch_b = st.number_input("Churn Rate (B) (e.g. 0.03)", value=0.03, key="ch_b")

    # Fixed Risk Variables
    with st.expander("⚠️ Underlying Risk Assumptions (Common to both)"):
        cost = st.number_input("Unit Cost $", value=60.0)
        mkt = st.number_input("Retention Marketing/Year $", value=20.0)
        disc = st.number_input("Base Discount Rate", value=0.08)
        real = st.number_input("Purchase Realization", value=0.85)
        risk_p = st.number_input("Customer Risk Premium", value=0.03)
        ret = st.slider("Retention Horizon (Years)", 1, 15, 5)

    if st.button("Execute Comparative Analysis"):
        # Base Calculations
        _, final_a, pb_a = get_clv_data(p_a, pr_a, cost, mkt, ret, disc, ch_a, real, risk_p, cac_a)
        _, final_b, pb_b = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)
        base_gap = final_b - final_a

        # --- Tornado Logic (Impact on Value Gap) ---
        # We calculate how much the GAP changes if we reset each variable in Scenario B back to Scenario A
        impacts = {}
        
        # 1. Price Impact
        _, val, _ = get_clv_data(p_b, pr_a, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)
        impacts["Price Effect"] = final_b - val
        
        # 2. Volume Impact
        _, val, _ = get_clv_data(p_a, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)
        impacts["Purchase Frequency Effect"] = final_b - val
        
        # 3. Churn Impact
        _, val, _ = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_a, real, risk_p, cac_b)
        impacts["Retention (Churn) Effect"] = final_b - val
        
        # 4. CAC Impact
        _, val, _ = get_clv_data(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_a)
        impacts["Acquisition Cost Effect"] = final_b - val

        # Sort for Tornado
        sorted_impacts = dict(sorted(impacts.items(), key=lambda item: abs(item[1])))

        # --- 1. Tornado Chart ---
        st.subheader("🌪️ Value Driver Sensitivity (Impact on Gap)")
        fig_tornado = go.Figure(go.Bar(
            y=list(sorted_impacts.keys()),
            x=list(sorted_impacts.values()),
            orientation='h',
            marker_color='#00CC96',
            text=[f"${v:,.2f}" for v in sorted_impacts.values()],
            textposition='auto',
        ))
        fig_tornado.update_layout(
            title="Contribution to Total Value Improvement ($)",
            xaxis_title="Added Value ($)",
            yaxis_title="Variable Lever"
        )
        st.plotly_chart(fig_tornado, use_container_width=True)
        

        # --- 2. Executive Metrics Summary ---
        st.markdown("### 📋 Executive Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Value Gap", f"${base_gap:,.2f}", f"{((final_b/final_a)-1)*100:.1f}%")
        m2.metric("LTV/CAC (Scenario B)", f"{(final_b + cac_b) / cac_b:.2f}x")
        m3.metric("Payback (Scenario B)", f"Year {pb_b}" if pb_b else "N/A")
        

        # --- 3. Insights ---
        st.divider()
        st.subheader("💡 Strategic Insight")
        top_driver = max(impacts, key=impacts.get)
        st.write(f"The analysis indicates that **{top_driver}** is your strongest lever. Focusing effort here will yield the highest marginal return per customer.")

        # --- 4. Detailed Metrics Table ---
        st.subheader("📊 Comparative Metrics Table")
        st.table(pd.DataFrame({
            "Metric": ["Risk-Adjusted CLV (Behavioral NPV)", "Payback Period", "LTV/CAC Ratio"],
            "Scenario A": [f"${final_a:,.2f}", f"{pb_a} Yrs" if pb_a else "N/A", f"{(final_a+cac_a)/cac_a:.2f}x"],
            "Scenario B": [f"${final_b:,.2f}", f"{pb_b} Yrs" if pb_b else "N/A", f"{(final_b+cac_b)/cac_b:.2f}x"]
        }))

if __name__ == "__main__":
    show_clv_calculator()
