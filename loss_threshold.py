import streamlit as st

# --- Helper functions for English number formatting ---
def parse_number(number_str):
    """Convert string with English decimal separator to float."""
    try:
        return float(number_str.replace(',', ''))
    except:
        return None

def format_number(number, decimals=2):
    return f"{number:,.{decimals}f}"

def format_percentage(number, decimals=1):
    return f"{number:.{decimals}f}%"

# --- Calculation ---
def calculate_sales_loss_threshold(
    competitor_old_price,
    competitor_new_price,
    our_price,
    unit_cost
):
    try:
        top = (competitor_new_price - competitor_old_price) / competitor_old_price
        bottom = (unit_cost - our_price) / our_price
        if bottom == 0:
            return None
        result = top / bottom
        return result * 100  # return as percentage
    except ZeroDivisionError:
        return None

# --- Streamlit UI ---
def show_loss_threshold_before_price_cut():
    st.header("📉 Sales Loss Threshold Before Price Reduction")
    st.title("How much sales can you lose before considering a price cut? ⚖️")

    st.markdown("""
    🧠 Competitors reduced their prices — should you follow?

    👉 This tool shows **how much percentage of sales you can afford to lose**
    before you need to lower your price to stay competitive.
    """)

    with st.form("loss_threshold_form"):
        col1, col2 = st.columns(2)

        with col1:
            competitor_old_price_input = st.text_input("Competitor's Original Price (€)", value=format_number(8.0))
            our_price_input = st.text_input("Our Product Price (€)", value=format_number(8.0))

        with col2:
            competitor_new_price_input = st.text_input("Competitor's New Price (€)", value=format_number(7.2))
            unit_cost_input = st.text_input("Unit Cost (€)", value=format_number(4.5))

        submitted = st.form_submit_button("Calculate")

    if submitted:
        competitor_old_price = parse_number(competitor_old_price_input)
        competitor_new_price = parse_number(competitor_new_price_input)
        our_price = parse_number(our_price_input)
        unit_cost = parse_number(unit_cost_input)

        if None in (competitor_old_price, competitor_new_price, our_price, unit_cost):
            st.error("⚠️ Please check that all numeric fields are correctly filled.")
            return

        result = calculate_sales_loss_threshold(
            competitor_old_price,
            competitor_new_price,
            our_price,
            unit_cost
        )

        if result is None:
            st.error("⚠️ Cannot calculate. Check the input values.")
        elif result <= 0:
            st.warning("❗ No sales loss margin. Your price is already less competitive.")
        else:
            st.success(f"✅ Maximum % of sales that can be lost before a price cut: {format_percentage(result)}")

    st.markdown("---")
