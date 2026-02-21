import streamlit as st

def show_home():
    st.title("🧪 Managers’ Lab — Control Center")
    
    if not st.session_state.get('baseline_locked', False):
        st.warning("⚠️ System Offline: No baseline defined.")
        st.write("The operating system requires structural data to begin simulation.")
        if st.button("Initialize System (Stage 0)", use_container_width=True, type="primary"):
            st.session_state.mode = "path"
            st.session_state.flow_step = 0
            st.rerun()
    else:
        # --- Financial Calculation Engine ---
        p, v = st.session_state.price, st.session_state.volume
        vc, fc = st.session_state.variable_cost, st.session_state.fixed_cost
        debt, rate = st.session_state.debt, st.session_state.interest_rate
        
        rev = p * v
        ebit = ((p - vc) * v) - fc
        interest_cost = debt * rate
        net_profit = ebit - interest_cost
        margin = (p - vc) / p if p > 0 else 0
        
        st.subheader("📊 System Status")
        c1, c2, c3 = st.columns(3)
        c1.metric("Annual Revenue", f"{rev:,.0f} €")
        # EBIT vs Net Profit distinction
        c2.metric("Net Profit (Post-Interest)", f"{net_profit:,.0f} €", 
                  delta=f"EBIT: {ebit:,.0f} €", delta_color="normal")
        c3.metric("Structural Margin", f"{margin:.1%}")

        st.divider()
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🧭 Analysis Mode (5-Stage Path)", use_container_width=True):
                st.session_state.mode = "path"
                st.session_state.flow_step = 1 
                st.rerun()
        with col_b:
            if st.button("📚 Advanced Tool Library", use_container_width=True):
                st.session_state.mode = "library"
                st.rerun()
        
        if st.button("🔄 Re-calibrate Baseline", use_container_width=True):
            st.session_state.baseline_locked = False
            st.session_state.mode = "path"
            st.session_state.flow_step = 0
            st.rerun()
