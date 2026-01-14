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
def calculate_max_product_A_sales_drop(
    old_price,
    price_increase_absolute,  # decimal, e.g., 0.05 for 5%
    profit_A,
    profit_B,
    profit_C,
    profit_D,
    percent_B,
    percent_C,
    percent_D
):
    """
    Returns estimated maximum % sales drop of Product A so that total profit does not decrease.
    """
    benefit_substitutes = (
        percent_B * profit_B +
        percent_C * profit_C +
        percent_D * profit_D
    )

    denominator = ((profit_A - benefit_substitutes) / old_price) + price_increase_absolute
    numerator = -price_increase_absolute

    try:
        max_sales_drop_decimal = numerator / denominator
        max_sales_drop_percent = max_sales_drop_decimal * 100
        return max_sales_drop_percent
    except ZeroDivisionError:
        return None

# --- Streamlit UI ---
def show_substitution_analysis():
    st.write("Substitution Analysis")
    st.header("📈 Estimate Acceptable Sales Drop of Product A after Price Increase")
    st.title("What happens if customers switch to another product? 🔄")
    st.markdown("""
You have similar products and are considering a price change for one of them.

👉 This tool estimates, based on the percentage of customers expected to switch to other products,  
how your total sales and revenue will be affected.

Useful for similar product lines or promotional pricing decisions.
""")

    with st.form("price_increase_form"):
        col1, col2 = st.columns(2)

        with col1:
            old_price_input = st.text_input("Current Unit Price of Product A (€)", value=format_number(1.50))
            price_increase_input = st.text_input("Price Increase (%)", value=format_number(5.0))
            profit_A_input = st.text_input("Profit per Unit of Product A (€)", value=format_number(0.30))

        with col2:
            profit_B_input = st.text_input("Profit per Unit of Product B (€)", value=format_number(0.20))
            profit_C_input = st.text_input("Profit per Unit of Product C (€)", value=format_number(0.20))
            profit_D_input = st.text_input("Profit per Unit of Product D (€)", value=format_number(0.05))

        percent_B = st.slider("Percentage of customers switching to Product B (%)", 0.0, 100.0, 45.0) / 100
        percent_C = st.slider("Percentage of customers switching to Product C (%)", 0.0, 100.0, 20.0) / 100
        percent_D = st.slider("Percentage of customers switching to Product D (%)", 0.0, 100.0, 5.0) / 100

        submitted = st.form_submit_button("Calculate")

    if submitted:
        old_price = parse_number(old_price_input)
        price_increase_pct = parse_number(price_increase_input) / 100  # convert % to decimal
        profit_A = parse_number(profit_A_input)
        profit_B = parse_number(profit_B_input)
        profit_C = parse_number(profit_C_input)
        profit_D = parse_number(profit_D_input)

        if None in (old_price, price_increase_pct, profit_A, profit_B, profit_C, profit_D):
            st.error("❌ Please check that all numeric fields are correctly filled.")
            return

        total_substitute = percent_B + percent_C + percent_D
        if total_substitute > 1:
            st.error("❌ Total customer switch percentage cannot exceed 100%.")
            return

        no_purchase = 1 - total_substitute

        result = calculate_max_product_A_sales_drop(
            old_price,
            price_increase_pct,
            profit_A,
            profit_B,
            profit_C,
            profit_D,
            percent_B,
            percent_C,
            percent_D
        )

        if result is None:
            st.error("❌ Cannot calculate. Try different values.")
        else:
            st.success(f"✅ Maximum acceptable sales drop for Product A: {format_percentage(result)}")
            st.info(f"ℹ️ Percentage of customers who will not buy anything: {format_percentage(no_purchase * 100)}")
