import streamlit as st

def calculate_weighted_average(customers, credit_days):
    total_customers = sum(customers)
    weighted_sum = sum(c * d for c, d in zip(customers, credit_days))
    weighted_average = weighted_sum / total_customers if total_customers != 0 else 0
    return total_customers, round(weighted_average, 2)

def show_credit_days_calculator():
    st.title("📅 Weighted Average Credit Days Calculator")

    st.write("Enter customer categories and their corresponding credit days.")

    num_categories = st.number_input("Number of customer categories", min_value=1, max_value=10, value=4)

    customers = []
    credit_days = []

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Customers")
        for i in range(num_categories):
            value = st.number_input(f"Category {i+1} - Number of Customers", key=f"cust_{i}", min_value=0)
            customers.append(value)

    with col2:
        st.markdown("### Credit Days")
        for i in range(num_categories):
            value = st.number_input(f"Category {i+1} - Credit Days", key=f"days_{i}", min_value=0)
            credit_days.append(value)

    if st.button("Calculate"):
        total_customers, weighted_avg = calculate_weighted_average(customers, credit_days)

        st.success(f"Total Customers: {total_customers}")
        st.success(f"Weighted Average Credit Days: {weighted_avg}")
