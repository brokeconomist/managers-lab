import streamlit as st

def show_home():
    # --- PHASE A: SYSTEM NOT INITIALIZED (Entry Mode) ---
    if not st.session_state.get('baseline_locked', False):
        st.title("🧪 Managers’ Lab")
        st.subheader("System Status: Offline")
        st.markdown("---")
        
        st.info("""
        **Welcome to the Laboratory.** Before we can begin simulation and analysis, the system requires your structural baseline. 
        Define your price, volume, and cost structure to initialize the Control Center.
        """)
        
        # Μοναδικό Call to Action
        if st.button("Initialize System (Stage 0)", use_container_width=True, type="primary"):
            st.session_state.mode = "path"
            st.session_state.flow_step = 0
            st.rerun()
            
        st.divider()
        st.caption("Analytical focus: Efficiency, Stability, & Survival Margin.")

    # --- PHASE B: SYSTEM OPERATIONAL (Control Center Mode) ---
    else:
        st.title("🧪 Managers’ Lab — Control Center")
        st.caption(f"Status: Operational | Base Currency: {st.session_state.get('currency', '€')}")
        st.markdown("---")

        # 1. Financial Calculation Engine
        p, v = st.session_state.price, st.session_state.volume
        vc, fc = st.session_state.variable_cost, st.session_state.fixed_cost
        debt, rate = st.session_state.debt, st.session_state.interest_rate
        
        rev = p * v
        ebit = ((p - vc) * v) - fc
        interest_cost = debt * rate
        net_profit = ebit - interest_cost
        margin = (p - vc) / p if p > 0 else 0
        ccc = st.session_state.ar_days + st.session_state.inventory_days - st.session_state.payables_days

        # 2. Executive Dashboard (The "Snapshot")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Annual Revenue", f"{rev:,.0f} €")
        with col2:
            st.metric("Net Profit (Post-Interest)", f"{net_profit:,.0f} €", 
                      delta=f"EBIT: {ebit:,.0f} €", delta_color="normal")
        with col3:
            st.metric("Structural Margin", f"{margin:.1%}")

        # 3. Decision Logic Layer
        st.divider()
        st.subheader("🛠️ Strategy & Operations")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🧭 Start Structured Path (Analysis)", use_container_width=True, type="primary"):
                st.session_state.mode = "path"
                st.session_state.flow_step = 1
                st.rerun()
        with btn_col2:
            if st.button("📚 Open Tool Library (Direct Access)", use_container_width=True):
                st.session_state.mode = "library"
                st.rerun()

        # 4. System Re-calibration
        st.divider()
        with st.expander("⚙️ System Management"):
            if st.button("Reset Baseline & Re-calibrate", use_container_width=True):
                st.session_state.baseline_locked = False
                st.session_state.mode = "path"
                st.session_state.flow_step = 0
                st.rerun()
