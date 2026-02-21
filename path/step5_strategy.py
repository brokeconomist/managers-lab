import streamlit as st
import pandas as pd

def run_step():
    st.header("🏁 Stage 5: Strategic Stress Test & Executive Summary")
    st.info("The final diagnostic. Testing business resilience against market volatility.")

    # 1. DATA GATHERING (Dynamic Sync with Stage 0)
    p = st.session_state.get('price', 0.0)
    vc = st.session_state.get('variable_cost', 0.0)
    q = st.session_state.get('volume', 0.0)  # This is your Volume from Calibration
    margin = p - vc
    
    # Financial constants from Stage 4
    fixed_costs = 7000.0 # Standard baseline if not saved
    loan = 1000.0
    total_monthly_burn = fixed_costs + loan

    st.subheader("🛠️ Model Stress Testing")
    st.write(f"**Current Baseline:** {q} Units/Year at {p:,.2f} € price.")

    # 2. STRESS TEST INPUTS
    col1, col2 = st.columns(2)
    with col1:
        drop_in_sales = st.slider("Drop in Sales Volume (%)", 0, 50, 20)
        increase_in_vc = st.slider("Increase in Variable Costs (%)", 0, 30, 10)
    
    with col2:
        # Recalculating based on Stress
        stressed_q = q * (1 - drop_in_sales/100)
        stressed_vc = vc * (1 + increase_in_vc/100)
        stressed_margin = p - stressed_vc
        
        # Annual View
        stressed_annual_profit = (stressed_margin * stressed_q) - (total_monthly_burn * 12)
        
        st.metric("Stress-Tested Annual Profit", f"{stressed_annual_profit:,.2f} €", 
                  delta=f"Impact: {stressed_annual_profit - ((margin * q) - (total_monthly_burn * 12)):,.2f} €", 
                  delta_color="inverse")

    st.divider()

    # 3. EXECUTIVE SCORECARD
    st.subheader("🏆 Executive Scorecard")
    
    score = 0
    metrics = []

    # Analysis Logic
    if p > (vc * 1.5): 
        score += 25
        metrics.append("✅ Healthy Contribution Margin")
    else: metrics.append("❌ Low Margin Structure")

    if st.session_state.get('inventory_days', 0) < 45: 
        score += 25
        metrics.append("✅ Efficient Cash Cycle")
    else: metrics.append("❌ High Working Capital Pressure")

    # Volume vs Break-even check
    annual_be = (total_monthly_burn / margin * 12) if margin > 0 else 999999
    if q > annual_be:
        score += 25
        metrics.append("✅ Operating Above Break-Even")
    else: metrics.append("❌ Structural Deficit Detected")

    # LTV/CAC check
    if st.session_state.get('ltv_cac_ratio', 0) > 3:
        score += 25
        metrics.append("✅ Scalable Unit Economics")
    else: metrics.append("❌ Customer Acquisition is Too Expensive")

    # 4. FINAL RATING
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Business Health Score", f"{score}/100")
        if score <= 25: st.error("CRITICAL RISK")
        elif score <= 50: st.warning("FRAGILE")
        elif score <= 75: st.info("STABLE")
        else: st.success("ELITE")

    with c2:
        st.write("### Strategic Signals")
        for m in metrics:
            st.write(m)

    

    st.divider()

    # 5. THE COLD ROADMAP
    st.subheader("📍 The Cold Roadmap")
    if score <= 25:
        st.error("**URGENT:** Pivot or Liquidation Risk. Your fixed costs are suffocating your low volume. Immediate price hike or massive cost cutting required.")
    elif score <= 50:
        st.warning("**CAUTION:** Optimize the engine. Your unit economics are too thin to support growth. Fix the Churn and CAC before scaling.")
    else:
        st.success("**GO:** You have a sustainable model. Focus on increasing acquisition budget to capture market share.")

    if st.button("🔄 Restart Analysis", use_container_width=True):
        st.session_state.flow_step = 0
        st.rerun()
