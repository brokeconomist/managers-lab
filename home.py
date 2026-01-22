import streamlit as st
from navigation import navigate_to

def show_home():

    st.title("🧪 Managers’ Lab")

    st.markdown("""
    An interactive environment for financial decision testing.

    This is a decision laboratory.
    """)

    st.divider()

    # -------- Strategy & Pricing --------
    st.subheader("Pricing & Viability")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Break-Even Shift Analysis"):
            navigate_to("📈 Break-Even & Pricing", "Break-Even Shift Analysis")
    with col2:
        if st.button("Loss Threshold Before Price Cut"):
            navigate_to("📈 Break-Even & Pricing", "Loss Threshold Before Price Cut")

    # -------- Customer Economics --------
    st.subheader("Customer Economics")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("CLV Analysis"):
            navigate_to("👥 Customer Value", "CLV Analysis")
    with col2:
        if st.button("Substitution Analysis"):
            navigate_to("👥 Customer Value", "Substitution Analysis")

    col3, _ = st.columns(2)
    with col3:
        if st.button("Complementary Product Analysis"):
            navigate_to("👥 Customer Value", "Complementary Product Analysis")

    # -------- Finance & Cash Flow --------
    st.subheader("Finance & Cash Flow")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cash Cycle Calculator"):
            navigate_to("💰 Finance & Cash Flow", "Cash Cycle Calculator")
    with col2:
        if st.button("Credit Policy Analysis"):
            navigate_to("💰 Finance & Cash Flow", "Credit Policy Analysis")

    # -------- Cost Structure --------
    st.subheader("Cost Structure")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Unit Cost Calculator"):
            navigate_to("📊 Cost & Profit", "Unit Cost Calculator")
    with col2:
        if st.button("Discount NPV Analysis"):
            navigate_to("📊 Cost & Profit", "Discount NPV Analysis")

    # -------- Operations --------
    st.subheader("Operations & Working Capital")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Inventory Turnover Analysis"):
            navigate_to("📦 Inventory & Operations", "Inventory Turnover Analysis")
    with col2:
        if st.button("Credit Days Calculator"):
            navigate_to("📦 Inventory & Operations", "Credit Days Calculator")

    st.divider()

    st.markdown("""
    **Contact**  
    ✉️ brokeconomist@gmail.com
    """)
