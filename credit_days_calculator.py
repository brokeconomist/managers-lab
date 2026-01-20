import streamlit as st

def calculate_weighted_average(customers, credit_days):
    """
    Calculate the weighted average of credit days.

    Parameters:
        customers (list of int/float): Number of customers per category
        credit_days (list of int/float): Credit days per category

    Returns:
        total_customers (int): Total number of customers
        weighted_average (float): Weighted average of credit days
    """
    total_customers = sum(customers)
    weighted_sum = sum(c * d for c, d in zip(customers, credit_days))
    weighted_average = weighted_sum / total_customers if total_customers != 0 else 0
    return total_customers, round(weighted_average, 2)


def show_credit_days_calculator():
    st.title("📅 Weighted Average Credit Days Calculator")
    st.caption(
        "Calculate the **average credit period** across different customer categories, "
        "weighted by the number of customers. Useful for cash flow and receivables planning."
    )

    st.header("🔢 Input Data")
    st.write("Enter the **number of customers** and the **credit days** for each category.")

    num_categories = st.number_input(
        "Number of customer categories",
        min_value=1, max_value=10, value=4
    )

    customers = []
    credit_days = []

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👥 Customers per Category")
        for i in range(num_categories):
            value = st.number_input(
                f"Category {i+1} - Number of Customers",
                key=f"cust_{i}",
                min_value=0
            )
            customers.append(value)
        st.caption(
            "Enter how many customers belong to each category. "
            "This determines the weight of each category in the average calculation."
        )

    with col2:
        st.subheader("📆 Credit Days per Category")
        for i in range(num_categories):
            value = st.number_input(
                f"Category {i+1} - Credit Days",
                key=f"days_{i}",
                min_value=0
            )
            credit_days.append(value)
        st.caption(
            "Enter the agreed credit days for each category. "
            "This represents the payment period granted to each group."
        )

    if st.button("📊 Calculate Weighted Average"):
        total_customers, weighted_avg = calculate_weighted_average(customers, credit_days)

        st.markdown("---")
        st.subheader("📈 Results")
        st.metric(
            "✅ Total Customers",
            f"{total_customers}"
        )
        st.caption(
            "The total number of customers across all categories."
        )

        st.metric(
            "🕐 Weighted Average Credit Days",
            f"{weighted_avg}"
        )
        st.caption(
            "The weighted average credit period, taking into account the number of customers in each category. "
            "Useful for **cash flow forecasting**, **accounts receivable management**, and financial planning."
        )
