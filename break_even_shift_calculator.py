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
# Core calculations (DO NOT CHANGE LOGIC)
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

    bep_old = total_fixed_old / old_cm
    bep_new = total_fixed_new / new_cm

    max_units = int(max(bep_old, bep_new) * 2) + 5
    x = list(range(0, max_units))

    old_total_cost = [total_fixed_old + old_unit_cost * q for q in x]
    new_total_cost = [total_fixed_new + new_unit_cost * q for q in x]
    old_revenue = [old_price * q for q in x]
    new_revenue = [new_price * q for q in x]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, old_total_cost, 'r--', label="Current Total Cost")
    ax.plot(x, new_total_cost, 'r-', label="New Total Cost")
    ax.plot(x, old_revenue, 'g--', label="Current Revenue")
    ax.plot(x, new_revenue, 'g-', label="New Revenue")

    ax.axvline(bep_old, linestyle="--", label="Current Break-Even")
    ax.axvline(bep_new, linestyle="--", label="New Break-Even")

    ax.set_xlabel("Units sold")
    ax.set_ylabel("USD")
    ax.set_title("Break-Even Shift After Decision")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    st.markdown("---")


# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------

def show_break_even_shift_calculator():
    st.header("🟠 Break-Even Decision Tool")
    st.markdown(
        "Answer client questions **immediately**, without spreadsheets. "
        "Leave any field as **0** if it does not apply."
    )

    with st.form("break_even_form"):
        fixed_costs_input = st.text_input("Existing fixed costs per period", "10000.00")
        st.caption("All recurring costs you must cover every period, regardless of sales volume.")

        new_investment_input = st.text_input("Additional fixed investment (enter 0 if none)", "0.00")
        st.caption("Any new fixed cost required by this decision.")

        target_profit_input = st.text_input("Target profit per period (leave 0 if none)", "0.00")
        st.caption("Optional. Enter the profit you want to generate per period.")

        old_price_input = st.text_input("Current selling price per unit", "10.50")
        st.caption("The price at which you currently sell one unit.")

        new_price_input = st.text_input("New selling price per unit", "11.00")
        st.caption("The new price you are considering after this decision.")

        old_unit_cost_input = st.text_input("Current variable cost per unit", "6.00")
        st.caption("Direct cost per unit sold.")

        new_unit_cost_input = st.text_input("New variable cost per unit", "6.50")
        st.caption("Expected direct cost per unit after the decision.")

        units_sold_input = st.text_input("Units sold per period (current level)", "500")
        st.caption("How many units you currently sell per period.")

        submitted = st.form_submit_button("Run decision check")

    if submitted:
        try:
            # 1. PARSING SECTION
            fixed_costs = parse_number_en(fixed_costs_input)
            new_investment = parse_number_en(new_investment_input)
            target_profit = parse_number_en(target_profit_input)
            old_price = parse_number_en(old_price_input)
            new_price = parse_number_en(new_price_input)
            old_unit_cost = parse_number_en(old_unit_cost_input)
            new_unit_cost = parse_number_en(new_unit_cost_input)
            units_sold = parse_number_en(units_sold_input)

            # --- ΠΡΟΣΘΗΚΗ 1: Dynamic pricing suggestion (Μετά τα parsing) ---
            
            suggested_price = (
                    (fixed_costs + new_investment + target_profit) / units_sold
                ) + new_unit_cost
            
            # -----------------------------------------

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
                st.error("Contribution margin is zero or negative. This decision destroys the business model.")
                return

            # 2. RESULTS SECTION
            st.success(f"Current break-even: {format_number_en(old_bep, 0)} units")
            st.success(f"New break-even after decision: {format_number_en(new_bep, 0)} units")

            # --- ΠΡΟΣΘΗΚΗ 2: Display Suggested Price (Μετά τα break even results) ---
            if suggested_price is not None:
                st.markdown("---")
                st.subheader("💡 Dynamic Pricing Suggestion")

                st.markdown(
                    f"If you sell **{format_number_en(units_sold,0)} units**, "
                    f"to generate **{format_number_en(target_profit,0)} USD profit**, "
                    f"you should charge approximately:"
                )

                st.success(
                    f"Suggested price per unit: {format_number_en(suggested_price,2)} USD"
                )
            # -----------------------------------------

            st.markdown(f"- **Additional units required:** {format_number_en(units_change,0)}")
            st.markdown(f"- **Change in required sales threshold:** {format_percentage_en(percent_change)}")

            if percent_change < 0.10:
                st.success("🟢 Absorbed by current model")
            elif percent_change <= 0.30:
                st.warning("🟠 Stretches sales capacity")
            else:
                st.error("🔴 High-risk decision — required sales threshold jumps")

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
            st.error(f"Input error: {e}")

# Call the function to run the app
if __name__ == "__main__":
    show_break_even_shift_calculator()
