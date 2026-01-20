import streamlit as st
import numpy_financial as npf


def pmt(rate, nper, pv, fv=0, when=0):
    return -npf.pmt(rate, nper, pv, fv, when)


def format_eur(x):
    return f"€ {x:,.0f}"


def loan_vs_leasing_ui():
    st.header("📊 Loan vs Leasing – Analytical Comparison")
    st.caption(
        "This tool compares **Loan vs Leasing** based on **total cash outflows, "
        "tax shields, and depreciation effects**, in order to identify the option "
        "with the **lower final financial burden**."
    )

    st.subheader("🔢 Input Parameters")
    col1, col2 = st.columns(2)

    with col1:
        loan_rate = st.number_input("Loan Interest Rate (%)", value=6.0) / 100
        st.caption("Nominal annual interest rate of the loan or leasing contract.")

        wc_rate = st.number_input("Working Capital Interest Rate (%)", value=8.0) / 100
        st.caption("Cost of financing the equity portion and additional expenses.")

        years = st.number_input("Duration (years)", value=15)
        st.caption("Total financing horizon.")

        tax_rate = st.number_input("Corporate Tax Rate (%)", value=35.0) / 100
        st.caption("Applied tax rate used to calculate tax shields.")

        timing = st.radio("Payment Timing", ["End of Period", "Beginning of Period"])
        st.caption("Defines whether installments are paid at the start or end of each period.")
        when = 1 if timing == "Beginning of Period" else 0

    with col2:
        value = st.number_input("Property Value (€)", value=250_000.0)
        st.caption("Market value of the asset being financed.")

        loan_pct = st.number_input("Loan Financing (%)", value=70.0) / 100
        st.caption("Percentage of the asset value financed through a loan.")

        lease_pct = st.number_input("Leasing Financing (%)", value=100.0) / 100
        st.caption("Percentage of the asset value financed through leasing.")

        exp_loan = st.number_input("Additional Acquisition Costs – Loan (€)", value=35_000.0)
        st.caption("Legal, notary, fees and other costs capitalized under loan financing.")

        exp_lease = st.number_input("Additional Acquisition Costs – Leasing (€)", value=30_000.0)
        st.caption("Upfront costs associated with the leasing option.")

        residual = st.number_input("Residual Value (Leasing €)", value=3_530.0)
        st.caption("Residual value payable at the end of the leasing period.")

        dep_years = st.number_input("Depreciation Period (years)", value=30)
        st.caption("Accounting depreciation period of the asset.")

    # ---------------- CALCULATIONS ----------------
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

    # ---------------- RESULTS ----------------
    st.markdown("---")
    st.subheader("📉 Analytical Breakdown")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 🏦 Loan")
        st.write("**Total Cash Outflows:**", format_eur(loan_cash))
        st.caption("Sum of loan installments and working capital financing.")

        st.write("**Interest Cost:**", format_eur(loan_interest))
        st.caption("Total financing cost over the entire period.")

        st.write("**Depreciation:**", format_eur(loan_depr))
        st.caption("Tax-deductible depreciation of the asset.")

        st.write("**Tax Shield:**", format_eur(loan_tax))
        st.caption("Tax savings from interest and depreciation.")

        st.metric("Final Financial Burden", format_eur(loan_final))

    with c2:
        st.markdown("### 🧾 Leasing")
        st.write("**Total Cash Outflows:**", format_eur(lease_cash))
        st.caption("Total leasing and working capital payments.")

        st.write("**Financing Cost:**", format_eur(lease_interest))
        st.caption("Implicit financing cost embedded in leasing.")

        st.write("**Depreciation + Residual:**", format_eur(lease_depr))
        st.caption("Depreciation of leasing acquisition plus residual value.")

        st.write("**Tax Shield:**", format_eur(lease_tax))
        st.caption("Tax benefit from deductible leasing-related costs.")

        st.metric("Final Financial Burden", format_eur(lease_final))

    st.markdown("---")
    if loan_final < lease_final:
        st.success("✅ **Loan financing results in a lower total financial burden.**")
    else:
        st.success("✅ **Leasing results in a lower total financial burden.**")
