import streamlit as st

def show_home():
    # 1. HEADER & PHILOSOPHY
    st.title("🧪 Managers’ Lab")
    st.markdown("""
    **A decision laboratory for managers.** This is not a dashboard. It's a simulator to test what must be true for a decision to work — and what breaks when it doesn't.
    """)

    st.divider()

    # 2. SYSTEM HEALTH INDEX (The Cold Truth)
    # Χρησιμοποιούμε try/except για να αποφύγουμε σφάλματα αν το state δεν έχει φορτώσει
    try:
        # Υπολογισμοί από το Shared Core (system_state)
        revenue = st.session_state.price * st.session_state.volume
        margin = (st.session_state.price - st.session_state.variable_cost) / st.session_state.price
        ccc = st.session_state.ar_days + st.session_state.inventory_days - st.session_state.payables_days
        
        st.subheader("🏥 System Health Index")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            color = "green" if margin > 0.3 else "orange" if margin > 0.15 else "red"
            st.metric("Profitability (Gross)", f"{margin:.1%}")
            st.caption(f":{color}[Targeting {st.session_state.price}€ / unit]")

        with col2:
            color = "green" if ccc < 45 else "orange" if ccc < 90 else "red"
            st.metric("Liquidity Gap", f"{int(ccc)} Days")
            st.caption(f":{color}[Cash Conversion Cycle]")

        with col3:
            denominator = (st.session_state.price - st.session_state.variable_cost)
            breakeven = st.session_state.fixed_cost / denominator if denominator > 0 else 1
            safety_margin = (st.session_state.volume / breakeven) - 1
            color = "green" if safety_margin > 0.2 else "orange" if safety_margin > 0 else "red"
            st.metric("Survival Margin", f"{safety_margin:.1%}")
            st.caption(f":{color}[Distance from Break-even]")
            
    except Exception as e:
        st.error("System State not initialized. Please refresh the app.")

    st.divider()
    st.markdown("**Direct Access to Decision Modules:**")

    # 3. DECISION BUTTONS (Navigation)
    # Κάθε κουμπί αλλάζει το mode και κάνει rerun για να αλλάξει η σελίδα
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 📈 Pricing & Viability")
        if st.button("Break-Even Shift Analysis", use_container_width=True):
            st.session_state.mode = "library"
            st.session_state.selected_tool = "Break-Even Shift Analysis" # Για να το "πιάσει" η library
            st.rerun()
            
        if st.button("Loss Threshold Analysis", use_container_width=True):
            st.session_state.mode = "library"
            st.session_state.selected_tool = "Loss Threshold Analysis"
            st.rerun()

    with col_b:
        st.markdown("### 💰 Cash & Finance")
        if st.button("Cash Cycle Calculator", use_container_width=True):
            st.session_state.mode = "library"
            st.session_state.selected_tool = "Cash Cycle Calculator"
            st.rerun()
            
        if st.button("Credit Policy Analysis", use_container_width=True):
            st.session_state.mode = "library"
            st.session_state.selected_tool = "Credit Policy Analysis"
            st.rerun()

    st.markdown("### 📦 Operations")
    col_c, col_d = st.columns(2)
    with col_c:
        if st.button("Unit Cost Calculator", use_container_width=True):
            st.session_state.mode = "library"
            st.session_state.selected_tool = "Unit Cost Calculator"
            st.rerun()
    with col_d:
        if st.button("Inventory Turnover Analysis", use_container_width=True):
            st.session_state.mode = "library"
            st.session_state.selected_tool = "Inventory Turnover Analysis"
            st.rerun()

    st.divider()
    
    # 4. FOOTER
    st.caption("Managers' Lab v2.0 | Integrated Shared State System")
    st.markdown("✉️ Contact: manosv18@gmail.com")
