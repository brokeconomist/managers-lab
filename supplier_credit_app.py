import streamlit as st

# ===== Calculation Logic =====
def calculate_supplier_credit_gain(
    supplier_credit_days,
    discount_pct,
    current_sales,
    total_unit_cost,
    interest_rate_pct
):
    """
    Compare:
    1) Paying early and taking the discount
    2) Using supplier credit and keeping cash longer

    Returns:
        discount_gain
        financing_benefit
        net_gain
    """

    discount = discount_pct / 100
    interest_rate = interest_rate_pct / 100

    # Cost of goods sold (approximation)
    cost_of_goods = current_sales * (total_unit_cost_ratio := total_unit_cost)

    # 1️⃣ Gain from discount
    discount_gain = cost_of_goods * discount

    # 2️⃣ Financing benefit from keeping cash for credit period
    financing_benefit = (
        cost_of_goods *
        (supplier_credit_days / 360) *
        interest_rate
    )

    net_gain = discount_gain - financing_benefit

    return discount_gain, financing_benefit, net_gain


# ===== Utility =====
def format_currency(amount):
    return f"€ {amount:,.0f}".replace(",", ".")


# ===== Streamlit UI =====
def show_supplier_credit_analysis():

    st.title("🏦 Supplier Credit vs Early Payment Decision")
    st.caption(
        "Evaluate whether taking the early payment discount is financially superior "
        "to using supplier credit as a short-term financing source."
    )

    # ===== Input Form =====
    with st.form("supplier_credit_form"):

        st.header("🔢 Input Data")

        col1, col2 = st.columns(2)

        with col1:
            supplier_credit_days = st.number_input(
                "📆 Supplier Credit Days",
                min_value=1,
                value=60
            )
            st.caption(
                "Number of days you can delay payment without penalty. "
                "This acts as short-term supplier financing."
            )

            discount_pct = st.number_input(
                "💸 Early Payment Discount (%)",
                min_value=0.0,
                value=2.0
            )
            st.caption(
                "Percentage discount offered if payment is made immediately."
            )

        with col2:
            current_sales = st.number_input(
                "💰 Annual Sales (€)",
                min_value=0.0,
                value=2_000_000.0,
                step=10_000.0,
                format="%.0f"
            )
            st.caption(
                "Total annual revenue."
            )

            total_unit_cost = st.number_input(
                "🧾 Cost of Goods as % of Sales",
                min_value=0.0,
                max_value=100.0,
                value=80.0
            ) / 100
            st.caption(
                "Cost of goods sold expressed as percentage of revenue."
            )

            interest_rate_pct = st.number_input(
                "🏦 Cost of Capital (%)",
                min_value=0.0,
                value=10.0
            )
            st.caption(
                "Annual financing cost or opportunity cost of capital."
            )

        submitted = st.form_submit_button("🔍 Calculate")

    # ===== Results =====
    if submitted:

        discount_gain, financing_benefit, net_gain = calculate_supplier_credit_gain(
            supplier_credit_days,
            discount_pct,
            current_sales,
            total_unit_cost,
            interest_rate_pct
        )

        st.divider()
        st.subheader("📊 Financial Comparison")

        col1, col2, col3 = st.columns(3)

        col1.metric("✅ Discount Benefit", format_currency(discount_gain))
        col2.metric("🏦 Financing Benefit of Credit", format_currency(financing_benefit))
        col3.metric(
            "🏁 Net Advantage",
            format_currency(net_gain),
            delta_color="normal" if net_gain >= 0 else "inverse"
        )

        st.divider()

        if net_gain > 0:
            st.success("👉 Taking the early payment discount is financially superior.")
        else:
            st.warning("👉 Using supplier credit is financially preferable.")

        # ===== Effective Annual Rate =====
        effective_rate = (discount_pct / (100 - discount_pct)) * (360 / supplier_credit_days)

        st.subheader("📈 Implied Annual Cost of Not Taking Discount")
        st.metric("Effective Annual Rate", f"{effective_rate:.2f}%")

        st.caption(
            "If the implied annual rate exceeds your cost of capital, "
            "you should take the discount."
        )


if __name__ == "__main__":
    show_supplier_credit_analysis()
