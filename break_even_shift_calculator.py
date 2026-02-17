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

    percent_change = (new_break_even - old_break_even) / old_break_even if old_break_even != 0 else 0
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
    
    bep_old = total_fixed_old / old_cm if old_cm > 0 else 0
    bep_new = total_fixed_new / new_cm if new_cm > 0 else 0

    max_units = int(max(bep_old, bep_new, units_sold) * 1.5) + 5
    x = list(range(0, max_units))

    old_total_cost = [total_fixed_old + old_unit_cost * q for q in x]
    new_total_cost = [total_fixed_new + new_unit_cost * q for q in x]
    old_revenue = [old_price * q for q in x]
    new_revenue = [new_price * q for q in x]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, old_total_cost, 'r--', label="Current Total Cost", alpha=0.5)
    ax.plot(x, new_total_cost, 'r-', label="New Total Cost")
    ax.plot(x, old_revenue, 'g--', label="Current Revenue", alpha=0.5)
    ax.plot(x, new_revenue, 'g-', label="New Revenue")

    ax.axvline(bep_new, color='blue', linestyle="--", label=f"New BEP ({int(bep_new)})")
    ax.axvline(units_sold, color='orange', linestyle="-.", label=f"Current Sales ({int(units_sold)})")

    ax.set_xlabel("Units sold")
    ax.set_ylabel("Currency")
    ax.set_title("Financial Impact Visualization")
    ax.legend(fontsize='small')
    ax.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig)

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------

def show_break_even_shift_calculator():
    st.set_page_config(page_title="Strategic Decision Tool", layout="wide")
    st.header("🟠 Strategic Break-Even & Pricing Analyzer")
    
    with st.sidebar:
        st.subheader("Financial Inputs")
        with st.form("break_even_form"):
            fixed_costs_input = st.text_input("Existing Fixed Costs", "10000.00")
            new_investment_input = st.text_input("New Investment/Fixed Cost", "2000.00")
            target_profit_input = st.text_input("Target Profit", "5000.00")
            st.divider()
            old_price_input = st.text_input("Current Price", "50.00")
            new_price_input = st.text_input("New Price", "55.00")
            st.divider()
            old_unit_cost_input = st.text_input("Current Variable Cost", "20.00")
            new_unit_cost_input = st.text_input("New Variable Cost", "22.00")
            st.divider()
            units_sold_input = st.text_input("Current Sales Volume (Units)", "400")
            
            submitted = st.form_submit_button("Generate Analysis")

    if submitted:
        try:
            # 1. PARSING
            f_costs = parse_number_en(fixed_costs_input)
            n_inv = parse_number_en(new_investment_input)
            t_profit = parse_number_en(target_profit_input)
            o_price = parse_number_en(old_price_input)
            n_price = parse_number_en(new_price_input)
            o_cost = parse_number_en(old_unit_cost_input)
            n_cost = parse_number_en(new_unit_cost_input)
            u_sold = parse_number_en(units_sold_input)

            # 2. CALCULATIONS
            # Dynamic pricing suggestion
            s_price = ((f_costs + n_inv + t_profit) / u_sold) + n_cost if u_sold > 0 else 0

            # Volume at current new price
            req_units_n_price = (f_costs + n_inv + t_profit) / (n_price - n_cost) if (n_price - n_cost) > 0 else 0

            # Break-even shift
            old_bep, new_bep, p_change, u_change = calculate_break_even_shift(
                f_costs + t_profit, n_inv, o_price, n_price, o_cost, n_cost, u_sold
            )

            if p_change is None:
                st.error("Negative contribution margin. The business model is not viable under these settings.")
                return

            # Margin of Safety
            mos_percent = (u_sold - new_bep) / u_sold if u_sold > 0 else 0

            # 3. UI LAYOUT
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📊 Key Metrics")
                kpi1, kpi2 = st.columns(2)
                kpi1.metric("New BEP", f"{int(new_bep)} units")
                kpi2.metric("Sales Gap", f"{int(req_units_n_price - u_sold)} units")
                
                # Margin of Safety Display
                st.write("**Margin of Safety:**")
                if mos_percent > 0:
                    st.success(f"{format_percentage_en(mos_percent)} safety buffer")
                else:
                    st.error(f"{format_percentage_en(mos_percent)} (Below Break-even)")

                plot_break_even_shift(f_costs + t_profit, n_inv, o_price, n_price, o_cost, n_cost, u_sold)

            with col2:
                st.subheader("📋 Client Executive Summary")
                
                # RISK ASSESSMENT
                risk_level = "High" if p_change > 0.3 else "Moderate" if p_change > 0.1 else "Low"
                
                report_text = f"""
**Strategic Analysis Report**
---
1. **Break-Even Impact:** The sales threshold required to hit your target profit has changed by **{format_percentage_en(p_change)}**. 
   - New target: **{int(new_bep)} units**.

2. **Pricing Strategy:** - To maintain current sales volume ({int(u_sold)} units) and hit your profit goal, the price should be adjusted to **{format_number_en(s_price, 2)}**.
   - At your proposed price ({format_number_en(n_price, 2)}), you need a total of **{int(req_units_n_price)} units** to meet objectives.

3. **Risk Profile:** This decision is considered **{risk_level} Risk**. 
   - Your current Margin of Safety is **{format_percentage_en(mos_percent)}**.

4. **Observation:** {'🟢 Current sales exceed the new break-even point.' if mos_percent > 0 else '🔴 Current sales are insufficient to cover the new cost structure.'}
                """
                st.markdown(report_text)
                st.button("Copy to Clipboard (Simulated)", help="Select text above to copy")

        except Exception as e:
            st.error(f"Analysis Error: {e}")

if __name__ == "__main__":
    show_break_even_shift_calculator()
