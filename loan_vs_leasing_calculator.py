import streamlit as st
from loan_vs_leasing_logic import calculate_final_burden


def format_number_en(value, decimals=0):
    try:
        return f"{value:,.{decimals}f}"
    except Exception:
        return str(value)


def loan_vs_leasing_ui():
    st.header("📊 Loan vs Leasing Comparison")

    st.subheader("🔢 Input Parameters")
    col1, col2 = st.columns(2)

    with col1:
        loan_rate = st.number_input("Loan Interest Rate (%)", value=6.0) / 100
        wc_rate = st.number_input("Working Capital Interest Rate (%)", value=8.0) / 100
        duration_years = st.number_input("Duration (years)", min_value=1, value=15)
        pay_when_radio = st.radio(
            "Payment Timing",
            ["Beginning of Period", "End of Period"]
        )
        pay_when = 1 if pay_when_radio == "Beginning of Period" else 0
        tax_rate = st.number_input("Corporate Tax Rate (%)", value=35.0) / 100

    with col2:
        property_value = st.number_input("Property Market Value (€)", min_value=0.0, value=250_000.0)
        loan_financing = st.number_input("Loan Financing (%)", value=70.0) / 100
        leasing_financing = st.number_input("Leasing Financing (%)", value=100.0) / 100
        add_expenses_loan = st.number_input("Additional Acquisition Costs (Loan €)", value=35_000.0)
        add_expenses_leasing = st.number_input("Additional Acquisition Costs (Leasing €)", value=30_000.0)
        residual_value = st.number_input("Leasing Residual Value (€)", value=3_530.0)
        depreciation_years = st.number_input("Depreciation Period (years)", min_value=1, value=30)

    st.subheader("📉 Results")

    final_loan, final_leasing = calculate_final_burden(
        loan_rate,
        wc_rate,
        duration_years,
        property_value,
        loan_financing,
        leasing_financing,
        add_expenses_loan,
        add_expenses_leasing,
        residual_value,
        depreciation_years,
        tax_rate,
        pay_when
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "📉 Total Cost – Loan",
        f"€ {format_number_en(final_loan, 0)}"
    )
    col2.metric(
        "📉 Total Cost – Leasing",
        f"€ {format_number_en(final_leasing, 0)}"
    )

    st.write("---")
    st.markdown(
        "✅ **The option with the lower total cost is the financially preferable choice.**"
    )
