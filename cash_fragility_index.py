import streamlit as st
import pandas as pd

# -----------------------------------
# Core Calculations
# -----------------------------------

def normalize(value, min_val, max_val):
    if max_val - min_val == 0:
        return 0
    return max(0, min(1, (value - min_val) / (max_val - min_val)))

def calculate_fragility_score(
    fixed_cost_ratio,
    revenue_volatility,
    runway_months,
    cash_flow_margin
):

    fixed_score = normalize(fixed_cost_ratio, 0, 1)
    volatility_score = normalize(revenue_volatility, 0, 0.5)
    runway_score = 1 - normalize(runway_months, 0, 24)
    margin_score = 1 - normalize(cash_flow_margin, -0.2, 0.4)

    final = (
        fixed_score * 0.30 +
        volatility_score * 0.25 +
        runway_score * 0.25 +
        margin_score * 0.20
    )

    return round(final * 100, 1)

def classify_fragility(score):
    if score < 30:
        return "Stable Structure", "🟢"
    elif score < 55:
        return "Vulnerable", "🟡"
    elif score < 75:
        return "Fragile", "🟠"
    else:
        return "Critical Liquidity Risk", "🔴"

# -----------------------------------
# UI
# -----------------------------------

def show_cash_fragility_index():

    st.header("💣 Cash Fragility Index")
    st.write("Evaluate structural liquidity risk under demand or revenue shocks.")

    # ---------------- Sidebar ----------------
    with st.sidebar:

        st.subheader("Financial Structure Inputs")

        fixed_cost_ratio = st.slider(
            "Fixed Costs as % of Total Costs",
            0.0, 100.0, 50.0
        ) / 100
        st.caption(
            "Share of costs that do not change with sales volume. "
            "Higher percentage = higher operating leverage and higher downside risk."
        )

        revenue_volatility = st.slider(
            "Revenue Volatility (Std Dev %)",
            0.0, 50.0, 15.0
        ) / 100
        st.caption(
            "How unstable sales are over time. "
            "Higher volatility increases the need for cash buffers."
        )

        runway_months = st.slider(
            "Cash Runway (Months)",
            0, 36, 8
        )
        st.caption(
            "How many months the company can operate without new revenue "
            "before cash is exhausted."
        )

        cash_flow_margin = st.slider(
            "Operating Cash Flow Margin (%)",
            -20.0, 40.0, 10.0
        ) / 100
        st.caption(
            "Percentage of revenue converted into operating cash. "
            "Higher margin improves survival capacity during downturns."
        )

        run = st.button("Evaluate Fragility")

    # ---------------- Results ----------------
    if run:

        score = calculate_fragility_score(
            fixed_cost_ratio,
            revenue_volatility,
            runway_months,
            cash_flow_margin
        )

        label, icon = classify_fragility(score)

        st.divider()
        st.subheader("📊 Liquidity Risk Assessment")

        col1, col2 = st.columns(2)
        col1.metric("Fragility Score", f"{score}/100")
        col2.metric("Classification", f"{icon} {label}")

        st.divider()
        st.subheader("📌 Interpretation")

        if score < 30:
            st.success("Structure is resilient under moderate shocks.")
        elif score < 55:
            st.warning("Liquidity stress possible under revenue contraction.")
        elif score < 75:
            st.warning("High sensitivity to downturns. Cost structure is rigid.")
        else:
            st.error("Severe liquidity exposure. Structural adjustment required.")

        st.divider()
        st.subheader("🧠 Structural Drivers")

        drivers = pd.DataFrame({
            "Driver": [
                "Cost Rigidity",
                "Revenue Volatility",
                "Liquidity Buffer",
                "Cash Flow Efficiency"
            ],
            "Current Level": [
                f"{fixed_cost_ratio*100:.1f}%",
                f"{revenue_volatility*100:.1f}%",
                f"{runway_months} months",
                f"{cash_flow_margin*100:.1f}%"
            ]
        })

        st.table(drivers)


if __name__ == "__main__":
    show_cash_fragility_index()
