import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# --- Utilities ---
def parse_number_en(number_str):
    try:
        return float(str(number_str).replace(",", ""))
    except:
        return 0.0

def format_number_en(number, decimals=2):
    return f"{number:,.{decimals}f}"

# --- Enhanced Plotting: Μεγαλύτερο και πιο καθαρό γράφημα ---
def plot_break_even(fixed_costs, price, unit_cost, units_sold):
    cm = price - unit_cost
    if cm <= 0:
        return

    bep = fixed_costs / cm
    # Δημιουργούμε ένα εύρος που να δείχνει καθαρά το Break-Even
    max_units = int(max(bep, units_sold) * 1.6) + 10
    x = list(range(0, max_units))

    total_cost = [fixed_costs + unit_cost * q for q in x]
    revenue = [price * q for q in x]

    # Αύξηση μεγέθους γραφήματος (12x7 αντί για 10x6)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(x, total_cost, label="Total Cost", color="#d62728", linewidth=3)
    ax.plot(x, revenue, label="Revenue", color="#2ca02c", linewidth=3)
    
    # Διακεκομμένες γραμμές για τα σημεία αναφοράς
    ax.axvline(bep, linestyle="--", color="#7f7f7f", linewidth=2, label=f"Break-Even Point ({int(bep)})")
    ax.axvline(units_sold, linestyle="-.", color="#1f77b4", linewidth=2, label=f"Stressed Sales ({int(units_sold)})")

    # Μορφοποίηση τίτλων και αξόνων
    ax.set_xlabel("Units Sold", fontsize=12, fontweight='bold')
    ax.set_ylabel("Currency (USD)", fontsize=12, fontweight='bold')
    ax.set_title("Executive Break-Even Analysis", fontsize=16, fontweight='bold', pad=20)
    
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Προσθήκη "σκίασης" στην περιοχή κέρδους
    ax.fill_between(x, revenue, total_cost, where=[r > c for r, c in zip(revenue, total_cost)], 
                    color='green', alpha=0.1, label='Profit Zone')

    st.pyplot(fig)

# --- Main Entry Point ---
def show_break_even_shift_calculator():
    st.header("📈 Executive Break-Even & Pricing Dashboard")
    st.write("Stress-test your business model against shifts in price, cost, and volume.")

    # SIDEBAR
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

        calculate = st.button("Run Executive Analysis")

    if calculate:
        try:
            # Parsing
            fixed = parse_number_en(f_costs) + parse_number_en(f_invest) + parse_number_en(t_profit)
            price = parse_number_en(u_price) * (1 + p_stress / 100)
            cost = parse_number_en(u_cost) * (1 + c_stress / 100)
            volume = parse_number_en(u_sold) * (1 + v_stress / 100)

            margin = price - cost
            if margin <= 0:
                st.error("🔴 Fatal Error: Contribution margin is zero or negative. The model collapses.")
                return

            bep_units = fixed / margin
            actual_profit = (margin * volume) - fixed
            mos = (volume - bep_units) / volume if volume > 0 else -1

            # Risk Assessment
            risk = 0
            if actual_profit < 0: risk += 50
            if mos < 0.10: risk += 30
            risk = min(risk, 100)

            st.divider()

            # 1. Dashboard Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Break-Even Units", f"{int(bep_units)}")
            c2.metric("Projected Profit", f"${actual_profit:,.0f}")
            c3.metric("Margin of Safety", f"{mos*100:.1f}%")

            st.divider()
            
            # 2. Visualization (Full Width)
            st.subheader("📊 Profit & Loss Visualization")
            plot_break_even(fixed, price, cost, volume)
            

            st.divider()

            # 3. Strategic Analysis Section
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("📋 Structural Analysis")
                summary_df = pd.DataFrame({
                    "Variable": ["Total Fixed Costs", "Volume Analyzed", "Stressed Unit Cost"],
                    "Value": [f"${fixed:,.2f}", f"{int(volume)} units", f"${cost:,.2f}"]
                })
                st.table(summary_df)
            
            with col_right:
                st.subheader("💡 Pricing Strategy")
                req_price = (fixed / volume) + cost if volume > 0 else 0
                
                st.info(f"""
                **Pricing Requirement:**
                To break even at a volume of **{int(volume)}** units:
                
                Minimum Price Needed: **${req_price:,.2f}**
                """)
                
                

                if volume < bep_units:
                    st.error(f"⚠️ **DEFICIT:** You are **{int(bep_units - volume)} units short** of break-even.")
                else:
                    st.success(f"✅ **SURPLUS:** You are **{int(volume - bep_units)} units above** break-even.")

        except Exception as e:
            st.error(f"Analysis Error: {e}")

if __name__ == "__main__":
    show_break_even_shift_calculator()
