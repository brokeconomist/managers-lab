import streamlit as st

def show_home():
    # 1. ΚΑΛΩΣΟΡΙΣΜΑ
    st.title("🧪 Managers’ Lab")
    st.subheader("Decision Engineering for Small Business")
    st.markdown("""
    Welcome to the laboratory. Here, we don't just track history; we simulate the future. 
    **How would you like to begin?**
    """)
    st.divider()

    # 2. ΟΙ ΔΥΟ ΚΥΡΙΕΣ ΕΠΙΛΟΓΕΣ (START HERE)
    col1, col2 = st.columns(2)

    with col1:
        st.info("### 🧭 Structured Journey")
        st.write("A step-by-step 5-stage analysis to calibrate your business, fix cash leaks, and test sustainability.")
        if st.button("Start Path (Recommended)", use_container_width=True, type="primary"):
            st.session_state.mode = "path"
            st.session_state.flow_step = 0
            st.rerun()

    with col2:
        st.success("### 📚 Tool Library")
        st.write("Direct access to specific simulators. Perfect if you already have your numbers and want a quick answer.")
        if st.button("Browse Tools", use_container_width=True):
            st.session_state.mode = "library"
            st.rerun()

    st.divider()

    # 3. EXECUTIVE PREVIEW (Μόνο αν υπάρχουν δεδομένα)
    # Ελέγχουμε αν ο χρήστης έχει αλλάξει τα defaults (π.χ. αν ο τζίρος δεν είναι ο default)
    if st.session_state.price != 20.0 or st.session_state.volume != 1000:
        st.subheader("📊 Current Baseline Snapshot")
        
        # Υπολογισμοί (Σύντομη έκδοση του Dashboard)
        rev = st.session_state.price * st.session_state.volume
        unit_margin = st.session_state.price - st.session_state.variable_cost
        net_profit = (unit_margin * st.session_state.volume) - st.session_state.fixed_cost
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Revenue", f"{rev:,.0f} €")
        m2.metric("Net Profit", f"{net_profit:,.0f} €")
        m3.metric("Margin", f"{(unit_margin/st.session_state.price):.1%}")
        
        st.caption("Targeting: " + st.session_state.get('business_name', 'Current Project'))
    else:
        st.caption("💡 Tip: Use the 'Structured Journey' to input your business data and unlock the full Dashboard.")
