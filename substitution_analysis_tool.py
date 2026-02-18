import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# -------------------------------
# Calculation Engines
# -------------------------------

def parse_number(x):
    try:
        return float(str(x).replace(",", ""))
    except:
        return 0.0

def calculate_max_drop(old_price, price_inc_pct, profit_A, profit_B, profit_C, profit_D, pB, pC, pD):
    weighted_sub_profit = (pB * profit_B + pC * profit_C + pD * profit_D)
    numerator = -price_inc_pct
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
    ax.axvline(0, linewidth=1)
    ax.set_title("Sensitivity Analysis: Impact on Required Growth", fontsize=14, fontweight='bold')
    ax.set_xlabel("Percentage Point Shift (%)")
    ax.grid(True, linestyle=':', alpha=0.4)
    return fig

# -------------------------------
# Main UI Logic
# -------------------------------

def show_substitutes_sensitivity_tool():
    st.header("🔁 Strategic Substitution & Elasticity Analysis")
    st.write("Analyze structural risks from price movements and competitor substitution.")

    # -------------------------------
    # SIDEBAR INPUTS
    # -------------------------------
    with st.sidebar:
        mode = st.radio("Strategic Action:", ["Price Increase (Drop Limit)", "Price Reduction (Growth Required)"])
        
        st.divider()
        if mode == "Price Increase (Drop Limit)":
            st.subheader("Product A Parameters")
            old_p = st.text_input("Current Price (€)", "1.50")
            p_inc = st.slider("Price Increase (%)", 0.0, 50.0, 10.0) / 100
            p_A = st.text_input("Unit Profit - Product A (€)", "0.30")
            
            st.subheader("Substitute Profits (€)")
            p_B = st.number_input("Unit Profit B", value=0.20)
            p_C = st.number_input("Unit Profit C", value=0.20)
            p_D = st.number_input("Unit Profit D", value=0.05)
            
            st.subheader("Switching Behavior (%)")
            pct_B = st.slider("Switch to B", 0, 100, 45) / 100
            pct_C = st.slider("Switch to C", 0, 100, 20) / 100
            pct_D = st.slider("Switch to D", 0, 100, 5) / 100
            
        else:
            st.subheader("Pricing Strategy")
            p_red = st.slider("Price Reduction (%)", 0.0, 30.0, 5.0) / 100
            c_margin = st.slider("Contribution Margin (%)", 5.0, 95.0, 40.0) / 100
            
            st.subheader("Market Constraints")
            max_cap = st.number_input("User-Defined Max Capacity (%)", value=15.0)
            
            st.subheader("Substitution Intensity")
            s_low = st.slider("Low Intensity", 0.5, 1.0, 0.8)
            s_high = st.slider("High Intensity", 1.0, 2.0, 1.3)

        run = st.button("Execute Analysis")

    # -------------------------------
    # MAIN RESULTS
    # -------------------------------
    if run:
        st.divider()
        
        # =====================================
        # PRICE INCREASE MODE
        # =====================================
        if mode == "Price Increase (Drop Limit)":
            
            total_switch = pct_B + pct_C + pct_D
            if total_switch > 1.0:
                st.error("Total switching cannot exceed 100%. Adjust sliders.")
                return

            max_drop = calculate_max_drop(
                parse_number(old_p),
                p_inc,
                parse_number(p_A),
                p_B, p_C, p_D,
                pct_B, pct_C, pct_D
            )

            leakage = (1 - total_switch) * 100

            c1, c2 = st.columns(2)
            c1.metric("Max Acceptable Sales Drop", f"{max_drop:.2f}%")
            c2.metric("System Leakage (No Purchase)", f"{leakage:.1f}%")

            # ---------------- Strategic Verdict ----------------
            st.divider()
            st.subheader("🧠 Strategic Verdict")

            if abs(max_drop) < 5:
                st.error("High Fragility: Even small volume losses destroy pricing gains.")
            elif abs(max_drop) < 15:
                st.warning("Moderate Risk: Price increase is viable but sensitive to switching.")
            else:
                st.success("Pricing Power Detected: Business can tolerate meaningful volume loss.")

            # Break-even switching insight
            st.write(
                f"Strategic Boundary: Beyond {abs(max_drop):.2f}% volume loss, "
                "the price increase no longer compensates structural substitution."
            )

        # =====================================
        # PRICE REDUCTION MODE
        # =====================================
        else:
            base_req = required_sales_increase(p_red, c_margin)
            
            st.subheader("📊 Required Growth Scenarios")
            
            scenarios = {
                "Low Substitution": s_low,
                "Base Case": 1.0,
                "High Substitution": s_high
            }
            
            results_data = []
            for name, factor in scenarios.items():
                adj = base_req * factor
                status = "✅ Feasible" if adj <= max_cap else "❌ Infeasible"
                results_data.append({
                    "Scenario": name,
                    "Required Growth (%)": f"{adj:.2f}",
                    "Status": status
                })
            
            results_df = pd.DataFrame(results_data)
            st.table(results_df)
            
            # Sensitivity Chart
            st.subheader("📈 Sensitivity Analysis")
            fig = plot_sensitivity(base_req, scenarios)
            st.pyplot(fig)

            # ---------------- Strategic Assessment ----------------
            st.divider()
            st.subheader("🧠 Executive Assessment")

            if base_req > max_cap:
                st.error(
                    f"Structural Deficit: Required growth ({base_req:.1f}%) "
                    f"exceeds market capacity ({max_cap}%)."
                )
            else:
                st.success(
                    f"Structural Buffer: Required growth ({base_req:.1f}%) "
                    f"is within capacity constraint ({max_cap}%)."
                )

            # Strategic Signal
            st.divider()
            st.subheader("📌 Strategic Signal")

            if base_req <= max_cap:
                st.success("Recommendation: Price reduction is economically supportable.")
            else:
                st.warning("Recommendation: Avoid aggressive price cuts without demand expansion capability.")

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    show_substitutes_sensitivity_tool()
