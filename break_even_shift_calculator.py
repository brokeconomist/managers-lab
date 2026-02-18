import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# -----------------------
# Utilities
# -----------------------

def parse_number_en(number_str):
    try:
        return float(str(number_str).replace(",", ""))
    except:
        return 0.0


def calculate_metrics(fixed, target_profit, price, cost, volume):

    margin = price - cost
    if margin <= 0:
        return None

    required_units = (fixed + target_profit) / margin
    actual_profit = (margin * volume) - fixed
    mos = (volume - required_units) / volume if volume > 0 else -1

    risk = 0
    if actual_profit < 0:
        risk += 50
    if mos < 0.10:
        risk += 30
    if margin < price * 0.15:
        risk += 20

    risk = min(risk, 100)

    return {
        "margin": margin,
        "required_units": required_units,
        "profit": actual_profit,
        "mos": mos,
        "risk": risk
    }


# -----------------------
# Plot
# -----------------------

def plot_break_even(fixed, target_profit, price, cost, volume):

    metrics = calculate_metrics(fixed, target_profit, price, cost, volume)
    if not metrics:
        return

    required_units = metrics["required_units"]

    max_units = int(max(required_units, volume) * 1.6) + 10
    x = list(range(0, max_units))

    total_cost = [fixed + cost * q for q in x]
    revenue = [price * q for q in x]

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(x, total_cost, label="Total Cost", linewidth=3)
    ax.plot(x, revenue, label="Revenue", linewidth=3)

    ax.axvline(required_units, linestyle="--", linewidth=2,
               label=f"Required Units ({int(required_units)})")

    ax.axvline(volume, linestyle="-.", linewidth=2,
               label=f"Analyzed Volume ({int(volume)})")

    ax.set_title("Break-Even & Target Profit Analysis", fontsize=16, fontweight="bold")
    ax.set_xlabel("Units Sold")
    ax.set_ylabel("USD")

    profit_zone = [revenue[i] > total_cost[i] for i in range(len(x))]
    ax.fill_between(x, revenue, total_cost, where=profit_zone, alpha=0.1)

    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.5)

    st.pyplot(fig)


# -----------------------
# Main App
# -----------------------

def show_break_even_shift_calculator():

    st.header("📈 Executive Scenario Simulator")
    st.write("Compare Base vs Stress scenarios side by side.")

    with st.sidebar:

        st.subheader("Financial Inputs")
        f_costs = st.text_input("Existing Fixed Costs", "10000")
        f_invest = st.text_input("New Fixed Investment", "5000")
        t_profit = st.text_input("Target Profit", "2000")

        st.divider()

        u_price = st.text_input("Price per Unit", "11")
        u_cost = st.text_input("Variable Cost per Unit", "6.5")
        u_sold = st.text_input("Units Sold", "4000")

        st.divider()

        st.subheader("Stress Adjustments")
        p_stress = st.slider("Price Shift (%)", -30, 30, 0)
        c_stress = st.slider("Cost Shift (%)", -30, 30, 0)
        v_stress = st.slider("Volume Shift (%)", -50, 50, 0)

        run = st.button("Run Scenario Comparison")

    if run:

        fixed = parse_number_en(f_costs) + parse_number_en(f_invest)
        target_profit = parse_number_en(t_profit)

        base_price = parse_number_en(u_price)
        base_cost = parse_number_en(u_cost)
        base_volume = parse_number_en(u_sold)

        stress_price = base_price * (1 + p_stress / 100)
        stress_cost = base_cost * (1 + c_stress / 100)
        stress_volume = base_volume * (1 + v_stress / 100)

        base_metrics = calculate_metrics(fixed, target_profit,
                                         base_price, base_cost, base_volume)

        stress_metrics = calculate_metrics(fixed, target_profit,
                                           stress_price, stress_cost, stress_volume)

        if not base_metrics or not stress_metrics:
            st.error("Contribution margin became zero or negative.")
            return

        st.divider()

        # -----------------------
        # Comparison Table
        # -----------------------

        comparison_df = pd.DataFrame({
            "Metric": [
                "Required Units",
                "Projected Profit",
                "Margin of Safety",
                "Risk Score"
            ],
            "Base Scenario": [
                int(base_metrics["required_units"]),
                f"${base_metrics['profit']:,.0f}",
                f"{base_metrics['mos']*100:.1f}%",
                base_metrics["risk"]
            ],
            "Stress Scenario": [
                int(stress_metrics["required_units"]),
                f"${stress_metrics['profit']:,.0f}",
                f"{stress_metrics['mos']*100:.1f}%",
                stress_metrics["risk"]
            ]
        })

        st.subheader("📊 Scenario Comparison")
        st.table(comparison_df)

        st.divider()

        # -----------------------
        # Visualization (Stress)
        # -----------------------

        st.subheader("📈 Stress Scenario Visualization")
        plot_break_even(fixed, target_profit,
                        stress_price, stress_cost, stress_volume)

        # Risk bar
        st.progress(stress_metrics["risk"] / 100)
        st.caption(f"Stress Scenario Risk Score: {stress_metrics['risk']}/100")


if __name__ == "__main__":
    show_break_even_shift_calculator()
