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
    bep_old = total_fixed_old / old_cm
    bep_new = total_fixed_new / new_cm

    max_units = int(max(bep_old, bep_new, units_sold) * 1.5) + 5
    x = list(range(0, max_units))

    old_total_cost = [total_fixed_old + old_unit_cost * q for q in x]
    new_total_cost = [total_fixed_new + new_unit_cost * q for q in x]
    old_revenue = [old_price * q for q in x]
    new_revenue = [new_price * q for q in x]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, old_total_cost, 'r--', label="Current Total Cost", alpha=0.6)
    ax.plot(x, new_total_cost, 'r-', label="New Total Cost")
    ax.plot(x, old_revenue, 'g--', label="Current Revenue", alpha=0.6)
    ax.plot(x, new_revenue, 'g-', label="New Revenue")

    ax.axvline(bep_new, color='blue', linestyle="--", label=f"New Break-Even ({int(bep_new)})")
    ax.axvline(units_sold, color='orange', linestyle="-.", label=f"Current Sales ({int(units_sold)})")

    ax.set_xlabel("Units sold")
    ax.set_ylabel("USD")
    ax.set_title("Break-Even Shift & Sales Position")
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.7)
    st.pyplot(fig)

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------

def show_break_even_shift_calculator():
    st.set_page_config(page_title="Break-Even Decision Tool", layout="wide")
    st.header("🟠 Strategic Break-Even & Pricing Tool")
    
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
            
            submitted = st.form_submit_button("Analyze Decision")

    if submitted:
        try:
            # 1. PARSING
            fixed_costs = parse_number_en(fixed_costs_input)
            new_investment = parse_number_en(new_investment_input)
            target_profit = parse_number_en(target_profit_input)
            old_price = parse_number_en(old_price_input)
            new_price = parse_number_en(new_price_input)
            old_unit_cost = parse_number_en(old_unit_cost_input)
            new_unit_cost = parse_number_en(new_unit_cost_input)
            units_sold = parse_number_en(units_sold_input)

            # 2. CALCULATIONS
            # Dynamic pricing suggestion
            suggested_price = None
            if units_sold > 0:
                suggested_price = ((fixed_costs + new_investment + target_profit) / units_sold) + new_unit_cost

            # Volume at current new price
            required_units_current_price = None
            current_cm = new_price - new_unit_cost
            if current_cm > 0:
                required_units_current_price = (fixed_costs + new_investment + target_profit) / current_cm

            # Break-even shift
            old_bep, new_bep, percent_change, units_change = calculate_break_even_shift(
                fixed_costs + target_profit, new_investment, old_price, new_price, 
                old_unit_cost, new_unit_cost, units_sold
            )

            if percent_change is None:
                st.error("Negative contribution margin. The model is unsustainable.")
                return

            # 3. DISPLAY RESULTS
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Break-Even Analysis")
                st.metric("New Break-Even Point", f"{format_number_en(new_bep, 0)} units")
                st.write(f"Old BEP: {format_number_en(old_bep, 0)} | Change: {format_percentage_en(percent_change)}")
                
                # --- MARGIN OF SAFETY ---
                if units_sold > 0:
                    mos_units = units_sold - new_bep
                    mos_percent = (units_sold - new_bep) / units_sold
                    
                    st.subheader("🛡️ Margin of Safety")
                    if mos_percent > 0:
                        st.success(f"Your margin of safety is **{format_percentage_en(mos_percent)}**")
                        st.caption(f"You can lose up to {int(mos_units)} sales before hitting zero profit.")
                    else:
                        st.error(f"Negative Margin: **{format_percentage_en(mos_percent)}**")
                        st.warning("You are currently below the break-even point for this new scenario.")

            with col2:
                if suggested_price and units_sold < new_bep:
                    st.subheader("💡 Dynamic Pricing Suggestion")
                    st.info(f"Target Price: **{format_number_en(suggested_price, 2)} USD**")
                    st.caption(f"Price needed to hit {format_number_en(target_profit, 0)} USD profit with current volume.")

                if required_units_current_price is not None:
                    st.subheader("📊 Volume Requirement")
                    st.write(f"Required units at {new_price} USD: **{format_number_en(required_units_current_price, 0)}**")
                    gap = required_units_current_price - units_sold
                    if gap > 0:
                        st.warning(f"Sales gap: +{int(gap)} units needed.")

            st.divider()
            plot_break_even_shift(fixed_costs + target_profit, new_investment, old_price, new_price, old_unit_cost, new_unit_cost, units_sold)

        except Exception as e:
            st.error(f"System Error: {e}")

if __name__ == "__main__":
    show_break_even_shift_calculator()
