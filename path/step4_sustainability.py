import streamlit as st
import pandas as pd

def run_step():
    st.header("🏢 Stage 4: Sustainability & Structural Break-Even")
    
    # 1. SYNC WITH PREVIOUS STAGES
    p = st.session_state.get('price', 0.0)
    vc = st.session_state.get('variable_cost', 0.0)
    q_monthly = st.session_state.get('volume', 0.0) / 12
    unit_margin = p - vc
    
    # Τραβάμε το Liquidity Drain (κόστος αποθήκευσης/χρηματοδότησης) από το Stage 2
    liquidity_drain_annual = st.session_state.get('liquidity_drain', 0.0)
    liquidity_drain_monthly = liquidity_drain_annual / 12

    # 2. FIXED COSTS
    st.subheader("Monthly Operating Obligations")
    col1, col2 = st.columns(2)
    
    with col1:
        rent = st.number_input("Rent & Utilities (€)", value=1500.0)
        salaries = st.number_input("Salaries & Insurance (€)", value=4500.0)
        
    with col2:
        software = st.number_input("Software & Admin (€)", value=500.0)
        loan_payment = st.number_input("Monthly Loan Repayment (€)", value=1000.0)

    # 3. CALCULATIONS
    total_fixed_costs = rent + salaries + software
    ebit = (unit_margin * q_monthly) - total_fixed_costs
    
    # Εδώ μπαίνει η δική σου προϋπόθεση: 
    # Το Slow-moving stock δεν είναι "κενό" αλλά "έξοδο καθυστέρησης" (Carrying Cost)
    net_profit_before_drain = ebit - loan_payment
    final_net_profit = net_profit_before_drain - liquidity_drain_monthly

    # 4. RESULTS DISPLAY
    st.divider()
    res1, res2, res3 = st.columns(3)
    
    res1.metric("EBIT (Operating)", f"{ebit:,.2f} €")
    
    # Εμφάνιση του κόστους δέσμευσης κεφαλαίου
    res2.metric("Slow-Stock Penalty", f"-{liquidity_drain_monthly:,.2f} €", delta="Carrying Cost")
    res2.caption("Το κόστος επειδή τα κεφάλαια αργούν να κινηθούν.")
    
    res3.metric("Final Net Profit", f"{final_net_profit:,.2f} €")

    # 5. COLD INSIGHT
    if liquidity_drain_monthly > (ebit * 0.1):
        st.warning(f"⚠️ **Analytical Warning:** Το κόστος δέσμευσης των βραδέως κινούμενων αποθεμάτων απορροφά το { (liquidity_drain_monthly/ebit)*100:.1f}% της λειτουργικής σου κερδοφορίας.")

    st.info("Σημείωση: Το Slow-moving stock δεν υπολογίζεται ως έλλειμμα, αλλά ως λειτουργική επιβάρυνση λόγω του χρόνου δέσμευσης των κεφαλαίων.")

    # NAVIGATION
    if st.button("Final Strategy (Stage 5) ➡️"):
        st.session_state.flow_step = 5
        st.rerun()
