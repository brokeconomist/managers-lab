import streamlit as st
import matplotlib.pyplot as plt

# -------------------------------------------------
# Helper functions
# -------------------------------------------------

def parse_number_en(number_str):
    try:
        return float(str(number_str).replace(",", ""))
    except:
        return 0.0

def format_number_en(number, decimals=2):
    return f"{number:,.{decimals}f}"

def format_percentage_en(number, decimals=1):
    return f"{number*100:.{decimals}f}%"

# -------------------------------------------------
# Plot
# -------------------------------------------------

def plot_break_even(fixed_costs, price, unit_cost, units_sold):
    cm = price - unit_cost
    if cm <= 0:
        return

    bep = fixed_costs / cm
    max_units = int(max(bep, units_sold) * 1.5) + 5
    x = list(range(0, max_units))

    total_cost = [fixed_costs + unit_cost * q for q in x]
    revenue = [price * q for q in x]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, total_cost, label="Total Cost", color="#d62728", linewidth=2)
    ax.plot(x, revenue, label="Revenue", color="#2ca02c", linewidth=2)
    ax.axvline(bep, linestyle="--", color="gray", label=f"Break-Even ({int(bep)})")
    ax.axvline(units_sold, linestyle="-.", color="blue", label=f"Current Sales ({int(units_sold)})")

    ax.set_xlabel("Units sold")
    ax.set_ylabel("USD")
    ax.set_title("Break-Even Analysis Chart")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

# -------------------------------------------------
# Streamlit UI (RENAMED TO MATCH APP.PY)
# -------------------------------------------------

def show_break_even_shift_calculator():
    # Κατάργηση st.set_page_config (υπάρχει ήδη στο app.py)
    st.header("📈 Executive Break-Even & Pricing Dashboard")
    st.caption("Stress-test your business model against price, cost, and volume shifts.")

    # SIDEBAR INPUTS
    with st.sidebar:
        st.subheader("Base Inputs")
        fixed_costs_input = st.text_input("Existing fixed costs", "10000.00")
        new_investment_input = st.text_input("New fixed investment", "0.00")
        target_profit_input = st.text_input("Target profit", "0.00")

        st.divider()
        new_price_input = st.text_input("New price", "11.00")
        new_unit_cost_input = st.text_input("New variable cost", "6.50")
        units_sold_input = st.text_input("Current units sold", "500")

        st.divider()
        st.subheader("Stress Testing")
        price_stress = st.slider("Price Change (%)", -30, 30, 0)
        cost_stress = st.slider("Cost Change (%)", -30, 30, 0)
        volume_stress = st.slider("Volume Change (%)", -50, 50, 0)

        run = st.button("Run Executive Analysis")

    if run:
        try:
            # PARSING
            fixed_costs = parse_number_en(fixed_costs_input)
            new_investment = parse_number_en(new_investment_input)
            target_profit = parse_number_en(target_profit_input)
            new_price = parse_number_en(new_price_input)
            new_unit_cost = parse_number_en(new_unit_cost_input)
            units_sold = parse_number_en(units_sold_input)

            total_fixed = fixed_costs + new_investment + target_profit

            # APPLY STRESS
            stressed_price = new_price * (1 + price_stress / 100)
            stressed_cost = new_unit_cost * (1 + cost_stress / 100)
            stressed_volume = units_sold * (1 + volume_stress / 100)

            st.info(f"Scenario: Price {price_stress}% | Cost {cost_stress}% | Volume {volume_stress}%")

            # CALCULATIONS
            stressed_cm = stressed_price - stressed_cost

            if stressed_cm <= 0:
                st.error("🔴 Contribution margin is negative. Model is not viable under this stress.")
                return

            new_bep = total_fixed / stressed_cm
            stressed_profit = stressed_cm * stressed_volume - total_fixed
            mos_percent = (stressed_volume - new_bep) / stressed_volume if stressed_volume > 0 else -1

            # RISK SCORE LOGIC
            risk_score = 0
            if mos_percent < 0: risk_score += 40
            elif mos_percent < 0.10: risk_score += 25
            elif mos_percent < 0.25: risk_score += 10
            if stressed_profit < 0: risk_score += 30
            if new_bep > stressed_volume: risk_score += 20
            risk_score = min(risk_score, 100)

            # EXECUTIVE SIGNAL
            st.divider()
            if risk_score < 25:
                st.success("🟢 LOW RISK — Business model is robust.")
            elif risk_score < 60:
                st.warning("🟠 MODERATE RISK — Monitor margins closely.")
            else:
                st.error("🔴 HIGH RISK — High probability of operational loss.")

            # KPI BOARD
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Break-Even Units", format_number_en(new_bep, 0))
            k2.metric("Stressed Profit", f"${format_number_en(stressed_profit, 0)}")
            k3.metric("Margin of Safety", format_percentage_en(mos_percent))
            k4.metric("Risk Score", f"{risk_score}/100")

            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Unit Analysis")
                st.write(f"Required for Target: **{format_number_en(new_bep, 0)}** units")
                

[Image of break even point graph]

            with col2:
                st.subheader("💡 Strategic Insight")
                req_p = (total_fixed / stressed_volume + stressed_cost) if stressed_volume > 0 else 0
                st.write(f"Price needed for current volume: **${format_number_en(req_p, 2)}**")

            plot_break_even(total_fixed, stressed_price, stressed_cost, stressed_volume)

        except Exception as e:
            st.error(f"Analysis Error: {e}")

if __name__ == "__main__":
    show_break_even_shift_calculator()
