import streamlit as st

def run_cash_cycle_app():
    st.header("💸 Industrial Cash Conversion Cycle")
    
    # 1. SYNC WITH GLOBAL STATE
    annual_revenue = st.session_state.get('global_units', 1000) * st.session_state.get('global_price', 20.0)
    annual_cogs = st.session_state.get('global_units', 1000) * st.session_state.get('global_vc', 12.0)
    
    st.info(f"Global Reference: Annual COGS = {annual_cogs:,.2f} €")

    # 2. ΑΝΑΛΥΣΗ ΑΠΟΘΕΜΑΤΩΝ (Industrial Style)
    st.subheader("📦 Inventory Breakdown")
    col_inv1, col_inv2, col_inv3 = st.columns(3)
    
    with col_inv1:
        raw_materials = st.number_input("Raw Materials Value (€)", value=annual_cogs * 0.1) # Default 10% του COGS
    with col_inv2:
        wip = st.number_input("Work in Progress (WIP) (€)", value=annual_cogs * 0.05)   # Default 5% του COGS
    with col_inv3:
        finished_goods = st.number_input("Finished Goods (€)", value=annual_cogs * 0.15) # Default 15% του COGS
    
    total_inventory = raw_materials + wip + finished_goods
    st.write(f"**Total Inventory Value:** {total_inventory:,.2f} €")

    # 3. ΛΟΙΠΑ ΣΤΟΙΧΕΙΑ
    st.divider()
    col_fin1, col_fin2 = st.columns(2)
    with col_fin1:
        receivables = st.number_input("Accounts Receivable (€)", value=annual_revenue * 0.12) # ~45 μέρες πίστωση default
    with col_fin2:
        payables = st.number_input("Accounts Payable (€)", value=annual_cogs * 0.08)       # ~30 μέρες πίστωση default

    # 4. CALCULATIONS (365 Days Basis)
    days_in_year = 365
    
    dio = (total_inventory / annual_cogs) * days_in_year if annual_cogs > 0 else 0
    dso = (receivables / annual_revenue) * days_in_year if annual_revenue > 0 else 0
    dpo = (payables / annual_cogs) * days_in_year if annual_cogs > 0 else 0
    
    ccc = dio + dso - dpo

    # 5. ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ
    st.divider()
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Inventory Days", f"{dio:.1f} d")
    res2.metric("Receivables Days", f"{dso:.1f} d")
    res3.metric("Payables Days", f"{dpo:.1f} d")
    res4.metric("Total CCC", f"{ccc:.1f} d", delta=f"{ccc:.1f} gap", delta_color="inverse")

    # Οπτικοποίηση του Ταμειακού Κύκλου
    #
