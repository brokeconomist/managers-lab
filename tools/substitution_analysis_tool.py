import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -------------------------------
# Calculation Engines
# -------------------------------

def parse_number(x):
    try:
        return float(str(x).replace(",", ""))
    except:
        return 0.0

def calculate_max_drop(old_price, price_inc_pct, profit_A, profit_B, profit_C, profit_D, pB, pC, pD):
    # Weighted profit from customers who switch
    weighted_sub_profit = (pB * profit_B + pC * profit_C + pD * profit_D)
    
    numerator = -price_inc_pct
    # Strategic Formula: Maintenance of total profit including substitution recovery
    denominator = ((profit_A - weighted_sub_profit) / old_price) + price_inc_pct
    
    if denominator == 0:
        return 0.0
    return (numerator / denominator) * 100

def required_sales_increase(price_red_pct, contribution_margin):
    if contribution_margin <= 0:
        return 0.0
    return (price_red_pct / contribution_margin) * 100

# -------------------------------
# Visualization
# -------------------------------

def plot_sensitivity(base_value, scenarios):
    labels = list(scenarios.keys())
    impacts = [base_value * factor - base_value for factor in scenarios.values()]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#2ca02c' if x <= 0 else '#d62728' for x in impacts]
    ax.barh(labels, impacts, color=colors, alpha=0.8)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_title("Sensitivity Analysis: Impact on Required Growth", fontsize=12, fontweight='bold')
    ax.set_xlabel("Percentage Point Shift vs Base Case (%)")
    ax.grid(True, linestyle=':', alpha=0.4)
    return fig

# -------------------------------
# Main UI Logic
# -------------------------------

def show_substitutes_sensitivity_tool():
    st.header("🔁 Strategic Substitution & Elasticity Analysis")
    st.write("Quantitative assessment of volume risks and pricing power through substitution modeling.")

    # -------------------------------
    # SIDEBAR INPUTS
    # -------------------------------
    with st.sidebar:
        st.header("Parameters")
        mode = st.radio("Strategic Action:", ["Price Increase (Drop Limit)", "Price Reduction (Growth Required)"])
        
        st.divider()
        if mode == "Price Increase (Drop Limit)":
            st.subheader("Core Product A")
            old_p = st.text_input("Current Price (€)", "1.50")
            p_inc = st.slider("Proposed Price Increase (%)", 0.0, 50.0, 10.0) / 100
            p_A = st.text_input("Unit Profit (€)", "0.30")
            
            st.subheader("Substitution Matrix")
            st.caption("Profit per unit if they switch to:")
            p_B = st.number_input("Profit B (€)", value=0.20)
            p_C = st.number_input("Profit C (€)", value=0.20)
            p_D = st.number_input("Profit D (€)", value=0.05)
            
            st.subheader("Switching Probability (%)")
            pct_B = st.slider("Switch to B", 0, 100, 45) / 100
            pct_C = st.slider("Switch to C", 0, 100, 20) / 100
            pct_D = st.slider("Switch to D", 0, 100, 5) / 100
            
        else:
            st.subheader("Pricing Strategy")
            p_red = st.slider("Price Reduction (%)", 0.0, 40.0, 5.0) / 100
            c_margin = st.slider("Contribution Margin (%)", 5.0, 95.0, 40.0) / 100
            
            st.subheader("Constraints")
            max_cap = st.number_input("Market Capacity Limit (%)", value=15.0)
            
            st.subheader("Elasticity Sensitivity")
            s_low = st.slider("Low Intensity Factor", 0.5, 1.0, 0.8)
            s_high = st.slider("High Intensity Factor", 1.0, 2.5, 1.3)

        run = st.button("Execute Analysis")

    # -------------------------------
    # MAIN RESULTS
    # -------------------------------
    if not run:
        st.info("👈 Adjust parameters in the sidebar and click 'Execute Analysis'.")
        return

    st.divider()
    
    if mode == "Price Increase (Drop Limit)":
        # Check for logical errors
        total_switch = pct_B + pct_C + pct_D
        leakage = 1.0 - total_switch
        
        if total_switch > 1.0:
            st.error("❌ Invalid Distribution: Total switching probabilities exceed 100%.")
            return

        # 1. Visualization: Demand Distribution
        st.subheader("🎯 Projected Demand Redistribution")
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Switch to B', 'Switch to C', 'Switch to D', 'Market Leakage (Lost)'],
            values=[pct_B, pct_C, pct_D, max(0, leakage)],
            hole=.4,
            marker_colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
        )])
        st.plotly_chart(fig_pie, use_container_width=True)

        # 2. Key Metrics
        max_drop = calculate_max_drop(
            parse_number(old_p), p_inc, parse_number(p_A),
            p_B, p_C, p_D, pct_B, pct_C, pct_D
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Max Allowed Vol. Drop", f"{max_drop:.2f}%")
        c2.metric("Switching Rate", f"{total_switch*100:.1f}%")
        c3.metric("System Leakage", f"{leakage*100:.1f}%")

        # 3. Strategic Verdict
        st.divider()
        st.subheader("🧠 Analytical Verdict")
        if abs(max_drop) < 8:
            st.error("🔴 **High Fragility:** Your margin structure cannot tolerate volume loss. Pricing power is weak.")
        elif abs(max_drop) < 18:
            st.warning("🟡 **Moderate Resilience:** The price increase is viable only if brand loyalty is high.")
        else:
            st.success("🟢 **Strong Pricing Power:** You have a significant buffer to absorb substitution.")

        st.info("💡 **Manager's Tip:** If any substitute is a competitor product, set its profit to €0.00 to see the net loss to your company.")

    else:
        # PRICE REDUCTION MODE
        base_req = required_sales_increase(p_red, c_margin)
        
        st.subheader("📊 Volume Growth Requirements")
        
        scenarios = {
            "High Loyalty (Low Sub)": s_low,
            "Base Case": 1.0,
            "Aggressive Sub": s_high
        }
        
        results_data = []
        for name, factor in scenarios.items():
            adj = base_req * factor
            status = "✅ Feasible" if adj <= max_cap else "❌ Infeasible"
            results_data.append({
                "Scenario": name,
                "Growth Required (%)": f"{adj:.2f}%",
                "Status": status
            })
        
        st.table(pd.DataFrame(results_data))
        
        # Tornado Chart
        st.pyplot(plot_sensitivity(base_req, scenarios))

        

        st.divider()
        st.subheader("🧭 Executive Decision Support")
        if base_req > max_cap:
            st.error(f"**Structural Deficit:** Required growth ({base_req:.1f}%) exceeds your market capacity constraint ({max_cap}%). Do not reduce price.")
        else:
            st.success(f"**Structural Buffer:** Required growth ({base_req:.1f}%) is within limits. Action is economically supportable.")

if __name__ == "__main__":
    show_substitutes_sensitivity_tool()
