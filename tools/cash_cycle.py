import streamlit as st

def run_cash_cycle_app():
    st.header("💸 Cash Conversion Cycle (CCC)")
    st.caption("Stage 2: Analyzing liquidity pressure using global sales data.")

    # 1. SYNC WITH GLOBAL STATE
    if "global_units" not in st.session_state: st.session_state.global_units = 1000
    if "global_price" not in st.session_state: st.session_state.global_price = 20.0
    if "global_vc" not in st.session_state: st.session_state.global_vc = 12.0

    # Υπολογισμός Ετήσιου Κύκλου Εργασιών και COGS για προτάσεις
    annual_revenue = st.session_state.global_units * st.session_state.global_price
    annual_cogs = st.session_state.global_units * st.session_state.global_vc

    st.info(f"Connected to Global Model: Annual Revenue ~{annual_revenue:,.0f}€ | COGS ~{annual_cogs:,.0f}€")

    # 2. INPUTS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Balance Sheet Figures")
        inventory = st.number_input("Average Inventory Value (€)", value=annual_cogs/6 if annual_cogs > 0 else 1000.0)
        receivables = st.number_input("Accounts Receivable (€)", value=annual_revenue/10 if annual_revenue > 0 else 1000.0)
        payables = st.number_input("Accounts Payable (€)", value=annual_cogs/12 if annual_cogs > 0 else 500.0)

    with col2:
        st.subheader("Annual Basis (Global)")
        # Χρησιμοποιούμε 365 ημέρες βάσει της οδηγίας σου
        days_in_year = 365 
        st.write(f"Calculation Basis: **{days_in_year} Days**")
        rev_for_calc = st.number_input("Annual Revenue for CCC (€)", value=float(annual_revenue))
        cogs_for_calc = st.number_input("Annual COGS for CCC (€)", value=float(annual_cogs))

    # 3. CALCULATIONS (Efficiency Ratios)
    dio = (inventory / cogs_for_calc) * days_in_year if cogs_for_calc > 0 else 0
    dso = (receivables / rev_for_calc) * days_in_year if rev_for_calc > 0 else 0
    dpo = (payables / cogs_for_calc) * days_in_year if cogs_for_calc > 0 else 0
    
    ccc = dio + dso - dpo

    # 4. DISPLAY RESULTS
    st.divider()
    res1, res2, res3, res4 = st.columns(4)
    
    res1.metric("Inventory Days (DIO)", f"{dio:.1f} d")
    res2.metric("Receivables Days (DSO)", f"{dso:.1f} d")
    res3.metric("Payables Days (DPO)", f"{dpo:.1f} d")
    res4.metric("Cash Cycle (CCC)", f"{ccc:.1f} d", delta=f"{ccc:.1f} days of gap", delta_color="inverse")

    # 5. STRATEGIC INSIGHT
    st.subheader("🧠 Analytical Interpretation")
    if ccc > 90:
        st.error(f"High Fragility: You are financing your operations for {ccc:.0f} days. This requires heavy working capital.")
    elif ccc > 45:
        st.warning("Standard Cycle: Efficiency improvements in inventory or collections could release significant cash.")
    else:
        st.success("Lean Cycle: Your business model is highly efficient in converting resources to cash.")

    # Αποθήκευση του CCC στο state για χρήση στο Sustainability Stage
    st.session_state.global_ccc = ccc
