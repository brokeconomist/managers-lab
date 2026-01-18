import streamlit as st
import matplotlib.pyplot as plt

# --- Helper functions ---
def parse_number_en(number_str):
    """Convert string to float, English style (10.50, not 10,50)."""
    return float(number_str)

def format_number_en(number, decimals=2):
    """Format number in English style 1234.56 -> 1,234.56"""
    return f"{number:,.{decimals}f}"

def format_percentage_en(number, decimals=1):
    return f"{number*100:.{decimals}f}%"

# --- Break-Even calculations ---
def calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit):
    try:
        if price_per_unit == variable_cost_per_unit:
            return None
        return fixed_costs / (price_per_unit - variable_cost_per_unit)
    except ZeroDivisionError:
        return None

# --- Plot ---
def plot_break_even_shift(price_per_unit, variable_cost, fixed_costs, bep_old, bep_new):
    max_units = int(max(bep_old, bep_new) * 2) + 5
    units = list(range(0, max_units))
    revenue = [price_per_unit * u for u in units]
    total_cost = [fixed_costs + variable_cost * u for u in units]

    fig, ax = plt.subplots()
    ax.plot(units, revenue, label="Revenue", color="green")
    ax.plot(units, total_cost, label="Total Cost", color="blue")
    ax.axvline(bep_old, color="red", linestyle="--", label="Old Break-Even")
    ax.axvline(bep_new, color="orange", linestyle="--", label="New Break-Even")
    ax.set_xlabel("Units Sold")
    ax.set_ylabel("$")
    ax.set_title("Break-Even Analysis — Shift")
    ax.legend()
    st.pyplot(fig)
    st.markdown("---")

# --- Streamlit UI ---
def show_break_even_calculator():
    st.header("🟢 Break-Even Calculator (Shift)")
    st.markdown("See how a small change in price or cost moves the break-even point.")

    with st.form("break_even_form"):
        fixed_costs_input = st.text_input("Fixed Costs ($)", value="10000.00")
        price_per_unit_input = st.text_input("Price per Unit ($)", value="50.00")
        variable_cost_per_unit_input = st.text_input("Variable Cost per Unit ($)", value="30.00")
        new_price_per_unit_input = st.text_input("New Price per Unit ($)", value="50.00")
        new_variable_cost_input = st.text_input("New Variable Cost per Unit ($)", value="30.00")
        submitted = st.form_submit_button("Calculate")

    if submitted:
        try:
            fixed_costs = parse_number_en(fixed_costs_input)
            price_per_unit = parse_number_en(price_per_unit_input)
            variable_cost_per_unit = parse_number_en(variable_cost_per_unit_input)
            new_price_per_unit = parse_number_en(new_price_per_unit_input)
            new_variable_cost = parse_number_en(new_variable_cost_input)

            bep_old = calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)
            bep_new = calculate_break_even_point(fixed_costs, new_price_per_unit, new_variable_cost)

            if bep_old is None or bep_new is None:
                st.error("⚠️ Price must be higher than variable cost.")
                return

            st.success(f"✅ Break-Even (Old): {format_number_en(bep_old,0)} units")
            st.success(f"✅ Break-Even (New): {format_number_en(bep_new,0)} units")

            change_pct = (bep_new - bep_old) / bep_old

            # Zone messages
            if change_pct < 0.10:
                st.success(f"🟢 Decision absorbed by existing model (Change: {format_percentage_en(change_pct)})")
            elif 0.10 <= change_pct <= 0.30:
                st.warning(f"🟠 Decision seems small, but requires unrealistic volume increase (Change: {format_percentage_en(change_pct)})")
            else:
                st.error(f"🔴 Decision drastically increases survival threshold! (Change: {format_percentage_en(change_pct)})")

            plot_break_even_shift(price_per_unit, variable_cost_per_unit, fixed_costs, bep_old, bep_new)

        except Exception as e:
            st.error(f"⚠️ Input error: {e}")
