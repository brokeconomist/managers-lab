import streamlit as st

def show_home():
    # 1. HEADER & INTRO
    st.title("🧪 Managers’ Lab")
    st.markdown("""
    A decision laboratory for managers. Not a dashboard. Not a reporting tool.  
    **Managers’ Lab tests what must be true for a decision to work.**
    """)

    st.divider()

    # 2. SYSTEM HEALTH INDEX (The "Cold Truth" Layer)
    # Υπολογισμοί από το Shared State
    try:
        revenue = st.session_state.price * st.session_state.volume
        margin = (st.session_state.price - st.session_state.variable_cost) / st.session_state.price
        ccc = st.session_state.ar_days + st.session_state.inventory_days - st.session_state.payables_days
        
        st.subheader("🏥 System Health Index")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            color = "green" if margin > 0.3 else "orange" if margin > 0.15 else "red"
            st.metric("Profitability (Gross)", f"{margin:.1%}", delta_color="normal")
            st.caption(f":{color}[Status based on {st.session_state.price}€ price]")

        with col2:
            color = "green" if ccc < 45 else "orange" if ccc < 90 else "red"
            st.metric("Liquidity Gap", f"{int(ccc)} Days", delta_color="inverse")
            st.caption(f":{color}[Cash Conversion Cycle]")

        with col3:
            breakeven = st.session_state.fixed_cost / (st.session_state.price - st.session_state.variable_cost) if (st.session_state.price - st.session_state.variable_cost) > 0 else 1
            safety_margin = (st.session_state.volume / breakeven) - 1
            color = "green" if safety_margin > 0.2 else "orange" if safety_margin > 0 else "red"
            st.metric("Survival Margin", f"{safety_margin:.1%}")
            st.caption(f":{color}[Distance from Break-even]")
            
    except Exception as e:
        st.warning("Initialize system state to see Health Index.")

    st.divider()
    st.markdown("**Choose the type of decision you are trying to make.**")

    # 3. DECISION GROUPS (Buttons)
    # Χρησιμοποιούμε columns για να είναι φιλικό σε tablet
    
    st.subheader("📈 Pricing & Viability")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Break-Even Shift Analysis", use_container_width=True):
            st.info("Navigate to Library -> Pricing & Break-Even")
    with c2:
        if st.button("Loss Threshold Analysis", use_container_width=True):
            st.info("Navigate to Library -> Pricing & Break-Even")

    st.subheader("💰 Cash Flow & Finance")
    c3, c4 = st.columns(2)
    with c3:
        if st.button("Cash Cycle Calculator", use_container_width=True):
            st.info("Navigate to Library -> Finance & Cash Flow")
    with c4:
        if st.button("Credit Policy Analysis", use_container_width=True):
            st.info("Navigate to Library -> Finance & Cash Flow")

    st.subheader("📦 Operations & Costs")
    c5, c6 = st.columns(2)
    with c5:
        if st.button("Unit Cost Calculator", use_container_width=True):
            st.info("Navigate to Library -> Operations")
    with c6:
        if st.button("Inventory Turnover", use_container_width=True):
            st.info("Navigate to Library -> Operations")

    st.divider()

    # 4. FOOTER
    st.markdown("""
    **How to use the Lab** Focus on **tolerance**, not forecasts. Small changes in the Shared Core (Price, Volume, Costs) compound structurally across all tools.
    
    **Contact** ✉️ manosv18@gmail.com
    """)
