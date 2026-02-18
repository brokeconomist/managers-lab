import streamlit as st
import pandas as pd

# -----------------------
# Utilities
# -----------------------

def parse_number(number_str):
    try:
        return float(str(number_str).replace(",", ""))
    except:
        return 0.0

def format_percentage(number, decimals=2):
    return f"{number:.{decimals}f}%"

# -----------------------
# Core Calculation
# -----------------------

def calculate_required_sales_increase(
    suit_price, price_decrease_pct, profit_suit,
    profit_shirt, profit_tie, profit_belt, profit_shoes,
    p_shirt, p_tie, p_belt, p_shoes
):
    # Expected profit from complements per main unit sold
    expected_complement_profit = (
        p_shirt * profit_shirt +
        p_tie * profit_tie +
        p_belt * profit_belt +
        p_shoes * profit_shoes
    )

    total_profit_per_main_unit = profit_suit + expected_complement_profit

    try:
        # Indifference point formula for total profit maintenance
        required_increase = -price_decrease_pct / (
            (total_profit_per_main_unit / suit_price) + price_decrease_pct
        )
        return required_increase * 100
    except ZeroDivisionError:
        return None

# -----------------------
# UI Logic
# -----------------------

def show_complementary_analysis():
    st.header("🧥 Complementary Products & Cross-Sell Analysis")
    st.write("Evaluate the required volume growth to offset price cuts, accounting for secondary profit streams.")

    # SIDEBAR: All Financial Inputs
    with st.sidebar:
        st.subheader("Core Product (Main)")
        s_price = st.text_input("Main Unit Price (€)", "200.00")
        s_profit = st.text_input("Main Unit Profit (€)", "60.00")
        s_discount = st.slider("Proposed Discount (%)", 0.0, 40.0, 10.0) / 100

        st.divider()
        st.subheader("Complementary Profits (€)")
        prof_shirt = st.number_input("Profit: Shirt", value=13.0)
        prof_tie = st.number_input("Profit: Tie", value=11.0)
        prof_belt = st.number_input("Profit: Belt", value=11.0)
        prof_shoes = st.number_input("Profit: Shoes", value=45.0)

        st.divider()
        st.subheader("Attach Rates (Probabilities)")
        prob_shirt = st.slider("Shirt Attach Rate (%)", 0, 100, 90) / 100
        prob_tie = st.slider("Tie Attach Rate (%)", 0, 100, 70) / 100
        prob_belt = st.slider("Belt Attach Rate (%)", 0, 100, 10) / 100
        prob_shoes = st.slider("Shoes Attach Rate (%)", 0, 100, 5) / 100

        run = st.button("Run Impact Analysis")

    # MAIN SCREEN: Results
    if run:
        # Data Parsing
        price = parse_number(s_price)
        profit_base = parse_number(s_profit)
        discount = -abs(s_discount)

        result = calculate_required_sales_increase(
            price, discount, profit_base,
            prof_shirt, prof_tie, prof_belt, prof_shoes,
            prob_shirt, prob_tie, prob_belt, prob_shoes
        )

        if result is None or result < 0:
            st.error("🔴 Strategic Deficit: The proposed discount collapses the margin beyond recovery.")
            return

        # 1. Executive Metrics
        st.subheader("📊 Strategic Indifference Point")
        c1, c2, c3 = st.columns(3)
        
        expected_cross_sell = (prob_shirt * prof_shirt + prob_tie * prof_tie + 
                               prob_belt * prof_belt + prob_shoes * prof_shoes)
        
        c1.metric("Required Volume Growth", format_percentage(result))
        c2.metric("Avg. Cross-Sell Profit", f"€{expected_cross_sell:.2f}")
        c3.metric("Total Margin / Bundle", f"€{(profit_base + expected_cross_sell):.2f}")

        # 2. Impact Table
        st.divider()
        st.subheader("📈 Scenario Breakdown")
        
        impact_df = pd.DataFrame({
            "Component": ["Base Product Margin", "Expected Cross-Sell Contribution", "Effective Bundle Margin", "Post-Discount Margin"],
            "Value (€)": [
                f"€{profit_base:,.2f}",
                f"€{expected_cross_sell:,.2f}",
                f"€{(profit_base + expected_cross_sell):,.2f}",
                f"€{(profit_base + expected_cross_sell + (price * discount)):,.2f}"
            ]
        })
        st.table(impact_df)

        # 3. Visual Context
        st.divider()
        st.subheader("💡 Strategic Assessment")
        
        
        
        if result > 30:
            st.warning(f"⚠️ HIGH SENSITIVITY: A volume increase of {result:.1f}% is required. Verify if the market can absorb this growth.")
        else:
            st.success(f"🟢 MANAGEABLE: The cross-sell profit buffers the discount. Growth required: {result:.1f}%.")

        st.info("""
        **Analytical Logic:** This tool uses 'Indifference Analysis'. It calculates the exact volume increase needed so that the 
        gain from new sales (including complements) exactly offsets the loss from the price reduction 
        on existing volume.
        """)

if __name__ == "__main__":
    show_complementary_analysis()
