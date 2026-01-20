import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# LOGIC (UNCHANGED)
# -------------------------------

def required_sales_increase(price_reduction_pct, contribution_margin):
    """
    Calculates the required sales increase (%) to offset a price reduction,
    given the contribution margin.
    """
    if contribution_margin <= 0 or contribution_margin >= 1:
        return 0
    return round(price_reduction_pct / contribution_margin * 100, 2)


def apply_substitution_effect(base_increase, substitution_factor):
    """
    Applies substitution intensity factor to required sales increase.
    """
    return round(base_increase * substitution_factor, 2)


def plot_substitutes_sensitivity(base_value, scenarios):
    """
    Tornado-style sensitivity chart for substitutes
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
    ### Technical perspective

    This tool evaluates **how substitution pressure affects the required sales increase**
    following a **price reduction**.

    ⚠️ The model performs **no market forecasting**.  
    All feasibility judgments are based on **user-defined assumptions**.
    """)

    # -------------------------------
    # BASE SCENARIO
    # -------------------------------

    st.subheader("📥 Base Scenario (Model Calculation)")

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

    st.info(f"📌 **Model-derived required sales increase:** {base_required}%")

    st.caption(
        "This value is purely mechanical: "
        "price reduction divided by contribution margin."
    )

    st.divider()

    # -------------------------------
    # USER ASSUMPTION (EXOGENOUS)
    # -------------------------------

    st.subheader("👤 User-Defined Market Capacity (External Assumption)")

    max_capacity = st.number_input(
        "Maximum feasible sales increase (%)",
        min_value=0.0,
        value=10.0,
        step=1.0
    )

    st.warning(
        "This input represents **your own judgment** about market limits.\n\n"
        "• It is NOT calculated by the model\n"
        "• It does NOT represent a forecast\n"
        "• It reflects beliefs about market size, consumption frequency, "
        "and ability to capture share from competitors"
    )

    st.divider()

    # -------------------------------
    # SUBSTITUTION SCENARIOS
    # -------------------------------

    st.subheader("🔁 Substitution Intensity Scenarios")

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

    # -------------------------------
    # RESULTS
    # -------------------------------

    if st.button("📊 Run Sensitivity Analysis"):
        st.subheader("📈 Results")

        for name, factor in scenarios.items():
            adjusted = apply_substitution_effect(base_required, factor)

            feasible = adjusted <= max_capacity

            status = "✅ Feasible" if feasible else "❌ Infeasible"

            st.write(
                f"**{name}** → Required increase: **{adjusted}%** "
                f"| User capacity: {max_capacity}% → {status}"
            )

        st.subheader("📊 Sensitivity Diagram")
        fig = plot_substitutes_sensitivity(base_required, scenarios)
        st.pyplot(fig)

        st.divider()

        st.markdown("""
        ### Technical interpretation

        - The model **does not decide** whether a strategy is viable  
        - It only computes **required sales growth**
        - Feasibility depends entirely on **your externally imposed constraint**

        If required growth exceeds your stated market capacity,
        the scenario should be rejected **based on your own assumptions**.
        """)
