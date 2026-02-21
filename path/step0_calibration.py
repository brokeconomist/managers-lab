import streamlit as st

def run_step():
    st.header("⚙️ Stage 0: System Calibration")
    st.caption("Define the structural economics of your business baseline.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Structure")
        st.session_state.price = st.number_input("Price per Unit (€)", min_value=0.0, value=float(st.session_state.price))
        st.session_state.volume = st.number_input("Annual Volume (Units)", min_value=0, value=int(st.session_state.volume))
        
        revenue = st.session_state.price * st.session_state.volume
        st.metric("Annual Revenue", f"{revenue:,.0f} €")

    with col2:
        st.subheader("Cost Structure")
        st.session_state.variable_cost = st.number_input("Variable Cost per Unit (€)", min_value=0.0, value=float(st.session_state.variable_cost))
        st.session_state.fixed_cost = st.number_input("Annual Fixed Costs (€)", min_value=0.0, value=float(st.session_state.fixed_cost))

        # Margin Calculation & Validation
        p = st.session_state.price
        vc = st.session_state.variable_cost
        margin = (p - vc) / p if p > 0 else 0

        if p <= 0:
            st.error("❌ Price must be greater than zero.")
        elif p <= vc:
            st.error(f"❌ Critical: Negative Margin ({margin:.1%}). Value destruction in progress.")
        elif margin < 0.20:
            st.warning(f"⚠️ Low structural buffer ({margin:.1%}). Highly sensitive model.")
        else:
            st.success(f"✅ Healthy Margin: {margin:.1%}")

    st.divider()

    with st.expander("Cash Timing & Durability"):
        c1, c2, c3 = st.columns(3)
        st.session_state.ar_days = c1.number_input("Receivables Days", value=int(st.session_state.ar_days))
        st.session_state.inventory_days = c2.number_input("Inventory Days", value=int(st.session_state.inventory_days))
        st.session_state.payables_days = c3.number_input("Payables Days", value=int(st.session_state.payables_days))

    st.divider()

    if st.button("Lock Baseline & Continue ➡️", use_container_width=True, type="primary"):
        if st.session_state.price > st.session_state.variable_cost:
            st.session_state.baseline_locked = True
            st.session_state.flow_step = 1
            st.session_state.mode = "path"
            st.rerun()
        else:
            st.error("Cannot lock: Non-viable economic structure.")
