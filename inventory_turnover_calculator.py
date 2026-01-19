import streamlit as st

def turnover_quantity_based(avg_qty, sold_qty):
    if sold_qty == 0:
        return 0
    return round((avg_qty * 365) / sold_qty, 2)

def turnover_value_based(avg_value, cost_of_goods_sold):
    if cost_of_goods_sold == 0:
        return 0
    return round((avg_value * 365) / cost_of_goods_sold, 2)

def show_inventory_turnover_calculator():
    st.title("📦 Inventory Turnover Calculator")
    st.write("Select the calculation method:")

    method = st.radio("Calculation Method", ["📊 Quantity-Based", "💶 Value-Based"])

    num_items = st.number_input("Number of Products", min_value=1, max_value=10, value=4)

    product_names = []
    quantity_inputs = []
    value_inputs = []

    st.markdown("### Input Data")
    for i in range(num_items):
        st.markdown(f"#### Product {i+1}")
        name = st.text_input(f"Product Name {i+1}", key=f"name_{i}")

        if method == "📊 Quantity-Based":
            avg_inventory = st.number_input("Average Inventory (units)", min_value=0.0, key=f"inv_qty_{i}")
            sold_quantity = st.number_input("Units Sold", min_value=0.0, key=f"sold_qty_{i}")
            quantity_inputs.append((avg_inventory, sold_quantity))
        else:
            avg_inventory_value = st.number_input("Average Inventory Value (€)", min_value=0.0, key=f"inv_val_{i}")
            cogs = st.number_input("Cost of Goods Sold (€)", min_value=0.0, key=f"cogs_{i}")
            value_inputs.append((avg_inventory_value, cogs))

        product_names.append(name)

    if st.button("📈 Calculate"):
        st.subheader("Results")
        for i, name in enumerate(product_names):
            if method == "📊 Quantity-Based":
                avg_inv, sold = quantity_inputs[i]
                result = turnover_quantity_based(avg_inv, sold)
                st.write(f"🛒 **{name}**: {result} days turnover (quantity)")
            else:
                avg_val, cogs = value_inputs[i]
                result = turnover_value_based(avg_val, cogs)
                st.write(f"💰 **{name}**: {result} days turnover (value)")
