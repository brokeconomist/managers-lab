import streamlit as st

def calculate_supplier_credit_gain(supplier_credit_days, discount_pct, clients_pct, current_sales, unit_price, total_unit_cost, interest_rate_pct):
    # Convert percentages to decimals
    discount = discount_pct / 100
    clients = clients_pct / 100
    interest_rate = interest_rate_pct / 100

    # Gain from discount for early payment
    discount_gain = current_sales * discount * clients

    # Opportunity cost from lost credit
    average_cost = total_unit_cost / unit_price
    credit_benefit = ((current_sales / (360 / supplier_credit_days)) * average_cost
                      - ((current_sales * (1 - clients)) / (360 / supplier_credit_days)) * average_cost) * interest_rate

    net_gain = discount_gain - credit_benefit
    return discount_gain, credit_benefit, net_gain

def format_currency(amount):
    return f"€ {amount:,.0f}".replace(",", ".")

def show_supplier_credit_analysis():
    st.title("🏦 Supplier Credit Analysis (Discount)")
    st.markdown("Evaluate the benefit of **early payment with discount** versus taking supplier credit.")

    with st.form("supplier_credit_form"):
        col1, col2 = st.columns(2)
        with col1:
            supplier_credit_days = st.number_input("📆 Supplier Credit Days", min_value=0, value=60)
            discount_pct = st.number_input("💸 Early Payment Discount (%)", min_value=0.0, value=2.0)
            clients_pct = st.number_input("👥 % of Sales Paid in Cash", min_value=0.0, max_value=100.0, value=50.0)

        with col2:
            current_sales = st.number_input(
    "💰 Current Sales (€)",
    min_value=0.0,
    value=2_000_000.0,
    step=1000.0,
    format="%.0f"
)
            unit_price = st.number_input("📦 Unit Price (€)", min_value=0.01, value=20.0)
            total_unit_cost = st.number_input("🧾 Total Unit Cost (€)", min_value=0.01, value=18.0)
            interest_rate_pct = st.number_input("🏦 Cost of Capital (%)", min_value=0.0, value=10.0)

        submitted = st.form_submit_button("🔍 Calculate")

    if submitted:
        discount_gain, credit_cost, net_gain = calculate_supplier_credit_gain(
            supplier_credit_days, discount_pct, clients_pct,
            current_sales, unit_price, total_unit_cost, interest_rate_pct
        )

        st.subheader("📊 Results")
        st.metric("✅ Gain from Discount", format_currency(discount_gain))
        st.metric("💸 Credit Opportunity Cost", format_currency(credit_cost))
        st.metric("🏁 Net Benefit", format_currency(net_gain), delta_color="normal" if net_gain >= 0 else "inverse")

        if net_gain > 0:
            st.success("👉 Early payment with the proposed discount is profitable.")
        else:
            st.error("⚠️ Early payment with this discount is not profitable.")

