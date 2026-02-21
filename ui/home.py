import streamlit as st

def show_home():
    st.title("🧪 Managers' Lab: Executive Insights")
    st.markdown("---")

    # 1. FETCH & CALCULATE
    p = st.session_state.price
    q = st.session_state.volume
    vc = st.session_state.variable_cost
    fc = st.session_state.fixed_cost
    
    rev = p * q
    gross_profit = (p - vc) * q
    net_profit = gross_profit - fc
    margin_pct = (p - vc) / p if p > 0 else 0
    
    # Safety & Burn Rate
    be_units = fc / (p - vc) if (p - vc) > 0 else 0
    safety_margin = (q - be_units) / q if q > 0 else 0
    daily_burn = fc / 365 # Σύμφωνα με τις οδηγίες σου για 365 ημέρες

    # 2. THE DASHBOARD GRID
    st.subheader("🏥 Enterprise Health Status")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Annual Revenue", f"{rev:,.0f} €")
    with m2:
        st.metric("Net Profit (EBIT)", f"{net_profit:,.0f} €", 
                  delta=f"{(net_profit/rev*100) if rev > 0 else 0:.1f}% Net Margin")
    with m3:
        color = "normal" if safety_margin > 0.2 else "inverse"
        st.metric("Survival Buffer", f"{safety_margin:.1%}", delta="Safety Margin", delta_color=color)
    with m4:
        ccc = st.session_state.ar_days + st.session_state.inventory_days - st.session_state.payables_days
        st.metric("Cash Conversion", f"{int(ccc)} Days")

    st.divider()

    # 3. COLD ANALYSIS ALERTS
    st.subheader("⚠️ Strategic Warnings")
    c1, c2 = st.columns(2)
    
    with c1:
        if net_profit < 0:
            st.error(f"**Action Required:** You are burning **{daily_burn:,.2f} € per day** in fixed costs without coverage. Your business model is currently value-destructive.")
        elif safety_margin < 0.15:
            st.warning(f"**Fragility Alert:** A drop of more than {safety_margin:.1%} in volume will push the business into losses.")
        else:
            st.success("**Stability Confirmed:** Your current volume comfortably covers fixed costs and generates surplus.")

    with c2:
        if ccc > 90:
            st.error("**Cash Trap:** Your Cash Conversion Cycle is too long. You are risking a liquidity crunch despite accounting profits.")
        else:
            st.info("**Flow Efficiency:** Your collection and payment cycles are optimized for stability.")

    # 4. QUICK NAVIGATION BUTTONS
    st.divider()
    st.markdown("### 🛠️ Decision Modules")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📊 Re-calibrate Baseline (Stage 0)", use_container_width=True):
            st.session_state.mode = "path"
            st.session_state.flow_step = 0
            st.rerun()
    with col_b:
        if st.button("📚 Open Tool Library", use_container_width=True):
            st.session_state.mode = "library"
            st.rerun()
