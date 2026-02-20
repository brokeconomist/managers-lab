import streamlit as st

def run_cash_cycle_app():
    st.header("💰 Cash Conversion Cycle (CCC)")
    st.info("Measures the time (in days) it takes to convert investments in inventory into cash flows from sales.")

    # 1. SYNC WITH SHARED CORE (365-day base)
    q = st.session_state.get('volume', 1000)
    vc = st.session_state.get('variable_cost', 12.0)
    annual_cogs = q * vc # Annual Cost of Goods Sold
    days_in_year = 365

    st.write(f"**Global Baseline:** Annual COGS: {annual_cogs:,.2f} € (Based on {q} units at {vc}€ VC)")

    st.divider()

    # 2. INPUTS ΓΙΑ ΤΟΝ ΚΥΚΛΟ
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Inventory")
        inv_days = st.number_input("Inventory Days", min_value=0, value=st.session_state.get('inventory_days', 60))
        inventory_value = (inv_days / days_in_year) * annual_cogs
        st.caption(f"Stock Value: {inventory_value:,.2f} €")

    with col2:
        st.subheader("Receivables")
        ar_days = st.number_input("Accounts Receivable Days", min_value=0, value=st.session_state.get('ar_days', 45))
        ar_value = (ar_days / days_in_year) * (st.session_state.get('price', 20.0) * q)
        st.caption(f"Owed by Clients: {ar_value:,.2f} €")

    with col3:
        st.subheader("Payables")
        ap_days = st.number_input("Accounts Payable Days", min_value=0, value=st.session_state.get('payables_days', 30))
        ap_value = (ap_days / days_in_year) * annual_cogs
        st.caption(f"Owed to Suppliers: {ap_value:,.2f} €")

    # 3. CALCULATIONS
    ccc = inv_days + ar_days - ap_days
    working_capital_req = inventory_value + ar_value - ap_value

    st.divider()

    # 4. RESULTS & SYNC
    res1, res2 = st.columns(2)
    
    with res1:
        color = "red" if ccc > 90 else "orange" if ccc > 60 else "green"
        st.metric("Cash Conversion Cycle", f"{ccc} Days", delta=f"{ccc} days delay", delta_color="inverse")
        st.markdown(f"Status: :{color}[{'High Risk' if ccc > 90 else 'Healthy' if ccc < 60 else 'Monitor'}]")

    with res2:
        st.metric("Liquidity Gap (€)", f"{working_capital_req:,.2f} €")
        if st.button("🔄 Sync Days to Core", use_container_width=True):
            st.session_state.inventory_days = inv_days
            st.session_state.ar_days = ar_days
            st.session_state.payables_days = ap_days
            st.success("Global Cash Pressure updated!")
            st.rerun()

    st.divider()
    st.markdown(f"""
    **Cold Insight:** Every day you reduce the CCC, you 'release' approximately **{annual_cogs / days_in_year:,.2f} €** in cash that was previously locked in operations.
    """)
