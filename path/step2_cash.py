import streamlit as st

def run_step():
    st.header("💰 Stage 2: Cash Conversion Cycle (CCC)")
    st.info("Measures the time (in days) it takes to convert investments in inventory into cash flows from sales.")

    # 1. SYNC WITH SHARED CORE
    q = st.session_state.get('volume', 1000)
    vc = st.session_state.get('variable_cost', 12.0)
    price = st.session_state.get('price', 20.0)
    annual_cogs = q * vc 
    days_in_year = 365

    st.write(f"**🔗 Global Baseline Linked:** Annual COGS: {annual_cogs:,.2f} €")

    st.divider()

    # 2. INPUTS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📦 Inventory")
        inv_days = st.number_input("Inventory Days", min_value=0, value=st.session_state.get('inventory_days', 60))
                
        # Νέος "Cold" υπολογισμός (περιλαμβάνει το Dead Stock):
        dead_stock_pct = st.slider("Dead Stock / Non-Moving (%)", 0, 50, 10)
        carrying_cost_pct = 0.20 # 20% ετήσιο κόστος αποθήκευσης/χρηματοδότησης

        effective_inventory_value = inventory_value * (1 + dead_stock_pct/100)
        liquidity_drain = effective_inventory_value * carrying_cost_pct
          
    with col2:
        st.subheader("💳 Receivables")
        ar_days = st.number_input("Accounts Receivable Days", min_value=0, value=st.session_state.get('ar_days', 45))
        ar_value = (ar_days / days_in_year) * (price * q)
        st.caption(f"Owed by Clients: {ar_value:,.2f} €")

    with col3:
        st.subheader("🤝 Payables")
        ap_days = st.number_input("Accounts Payable Days", min_value=0, value=st.session_state.get('payables_days', 30))
        ap_value = (ap_days / days_in_year) * annual_cogs
        st.caption(f"Owed to Suppliers: {ap_value:,.2f} €")

    # 3. CALCULATIONS
    ccc = inv_days + ar_days - ap_days
    working_capital_req = inventory_value + ar_value - ap_value

    st.divider()

    # 4. RESULTS
    res1, res2 = st.columns(2)
    
    with res1:
        color = "red" if ccc > 90 else "orange" if ccc > 60 else "green"
        st.metric("Cash Conversion Cycle", f"{ccc} Days", delta=f"{ccc} days delay", delta_color="inverse")
        st.markdown(f"Status: :{color}[{'High Risk' if ccc > 90 else 'Healthy' if ccc < 60 else 'Monitor'}]")

    with res2:
        st.metric("Liquidity Gap (€)", f"{working_capital_req:,.2f} €")
        # Auto-save state
        st.session_state.inventory_days = inv_days
        st.session_state.ar_days = ar_days
        st.session_state.payables_days = ap_days
        st.session_state.working_capital_req = working_capital_req

    

    st.divider()
    
    # 5. NAVIGATION
    nav_col1, nav_col2 = st.columns(2)
    
    with nav_col1:
        if st.button("⬅️ Back to Stage 1", use_container_width=True):
            st.session_state.flow_step = 1
            st.rerun()
            
    with nav_col2:
        if st.button("Proceed to Unit Economics (Stage 3) ➡️", use_container_width=True, type="primary"):
            st.session_state.flow_step = 3
            st.rerun()

    # Cold Insight
    st.info(f"**Cold Insight:** Every day you reduce the CCC, you 'release' approximately **{annual_cogs / days_in_year:,.2f} €** in cash.")
