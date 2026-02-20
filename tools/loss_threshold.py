import streamlit as st
import pandas as pd

# -----------------------
# Utilities
# -----------------------

def parse_number(number_str):
    try:
        return float(str(number_str).replace(',', ''))
    except:
        return None

def format_percentage(number, decimals=1):
    return f"{number:.{decimals}f}%"

# -----------------------
# Calculation Logic
# -----------------------

def calculate_sales_loss_threshold(comp_old, comp_new, our_price, unit_cost):
    try:
        # Price change ratio of competitor
        comp_price_change = (comp_new - comp_old) / comp_old
        # Our contribution margin ratio
        our_margin_ratio = (unit_cost - our_price) / our_price
        
        if our_margin_ratio == 0:
            return None
            
        # The threshold: How much volume loss equals the profit loss of a price match
        result = comp_price_change / our_margin_ratio
        return result * 100 
    except ZeroDivisionError:
        return None

# -----------------------
# Main UI
# -----------------------

def show_loss_threshold_before_price_cut():
    st.header("📉 Sales Loss Threshold Analysis")
    st.write("Determine the structural limit of volume loss before a defensive price reduction becomes mathematically necessary.")

    # SIDEBAR: Strategic Inputs
    with st.sidebar:
        st.subheader("Competitor Action")
        c_old = st.text_input("Competitor's Original Price (€)", "8.00")
        c_new = st.text_input("Competitor's New Price (€)", "7.20")
        
        st.divider()
        st.subheader("Internal Economics")
        u_price = st.text_input("Our Current Price (€)", "8.00")
        u_cost = st.text_input("Unit Variable Cost (€)", "4.50")
        
        st.divider()
        run = st.button("Calculate Resilience Threshold")

    # MAIN SCREEN: Analytical Results
    if run:
        # Data Parsing
        comp_old = parse_number(c_old)
        comp_new = parse_number(c_new)
        our_price = parse_number(u_price)
        unit_cost = parse_number(u_cost)

        if None in (comp_old, comp_new, our_price, unit_cost):
            st.error("⚠️ Strategic Error: Incomplete financial data. Please check sidebar inputs.")
            return

        threshold = calculate_sales_loss_threshold(comp_old, comp_new, our_price, unit_cost)
        comp_drop_pct = ((comp_new - comp_old) / comp_old) * 100
        our_margin = our_price - unit_cost

        st.subheader("📊 Executive Summary")
        
        if threshold is None:
            st.error("⚠️ Calculation collapsed. Check for zero margins.")
        elif threshold <= 0:
            st.warning("❗ No Buffer: Your current margin structure cannot absorb this competitor move.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Max Volume Loss Allowed", format_percentage(threshold))
            c2.metric("Competitor Price Cut", f"{comp_drop_pct:.1f}%")
            c3.metric("Current Unit Margin", f"€{our_margin:.2f}")

            # 1. Strategic Interpretation
            st.divider()
            st.subheader("🧠 Strategic Interpretation")
            
            
            
            st.info(f"""
            **The Cold Reality:** A price match will drop your profit on *every* unit sold. 
            Staying at your current price is more profitable **as long as your sales drop is less than {format_percentage(threshold)}**.
            
            If you expect to lose *more* than {format_percentage(threshold)} of your customers to the competitor, only then is a price cut mathematically justified.
            """)

            # 2. Risk Matrix
            st.subheader("📋 Decision Framework")
            
            decision_data = {
                "Scenario": ["Actual Loss < Threshold", "Actual Loss = Threshold", "Actual Loss > Threshold"],
                "Action": ["HOLD PRICE", "INDIFFERENT", "REDUCE PRICE"],
                "Financial Impact": ["Higher Profit via Margin", "Breakeven Point", "Profit Protection via Volume"]
            }
            st.table(pd.DataFrame(decision_data))

            # 3. Visualization of the Margin Buffer
            st.divider()
            st.subheader("📉 Structural Resilience Visualization")
            
            # Simple Progress bar to show how much "Safety Room" exists
            st.write(f"Volume Loss Tolerance: {threshold:.1f}%")
            st.progress(min(threshold / 100, 1.0))
            
            st.caption("Note: This model assumes linear demand and no change in variable costs. It measures the 'Indifference Point' between margin erosion and volume erosion.")

if __name__ == "__main__":
    show_loss_threshold_before_price_cut()
