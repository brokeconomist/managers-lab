import streamlit as st

def run_step():
    st.header("⚙️ Stage 0: System Calibration")
    st.caption("Establish the core economic parameters of the enterprise.")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.price = st.number_input("Price per Unit (€)", min_value=0.0, value=float(st.session_state.price))
        st.session_state.volume = st.number_input("Annual Volume (Units)", min_value=0, value=int(st.session_state.volume))
    with col2:
        st.session_state.variable_cost = st.number_input("Variable Cost per Unit (€)", min_value=0.0, value=float(st.session_state.variable_cost))
        st.session_state.fixed_cost = st.number_input("Annual Fixed Costs (€)", min_value=0.0, value=float(st.session_state.fixed_cost))

    # Structural Warning Logic
    margin = (st.session_state.price - st.session_state.variable_cost) / st.session_state.price if st.session_state.price > 0 else 0
    if 0 < margin < 0.20:
        st.warning(f"⚠️ Low structural buffer detected ({margin:.1%}). The business model is highly sensitive to volume fluctuations.")
    elif margin <= 0:
        st.error("❌ Critical Error: Negative or Zero Margin. Value destruction in progress.")

    st.subheader("⏳ Cash Timing & Durability")
    c1, c2, c3 = st.columns(3)
    st.session_state.ar_days = c1.number_input("Receivables Days", value=int(st.session_state.ar_days))
    st.session_state.inventory_days = c2.number_input("Inventory Days", value=int(st.session_state.inventory_days))
    st.session_state.payables_days = c3.number_input("Payables Days", value=int(st.session_state.payables_days))

    st.divider()

    if st.button("Lock Baseline & Continue ➡️", use_container_width=True, type="primary"):
        if st.session_state.price > st.session_state.variable_cost:
            st.session_state.baseline_locked = True
            st.session_state.flow_step = 1 # Στέλνουμε τον χρήστη στο πρώτο βήμα της ανάλυσης
            st.session_state.mode = "path"
            st.rerun()
        else:
            st.error("Cannot lock baseline with invalid economic structure.")
