import streamlit as st


def format_en_number(x, decimals=2):
    """
    English number formatting:
    1234567.89 -> 1,234,567.89
    """
    try:
        return f"{x:,.{decimals}f}"
    except Exception:
        return str(x)


def show_gross_profit_analysis():
    st.title("📈 Gross Profit Analysis")
    st.markdown("Enter your data below to analyze revenue, cost of goods sold, and gross margin.")

    col1, col2 = st.columns(2)

    with col1:
        unit_price = st.number_input("Unit Price (€)", value=12.00, min_value=0.0, step=0.01)
        units_sold = st.number_input("Units Sold", value=22_500, min_value=0)
        returns = st.number_input("Returns (€)", value=1_000.00, min_value=0.0, step=0.01)
        discounts = st.number_input("Discounts (€)", value=2_000.00, min_value=0.0, step=0.01)
        opening_inventory = st.number_input("Opening Inventory (€)", value=40_000.00, min_value=0.0, step=0.01)

    with col2:
        purchases = st.number_input("Purchases (€)", value=132_000.00, min_value=0.0, step=0.01)
        closing_inventory = st.number_input("Closing Inventory (€)", value=42_000.00, min_value=0.0, step=0.01)
        direct_labor = st.number_input("Direct Labor (€)", value=10_000.00, min_value=0.0, step=0.01)
        manufacturing_overhead = st.number_input("Manufacturing Overhead (€)", value=30_000.00, min_value=0.0, step=0.01)
        depreciation = st.number_input("Depreciation (€)", value=20_000.00, min_value=0.0, step=0.01)

    # --- Calculations ---
    net_sales = (
        unit_price * units_sold
        - returns
        - discounts
    )

    cost_of_goods_sold = (
        opening_inventory
        + purchases
        + direct_labor
        + manufacturing_overhead
        + depreciation
        - closing_inventory
    )

    gross_profit = net_sales - cost_of_goods_sold
    gross_margin_pct = (gross_profit / net_sales * 100) if net_sales != 0 else 0

    # --- Results ---
    st.markdown("---")
    st.subheader("📊 Results")

    st.metric("Net Sales", f"€ {format_en_number(net_sales)}")
    st.metric("Cost of Goods Sold (COGS)", f"€ {format_en_number(cost_of_goods_sold)}")
    st.metric("Gross Profit", f"€ {format_en_number(gross_profit)}")
    st.metric("Gross Margin", f"{format_en_number(gross_margin_pct)} %")
