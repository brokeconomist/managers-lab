import streamlit as st
import matplotlib.pyplot as plt

# --- Helper functions ---
def parse_number_en(number_str):
    return float(number_str)

def format_number_en(number, decimals=2):
    return f"{number:,.{decimals}f}"

def format_percentage_en(number, decimals=1):
    return f"{number*100:.{decimals}f}%"

# --- Calculations ---
def calculate_break_even_shift_v2(old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
    old_cm = old_price - old_cost
    new_cm = new_price - new_cost

    if old_cm <= 0 or new_cm <= 0:
        return None, None, None, None

    fixed_costs_old = old_cm * units_sold
    fixed_costs_new = fixed_costs_old + investment_cost

    old_break_even = fixed_costs_old / old_cm
    new_break_even = fixed_costs_new / new_cm

    percent_change = (new_break_even - old_break_even) / old_break_even
    units_change = new_break_even - old_break_even

    return old_break_even, new_break_even, percent_change, units_change

# --- Plot ---
def plot_break_even_shift(old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
    old_cm = old_price - old_cost
    fixed_costs_old = old_cm * units_sold
    fixed_costs_new = fixed_costs_old + investment_cost

    x = list(range(0, int(units_sold * 2)))
    old_total_cost = [fixed_costs_old + old_cost * q for q in x]
    new_total_cost = [fixed_costs_new + new_cost * q for q in x]
    old_revenue = [old_price * q for q in x]
    new_revenue = [new_price * q for q in x]

    plt.figure(figsize=(8, 5))
    plt.plot(x, old_total_cost, 'r--', label="Old Cost")
    plt.plot(x, new_total_cost, 'r-', label="New Cost")
    plt.plot(x, old_revenue, 'g--', label="Old Price")
    plt.plot(x, new_revenue, 'g-', label="New Price")
    plt.xlabel("Units Sold")
    plt.ylabel("$")
    plt.title("Break-Even Comparison")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# --- Streamlit UI ---
def show_break_even_shift_calculator():
    st.header("🟠 Break-Even Shift Analysis (New Price / Cost / Investment)")

    with st.form("break_even_shift_form"):
        old_price_input = st.text_input("Old Selling Price ($):", value="10.50")
        new_price_input = st.text_input("New Selling Price ($):", value="11.00")
        old_cost_input = st.text_input("Old Unit Cost ($):", value="6.00")
        new_cost_input = st.text_input("New Unit Cost ($):", value="6.50")
        investment_cost_input = st.text_input("Investment Cost ($):", value="2000.00")
        units_sold_input = st.text_input("Units Sold (last period):", value="500")
        submitted = st.form_submit_button("Calculate")

    if submitted:
        try:
            old_price = parse_number_en(old_price_input)
            new_price = parse_number_en(new_price_input)
            old_cost = parse_number_en(old_cost_input)
            new_cost = parse_number_en(new_cost_input)
            investment_cost = parse_number_en(investment_cost_input)
            units_sold = parse_number_en(units_sold_input)

            old_bep, new_bep, percent_change, units_change = calculate_break_even_shift_v2(
                old_price, new_price, old_cost, new_cost, investment_cost, units_sold
            )

            if percent_change is None:
                st.error("Contribution margin is zero or negative. Cannot calculate break-even.")
            else:
                st.success(f"✅ Break-Even (Old): {format_number_en(old_bep,0)} units")
                st.success(f"✅ Break-Even (New): {format_number_en(new_bep,0)} units")
                st.markdown(f"- Change in units: **{format_number_en(units_change,0)}**")
                st.markdown(f"- Percent Change: **{format_percentage_en(percent_change)}**")

                # Zone messages
                if percent_change < 0.10:
                    st.success(f"🟢 Decision absorbed by existing model (Change: {format_percentage_en(percent_change)})")
                elif 0.10 <= percent_change <= 0.30:
                    st.warning(f"🟠 Decision seems small, but requires unrealistic volume increase (Change: {format_percentage_en(percent_change)})")
                else:
                    st.error(f"🔴 Decision drastically increases survival threshold! (Change: {format_percentage_en(percent_change)})")

                plot_break_even_shift(old_price, new_price, old_cost, new_cost, investment_cost, units_sold)

        except Exception as e:
            st.error(f"⚠️ Input error: {e}")
