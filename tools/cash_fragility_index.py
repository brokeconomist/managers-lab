import streamlit as st

def show_cash_fragility_index():
    st.header("🛡️ Cash Fragility Index")
    st.info("Stress Test: How many days can the business survive if all inflows (collections) stop today?")

    # 1. READ FROM CORE (Shared Data)
    # Χρειαζόμαστε τα Fixed Costs για να ξέρουμε τα καθημερινά έξοδα
    fixed_costs_annual = st.session_state.get('fixed_cost', 0.0)
    daily_burn_rate = fixed_costs_annual / 365

    st.write(f"**Baseline Fixed Costs:** {fixed_costs_annual:,.2f} €/year")
    st.write(f"**Daily Operational Burn Rate:** {daily_burn_rate:,.2f} €/day")

    st.divider()

    # 2. USER INPUTS (Specific to this moment)
    col1, col2 = st.columns(2)
    with col1:
        current_cash = st.number_input("Current Cash in Bank (€)", min_value=0.0, value=10000.0)
    with col2:
        unused_credit_lines = st.number_input("Available Credit Lines (€)", min_value=0.0, value=5000.0)

    total_liquidity = current_cash + unused_credit_lines

    # 3. CALCULATIONS
    if daily_burn_rate > 0:
        days_to_zero = total_liquidity / daily_burn_rate
    else:
        days_to_zero = float('inf')

    # 4. RESULTS
    st.subheader("Survival Runway")
    
    # Χρωματική κωδικοποίηση βάσει επικινδυνότητας
    if days_to_zero < 30:
        color = "red"
        status = "CRITICAL FRAGILITY"
    elif days_to_zero < 60:
        color = "orange"
        status = "LOW BUFFER"
    else:
        color = "green"
        status = "STABLE"

    st.metric("Days of Survival", f"{int(days_to_zero)} Days", delta=f"{status}", delta_color="normal")
    st.progress(min(days_to_zero / 120, 1.0)) # Display progress up to 120 days
    st.caption("Safety threshold is typically 60-90 days of fixed expenses.")

    st.divider()

    # 5. COLD INSIGHT
    st.markdown(f"""
    ### 🧠 Strategic Verdict
    To reach a 'Safe' status (90 days), you need a total liquidity of **{daily_burn_rate * 90:,.2f} €**. 
    Current gap: **{max(0.0, (daily_burn_rate * 90) - total_liquidity):,.2f} €**.
    """)
