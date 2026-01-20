import streamlit as st
import numpy_financial as npf


def pmt(rate, nper, pv, fv=0, when=0):
    return -npf.pmt(rate, nper, pv, fv, when)


def format_eur(x):
    return f"€ {x:,.0f}"


def loan_vs_leasing_ui():
    st.header("📊 Loan vs Leasing – Analytical Breakdown")

    st.info(
        "This view explicitly breaks down cash flows, tax benefits and depreciation. "
        "If you can read this sentence, the correct file is loaded."
    )

    col1, col2 = st.columns(2)

    with col1:
        loan_rate = st.number_input("Loan Interest Rate (%)", value=6.0) / 100
        wc_rate = st.number_input("Working Capital Rate (%)", value=8.0) / 100
        years = st.number_input("Duration (years)", value=15)
        tax_rate = st.number_input("Corporate Tax Rate (%)", value=35.0) / 100
        timing = st.radio("Payment Timing", ["End of Period", "Beginning of Period"])
        when = 1 if timing == "Beginning of Period" else 0

    with col2:
        value = st.number_input("Property Value (€)", value=250_000.0)
        loan_pct = st.number_input("Loan Financing (%)", value=70.0) / 100
        lease_pct = st.number_input("Leasing Financing (%)", value=100.0) / 100
        exp_loan = st.number_input("Extra Costs – Loan (€)", value=35_000.0)
        exp_lease = st.number_input("Extra Costs – Leasing (€)", value=30_000.0)
        residual = st.number_input("Residual Value (€)", value=3_530.0)
        dep_years = st.number_input("Depreciation Years", value=30)

    months = years * 12

    # --- LOAN ---
    loan_inst = pmt(loan_rate / 12, months, value * loan_pct, 0, when)
    wc_loan = value * (1 - loan_pct) + exp_loan
    wc_inst = pmt(wc_rate / 12, months, wc_loan, 0, when)

    loan_cash = (loan_inst + wc_inst) * months
    loan_interest = loan_cash - value
    loan_depr = (value + exp_loan) / dep_years * years
    loan_tax = (loan_interest + loan_depr) * tax_rate
    loan_final = value + loan_interest - loan_tax

    # --- LEASING ---
    lease_inst = pmt(loan_rate / 12, months, value * lease_pct, 0, when)
    wc_lease = value * (1 - lease_pct) + exp_lease
    wc_lease_inst = pmt(wc_rate / 12, months, wc_lease, 0, when)

    lease_cash = (lease_inst + wc_lease_inst) * months
    lease_interest = lease_cash - value
    lease_depr = value + exp_lease + residual
    lease_tax = ((wc_lease_inst * months - wc_lease) + lease_depr) * tax_rate
    lease_final = value + lease_interest - lease_tax

    st.subheader("📉 Breakdown")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 🏦 Loan")
        st.write("Cash Outflows:", format_eur(loan_cash))
        st.write("Interest Cost:", format_eur(loan_interest))
        st.write("Depreciation:", format_eur(loan_depr))
        st.write("Tax Benefit:", format_eur(loan_tax))
        st.metric("Final Burden", format_eur(loan_final))

    with c2:
        st.markdown("### 🧾 Leasing")
        st.write("Cash Outflows:", format_eur(lease_cash))
        st.write("Financing Cost:", format_eur(lease_interest))
        st.write("Depreciation + Residual:", format_eur(lease_depr))
        st.write("Tax Benefit:", format_eur(lease_tax))
        st.metric("Final Burden", format_eur(lease_final))
