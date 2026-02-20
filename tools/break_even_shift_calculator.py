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

    # Units needed to cover Fixed Costs + Target Profit
    required_units = (fixed + target_profit) / margin
    actual_profit = (margin * volume) - fixed
    mos = (volume - required_units) / volume if volume > 0 else -1

    # Analytical Risk Scoring
    risk = 0
    if actual_profit < 0: risk += 50
    if mos < 0.10: risk += 30
    if margin < price * 0.15: risk += 20 

    risk = min(risk, 100)

    return {
        "margin": margin,
        "required_units": required_units,
        "profit": actual_profit,
        "mos": mos,
        "risk": risk
    }

# -----------------------
# Plot (Enhanced for Clarity)
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

    ax.plot(x, total_cost, label="Total Cost", color="#d62728", linewidth=3)
    ax.plot(x, revenue, label="Revenue", color="#2ca02c", linewidth=3)

    # Key Strategic Indicators
    ax.axvline(required_units, linestyle="--", color="#7f7f7f", linewidth=2,
               label=f"Required Units ({int(required_units)})")
    ax.axvline(volume, linestyle="-.", color="#1f77b4", linewidth=2,
               label=f"Analyzed Volume ({int(volume)})")

    ax.set_title("Break-Even & Target Profit Analysis", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Units Sold", fontweight="bold")
    ax.set_ylabel("Currency (USD)", fontweight="bold")

    # Visualize Profit Zone
    profit_zone = [revenue[i] > total_cost[i] for i in range(len(x))]
    ax.fill_between(x, revenue, total_cost, where=profit_zone, color='green', alpha=0.1)

    ax.legend(loc="upper left")
    ax.grid(True, linestyle=":", alpha=0.5)

    st.pyplot(fig)

# -----------------------
# Main App
# -----------------------

def show_break_even_shift_calculator():
    st.header("📈 Executive Scenario Simulator")
    st.write("Analyze the structural resilience of your business model against market shocks.")

    with st.sidebar:
        st.subheader("Structural Cost Inputs")
        f_costs = st.text_input("Existing Fixed Costs", "10000")
        f_invest = st.text_input("New Investment", "5000")
        t_profit = st.text_input("Target Profit", "2000")

        st.divider()
        st.subheader("Unit Economics")
        u_price = st.text_input("Unit Price", "11")
        u_cost = st.text_input("Variable Cost", "6.5")
        u_sold = st.text_input("Planned Volume", "4000")

        st.divider()
        st.subheader("Stress Testing (Volatility)")
        p_stress = st.slider("Price Shift (%)", -30, 30, 0)
        c_stress = st.slider("Cost Shift (%)", -30, 30, 0)
        v_stress = st.slider("Volume Shift (%)", -50, 50, 0)

        run = st.button("Execute Strategic Analysis")

    if run:
        # 1. Data Processing
        fixed_total = parse_number_en(f_costs) + parse_number_en(f_invest)
        target_profit = parse_number_en(t_profit)

        base_p, base_c, base_v = parse_number_en(u_price), parse_number_en(u_cost), parse_number_en(u_sold)
        
        stress_p = base_p * (1 + p_stress / 100)
        stress_c = base_c * (1 + c_stress / 100)
        stress_v = base_v * (1 + v_stress / 100)

        base_metrics = calculate_metrics(fixed_total, target_profit, base_p, base_c, base_v)
        stress_metrics = calculate_metrics(fixed_total, target_profit, stress_p, stress_c, stress_v)

        if not base_metrics or not stress_metrics:
            st.error("🔴 Fatal Error: Contribution margin collapsed in stress scenario.")
            return

        # 2. Executive Comparison Table
        st.subheader("📊 Scenario Comparison")
        comparison_df = pd.DataFrame({
            "Metric": ["Required Units", "Projected Net Profit", "Margin of Safety (%)", "Risk Index (0-100)"],
            "Base Case": [
                f"{int(base_metrics['required_units'])} units",
                f"${base_metrics['profit']:,.0f}",
                f"{base_metrics['mos']*100:.1f}%",
                f"{base_metrics['risk']}"
            ],
            "Stress Case": [
                f"{int(stress_metrics['required_units'])} units",
                f"${stress_metrics['profit']:,.0f}",
                f"{stress_metrics['mos']*100:.1f}%",
                f"{stress_metrics['risk']}"
            ]
        })
        st.table(comparison_df)

        # 3. Delta Impact Analysis
        st.subheader("📉 Variance Analysis (Impact of Stress)")
        d_profit = stress_metrics["profit"] - base_metrics["profit"]
        d_risk = stress_metrics["risk"] - base_metrics["risk"]
        d_mos = (stress_metrics["mos"] - base_metrics["mos"]) * 100

        c1, c2, c3 = st.columns(3)
        c1.metric("Profit Variance", f"${d_profit:,.0f}", delta=d_profit)
        c2.metric("Risk Delta", f"{d_risk} pts", delta=d_risk, delta_color="inverse")
        c3.metric("MoS Variance", f"{d_mos:.1f}%", delta=d_mos)

        # 4. Strategic Assessment
        st.divider()
        st.subheader("🧠 Strategic Assessment")
        
        if stress_metrics["risk"] > 75:
            st.error("🔴 FRAGILE: The model fails to absorb the current stress level. Immediate restructuring required.")
        elif stress_metrics["risk"] > 40:
            st.warning("🟠 VULNERABLE: Significant erosion of safety buffers. Monitor unit economics.")
        else:
            st.success("🟢 RESILIENT: Business model remains structurally sound under the analyzed stress.")

        # 5. Visual Analysis
        st.divider()
        st.subheader("📈 Stress Scenario Chart")
        
        
        
        plot_break_even(fixed_total, target_profit, stress_p, stress_c, stress_v)

        # 6. Final Risk Signal
        st.markdown(f"**Calculated Stress Risk:** {stress_metrics['risk']}/100")
        st.progress(stress_metrics["risk"] / 100)


        # -----------------------------
        # 6. Tornado Sensitivity
        # -----------------------------

        st.divider()
        st.subheader("🌪 Sensitivity Analysis (Tornado Chart)")
        plot_tornado(fixed_total, target_profit, stress_p, stress_c, stress_v)

if __name__ == "__main__":
    show_break_even_shift_calculator()
# -----------------------
# Tornado Sensitivity Chart
# -----------------------

def plot_tornado(fixed, target_profit, price, cost, volume):

    base_metrics = calculate_metrics(fixed, target_profit, price, cost, volume)
    if not base_metrics:
        return

    base_profit = base_metrics["profit"]

    shock = 0.10  # 10% sensitivity

    scenarios = {
        "Price +10%": calculate_metrics(fixed, target_profit, price*1.1, cost, volume)["profit"],
        "Price -10%": calculate_metrics(fixed, target_profit, price*0.9, cost, volume)["profit"],
        "Cost +10%": calculate_metrics(fixed, target_profit, price, cost*1.1, volume)["profit"],
        "Cost -10%": calculate_metrics(fixed, target_profit, price, cost*0.9, volume)["profit"],
        "Volume +10%": calculate_metrics(fixed, target_profit, price, cost, volume*1.1)["profit"],
        "Volume -10%": calculate_metrics(fixed, target_profit, price, cost, volume*0.9)["profit"],
    }

    impact = {k: v - base_profit for k, v in scenarios.items()}

    sorted_impact = dict(sorted(impact.items(), key=lambda x: abs(x[1]), reverse=True))

    labels = list(sorted_impact.keys())
    values = list(sorted_impact.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels, values)

    ax.set_title("Tornado Sensitivity Analysis (±10%)", fontweight="bold")
    ax.set_xlabel("Impact on Profit ($)")
    ax.axvline(0)

    st.pyplot(fig)
