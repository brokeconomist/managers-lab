import streamlit as st
import numpy_financial as npf

# ===== Financial Functions =====
def pmt(rate, nper, pv, fv=0, when=0):
    """Compute payment for a loan/lease (monthly)"""
    return -npf.pmt(rate, nper, pv, fv, when)

def calculate_final_burden(
    loan_rate,
    wc_rate,
    duration_years,
    property_value,
    loan_financing_percent,
    leasing_financing_percent,
    add_expenses_loan,
    add_expenses_leasing,
    residual_value_leasing,
    depreciation_years,
    tax_rate,
    pay_when
):
    """Calculate total financial burden for loan vs leasing."""
    months = 12
    n_months = duration_years * months

    # Acquisition cost
    acquisition_cost_loan = property_value + add_expenses_loan
    acquisition_cost_lease = property_value + add_expenses_leasing

    # Working capital loans
    wc_loan = property_value - (property_value * loan_financing_percent) + add_expenses_loan
    wc_lease = property_value - (property_value * leasing_financing_percent) + add_expenses_leasing

    # Monthly payments
    monthly_loan = pmt(loan_rate / months, n_months, property_value * loan_financing_percent, 0, pay_when)
    monthly_lease = pmt(loan_rate / months, n_months, property_value * leasing_financing_percent, 0, pay_when)
    monthly_wc_loan = pmt(wc_rate / months, n_months, wc_loan, 0, pay_when)
    monthly_wc_lease = pmt(wc_rate / months, n_months, wc_lease, 0, pay_when)

    # Total monthly outflow
    total_monthly_loan = monthly_loan + monthly_wc_loan
    total_monthly_lease = monthly_lease + monthly_wc_lease

    # Total interest
    total_interest_loan = (total_monthly_loan * n_months) - property_value
    total_interest_lease = (total_monthly_lease * n_months) - property_value

    # Total cost over duration
    total_cost_loan = total_interest_loan + property_value
    total_cost_lease = total_interest_lease + property_value

    # Depreciation
    depreciation_loan = acquisition_cost_loan / depreciation_years * duration_years
    depreciation_lease = (acquisition_cost_lease / duration_years * duration_years) + residual_value_leasing

    # Deductible expenses
    deductible_loan = total_interest_loan + depreciation_loan
    deductible_lease = (monthly_wc_lease * n_months - wc_lease) + depreciation_lease

    # Tax benefits
    tax_benefit_loan = deductible_loan * tax_rate
    tax_benefit_lease = deductible_lease * tax_rate

    # Final financial burden
    final_loan = total_cost_loan - tax_benefit_loan
    final_lease = total_cost_lease - tax_benefit_lease

    return round(final_loan), round(final_lease)

# ===== Streamlit UI =====
def loan_vs_leasing_ui():
    st.title("🏦 Loan vs Leasing Analysis")
    st.caption(
        "Compare the **total financial burden** of acquiring an asset via loan or leasing, "
        "taking into account interest, working capital, depreciation, and tax benefits."
    )

    with st.form("loan_vs_leasing_form"):
        st.header("🔢 Input Data")

        col1, col2 = st.columns(2)

        with col1:
            property_value = st.number_input("🏠 Asset Value (€)", min_value=0.0, value=1_000_000.0, step=10_000.0)
            st.caption("Purchase price of the asset (e.g., machinery, vehicle, equipment).")

            loan_financing_percent = st.number_input("💰 Loan Financing (%)", min_value=0.0, max_value=100.0, value=70.0)
            st.caption("Percentage of asset financed via bank loan.")

            leasing_financing_percent = st.number_input("💸 Leasing Financing (%)", min_value=0.0, max_value=100.0, value=100.0)
            st.caption("Percentage of asset financed via leasing.")

            duration_years = st.number_input("⏳ Duration (years)", min_value=1, value=5)
            st.caption("Contract duration in years.")

            pay_when = st.selectbox("📅 Payment Timing", options=["End of Period", "Beginning of Period"])
            st.caption("Choose if loan/lease payments are made at the end or beginning of each period.")
            pay_when_val = 0 if pay_when == "End of Period" else 1

        with col2:
            loan_rate = st.number_input("🏦 Loan Interest Rate (%)", min_value=0.0, value=6.0)
            st.caption("Annual interest rate on the bank loan.")

            wc_rate = st.number_input("💳 Working Capital Rate (%)", min_value=0.0, value=10.0)
            st.caption("Cost of financing required working capital.")

            add_expenses_loan = st.number_input("🧾 Additional Loan Expenses (€)", min_value=0.0, value=10_000.0)
            st.caption("Upfront fees or administrative costs for the loan.")

            add_expenses_leasing = st.number_input("🧾 Additional Leasing Expenses (€)", min_value=0.0, value=5_000.0)
            st.caption("Upfront fees or administrative costs for the lease.")

            residual_value_leasing = st.number_input("🔄 Residual Value (Leasing, €)", min_value=0.0, value=100_000.0)
            st.caption("Estimated value of the asset at the end of the leasing period.")

            depreciation_years = st.number_input("📉 Depreciation Period (years)", min_value=1, value=10)
            st.caption("Number of years to depreciate the asset for tax purposes.")

            tax_rate = st.number_input("🏦 Tax Rate (%)", min_value=0.0, value=24.0) / 100
            st.caption("Corporate income tax rate used for tax benefit calculation.")

        submitted = st.form_submit_button("🔍 Calculate")

    if submitted:
        final_loan, final_lease = calculate_final_burden(
            loan_rate / 100,
            wc_rate / 100,
            duration_years,
            property_value,
            loan_financing_percent / 100,
            leasing_financing_percent / 100,
            add_expenses_loan,
            add_expenses_leasing,
            residual_value_leasing,
            depreciation_years,
            tax_rate,
            pay_when_val
        )

        st.markdown("---")
        st.subheader("📊 Results")

        col1, col2 = st.columns(2)
        col1.metric("🏦 Total Burden with Loan", f"€ {final_loan:,}")
        col2.metric("💸 Total Burden with Leasing", f"€ {final_lease:,}")

        st.caption(
            "The tool shows the **overall financial cost** of acquiring an asset via loan or leasing, "
            "including interest, working capital, depreciation, and tax benefits. "
            "Use this to decide the most cost-efficient financing option."
        )
