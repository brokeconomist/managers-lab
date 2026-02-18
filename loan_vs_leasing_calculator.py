import streamlit as st
import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Calculation Engines
# -------------------------------

def pmt(rate, nper, pv, fv=0, when=0):
    # Standard Excel-compatible PMT function
    return -npf.pmt(rate, nper, pv, fv, when)

def calculate_burden(rate, years, asset_val, funding_pct, add_costs, wc_rate, tax_rate, is_lease=False, residual=0, when=0):
    # Μηνιαία βάση υπολογισμού (Standard Banking Logic)
    months = int(years * 12)
    monthly_rate = rate / 12
    monthly_wc_rate = wc_rate / 12
    
    # 1. Κύρια Δόση (Δάνειο ή Leasing)
    principal_inst = pmt(monthly_rate, months, asset_val * funding_pct, 0, when)
    
    # 2. Δόση για Ίδια Κεφάλαια & Έξοδα (Opportunity Cost)
    wc_amt = asset_val * (1 - funding_pct) + add_costs
    wc_inst = pmt(monthly_wc_rate, months, wc_amt, 0, when)
    
    # Συνολικές Εκροές (Cash Out)
    total_cash_out = (principal_inst + wc_inst) * months + (residual if is_lease else 0)
    
    # Τόκοι (Συνολική Εκροή μείον το Αρχικό Κεφάλαιο και τα Έξοδα)
    # Στο Leasing περιλαμβάνεται και το residual στην αξία που "αγοράζεις" στο τέλος
    interest_only = total_cash_out - asset_val - add_costs - (residual if is_lease else 0)
    
    # 3. Tax Shield (Interest + Depreciation)
    # Η απόσβεση υπολογίζεται στην αρχική αξία + έξοδα
    tax_shield = (interest_only + (asset_val + add_costs)) * tax_rate
    
    return total_cash_out - tax_shield, principal_inst + wc_inst, total_cash_out

# -------------------------------
# UI Logic
# -------------------------------

def loan_vs_leasing_ui():
    st.header("📊 Loan vs Leasing & Sensitivity Analysis")
    st.caption("Standard Monthly Amortization (Excel-Compatible Logic)")

    with st.sidebar:
        st.header("🔢 Global Variables")
        asset_value = st.number_input("Property Value (€)", value=250000.0, step=1000.0)
        years = st.number_input("Duration (Years)", value=15, min_value=1)
        tax_rate = st.number_input("Tax Rate (%)", value=22.0) / 100
        wc_rate = st.number_input("WACC / Opp. Cost (%)", value=8.0) / 100
        
        st.divider()
        st.subheader("🏦 Loan Parameters")
        loan_rate = st.number_input("Loan Rate (%)", value=6.0) / 100
        loan_pct = st.slider("Loan Funding (%)", 0, 100, 70) / 100
        loan_exp = st.number_input("Loan Costs (€)", value=35000.0)
        
        st.divider()
        st.subheader("🧾 Leasing Parameters")
        lease_rate_base = st.number_input("Lease Rate (%)", value=6.0) / 100
        lease_pct = st.slider("Lease Funding (%)", 0, 100, 100) / 100
        lease_exp = st.number_input("Lease Costs (€)", value=30000.0)
        residual = st.number_input("Residual Value (€)", value=3530.0)
        
        timing = st.radio("Payment Timing", ["End of Month", "Start of Month"])
        when = 1 if timing == "Start of Month" else 0
        
        run = st.button("Calculate Decision")

    if run:
        # --- BASE CASE ---
        loan_burden, loan_monthly, loan_cash = calculate_burden(loan_rate, years, asset_value, loan_pct, loan_exp, wc_rate, tax_rate, False, 0, when)
        lease_burden, lease_monthly, lease_cash = calculate_burden(lease_rate_base, years, asset_value, lease_pct, lease_exp, wc_rate, tax_rate, True, residual, when)

        st.subheader("🔍 Financial Summary")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Loan Net Burden", f"€ {loan_burden:,.0f}".replace(",", "."))
            st.write(f"Monthly Installment: **€ {loan_monthly:,.2f}**")
        with c2:
            st.metric("Leasing Net Burden", f"€ {lease_burden:,.0f}".replace(",", "."))
            st.write(f"Monthly Installment: **€ {lease_monthly:,.2f}**")

        # --- SENSITIVITY ANALYSIS ---
        st.divider()
        st.subheader("📈 Lease Rate Sensitivity & Indifference Point")
        
        test_rates = [lease_rate_base + (i/1000) for i in range(-40, 45, 5)] 
        test_burdens = [calculate_burden(r, years, asset_value, lease_pct, lease_exp, wc_rate, tax_rate, True, residual, when)[0] for r in test_rates]
        
        indifference_rate = None
        for i in range(len(test_rates)-1):
            if (test_burdens[i] - loan_burden) * (test_burdens[i+1] - loan_burden) <= 0:
                r1, r2 = test_rates[i], test_rates[i+1]
                b1, b2 = test_burdens[i], test_burdens[i+1]
                indifference_rate = r1 + (loan_burden - b1) * (r2 - r1) / (b2 - b1)
                break

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot([r*100 for r in test_rates], test_burdens, label='Leasing Cost Curve', marker='s', color='#1f77b4')
        ax.axhline(y=loan_burden, color='#d62728', linestyle='--', label=f'Loan Fixed Cost')
        
        if indifference_rate:
            ax.plot(indifference_rate*100, loan_burden, 'go', markersize=10, label=f'Equilibrium @ {indifference_rate*100:.2f}%')

        ax.set_xlabel("Leasing Interest Rate (%)")
        ax.set_ylabel("Net Financial Burden (€)")
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)
        st.pyplot(fig)

        # --- VERDICT ---
        st.divider()
        if indifference_rate:
            if lease_rate_base > indifference_rate:
                st.error(f"❌ **USE LOAN:** The lease rate must be below **{indifference_rate*100:.2f}%** to be competitive.")
            else:
                st.success(f"✅ **USE LEASING:** Your rate is efficient. It can rise up to **{indifference_rate*100:.2f}%** before losing its advantage.")

if __name__ == "__main__":
    loan_vs_leasing_ui()
