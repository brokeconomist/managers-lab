import streamlit as st
import matplotlib.pyplot as plt

# ----------------------------
# Helper functions
# ----------------------------
def parse_number(number_str):
    try:
        return float(number_str.replace(',', ''))
    except:
        return None

def format_percentage(number, decimals=1):
    return f"{number:.{decimals}f}%"

# ----------------------------
# Calculation
# ----------------------------
def calculate_required_sales_increase(
    old_price,
    price_decrease_pct,
    profit_suit,
    profit_shirt,
    profit_tie,
    profit_belt,
    profit_shoes,
    percent_shirt,
    percent_tie,
    percent_belt,
    percent_shoes
):
    combined_profit = (
        profit_suit +
        percent_shirt * profit_shirt +
        percent_tie * profit_tie +
        percent_belt * profit_belt +
        percent_shoes * profit_shoes
    )
    new_price = old_price * (1 - price_decrease_pct)
    loss_per_unit = old_price - new_price

    try:
        required_increase = loss_per_unit / combined_profit
        return required_increase * 100
    except ZeroDivisionError:
        return None

# ----------------------------
# Plot
# ----------------------------
def plot_sales_increase(required_increase, current_sales_pct):
    labels = ["Baseline (0%)", "Current Sales", "Required Increase"]
    values = [0, current_sales_pct, required_increase]
    colors = ["gray", "blue", "orange"]

    fig, ax = plt.subplots(figsize=(5, 6))
    ax.bar(labels, values, color=colors)
    ax.set_ylabel("Sales (%)")
    ax.set_ylim(0, max(values)*1.3)
    ax.set_title("Required Suit Sales Increase After Discount")

    # Vertical line at Required Increase
    ax.axhline(y=required_increase, color='orange', linestyle='--')

    # Annotate bars
    for i, v in enumerate(values):
        ax.text(i, v + max(values)*0.02, format_percentage(v), ha='center', fontsize=10)

    st.pyplot(fig)
    st.markdown("---")

# ----------------------------
# Streamlit UI
# ----------------------------
def show_complementary_analysis():
    st.write("Complementary Product Analysis")
    st.header("🧥 Estimate Suit Sales Increase after Discount")
    st.markdown("""
The manager is considering a price reduction on suits. Customers may also purchase
other products (shirts, ties, belts, shoes).

👉 This tool calculates **how much suit sales must increase** to maintain total profit.
""")

    with st.form("discount_impact_form"):
        col1, col2 = st.columns(2)

        with col1:
            old_price_input = st.text_input("Suit Price (€)", value="200")
            profit_suit_input = st.text_input("Profit per Suit (€)", value="60")
            price_decrease_input = st.text_input("Price Decrease (%)", value="10")
            shirt_profit_input = st.text_input("Profit per Shirt (€)", value="13")
            tie_profit_input = st.text_input("Profit per Tie (€)", value="11")

        with col2:
            belt_profit_input = st.text_input("Profit per Belt (€)", value="11")
            shoes_profit_input = st.text_input("Profit per Shoes (€)", value="45")

            percent_shirt = st.slider("Percentage of customers buying Shirt (%)", 0.0, 100.0, 90.0) / 100
            percent_tie = st.slider("Percentage of customers buying Tie (%)", 0.0, 100.0, 70.0) / 100
            percent_belt = st.slider("Percentage of customers buying Belt (%)", 0.0, 100.0, 10.0) / 100
            percent_shoes = st.slider("Percentage of customers buying Shoes (%)", 0.0, 100.0, 5.0) / 100
            current_sales_pct = st.slider("Current Suit Sales (%)", 0, 200, 0)
            st.caption("Current sales of suits as % of previous period. Adjust to see distance from required increase.")

        submitted = st.form_submit_button("Calculate")

    if submitted:
        old_price = parse_number(old_price_input)
        profit_suit = parse_number(profit_suit_input)
        price_decrease_pct = parse_number(price_decrease_input)/100
        profit_shirt = parse_number(shirt_profit_input)
        profit_tie = parse_number(tie_profit_input)
        profit_belt = parse_number(belt_profit_input)
        profit_shoes = parse_number(shoes_profit_input)

        if None in [old_price, profit_suit, price_decrease_pct, profit_shirt, profit_tie, profit_belt, profit_shoes]:
            st.error("❌ Please check all numeric fields.")
            return

        result = calculate_required_sales_increase(
            old_price,
            price_decrease_pct,
            profit_suit,
            profit_shirt,
            profit_tie,
            profit_belt,
            profit_shoes,
            percent_shirt,
            percent_tie,
            percent_belt,
            percent_shoes
        )

        if result is None:
            st.error("❌ Cannot calculate. Try different values.")
        else:
            st.success(f"✅ Required suit sales increase: {format_percentage(result)}")
            # Plot vertical bar chart
            plot_sales_increase(result, current_sales_pct)
