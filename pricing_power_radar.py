import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------
# Core Calculations
# -----------------------------------

def normalize(value, min_val, max_val):
    if max_val - min_val == 0:
        return 0
    return (value - min_val) / (max_val - min_val)

def calculate_pricing_power_score(margin, substitution, elasticity, concentration):

    # Margin strength (higher = better)
    margin_score = normalize(margin, 0, 0.8)

    # Substitution exposure (lower = better)
    substitution_score = 1 - normalize(substitution, 0, 1)

    # Elasticity fragility (lower elasticity = stronger power)
    elasticity_score = 1 - normalize(elasticity, 0, 3)

    # Revenue concentration risk (lower = better)
    concentration_score = 1 - normalize(concentration, 0, 1)

    final_score = (
        margin_score * 0.35 +
        substitution_score * 0.25 +
        elasticity_score * 0.25 +
        concentration_score * 0.15
    )

    return round(final_score * 100, 1)

def classify_power(score):
    if score < 30:
        return "Weak Pricing Power", "🔴"
    elif score < 55:
        return "Defensive Structure", "🟠"
    elif score < 75:
        return "Strong Position", "🟢"
    else:
        return "Dominant Pricing Power", "🏆"

# -----------------------------------
# UI
# -----------------------------------

def show_pricing_power_radar():

    st.header("📊 Pricing Power Radar")
    st.write("Evaluate structural pricing strength beyond simple elasticity calculations.")

    with st.sidebar:
        st.subheader("Core Structural Inputs")

        margin = st.slider("Contribution Margin (%)", 5.0, 90.0, 40.0) / 100
        substitution = st.slider("Substitution Exposure (%)", 0.0, 100.0, 40.0) / 100
        elasticity = st.slider("Estimated Price Elasticity", 0.1, 3.0, 1.2)
        concentration = st.slider("Revenue Concentration Risk (%)", 0.0, 100.0, 30.0) / 100

        run = st.button("Evaluate Pricing Power")

    if run:

        score = calculate_pricing_power_score(
            margin,
            substitution,
            elasticity,
            concentration
        )

        label, icon = classify_power(score)

        st.divider()
        st.subheader("🏁 Structural Pricing Assessment")

        col1, col2 = st.columns(2)
        col1.metric("Pricing Power Score", f"{score}/100")
        col2.metric("Classification", f"{icon} {label}")

        st.divider()
        st.subheader("📌 Strategic Interpretation")

        if score < 30:
            st.error("Business is highly exposed. Price increases likely destroy volume.")
        elif score < 55:
            st.warning("Pricing decisions must be cautious. Substitution pressure limits flexibility.")
        elif score < 75:
            st.success("Company has measurable pricing flexibility.")
        else:
            st.success("Structural pricing dominance. Brand or positioning creates insulation.")

        st.divider()
        st.subheader("🧠 Structural Drivers")

        drivers = pd.DataFrame({
            "Driver": [
                "Margin Strength",
                "Substitution Protection",
                "Elasticity Resistance",
                "Revenue Diversification"
            ],
            "Impact Level": [
                f"{margin*100:.1f}%",
                f"{(1-substitution)*100:.1f}%",
                f"{(1 - (elasticity/3))*100:.1f}%",
                f"{(1-concentration)*100:.1f}%"
            ]
        })

        st.table(drivers)


if __name__ == "__main__":
    show_pricing_power_radar()

