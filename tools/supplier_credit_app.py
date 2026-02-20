import streamlit as st

def show_supplier_credit_analysis():
    st.header("🤝 Supplier Credit Analysis")
    st.info("Analyze how supplier payment terms affect your working capital and cash position.")

    # 1. SYNC WITH SHARED CORE
    # Χρειαζόμαστε το ετήσιο κόστος αγορών (Annual COGS)
    q = st.session_state.get('volume', 1000)
    vc = st.session_state.get('variable_cost', 12.0)
    annual_cogs = q * vc
    current_ap_days = st.session_state.get('payables_days', 30)
    
    st.write(f"**Current Baseline:** Annual Purchases (COGS): {annual_cogs:,.2f} € | Current Terms: {current_ap_days} days")

    st.divider()

    # 2. SCENARIO INPUTS
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current Terms")
        st.write(f"Days: {current_ap_days}")
        current_ap_value = (current_ap_days / 365) * annual_cogs
        st.metric("Financing from Suppliers", f"{current_ap_value:,.2f} €")

    with col2:
        st.subheader("Target Terms")
        new_ap_days = st.slider("New Payment Terms (Days)", 0, 180, 45)
        new_ap_value = (new_ap_days / 365) * annual_cogs
        st.metric("New Financing Value", f"{new_ap_value:,.2f} €")

    # 3. IMPACT ANALYSIS
    cash_benefit = new_ap_value - current_ap_value
    
    st.divider()
    
    # 4. RESULTS
    res1, res2 = st.columns(2)
    
    with res1:
        if cash_benefit > 0:
            st.success(f"**Cash Inflow:** +{cash_benefit:,.2f} €")
            st.caption("This amount is effectively an interest-free loan from suppliers.")
        else:
            st.error(f"**Cash Outflow:** {abs(cash_benefit):,.2f} €")
            st.caption("Shortening payment terms will drain your cash bank.")

    with res2:
        # Cost of Money saved (Interest avoided)
        interest_rate = 0.08 
        savings = cash_benefit * interest_rate
        st.metric("Annual Interest Saved", f"{max(0.0, savings):,.2f} €")

    # 5. STRATEGIC INSIGHT (The Cold Truth)
    st.subheader("🔍 Strategic Verdict")
    if cash_benefit > 0:
        st.markdown(f"""
        **Negotiation Goal:** By moving to {new_ap_days} days, you release **{cash_benefit:,.2f} €** into your bank account. This can be used to offset the credit you give to customers or to 
        improve your **Cash Fragility Index**.
        """)
    
    st.info("⚠️ Warning: Be careful not to lose 'Early Payment Discounts'. If a supplier offers 2% discount for payment in 10 days, it is usually better to pay early than to keep the cash.")

    if st.button("🔄 Update Global AP Days"):
        st.session_state.payables_days = new_ap_days
        st.success("Global AP Days updated!")
        st.rerun()
