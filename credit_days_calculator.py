import streamlit as st

# =========================================
# LOGIC
# =========================================

def calculate_weighted_average(customers, credit_days):
    """
    Weighted average of credit days based on number of customers.
    """
    total_customers = sum(customers)

    if total_customers == 0:
        return 0, 0.0

    weighted_sum = sum(c * d for c, d in zip(customers, credit_days))
    weighted_average = weighted_sum / total_customers

    return total_customers, round(weighted_average, 2)


# =========================================
# UI
# =========================================

def show_credit_days_calculator():
    st.title("📅 Weighted Average Credit Days")

    st.caption(
        "Calculate the **average credit period** across customer categories, "
        "weighted by the **number of customers**. "
        "Useful for receivables and cash-flow planning."
    )

    st.markdown("---")

    num_categories = st.number_input(
        "Number of customer categories",
        min_value=1,
        max_value=10,
        value=4
    )

    customers = []
    credit_days = []

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👥 Customers")
        for i in range(num_categories):
            customers.append(
                st.number_input(
                    f"Category {i+1} – Customers",
                    min_value=0,
                    step=1,
                    key=f"cust_{i}"
                )
            )

    with col2:
        st.subheader("📆 Credit Days")
        for i in range(num_categories):
            credit_days.append(
                st.number_input(
                    f"Category {i+1} – Credit Days",
                    min_value=0,
                    step=1,
                    key=f"days_{i}"
                )
            )

    st.markdown("---")

    if st.button("📊 Calculate", type="primary"):

        total_customers, weighted_avg = calculate_weighted_average(
            customers, credit_days
        )

        if total_customers == 0:
            st.error("⚠️ Enter at least one customer.")
            return

        st.subheader("📈 Results")

        c1, c2 = st.columns(2)

        c1.metric(
            "Total Customers",
            f"{total_customers}"
        )

        c2.metric(
            "Weighted Avg Credit Days",
            f"{weighted_avg} days"
        )

        st.info(
            "💡 This average reflects **where most of your customers actually are**, "
            "not a simple arithmetic mean."
        )
