import streamlit as st

def show_home():
    st.title("🧪 Managers’ Lab — Executive Dashboard")
    st.markdown("---")

    # 1. Υπολογισμοί από το Shared Core
    p = st.session_state.price
    v = st.session_state.volume
    vc = st.session_state.variable_cost
    fc = st.session_state.fixed_cost
    
    revenue = p * v
    unit_margin = p - vc
    total_margin = unit_margin * v
    net_profit = total_margin - fc
    
    # Break-even & Safety (Cold Analysis)
    be_point = fc / unit_margin if unit_margin > 0 else 0
    safety_margin = (v - be_point) / v if v > 0 else 0
    daily_burn = fc / 365 # Σταθερά 365 ημέρες βάσει οδηγιών

    # 2. Executive Metrics
    st.subheader("🏥 System Health Index")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Net Profit (EBIT)", f"{net_profit:,.0f} €", 
                  delta=f"{(net_profit/revenue*100) if revenue > 0 else 0:.1f}% Margin")
    
    with col2:
        # Cash Cycle calculation
        ccc = st.session_state.ar_days + st.session_state.inventory_days - st.session_state.payables_days
        st.metric("Cash Conversion Cycle", f"{int(ccc)} Days")
        
    with col3:
        color = "normal" if safety_margin > 0.2 else "inverse"
        st.metric("Survival Buffer", f"{safety_margin:.1%}", delta="Safety Margin", delta_color=color)

    st.divider()

    # 3. Decision Alerts (Cold Insights)
    st.subheader("⚠️ Critical Insights")
    c1, c2 = st.columns(2)
    
    with c1:
        if net_profit < 0:
            st.error(f"**Structural Risk:** Your fixed costs of **{daily_burn:,.2f} €/day** are not covered. Immediate intervention in pricing or cost structure is required.")
        elif safety_margin < 0.15:
            st.warning("**High Sensitivity:** Your business is fragile. A 15% drop in volume will eliminate all profits.")
        else:
            st.success("**Operational Strength:** Your current structure provides a solid cushion against market volatility.")

    with c2:
        if ccc > 90:
            st.error("**Liquidity Warning:** Your capital is trapped for too long. Focus on 'Receivables' or 'Inventory' optimization.")
        else:
            st.info("**Flow Efficiency:** Your cash cycle is healthy, minimizing the need for external working capital financing.")

    st.divider()
    
    # 4. Navigation
    st.markdown("### 🛠️ Action Center")
    n1, n2 = st.columns(2)
    with n1:
        if st.button("🔄 Re-calibrate Baseline (Stage 0)", use_container_width=True):
            st.session_state.mode = "path"
            st.session_state.flow_step = 0
            st.rerun()
    with n2:
        if st.button("📚 Access Tool Library", use_container_width=True):
            st.session_state.mode = "library"
            st.rerun()
