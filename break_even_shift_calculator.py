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


# -----------------------
# Plotting Logic
# -----------------------

def plot_break_even(fixed_costs, target_profit, price, unit_cost, units_sold):
    cm = price - unit_cost
    if cm <= 0:
        return

    required_units = (fixed_costs + target_profit) / cm

    max_units = int(max(required_units, units_sold) * 1.6) + 10
    x = list(range(0, max_units))

    total_cost = [fixed_costs + unit_cost * q for q in x]
    revenue = [price * q for q in x]

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(x, total_cost, label="Total Cost", linewidth=3)
    ax.plot(x, revenue, label="Revenue", linewidth=3)

    ax.axvline(required_units, linestyle="--", linewidth=2,
               label=f"Required Units ({int(required_units)})")

    ax.axvline(units_sold, linestyle="-.", linewidth=2,
               label=f"Analyzed Volume ({int(units_sold)})")

    ax.set_xlabel("Units Sold", fontsize=12, fontweight='bold')
    ax.set_ylabel("Currency (USD)", fontsize=12, fontweight='bold')
    ax.set_title("Executive Break-Even & Target Profit Analysis",
                 fontsize=16, fontweight='bold', pad=20)

    ax.legend(loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)

    # Profit shading
    profit_zone = [revenue[i] > total_cost[i] for i in range(len(x))]
    ax.fill_between(x, revenue, total_cost,
                    where=profit_zone,
                    alpha=0.1)

    st.pyplot(fig)


# -----------------------
# Main App
# -----------------------

def show_break_even_shift_calculator():

    st.header("📈 Executive Break-Even & Pricing Dashboard")
    st.write("Stress-test your business model against price, cost, and volume shifts.")

    # Sidebar
    with st.sidebar:

        st.subheader("Financial Inputs")
        f_costs = st.text_input("Existing Fixed Costs", "10000.00")
        f_invest = st.text_input("New Fixed Investment", "5000.00")
        t_profit = st.text_input("Target Profit", "2000.00")

        st.divider()

        u_price = st.text_input("Price per Unit", "11.00")
        u_cost = st.text_input("Variable Cost per Unit", "6.50")
        u_sold = st.text_input("Units Currently Sold", "4000")

        st.divider()

        st.subheader("Stress Testing")
        p_stress = st.slider("Price Shift (%)", -30, 30, 0)
        c_stress = st.slider("Cost Shift (%)", -30, 30, 0)
        v_stress = st.slider("Volume Shift (%)", -50, 50, 0)

        calculate = st.button("Run Executive Analysis")

    if calculate:
        try:
            # Parsing
            fixed = parse_number_en(f_costs) + parse_number_en(f_invest)
            target_profit = parse_number_en(t_profit)

            price = parse_number_en(u_price) * (1 + p_stress / 100)
            cost = parse_number_en(u_cost) * (1 + c_stress / 100)
            volume = parse_number_en(u_sold) * (1 + v_stress / 100)

            margin = price - cost

            if margin <= 0:
                st.error("🔴 Fatal Error: Contribution margin is zero or negative.")
                return

            required_units = (fixed + target_profit) / margin
            actual_profit = (margin * volume) - fixed
            mos = (volume - required_units) / volume if volume > 0 else -1

            # -----------------------
            # Risk Assessment
            # -----------------------

            risk = 0
            if actual_profit < 0:
                risk += 50
            if mos < 0.10:
                risk += 30
            if margin < price * 0.15:
                risk += 20

            risk = min(risk, 100)

            st.divider()

            # -----------------------
            # KPI Section
            # -----------------------

            c1, c2, c3 = st.columns(3)
            c1.metric("Required Units", f"{int(required_units)}")
            c2.metric("Projected Profit", f"${actual_profit:,.0f}")
            c3.metric("Margin of Safety", f"{mos*100:.1f}%")

            # Risk Indicator
            st.progress(risk / 100)
            st.caption(f"Risk Score: {risk}/100")

            st.divider()

            # -----------------------
            # Visualization
            # -----------------------

            st.subheader("📊 Profit & Loss Visualization")
            plot_break_even(fixed, target_profit, price, cost, volume)

            st.divider()

            # -----------------------
            # Strategic Analysis
            # -----------------------

            col_left, col_right = st.columns(2)

            with col_left:
                st.subheader("📋 Structural Analysis")

                summary_df = pd.DataFrame({
                    "Variable": [
                        "Total Fixed Costs",
                        "Target Profit",
                        "Analyzed Volume",
                        "Contribution Margin"
                    ],
                    "Value": [
                        f"${fixed:,.2f}",
                        f"${target_profit:,.2f}",
                        f"{int(volume)} units",
                        f"${margin:,.2f}"
                    ]
                })

                st.table(summary_df)

            with col_right:
                st.subheader("💡 Pricing Strategy")

                req_price = ((fixed + target_profit) / volume) + cost if volume > 0 else 0

                st.info(f"""
To achieve your target profit at **{int(volume)} units**:

Minimum Required Price: **${req_price:,.2f}**
""")

                if volume < required_units:
                    st.error(f"⚠ DEFICIT: {int(required_units - volume)} units short of target.")
                else:
                    st.success(f"✅ SURPLUS: {int(volume - required_units)} units above target.")

        except Exception as e:
            st.error(f"Analysis Error: {e}")


if __name__ == "__main__":
    show_break_even_shift_calculator()

