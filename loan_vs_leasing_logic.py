import numpy_financial as npf


def pmt(rate, nper, pv, fv=0, when=0):
    return -npf.pmt(rate, nper, pv, fv, when)


def calculate_loan_vs_leasing_breakdown(
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
    months = 12
    n_months = duration_years * months

    # --- Acquisition cost ---
    acquisition_cost_loan = property_value + add_expenses_loan
    acquisition_cost_lease = property_value + add_expenses_leasing

    # --- Working capital ---
    wc_loan = property_value * (1 - loan_financing_percent) + add_expenses_loan
    wc_lease = property_value * (1 - leasing_financing_percent) + add_expenses_leasing

    # --- Monthly payments ---
    loan_installment = pmt(loan_rate / months, n_months, property_value * loan_financing_percent, 0, pay_when)
    lease_installment = pmt(loan_rate / months, n_months, property_value * leasing_financing_percent, 0, pay_when)

    wc_loan_installment = pmt(wc_rate / months, n_months, wc_loan, 0, pay_when)
    wc_lease_installment = pmt(wc_rate / months, n_months, wc_lease, 0, pay_when)

    # --- Total payments ---
    total_loan_payments = (loan_installment + wc_loan_installment) * n_months
    total_lease_payments = (lease_installment + wc_lease_installment) * n_months

    # --- Interest ---
    interest_loan = total_loan_payments - property_value
    interest_lease = total_lease_payments - property_value

    # --- Depreciation ---
    depreciation_loan = acquisition_cost_loan / depreciation_years * duration_years
    depreciation_lease = acquisition_cost_lease + residual_value_leasing

    # --- Tax deductible ---
    deductible_loan = interest_loan + depreciation_loan
    deductible_lease = (wc_lease_installment * n_months - wc_lease) + depreciation_lease

    tax_benefit_loan = deductible_loan * tax_rate
    tax_benefit_lease = deductible_lease * tax_rate

    # --- Final burden ---
    final_loan = property_value + interest_loan - tax_benefit_loan
    final_lease = property_value + interest_lease - tax_benefit_lease

    return {
        "loan": {
            "Total Payments": round(total_loan_payments),
            "Interest Cost": round(interest_loan),
            "Depreciation": round(depreciation_loan),
            "Tax Benefit": round(tax_benefit_loan),
            "Final Financial Burden": round(final_loan),
        },
        "leasing": {
            "Total Payments": round(total_lease_payments),
            "Interest & Financing Cost": round(interest_lease),
            "Depreciation + Residual": round(depreciation_lease),
            "Tax Benefit": round(tax_benefit_lease),
            "Final Financial Burden": round(final_lease),
        },
    }
