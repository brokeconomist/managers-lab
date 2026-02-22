import streamlit as st
import pandas as pd

def run_step():
    st.header("🏁 Stage 5: Strategic Stress Test & Final Verdict")
    st.info("The final diagnostic. Testing business resilience and strategic alignment.")

    # 1. DATA GATHERING
    p = st.session_state.get('price', 0.0)
    vc = st.session_state.get('variable_cost', 0.0)
    q = st.session_state.get('volume', 0.0)
    unit_margin = p - vc
    
    # Financial metrics from Stage 4
    liquidity_drain_annual = st.session_state.get('liquidity_drain', 0.0)
    # We assume a base fixed cost structure from the previous session state or defaults
    total_annual_burn = (7000.0 * 12) + 12000.0 # Example Fixed + Loans
    
    # 2. STRESS TEST
    st.subheader("🛠️ Model Stress Testing")
    col1, col2 = st.columns(2)
    with col1:
        drop_sales = st.slider("Drop in Sales Volume (%)", 0, 50, 20)
        inc_costs = st.slider("Increase in Variable Costs (%)", 0, 30, 10)
    
    with col2:
        stressed_q = q * (1 - drop_sales/100)
        stressed_vc = vc * (1 + inc_costs/100)
        # Final Profit after Stress and Slow-Stock Penalty
        stressed_profit = ( (p - stressed_vc) * stressed_q ) - total_annual_burn - liquidity_drain_annual
        
        st.metric("Stress-Tested Annual Profit", f"{stressed_profit:,.2f} €", delta_color="inverse")
        st.caption("Includes the penalty for slow-moving inventory.")

    st.divider()

    # 3. EXECUTIVE SCORECARD
    st.subheader("🏆 Executive Scorecard")
    
    score = 0
    signals = []

    # Criteria 1: Margin Health
    if p > (vc * 1.6): 
        score += 30
        signals.append("✅ Robust Unit Economics")
    else: signals.append("❌ Thin Margins: Vulnerable to cost spikes")

    # Criteria 2: Inventory Efficiency (The Penalty Factor)
    ebit_approx = (unit_margin * q) - total_annual_burn
    penalty_ratio = (liquidity_drain_annual / ebit_approx) if ebit_approx > 0 else 1
    
    if penalty_ratio < 0.10:
        score += 30
        signals.append("✅ Efficient Capital Rotation")
    else:
        signals.append(f"❌ Capital Stagnation: Inventory penalty eats {penalty_ratio*100:.1f}% of EBIT")

    # Criteria 3: Break-even Proximity
    annual_be = total_annual_burn / unit_margin if unit_margin > 0 else 999999
    if q > (annual_be * 1.2):
        score += 40
        signals.append("✅ Safe Operating Volume")
    else: signals.append("❌ Dangerous Break-even Proximity")

    # Display Score
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Health Score", f"{score}/100")
        if score <= 40: st.error("CRITICAL RISK")
        elif score <= 70: st.warning("FRAGILE")
        else: st.success("SUSTAINABLE")

    with c2:
        for s in signals:
            st.write(s)

    

    # 4. QSPM STRATEGIC SELECTION
    st.divider()
    st.subheader("🎯 Strategic Decision (QSPM Logic)")
    
    # If the inventory penalty is high, Efficiency is the only logical choice
    if penalty_ratio > 0.15 or score < 60:
        st.warning("⚖️ **Recommendation: EFFICIENCY FIRST**")
        st.write("Your capital is 'stagnating' in slow-moving stock. Scaling now would only multiply your financing costs. Focus on inventory liquidation and cost reduction.")
    else:
        st.success("🚀 **Recommendation: AGGRESSIVE SCALING**")
        st.write("Your fundamentals are clean. Low inventory penalty and healthy margins justify an increase in market share acquisition.")

    if st.button("🔄 Restart Lab Analysis", use_container_width=True):
        st.session_state.flow_step = 0
        st.rerun()
