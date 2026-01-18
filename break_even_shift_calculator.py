import streamlit as st
import matplotlib.pyplot as plt

# -------------------------------------------------
# Helper functions
# -------------------------------------------------

def parse_number_en(number_str):
    return float(number_str)

def format_number_en(number, decimals=2):
    return f"{number:,.{decimals}f}"

def format_percentage_en(number, decimals=1):
    return f"{number*100:.{decimals}f}%"


# -------------------------------------------------
# Core calculations (LOGIC MUST NOT CHANGE)
# -------------------------------------------------

def calculate_break_even_shift_v2(
    fixed_costs,
    additional_investment,
    old_price,
    new_price,
    old_cost,
    new_cost
):
    old_cm = old_price - old_cost
    new_cm = new_price - new_cost

    if old_cm <= 0 or new_cm <= 0:
        return None, None, None, None

    fixed_costs_old = fixed_costs
    fixed_costs_new = fixed_costs + additional_investment

    old_break_even = fixed_costs_old / old_cm
    new_break_even = fixed_costs_new / new_cm

    percent_change = (new_break_even - old_break_even) / old_break_even
    units_change = new_break_even - old_break_even

    return old_break_even, new_break_even, percent_change, units_change


# -------------------------------------------------
# Plot (same logic as the reference diagram you sent)
# -------------------------------------------------

def plot_break_even_shift(
    price_per_unit,
    variable_cost,
    fixed_costs_old,
    fixed_costs_new,
    bep_old,
    bep_new
):
    max_units = int(max(bep_old, bep_new) * 2) + 5
    units = list(range(0, max_units))

    revenue = [price_per_unit * u for u in units]
    total_cost_old = [fixed_costs_old + variable_cost * u for u in units]
    total_cost_new = [fixed_costs_new + variable_cost * u for u in units]

    fig, ax = plt.subplots()

    ax.plot(units, revenue, label="Revenue")
    ax.plot(units, total_cost_old, linestyle="--", label="Total Cost (Before)")
    ax.plot(units, total_cost_new, linestyle="-", label="Total Cost (After)")

    ax.axvline(bep_old, linestyle="--", label="Current Break-Even")
    ax.axvline(bep_new, linestyle="--", label="New Break-Even")

    ax.set_xlabel("Units sold")
    ax.set_ylabel("$")
    ax.set_title("Break-Even Shift After Decision")
    ax.legend()

    st.pyplot(fig)


# -------------------------------------------------
# UI — this is what app.py calls
# -------------------------------------------------

def show_break_even_shift_calculator():

    st.header("🟢 Can you afford this decision?")
    st.markdown(
        """
        Answer pricing, cost, or investment questions **in seconds** —  
        without spreadsheets, without assumptions.

        Fill only what applies to your case.  
        If something does **not** apply, leave it as **0**.
        """
    )

    with st.form("break_even_form"):

        fixed_costs_input = st.text_input(
            "Existing fixed costs per period ($)",
            value="10000.00",
            help="All costs you must pay regardless of sales volume (rent, salaries, overheads)."
        )

        additional_investment_input = st.text_input(
            "Additional fixed investment ($)",
            value="0.00",
            help="Any new fixed cost required by this decision (equipment, software, hiring). Enter 0 if none."
        )

        old_price_input = st.text_input(
            "Current selling price per unit ($)",
            value="50.00",
            help="The price at which you currently sell one unit of the product."
        )

        new_price_input = st.text_input(
            "Proposed new selling price per unit ($)",
            value="50.00",
            help="The new price you are considering after the decision."
        )

        old_cost_input = st.text_input(
            "Current unit cost ($)",
            value="30.00",
            help="Direct cost per unit (materials, labor, delivery, commissions)."
        )

        new_cost_input = st.text_input(
            "Proposed new unit cost ($)",
            value="30.00",
            help="Expected unit cost after the decision (higher or lower)."
        )

        submitted = st.form_submit_button("Test the decision")

    if submitted:
        try:
            fixed_costs = parse_number_en(fixed_costs_input)
            additional_investment = parse_number_en(additional_investment_input)
            old_price = parse_number_en(old_price_input)
            new_price = parse_number_en(new_price_input)
            old_cost = parse_number_en(old_cost_input)
            new_cost = parse_number_en(new_cost_input)

            old_bep, new_bep, percent_change, units_change = (
                calculate_break_even_shift_v2(
                    fixed_costs,
                    additional_investment,
                    old_price,
                    new_price,
                    old_cost,
                    new_cost
                )
            )

            if percent_change is None:
                st.error(
                    "⚠️ Selling price is not higher than unit cost. "
                    "This decision breaks the business model."
                )
                return

            st.success(f"Current break-even: {format_number_en(old_bep, 0)} units")
            st.success(f"New break-even after decision: {format_number_en(new_bep, 0)} units")

            st.markdown(f"- **Additional units required:** {format_number_en(units_change, 0)}")
            st.markdown(f"- **Break-even change:** {format_percentage_en(percent_change)}")

            if percent_change < 0.10:
                st.success("🟢 The business model absorbs this decision.")
            elif percent_change <= 0.30:
                st.warning("🟠 The decision looks small, but heavily pressures sales.")
            else:
                st.error("🔴 Dangerous decision — survival threshold jumps sharply.")

            plot_break_even_shift(
                old_price,
                old_cost,
                fixed_costs,
                fixed_costs + additional_investment,
                old_bep,
                new_bep
            )

        except Exception as e:
            st.error(f"Input error: {e}")
