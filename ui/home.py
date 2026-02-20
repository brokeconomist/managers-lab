import streamlit as st

def show_home():
    # 1. HEADER
    st.title("🧪 Managers’ Lab")
    st.markdown("---")

    # 2. SYSTEM HEALTH INDEX (The "Core" Analytics)
    # Χρησιμοποιούμε try/except για να μην σπάσει αν λείπει κάτι από το state
    try:
        revenue = st.session_state.get('price', 0) * st.session_state.get('volume', 0)
        margin = (st.session_state.get('price', 0) - st.session_state.get('variable_cost', 0)) / st.session_state.get('price', 1)
        ccc = st.session_state.get('ar_days', 0) + st.session_state.get('inventory_days', 0) - st.session_state.get('payables_days', 0)

        st.subheader("🏥 Business Health Snapshot")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            m_color = "green" if margin > 0.3 else "orange" if margin > 0.15 else "red"
            st.metric("Gross Margin", f"{margin:.1%}")
            st.markdown(f"Status: :{m_color}[Analysis Base]")
            
        with c2:
            c_color = "green" if ccc < 45 else "orange" if ccc < 90 else "red"
            st.metric("Cash Gap", f"{int(ccc)} Days")
            st.markdown(f"Status: :{c_color}[Liquidity]")

        with c3:
            # Υπολογισμός Survival Margin
            denominator = (st.session_state.price - st.session_state.variable_cost)
            be_units = st.session_state.fixed_cost / denominator if denominator > 0 else 1
            safety = (st.session_state.volume / be_units) - 1
            s_color = "green" if safety > 0.2 else "orange" if safety > 0 else "red"
            st.metric("Survival Margin", f"{safety:.1%}")
            st.markdown(f"Status: :{s_color}[Safety]")

    except Exception:
        st.warning("⚠️ Core system values are being initialized...")

    st.divider()

    # 3. DECISION SHORTCUTS
    st.subheader("🕹️ Decision Tools")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("⚖️ Analyze Break-Even & Pricing", use_container_width=True):
            st.session_state.mode = "library" # Σε στέλνει στη βιβλιοθήκη
            st.rerun()
            
    with col_b:
        if st.button("💸 Analyze Cash Flow & CCC", use_container_width=True):
            st.session_state.mode = "library"
            st.rerun()

    col_c, col_d = st.columns(2)
    with col_c:
        if st.button("📦 Analyze Unit Costs", use_container_width=True):
            st.session_state.mode = "library"
            st.rerun()
            
    with col_d:
        if st.button("🧭 Strategy Analysis (QSPM)", use_container_width=True):
            st.session_state.mode = "library"
            st.rerun()

    st.divider()
    st.caption("Managers’ Lab v2.0 | Integrated Shared Core Architecture")
