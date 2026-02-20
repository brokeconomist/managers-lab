import streamlit as st

def show_credit_policy_analysis():
    st.header("💳 Credit Policy Analysis")
    st.info("Analyze the financial impact of changing your payment terms for customers.")

    # 1. SYNC WITH SHARED CORE
    # Χρειαζόμαστε τον ετήσιο τζίρο (Revenue)
    p = st.session_state.get('price', 20.0)
    q = st.session_state.get('volume', 1000)
    annual_revenue = p * q
    current_ar_days = st.session_state.get('ar_days', 45)
    
    st.write(f"**Current Baseline:** Annual Revenue: {annual_revenue:,.2f} € | Current Terms: {current_ar_days} days")

    st.divider()

    # 2. SCENARIO INPUTS
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current Policy")
        st.write(f"Days: {current_ar_days}")
        current_ar_value = (current_ar_days / 365) * annual_revenue
        st.metric("Capital Locked", f"{current_ar_value:,.2f} €")

    with col2:
        st.subheader("Proposed Policy")
        new_ar_days = st.slider("New Credit Terms (Days)", 0, 180, 60)
        new_ar_value = (new_ar_days / 365) * annual_revenue
        st.metric("New Capital Locked", f"{new_ar_value:,.2f} €")

    # 3. IMPACT ANALYSIS
    capital_impact = new_ar_value - current_ar_value
    
    st.divider()
    
    # 4. RESULTS
    res1, res2 = st.columns(2)
    
    with res1:
        if capital_impact > 0:
            st.error(f"**Liquidity Drain:** +{capital_impact:,.2f} €")
            st.caption("You need this extra cash to fund the new policy.")
        else:
            st.success(f"**Liquidity Release:** {abs(capital_impact):,.2f} €")
            st.caption("Cash returned to your bank account.")

    with res2:
        # Υπολογισμός ευκαιρίας (Interest Cost)
        interest_rate = 0.08 # Default 8% bank rate
        opportunity_cost = capital_impact * interest_rate
        st.metric("Annual Financing Cost", f"{opportunity_cost:,.2f} €")

    # 5. STRATEGIC INSIGHT
    st.subheader("🔍 Strategic Verdict")
    if capital_impact > 0:
        st.warning(f"""
        To extend credit by {new_ar_days - current_ar_days} days, you must ensure you have 
        **{capital_impact:,.2f} €** in available liquidity. 
        If your 'Cash Fragility' is high, this move could be dangerous.
        """)
    else:
        st.success(f"Shortening credit terms by {current_ar_days - new_ar_days} days improves your survival runway immediately.")

    if st.button("🔄 Update Global Credit Days"):
        st.session_state.ar_days = new_ar_days
        st.success("Global AR Days updated!")
        st.rerun()
