import streamlit as st
import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Calculation Engines
# -------------------------------

def pmt(rate, nper, pv, fv=0, when=0):
    return -npf.pmt(rate, nper, pv, fv, when)

def calculate_burden(rate, years, asset_val, funding_pct, add_costs, wc_rate, tax_rate, is_lease=False, residual=0, when=0):
    # Μετατροπή σε μήνες - Η βάση 365 ημερών επηρεάζει τον ετήσιο ανατοκισμό
    months = years * 12
    
    # 1. Κύρια Χρηματοδότηση (Loan ή Lease)
    principal_inst = pmt(rate / 12, months, asset_val * funding_pct, 0, when)
    
    # 2. Χρηματοδότηση Ιδίων Κεφαλαίων & Εξόδων (Working Capital Cost)
    # Χρησιμοποιούμε 365 για να βρούμε το ακριβές κόστος ευκαιρίας αν χρειαζόταν
    wc_amt = asset_val * (1 - funding_pct) + add_costs
    wc_inst = pmt(wc_rate / 12, months, wc_amt, 0, when)
    
    total_cash_out = (principal_inst + wc_inst) * months + (residual if is_lease else 0)
    interest_only = total_cash_out - asset_val - add_costs - (residual if is_lease else 0)
    
    # 3. Tax Shield (Interest + Depreciation)
    # Οι αποσβέσεις υπολογίζονται επί του (Value + Costs)
    tax_shield = (interest_only + (asset_val + add_costs)) * tax_rate
    
    return total_cash_out - tax_shield

# -------------------------------
# UI Logic
# -------------------------------

def show_loan_vs_leasing_analysis():
    st.header("📊 Loan vs Leasing & Sensitivity Analysis")
    st.caption("Analytical comparison using a 365-day year basis and tax shield optimization.")

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
        
        run = st.button("Execute Strategic Analysis")

    if run:
        # --- BASE CASE ---
        loan_burden = calculate_burden(loan_rate, years, asset_value, loan_pct, loan_exp, wc_rate, tax_rate)
        lease_burden = calculate_burden(lease_rate_base, years, asset_value, lease_pct, lease_exp, wc_rate, tax_rate, True, residual)

        st.subheader("🔍 Financial Burden Breakdown")
        c1, c2 = st.columns(2)
        c1.metric("Loan Net Burden", f"€ {loan_burden:,.0f}".replace(",", "."))
        c2.metric("Leasing Net Burden", f"€ {lease_burden:,.0f}".replace(",", "."))

        # --- SENSITIVITY ANALYSIS ---
        st.divider()
        st.subheader("📈 Lease Rate Sensitivity & Indifference Point")
        
        # Παράγουμε μια λίστα επιτοκίων γύρω από το επιλεγμένο lease rate
        test_rates = [lease_rate_base + (i/1000) for i in range(-40, 45, 5)] # -4% έως +4%
        test_burdens = [calculate_burden(r, years, asset_value, lease_pct, lease_exp, wc_rate, tax_rate, True, residual) for r in test_rates]
        
        # Εύρεση Indifference Point (Σημείο Ισορροπίας)
        indifference_rate = None
        for i in range(len(test_rates)-1):
            if (test_burdens[i] - loan_burden) * (test_burdens[i+1] - loan_burden) <= 0:
                r1, r2 = test_rates[i], test_rates[i+1]
                b1, b2 = test_burdens[i], test_burdens[i+1]
                indifference_rate = r1 + (loan_burden - b1) * (r2 - r1) / (b2 - b1)
                break

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot([r*100 for r in test_rates], test_burdens, label='Leasing Cost Curve', marker='s', color='#1f77b4', linewidth=2)
        ax.axhline(y=loan_burden, color='#d62728', linestyle='--', label=f'Loan Fixed Cost ({loan_rate*100:.1f}%)')
        
        if indifference_rate:
            ax.plot(indifference_rate*100, loan_burden, 'go', markersize=10, label='Indifference Point')
            ax.annotate(f'{indifference_rate*100:.2f}%', 
                        xy=(indifference_rate*100, loan_burden), 
                        xytext=(indifference_rate*100 + 0.5, loan_burden + 5000),
                        arrowprops=dict(facecolor='black', shrink=0.05))

        ax.set_title("Sensitivity: Net Burden vs. Leasing Rate", fontsize=12, fontweight='bold')
        ax.set_xlabel("Leasing Interest Rate (%)")
        ax.set_ylabel("Net Financial Burden (€)")
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.6)
        st.pyplot(fig)

        

        # --- STRATEGIC VERDICT ---
        st.divider()
        st.subheader("🧠 Tactical Verdict")
        
        if indifference_rate:
            st.write(f"**Indifference Point:** {indifference_rate*100:.2f}%")
            if lease_rate_base > indifference_rate:
                st.error(f"The current Leasing Rate is **above** the indifference point ({indifference_rate*100:.2f}%). Use the **Loan**.")
            else:
                st.success(f"The current Leasing Rate is **below** the indifference point ({indifference_rate*100:.2f}%). Use **Leasing**.")
        else:
            st.info("The financing structures are too different to intersect within this rate range.")

        # Detailed Data Table
        with st.expander("View Data Table"):
            df = pd.DataFrame({
                "Lease Rate (%)": [f"{r*100:.2f}%" for r in test_rates],
                "Lease Burden (€)": [f"{b:,.0f}" for b in test_burdens],
                "Loan Burden (€)": [f"{loan_burden:,.0f}" for _ in test_rates]
            })
            st.table(df)

if __name__ == "__main__":
    show_loan_vs_leasing_analysis()
