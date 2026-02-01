import streamlit as st

# =========================================
# LOGIC
# =========================================

def calculate_weighted_average(amounts, credit_days):
    total_amount = sum(amounts)

    if total_amount == 0:
        return 0, 0.0

    weighted_sum = sum(a * d for a, d in zip(amounts, credit_days))
    weighted_avg = weighted_sum / total_amount

    return total_amount, round(weighted_avg, 2)


# =========================================
# UI
# =========================================

def show_credit_days_calculator():
    st.title("📅 Weighted Average Credit Days")

    st.caption(
        "True average credit period weighted by **amount owed**, "
        "not by number of customers."
    )

    st.markdown("---")

    num_categories = st.number_input(
        "Number of customer categories",
        min_value=1,
        max_value=10,
        value=4
    )

    names = []
    customers = []
    amounts = []
    credit_days = []

    st.markdown("### 📥 Input data")

    h1, h2, h3, h4 = st.columns([2, 1, 2, 1])
    h1.write("**Category**")
    h2.write("**Customers**")
    h3.write("**Amount Owed (€)**")
    h4.write("**Credit Days**")

    for i in range(num_categories):
        c1, c2, c3, c4 = st.columns([2, 1, 2, 1])

        names.append(
            c1.text_input(
                "Category",
                value=f"Category {i+1}",
                label_visibility="hidden",
                key=f"name_{i}"
            )
        )

        customers.append(
            c2.number_input(
                "Customers",
                min_value=0,
                step=1,
                label_visibility="hidden",
                key=f"cust_{i}"
            )
        )

        amounts.append(
            c3.number_input(
                "Amount",
                min_value=0.0,
                step=1000.0,
                label_visibility="hidden",
                key=f"amt_{i}"
            )
        )

        credit_days.append(
            c4.number_input(
                "Days",
                min_value=0,
                step=1,
                label_visibility="hidden",
                key=f"days_{i}"
            )
        )

    st.markdown("---")

    if st.button("📊 Calculate", type="primary"):

        total_amount, weighted_avg = calculate_weighted_average(
            amounts, credit_days
        )

        if total_amount == 0:
            st.error("⚠️ Enter at least one amount.")
            return

        st.subheader("📈 Results")

        m1, m2 = st.columns(2)

        m1.metric(
            "Total Receivables",
            f"€{total_amount:,.0f}"
        )

        m2.metric(
            "Weighted Avg Credit Days",
            f"{weighted_avg} days"
        )

        st.markdown("### 📋 Detail table")

        for n, c, a, d in zip(names, customers, amounts, credit_days):
            if a > 0:
                st.write(
                    f"• **{n}** | Customers: {c} | Amount: €{a:,.0f} | "
                    f"Days: {d} | Contribution: €{a*d:,.0f}"
                )
