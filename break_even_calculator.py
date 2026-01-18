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
    ax.plot(units, revenue, label="Revenue")
    ax.plot(units, total_cost, label="Total Cost")
    ax.axvline(bep_old, linestyle="--", label="Current Break-Even")
    ax.axvline(bep_new, linestyle="--", label="New Break-Even")
    ax.set_xlabel("Units sold")
    ax.set_ylabel("$")
    ax.set_title("Break-Even Shift After Decision")
    ax.legend()
    st.pyplot(fig)
    st.markdown("---")

# --- Streamlit UI ---
def show_break_even_calculator():

    st.header("🟢 Can you afford this decision?")
    st.markdown(
        "Answer pricing or cost questions instantly — without spreadsheets.\n\n"
        "Change the price or cost and see if your business model absorbs the decision."
    )

    with st.form("break_even_form"):
        fixed_costs_input = st.text_input(
            "Monthly fixed costs you must cover ($)",
            value="10000.00"
        )

        price_per_unit_input = st.text_input(
            "Current selling price per unit ($)",
            value="50.00"
        )

        variable_cost_per_unit_input = st.text_input(
            "Direct cost per unit (materials, labor, delivery) ($)",
            value="30.00"
        )

        new_price_per_unit_input = st.text_input(
            "Proposed new selling price ($)",
            value="50.00"
        )

        new_variable_cost_input = st.text_input(
            "Proposed new direct cost per unit ($)",
            value="30.00"
        )

        submitted = st.form_submit_button("Test the decision")

    if submitted:
        try:
            fixed_costs = parse_number_en(fixed_costs_input)
            price_per_unit = parse_number_en(price_per_unit_input)
            variable_cost_per_unit = parse_number_en(variable_cost_per_unit_input)
            new_price_per_unit = parse_number_en(new_price_per_unit_input)
            new_variable_cost = parse_number_en(new_variable_cost_input)

            bep_old = calculate_break_even_point(
                fixed_costs, price_per_unit, variable_cost_per_unit
            )
            bep_new = calculate_break_even_point(
                fixed_costs, new_price_per_unit, new_variable_cost
            )

            if bep_old is None or bep_new is None:
                st.error("⚠️ Selling price must be higher than direct cost.")
                return

            st.success(
                f"Current break-even: {format_number_en(bep_old,0)} units"
            )
            st.success(
                f"New break-even after decision: {format_number_en(bep_new,0)} units"
            )

            change_pct = (bep_new - bep_old) / bep_old

            if change_pct < 0.10:
                st.success(
                    f"🟢 Your business model absorbs this decision "
                    f"({format_percentage_en(change_pct)} change)."
                )
            elif 0.10 <= change_pct <= 0.30:
                st.warning(
                    f"🟠 This decision requires a significant increase in sales volume "
                    f"({format_percentage_en(change_pct)} change)."
                )
            else:
                st.error(
                    f"🔴 This decision raises the survival threshold to a dangerous level "
                    f"({format_percentage_en(change_pct)} change)."
                )

            plot_break_even_shift(
                price_per_unit,
                variable_cost_per_unit,
                fixed_costs,
                bep_old,
                bep_new
            )

        except Exception as e:
            st.error(f"⚠️ Input error: {e}")
