import streamlit as st

def format_currency(value, decimals=2):
    try:
        # Αγγλικοί δεκαδικοί με κόμμα χιλιάδων
        formatted = f"{value:,.{decimals}f}"
        return f"€ {formatted}"
    except Exception:
        return f"€ {value}"

def show_credit_policy_analysis():
    st.title("🕵️‍♂️ Credit Policy Analysis")

    with st.form("credit_policy_form"):
        st.subheader("📌 Current Policy")
        current_cash = st.number_input("Cash Sales % (current)", min_value=0.0, max_value=100.0, value=50.0) / 100
        current_credit_pct = st.number_input("Credit Sales % (current)", min_value=0.0, max_value=100.0, value=50.0) / 100
        current_credit_days = st.number_input("Credit Days (current)", min_value=0, value=60)

        st.subheader("📌 Proposed Policy")
        new_cash = st.number_input("Cash Sales % (new)", min_value=0.0, max_value=100.0, value=20.0) / 100
        new_credit_pct = st.number_input("Credit Sales % (new)", min_value=0.0, max_value=100.0, value=80.0) / 100
        new_credit_days = st.number_input("Credit Days (new)", min_value=0, value=90)

        st.subheader("📈 Sales Data")
        sales_increase = st.number_input("Expected Sales Increase (%)", min_value=0.0, value=20.0) / 100
        current_sales = st.number_input("Current Sales (€)", min_value=0.0, value=20_000_000.0)
        unit_price = st.number_input("Unit Price (€)", min_value=0.01, value=20.0)
        total_unit_cost = st.number_input("Total Unit Cost (€)", min_value=0.01, value=18.0)
        variable_unit_cost = st.number_input("Variable Unit Cost (€)", min_value=0.01, value=14.0)
        expected_bad_debts = st.number_input("Expected Bad Debts (%)", min_value=0.0, max_value=100.0, value=2.0) / 100
        interest_rate = st.number_input("Capital Cost (% per year)", min_value=0.0, max_value=100.0, value=10.0) / 100

        submitted = st.form_submit_button("Calculate")

    if submitted:
        # Units and profit from increase
        base_units = current_sales / unit_price
        increased_units = base_units * sales_increase
        profit_increase = increased_units * (unit_price - variable_unit_cost)

        # Capital cost (adjusted formula)
        avg_cost_per_unit = (
            ((base_units * total_unit_cost) + (increased_units * variable_unit_cost)) /
            (base_units + increased_units)
        )
        new_credit_sales = (current_sales * (1 + new_cash)) * new_credit_pct
        current_credit_sales = current_sales * current_cash

        capital_cost_new = (new_credit_sales / (360 / new_credit_days)) * (avg_cost_per_unit / unit_price)
        capital_cost_current = (current_credit_sales / (360 / current_credit_days)) * (total_unit_cost / unit_price)
        capital_cost_difference = capital_cost_new - capital_cost_current
        financial_cost = capital_cost_difference * interest_rate

        # Bad debts
        bad_debts_cost = current_sales * expected_bad_debts + current_sales * expected_bad_debts * sales_increase

        # Total cost
        total_cost = financial_cost + bad_debts_cost

        # Final evaluation
        anticipated_gain = profit_increase - total_cost
        suggestion = "✅ Increase Credit" if anticipated_gain > 0 else "❌ Do Not Increase Credit"

        # Results
        st.subheader("📊 Results")
        st.metric("Net Profit from Additional Sales", format_currency(profit_increase))
        st.metric("Total Cost of Increase", format_currency(total_cost))
        st.metric("Net Gain", format_currency(anticipated_gain))
        st.success(f"Recommendation: {suggestion}")


