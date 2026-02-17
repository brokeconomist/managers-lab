import streamlit as st
import matplotlib.pyplot as plt

# --- Utilities ---
def parse_number_en(number_str):
    try:
        return float(str(number_str).replace(",", ""))
    except:
        return 0.0

def format_number_en(number, decimals=2):
    return f"{number:,.{decimals}f}"

# --- Plotting Logic ---
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
    ax.set_ylabel("Currency")
    ax.set_title("Break-Even Analysis Chart")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

# --- Main Entry Point (Matches app.py Line 8) ---
def show_break_even_shift_calculator():
    # Note: No st.set_page_config here as it's handled in app.py
    st.header("📈 Executive Break-Even & Pricing Dashboard")
    st.write("Stress-test your business model against shifts in price, cost, and volume.")

    with st.sidebar:
        st.subheader("Financial Inputs")
        f_costs = st.text_input("Existing Fixed Costs", "10000.00")
        f_invest = st.text_input("New Fixed Investment", "0.00")
        t_profit = st.text_input("Target Profit", "0.00")

        st.divider()
        u_price = st.text_input("Price per Unit", "11.00")
        u_cost = st.text_input("Variable Cost per Unit", "6.50")
        u_sold = st.text_input("Units Currently Sold", "500")

        st.divider()
        st.subheader("Stress Testing")
        p_stress = st.slider("Price Shift (%)", -30, 30, 0)
        c_stress = st.slider("Cost Shift (%)", -30, 30, 0)
        v_stress = st.slider("Volume Shift (%)", -50, 50, 0)

        calculate = st.button("Run Stress Test Analysis")

    if calculate:
        try:
            # Data Parsing
            fixed = parse_number_en(f_costs) + parse_number_en(f_invest) + parse_number_en(t_profit)
            price = parse_number_en(u_price) * (1 + p_stress / 100)
            cost = parse_number_en(u_cost) * (1 + c_stress / 100)
            volume = parse_number_en(u_sold) * (1 + v_stress / 100)

            # Calculation
            margin = price - cost
            if margin <= 0:
                st.error("🔴 Fatal Error: Contribution margin is zero or negative. The model is structurally broken under these stress conditions.")
                return

            bep_units = fixed / margin
            actual_profit = (margin * volume) - fixed
            mos = (volume - bep_units) / volume if volume > 0 else -1

            # Decision Logic (Risk Score)
            risk = 0
            if actual_profit < 0: risk += 50
            if mos < 0.10: risk += 30
            risk = min(risk, 100)

            # Executive Summary
            st.divider()
            if risk > 70:
                st.error(f"🔴 High Risk Alert: Potential loss of ${abs(actual_profit):,.2f}")
            elif risk > 30:
                st.warning(f"🟠 Moderate Risk: Profit margin is thin (${actual_profit:,.2f})")
            else:
                st.success(f"🟢 Low Risk: Projected profit of ${actual_profit:,.2f}")

            # KPI Grid
            c1, c2, c3 = st.columns(3)
            c1.metric("Break-Even Point", f"{int(bep_units)} units")
            c2.metric("Projected Profit", f"${actual_profit:,.2f}")
            c3.metric("Margin of Safety", f"{mos*100:.1f}%")

            st.divider()
            
            # Insights
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("📊 Visualization")
                plot_break_even(fixed, price, cost, volume)
                
            
            with col_b:
                st.subheader("💡 Strategic Insights")
                req_price = (fixed / volume) + cost if volume > 0 else 0
                st.write(f"To break even at current volume, your price must be at least: **${req_price:,.2f}**")
                

        except Exception as e:
            st.error(f"Calculation Error: {e}")

if __name__ == "__main__":
    show_break_even_shift_calculator()
