import streamlit as st

def run_step():
    st.header("⚙️ Stage 0 — Define Your Baseline")
    st.caption("Establish the economic foundation of your simulation.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Structure")
        # Ενημερώνουμε απευθείας το session_state
        st.session_state.price = st.number_input(
            "Price per Unit (€)", 
            min_value=0.0, 
            value=float(st.session_state.price)
        )
        st.session_state.volume = st.number_input(
            "Annual Volume (Units)", 
            min_value=0, 
            value=int(st.session_state.volume)
        )
        
        revenue = st.session_state.price * st.session_state.volume
        st.metric("Annual Revenue", f"{revenue:,.0f} €")

    with col2:
        st.subheader("Cost Structure")
        st.session_state.variable_cost = st.number_input(
            "Variable Cost per Unit (€)", 
            min_value=0.0, 
            value=float(st.session_state.variable_cost)
        )
        st.session_state.fixed_cost = st.number_input(
            "Annual Fixed Costs (€)", 
            min_value=0.0, 
            value=float(st.session_state.fixed_cost)
        )

        # Υπολογισμός Margin για άμεσο feedback
        if st.session_state.price > st.session_state.variable_cost:
            margin = (st.session_state.price - st.session_state.variable_cost) / st.session_state.price
            st.metric("Contribution Margin", f"{margin:.1%}")
        else:
            st.error("Negative Margin detected.")

    st.divider()

    with st.expander("Cash Timing & Retention (Optional)"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.ar_days = st.number_input("Receivables Days", value=int(st.session_state.ar_days))
        with c2:
            st.session_state.inventory_days = st.number_input("Inventory Days", value=int(st.session_state.inventory_days))
        with c3:
            st.session_state.payables_days = st.number_input("Payables Days", value=int(st.session_state.payables_days))

        st.session_state.retention_rate = st.slider("Customer Retention Rate", 0.0, 1.0, float(st.session_state.retention_rate))

    st.divider()

    if st.button("Lock Baseline & View Dashboard", use_container_width=True):
        if st.session_state.price <= st.session_state.variable_cost:
            st.error("Baseline cannot be locked with zero or negative margin.")
        else:
            st.session_state.mode = "home"  # Επιστροφή στο Dashboard
            st.rerun()
