import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# LOGIC
# -------------------------------

def required_sales_increase(price_reduction_pct, contribution_margin):
    """
    Calculates the required sales increase (%) to offset
    a price reduction, given the contribution margin.
    """
    if contribution_margin <= 0 or contribution_margin >= 1:
        return 0
    return round(price_reduction_pct / contribution_margin * 100, 2)


def apply_substitution_effect(base_increase, substitution_factor):
    """
    Applies the substitution intensity factor
    """
    return round(base_increase * substitution_factor, 2)


def plot_substitutes_sensitivity(base_value, scenarios):
    """
    Tornado sensitivity chart for substitutes
    """
    labels = []
    impacts = []

    for name, factor in scenarios.items():
        adjusted = base_value * factor
        impact = adjusted - base_value
        labels.append(name)
        impacts.append(impact)

    impacts = np.array(impacts)

    fig, ax = plt.subplots()
    ax.barh(labels, impacts)
    ax.axvline(0)

    ax.set_xlabel("Impact on Required Sales Increase (%)")
    ax.set_title("Sensitivity Analysis – Substitutes")

    return fig


# -------------------------------
# UI
# -------------------------------

def show_substitutes_sensitivity_tool():
    st.title("🔁 Substitutes – Sensitivity Analysis Tool")

    st.markdown("""
    This tool shows **how substitutes affect**
    the **required sales increase** after a **price reduction**.

    👉 Purpose: **strategic decision-making**, not simple arithmetic.
    """)

    st.subheader("📥 Base Scenario")

    price_reduction = st.number_input(
        "Price Reduction (%)",
        min_value=0.0,
        value=5.0,
        step=0.5
    ) / 100

    contribution_margin = st.number_input(
        "Contribution Margin (%)",
        min_value=1.0,
        max_value=99.0,
        value=40.0,
        step=1.0
    ) / 100

    base_required = required_sales_increase(
        price_reduction,
        contribution_margin
    )

    st.info(f"📌 **Base Required Sales Increase:** {base_required}%")

    st.divider()

    st.subheader("🔁 Substitution Scenarios")

    st.markdown("Define how aggressively substitutes compete:")

    low = st.slider("Low substitution", 0.5, 1.0, 0.8, 0.05)
    base = st.slider("Base case", 0.8, 1.2, 1.0, 0.05)
    high = st.slider("High substitution", 1.0, 1.5, 1.25, 0.05)
    aggressive = st.slider("Very aggressive substitute", 1.2, 2.0, 1.5, 0.05)

    scenarios = {
        "Low substitution": low,
        "Base case": base,
        "High substitution": high,
        "Very aggressive substitute": aggressive
    }

    st.divider()

    if st.button("📊 Run Sensitivity Analysis"):
        st.subheader("📈 Results")

        for name, factor in scenarios.items():
            adjusted = apply_substitution_effect(base_required, factor)
            st.write(f"**{name}** → Required increase: **{adjusted}%**")

        st.subheader("📊 Sensitivity Diagram")
        fig = plot_substitutes_sensitivity(base_required, scenarios)
        st.pyplot(fig)

        st.divider()

        st.markdown("""
        ### 🧠 How to read this chart
        - ➖ Left: low substitution risk  
        - ➕ Right: **dangerous market**
        - The longer the bar → the **higher the strategic pressure**

        ✔ If the **worst-case scenario** is unrealistic → the price cut **should not be implemented**
        """)
