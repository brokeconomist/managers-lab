import streamlit as st
import matplotlib.pyplot as plt

# -------------------------------------------------
# Helper functions
# -------------------------------------------------

def parse_number_en(number_str):
    try:
        return float(number_str.replace(",", ""))
    except:
        return 0.0

def format_number_en(number, decimals=2):
    return f"{number:,.{decimals}f}"

def format_percentage_en(number, decimals=1):
    return f"{number*100:.{decimals}f}%"

# -------------------------------------------------
# Core calculations
# -------------------------------------------------

def calculate_break_even_shift(
    fixed_costs,
    new_investment,
    old_price,
    new_price,
    old_unit_cost,
    new_unit_cost,
    units_sold
):
    old_cm = old_price - old_unit_cost
    new_cm = new_price - new_unit_cost

    if old_cm <= 0 or new_cm <= 0:
        return None, None, None, None

    total_fixed_old = fixed_costs
    total_fixed_new = fixed_costs + new_investment

    old_break_even = total_fixed_old / old_cm
    new_break_even = total_fixed_new / new_cm

    percent_change = (new_break_even - old_break_even) / old_break_even
    units_change = new_break_even - old_break_even

    return old_break_even, new_break_even, percent_change, units_change

# -------------------------------------------------
# Plot
# -------------------------------------------------

def plot_break_even_shift(
    fixed_costs,
    new_investment,
    old_price,
    new_price,
    old_unit_cost,
    new_unit_cost,
    units_sold
):
    old_cm = old_price - old_unit_cost
    new_cm = new_price - new_unit_cost
    total_fixed_old = fixed_costs
    total_fixed_new = fixed_costs + new_investment
    bep_new = total_fixed_new / new_cm

    max_units = int(max(bep_new, units_sold) * 1.5) + 5
    x = list(range(0, max_units))

    new_total_cost = [total_fixed_new + new_unit_cost * q for q in x]
    new_revenue = [new_price * q for q in x]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, new_total_cost, label="Total Cost")
    ax.plot(x, new_revenue, label="Revenue")

    ax.axvline(bep_new, linestyle="--", label=f"Break-Even ({int(bep_new)})")
    ax.axvline(units_sold, linestyle="-.", label=f"Current Sales ({int(units_sold)})")

    ax.set_xlabel("Units sold")
    ax.set_ylabel("USD")
    ax.set_title("Break-Even Position")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------

def show_break_even_shift_calculator():
    st.set_page_config(page_title="Executive Decision Dashboard", layout="wide")
    st.header("🧭 Executive Break-Even & Pricing Dashboard")

    with st.sidebar:
        st.subheader("Input Parameters")
        with st.form("break_even_form"):
            fixed_costs_input = st.text_input("Existing fixed costs", "10000.00")
            new_investment_input = st.text_input("New fixed investment", "0.00")
            target_profit_input = st.text_input("Target profit", "0.00")
            st.divider()
            old_price_input = st.text_input("Current price", "10.50")
            new_price_input = st.text_input("New price", "11.00")
            st.divider()
            old_unit_cost_input = st.text_input("Current variable cost", "6.00")
            new_unit_cost_input = st.text_input("New variable cost", "6.50")
            st.divider()
            units_sold_input = st.text_input("Current units sold", "500")

            submitted = st.form_submit_button("Run Executive Analysis")

    if submitted:
        try:
            # Parsing
            fixed_costs = parse_number_en(fixed_costs_input)
            new_investment = parse_number_en(new_investment_input)
            target_profit = parse_number_en(target_profit_input)
            old_price = parse_number_en(old_price_input)
            new_price = parse_number_en(new_price_input)
            old_unit_cost = parse_number_en(old_unit_cost_input)
            new_unit_cost = parse_number_en(new_unit_cost_input)
            units_sold = parse_number_en(units_sold_input)

            # Core calculations
            old_bep, new_bep, percent_change, units_change = calculate_break_even_shift(
                fixed_costs + target_profit,
                new_investment,
                old_price,
                new_price,
                old_unit_cost,
                new_unit_cost,
                units_sold
            )

            if percent_change is None:
                st.error("Negative contribution margin. Model unsustainable.")
                return

            total_fixed = fixed_costs + new_investment
            current_profit = (new_price - new_unit_cost) * units_sold - total_fixed

            # Required units
            current_cm = new_price - new_unit_cost
            required_units_current_price = None
            if current_cm > 0:
                required_units_current_price = (total_fixed + target_profit) / current_cm

            # Dynamic pricing
            suggested_price = None
            if units_sold > 0:
                suggested_price = (total_fixed + target_profit) / units_sold + new_unit_cost

            # Margin of Safety
            mos_percent = (units_sold - new_bep) / units_sold if units_sold > 0 else -1

            # -------------------------------------------------
            # Executive Risk Score
            # -------------------------------------------------
            risk_score = 0

            if mos_percent < 0:
                risk_score += 40
            elif mos_percent < 0.10:
                risk_score += 25
            elif mos_percent < 0.25:
                risk_score += 10

            if percent_change > 0.30:
                risk_score += 30
            elif percent_change > 0.15:
                risk_score += 15

            if required_units_current_price and required_units_current_price > units_sold:
                risk_score += 20

            risk_score = min(risk_score, 100)

            # -------------------------------------------------
            # EXECUTIVE SIGNAL
            # -------------------------------------------------
            st.divider()
            st.subheader("🧭 Executive Decision Signal")

            if risk_score < 25:
                st.success("🟢 LOW RISK — Model comfortably absorbs decision.")
            elif risk_score < 60:
                st.warning("🟠 MODERATE RISK — Sales execution becomes critical.")
            else:
                st.error("🔴 HIGH RISK — Decision significantly increases failure probability.")

            # -------------------------------------------------
            # KPI ROW (Board View)
            # -------------------------------------------------
            k1, k2, k3, k4 = st.columns(4)

            k1.metric("Break-Even Units", format_number_en(new_bep,0))
            k2.metric("Current Profit", format_number_en(current_profit,0))
            k3.metric("Margin of Safety", format_percentage_en(mos_percent))
            k4.metric("Risk Score", f"{risk_score}/100")

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Volume Requirement")
                if required_units_current_price:
                    st.write(f"Required units at {new_price} USD: **{format_number_en(required_units_current_price,0)}**")
                    gap = required_units_current_price - units_sold
                    if gap > 0:
                        st.warning(f"Sales gap: +{int(gap)} units needed.")
                    else:
                        st.success("Current volume sufficient.")

            with col2:
                if suggested_price and units_sold < new_bep:
                    st.subheader("💡 Dynamic Pricing Suggestion")
                    st.info(f"Required Price: **{format_number_en(suggested_price,2)} USD**")

            st.divider()
            plot_break_even_shift(
                fixed_costs + target_profit,
                new_investment,
                old_price,
                new_price,
                old_unit_cost,
                new_unit_cost,
                units_sold
            )

        except Exception as e:
            st.error(f"System Error: {e}")

if __name__ == "__main__":
    show_break_even_shift_calculator()
