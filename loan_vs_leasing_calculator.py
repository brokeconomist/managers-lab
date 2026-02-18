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
    months = years * 12
    # Base financing
    inst = pmt(rate / 12, months, asset_val * funding_pct, 0, when)
    # WC financing for equity/costs
    wc_amt = asset_val * (1 - funding_pct) + add_costs
    wc_inst = pmt(wc_rate / 12, months, wc_amt, 0, when)
    
    total_cash = (inst + wc_inst) * months + (residual if is_lease else 0)
    interest = total_cash - asset_val - add_costs - (residual if is_lease else 0)
    
    # Tax Shield Logic
    # Simplified for comparison: Interest + Depreciation shield
    # In leasing, often more is deductible, but we'll use a standardized shield for the rate sensitivity
    tax_shield = (interest + (asset_val + add_costs)) * tax_rate
    return total_cash - tax_shield

# -------------------------------
# UI Logic
# -------------------------------

def loan_vs_leasing_ui():
    st.header("📊 Strategic Financing & Sensitivity Analysis")

    with st.sidebar:
        st.header("Core Parameters")
        asset_value = st.number_input("Property Value (€)", value=250000.0)
        years = st.number_input("Horizon (Years)", value=15)
        tax_rate = st.number_input("Tax Rate (%)", value=22.0) / 100
        wc_rate = st.number_input("WACC / Opp. Cost (%)", value=8.0) / 100
        
        st.divider()
        st.subheader("Loan Setup")
        loan_rate = st.number_input("Loan Rate (%)", value=6.0) / 100
        loan_pct = st.slider("Loan Funding %", 0, 100, 70) / 100
        loan_exp = st.number_input("Loan Costs (€)", value=35000.0)
        
        st.divider()
        st.subheader("Leasing Setup")
        lease_rate_base = st.number_input("Base Lease Rate (%)", value=6.0) / 100
        lease_pct = st.slider("Leasing Funding %", 0, 100, 100) / 100
        lease_exp = st.number_input("Lease Costs (€)", value=30000.0)
        residual = st.number_input("Residual (€)", value=3530.0)
        
        run = st.button("Run Full Analysis")

    if run:
        # 1. Base Case Calculation
        loan_burden = calculate_burden(loan_rate, years, asset_value, loan_pct, loan_exp, wc_rate, tax_rate)
        lease_burden = calculate_burden(lease_rate_base, years, asset_value, lease_pct, lease_exp, wc_rate, tax_rate, True, residual)

        st.subheader("📉 Financial Burden Comparison")
        c1, c2 = st.columns(2)
        c1.metric("Loan Net Burden", f"€ {loan_burden:,.0f}")
        c2.metric("Leasing Net Burden", f"€ {lease_burden:,.0f}")

        # 2. SENSITIVITY ANALYSIS
        st.divider()
        st.subheader("📈 Lease Rate Sensitivity")
        st.write("How changes in the Leasing Rate affect the decision compared to the fixed Loan Rate.")

        rates = [lease_rate_base + (i/1000) for i in range(-30, 35, 5)] # -3% to +3%
        burdens = [calculate_burden(r, years, asset_value, lease_pct, lease_exp, wc_rate, tax_rate, True, residual) for r in rates]
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot([r*100 for r in rates], burdens, label='Leasing Burden', marker='o', color='#1f77b4')
        ax.axhline(y=loan_burden, color='r', linestyle='--', label=f'Loan Fixed Burden ({loan_rate*100:.1f}%)')
        
        # Find Indifference Point
        # Simple linear interpolation or finding the closest value
        indifference_rate = None
        for i in range(len(rates)-1):
            if (burdens[i] - loan_burden) * (burdens[i+1] - loan_burden) <= 0:
                # Linear interpolation for more accuracy
                r1, r2 = rates[i], rates[i+1]
                b1, b2 = burdens[i], burdens[i+1]
                indifference_rate = r1 + (loan_burden - b1) * (r2 - r1) / (b2 - b1)
                break

        ax.set_xlabel("Leasing Interest Rate (%)")
        ax.set_ylabel("Net Financial Burden (€)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        

        # 3. STRATEGIC VERDICT
        st.divider()
        st.subheader("🧠 Tactical Verdict")
        if indifference_rate:
            st.success(f"**Indifference Point:** {indifference_rate*100:.2f}%")
            if lease_rate_base > indifference_rate:
                st.warning(f"The current Lease Rate ({lease_rate_base*100:.1f}%) is too high. It must drop below **{indifference_rate*100:.2f}%** to beat the Loan.")
            else:
                st.success(f"The current Lease Rate ({lease_rate_base*100:.1f}%) is efficient. You can afford it to rise up to **{indifference_rate*100:.2f}%** before the Loan becomes better.")
        else:
            st.info("The burden lines do not intersect within a +/- 3% range. One option is dominantly better.")

if __name__ == "__main__":
    loan_vs_leasing_ui()
