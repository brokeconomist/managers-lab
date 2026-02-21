import streamlit as st

def show_home():
    # PHASE A: Entry Mode
    if not st.session_state.get('baseline_locked', False):
        st.title("🧪 Managers’ Lab")
        st.subheader("System Status: Offline")
        st.divider()
        st.info("The operating system requires a structural baseline to begin simulation.")
        if st.button("Initialize System (Stage 0)", use_container_width=True, type="primary"):
            st.session_state.mode = "path"
            st.session_state.flow_step = 0
            st.rerun()

    # PHASE B: Control Center Mode
    else:
        st.title("🧪 Managers’ Lab — Control Center")
        st.markdown("---")

        # Calculations
        p, v = st.session_state.price, st.session_state.volume
        vc, fc = st.session_state.variable_cost, st.session_state.fixed_cost
        debt, rate = st.session_state.debt, st.session_state.interest_rate
        
        rev = p * v
        ebit = ((p - vc) * v) - fc
        net_profit = ebit - (debt * rate)
        margin = (p - vc) / p if p > 0 else 0

        # KPI Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Annual Revenue", f"{rev:,.0f} €")
        c2.metric("Net Profit (Post-Interest)", f"{net_profit:,.0f} €", delta=f"EBIT: {ebit:,.0f} €")
        c3.metric("Structural Margin", f"{margin:.1%}")

        st.divider()
        
        # Navigation
        st.subheader("🛠️ Operations")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🧭 Start Analysis Path", use_container_width=True, type="primary"):
                st.session_state.mode = "path"
                st.session_state.flow_step = 1
                st.rerun()
        with col_b:
            if st.button("📚 Browse Tool Library", use_container_width=True):
                st.session_state.mode = "library"
                st.rerun()

        st.divider()
        with st.expander("⚙️ System Management"):
            if st.button("Reset & Re-calibrate Baseline", use_container_width=True):
                st.session_state.baseline_locked = False
                st.session_state.mode = "path"
                st.session_state.flow_step = 0
                st.rerun()
