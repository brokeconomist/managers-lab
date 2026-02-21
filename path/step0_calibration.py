import streamlit as st

def run_step():
    st.header("⚙️ Stage 0: System Calibration")
    st.caption("Define the structural economics of your business baseline.")

    # Χρήση στηλών για καθαρό UI
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Revenue Engine")
        st.session_state.price = st.number_input(
            "Price per Unit (€)", 
            min_value=0.0, 
            value=float(st.session_state.get('price', 20.0)),
            help="The average selling price of your core product/service."
        )
        st.session_state.volume = st.number_input(
            "Annual Volume (Units)", 
            min_value=0, 
            value=int(st.session_state.get('volume', 1000)),
            help="Total units sold per year (365 days)."
        )
        
        revenue = st.session_state.price * st.session_state.volume
        st.metric("Total Annual Revenue", f"{revenue:,.0f} €")

    with col2:
        st.subheader("📉 Cost Structure")
        st.session_state.variable_cost = st.number_input(
            "Variable Cost per Unit (€)", 
            min_value=0.0, 
            value=float(st.session_state.get('variable_cost', 12.0))
        )
        st.session_state.fixed_cost = st.number_input(
            "Annual Fixed Costs (€)", 
            min_value=0.0, 
            value=float(st.session_state.get('fixed_cost', 5000.0)),
            help="Rent, salaries, and other costs that don't change with sales volume."
        )

        # Quick Math Check
        denom = st.session_state.price - st.session_state.variable_cost
        if denom > 0:
            margin = denom / st.session_state.price
            st.metric("Contribution Margin (%)", f"{margin:.1%}")
        else:
            st.error("Negative Margin: Your cost per unit exceeds your price.")

    st.divider()
    
    # Cash Timing Section
    with st.expander("⏳ Cash Timing & Retention (Recommended)"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.ar_days = st.number_input("Receivables Days", value=int(st.session_state.get('ar_days', 45)))
        with c2:
            st.session_state.inventory_days = st.number_input("Inventory Days", value=int(st.session_state.get('inventory_days', 60)))
        with c3:
            st.session_state.payables_days = st.number_input("Payables Days", value=int(st.session_state.get('payables_days', 30)))
        
        st.session_state.retention_rate = st.slider("Customer Retention Rate", 0.0, 1.0, float(st.session_state.get('retention_rate', 0.85)))

    st.divider()

    # VALIDATION & LOCK
    if st.button("🚀 Lock Baseline & See Dashboard", use_container_width=True):
        if st.session_state.price <= st.session_state.variable_cost:
            st.error("Cannot proceed with negative or zero margin. Adjust Price or Variable Costs.")
        else:
            # Μετάβαση στο Home για να δει τα αποτελέσματα
            st.session_state.mode = "home"
            st.success("Baseline Locked. Redirecting to Dashboard...")
            st.rerun()
