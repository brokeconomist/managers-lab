import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# --- Utilities: Συναρτήσεις για τη διαχείριση αριθμών ---
def parse_number_en(number_str):
    try:
        return float(str(number_str).replace(",", ""))
    except:
        return 0.0

def format_number_en(number, decimals=2):
    return f"{number:,.{decimals}f}"

# --- Plotting: Δημιουργία Γραφήματος ---
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
    ax.set_title("Break-Even Position Analysis")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

# --- Η Κύρια Συνάρτηση που τρέχει το εργαλείο ---
def show_break_even_shift_calculator():
    st.header("📈 Executive Break-Even & Pricing Dashboard")
    st.write("Stress-test your business model against shifts in price, cost, and volume.")

    # ΠΛΕΥΡΙΚΟ ΜΕΝΟΥ (Inputs)
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

    # ΑΠΟΤΕΛΕΣΜΑΤΑ (Outputs)
    if calculate:
        try:
            # Μετατροπή των κειμένων σε αριθμούς
            fixed = parse_number_en(f_costs) + parse_number_en(f_invest) + parse_number_en(t_profit)
            price = parse_number_en(u_price) * (1 + p_stress / 100)
            cost = parse_number_en(u_cost) * (1 + c_stress / 100)
            volume = parse_number_en(u_sold) * (1 + v_stress / 100)

            # Υπολογισμοί
            margin = price - cost
            if margin <= 0:
                st.error("🔴 Fatal Error: Contribution margin is zero or negative. The model collapses.")
                return

            bep_units = fixed / margin
            actual_profit = (margin * volume) - fixed
            mos = (volume - bep_units) / volume if volume > 0 else -1

            # Υπολογισμός Ρίσκου
            risk = 0
            if actual_profit < 0: risk += 50
            if mos < 0.10: risk += 30
            risk = min(risk, 100)

            st.divider()

            # 1. Executive Signal (Φανάρι Ρίσκου)
            if risk > 70:
                st.error(f"🔴 High Risk Alert: Projected Loss of ${abs(actual_profit):,.2f}")
            elif risk > 30:
                st.warning(f"🟠 Moderate Risk: Profit margin is thin (${actual_profit:,.2f})")
            else:
                st.success(f"🟢 Low Risk: Projected Profit of ${actual_profit:,.2f}")

            # 2. Κεντρικά Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Break-Even Point", f"{int(bep_units)} units")
            c2.metric("Projected Profit", f"${actual_profit:,.2f}")
            c3.metric("Margin of Safety", f"{mos*100:.1f}%")

            st.divider()
            
            # 3. Ανάλυση σε δύο στήλες
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("📊 Visualization")
                plot_break_even(fixed, price, cost, volume)
                
            
            with col_right:
                st.subheader("💡 Strategic Insights")
                req_price = (fixed / volume) + cost if volume > 0 else 0
                
                # Πίνακας για καθαρή εμφάνιση των δεδομένων
                st.markdown("**Structural Analysis Summary**")
                summary_df = pd.DataFrame({
                    "Variable": ["Total Fixed Costs", "Volume Analyzed", "Stressed Unit Cost"],
                    "Value": [f"${fixed:,.2f}", f"{int(volume)} units", f"${cost:,.2f}"]
                })
                st.table(summary_df)
                
                # Το κρίσιμο συμπέρασμα σε μπλε πλαίσιο
                st.info(f"""
                **Pricing Goal:**
                To cover your costs and target profit at a volume of **{int(volume)}** units:
                
                Your minimum price must be: **${req_price:,.2f}**
                """)
                
                

                # Operational status check
                if volume < bep_units:
                    gap = bep_units - volume
                    st.error(f"⚠️ **STATUS: DEFICIT** \nYou are **{int(gap)} units below** break-even.")
                else:
                    surplus = volume - bep_units
                    st.success(f"✅ **STATUS: SURPLUS** \nYou are **{int(surplus)} units above** break-even.")

        except Exception as e:
            st.error(f"System Error: {e}")

# Επιτρέπει στο εργαλείο να τρέξει και μόνο του
if __name__ == "__main__":
    show_break_even_shift_calculator()
