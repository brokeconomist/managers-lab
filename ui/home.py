import streamlit as st


import streamlit as st

def show_home():
    st.title("🚀 Managers' Lab: Global Strategy")
    st.markdown("---")

    # Υπολογισμοί για το Health Index
    revenue = st.session_state.price * st.session_state.volume
    margin = (st.session_state.price - st.session_state.variable_cost) / st.session_state.price
    ccc = st.session_state.ar_days + st.session_state.inventory_days - st.session_state.payables_days

    st.subheader("🏥 System Health Index")
    
    col1, col2, col3 = st.columns(3)
    
    # Φανάρι 1: Profitability
    with col1:
        color = "green" if margin > 0.3 else "orange" if margin > 0.15 else "red"
        st.markdown(f"**Profitability:** :{color}[{margin:.1%}]")
        st.caption("Gross Margin Health")

    # Φανάρι 2: Liquidity
    with col2:
        color = "green" if ccc < 45 else "orange" if ccc < 90 else "red"
        st.markdown(f"**Liquidity Gap:** :{color}[{ccc} Days]")
        st.caption("Cash Conversion Cycle")

    # Φανάρι 3: Volume Efficiency
    with col3:
        breakeven = st.session_state.fixed_cost / (st.session_state.price - st.session_state.variable_cost)
        safety_margin = (st.session_state.volume / breakeven) - 1
        color = "green" if safety_margin > 0.2 else "orange" if safety_margin > 0 else "red"
        st.markdown(f"**Survival Margin:** :{color}[{safety_margin:.1%}]")
        st.caption("Distance from Break-even")

    st.markdown("---")
    st.info("💡 Tip: Go to 'Break-Even Analysis' to update the global core data.")

def show_home():

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------
    st.title("🧪 Managers’ Lab")

    st.markdown("""
A decision laboratory for managers.  
Not a dashboard. Not a reporting or forecasting tool.  

Managers’ Lab tests what must be true for a decision to work —  
and what breaks when it doesn’t.  

The tools are already built. Judgment is yours.
    """)

    st.divider()
    st.markdown("**Choose the type of decision you are trying to make.**")

    # -------------------------------------------------
    # DECISION GROUPS
    # -------------------------------------------------

    st.subheader("Pricing & Viability")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Break-Even Shift Analysis"):
            st.session_state.selected_category = "📈 Break-Even & Pricing"
            st.session_state.selected_tool = "Break-Even Shift Analysis"
    with col2:
        if st.button("Loss Threshold Before Price Cut"):
            st.session_state.selected_category = "📈 Break-Even & Pricing"
            st.session_state.selected_tool = "Loss Threshold Before Price Cut"

    st.subheader("Customer Economics")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("CLV Analysis"):
            st.session_state.selected_category = "👥 Customer Value"
            st.session_state.selected_tool = "CLV Analysis"
    with col2:
        if st.button("Substitution Analysis"):
            st.session_state.selected_category = "👥 Customer Value"
            st.session_state.selected_tool = "Substitution Analysis"
    with col3:
        if st.button("Complementary Product Analysis"):
            st.session_state.selected_category = "👥 Customer Value"
            st.session_state.selected_tool = "Complementary Product Analysis"

    st.subheader("Cash Flow & Financing")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Cash Cycle Calculator"):
            st.session_state.selected_category = "💰 Finance & Cash Flow"
            st.session_state.selected_tool = "Cash Cycle Calculator"
    with col2:
        if st.button("Credit Policy Analysis"):
            st.session_state.selected_category = "💰 Finance & Cash Flow"
            st.session_state.selected_tool = "Credit Policy Analysis"
    with col3:
        if st.button("Supplier Payment Analysis"):
            st.session_state.selected_category = "💰 Finance & Cash Flow"
            st.session_state.selected_tool = "Supplier Payment Analysis"

    st.subheader("Cost Structure & Profitability")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Unit Cost Calculator"):
            st.session_state.selected_category = "📊 Cost & Profit"
            st.session_state.selected_tool = "Unit Cost Calculator"
    with col2:
        if st.button("Discount NPV Analysis"):
            st.session_state.selected_category = "📊 Cost & Profit"
            st.session_state.selected_tool = "Discount NPV Analysis"

    st.subheader("Inventory & Operations")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Inventory Turnover Analysis"):
            st.session_state.selected_category = "📦 Inventory & Operations"
            st.session_state.selected_tool = "Inventory Turnover Analysis"
    with col2:
        if st.button("Credit Days Calculator"):
            st.session_state.selected_category = "📦 Inventory & Operations"
            st.session_state.selected_tool = "Credit Days Calculator"

    st.subheader("Strategy & Decision")
    if st.button("QSPM – Strategy Comparison"):
        st.session_state.selected_category = "🧭 Strategy & Decision"
        st.session_state.selected_tool = "QSPM – Strategy Comparison"

    st.divider()

    # -------------------------------------------------
    # COFFEE BUTTON (optional support)
    # -------------------------------------------------
    #col1, col2, col3 = st.columns([1, 2, 1])
    #with col2:
        #st.markdown(
            #"<div style='text-align: center;'>"
            #"<a href='https://buymeacoffee.com/USERNAME' target='_blank'>"
            #"☕ Buy me a coffee"
            #"</a>"
            #"</div>",
            #unsafe_allow_html=True
        #)
        #st.caption("For those who find value here.")

    #st.divider()

    # -------------------------------------------------
    # HOW TO USE (micro-polished)
    # -------------------------------------------------
    st.markdown("""
**How to use the Lab**  
Open a tool from the sidebar or main menu once the decision frame is clear. Focus on tolerance, not forecasts — small changes compound structurally.
    """)

    st.divider()

    # -------------------------------------------------
    # CONTACT
    # -------------------------------------------------
    st.markdown("""
**Contact**  
For feedback, questions, or collaboration:  
✉️ manosv18@gmail.com
    """)

