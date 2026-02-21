import streamlit as st
import pandas as pd

def run_step():
    st.header("🏁 Stage 5: Strategic Stress Test & Executive Summary")
    st.info("The final diagnostic. Testing business resilience against market volatility.")

    # 1. DATA GATHERING FROM PREVIOUS STAGES
    # We pull everything we've calculated so far
    price = st.session_state.get('price', 0)
    vc = st.session_state.get('variable_cost', 0)
    margin = price - vc
    current_vol = st.session_state.get('volume', 0)
    working_capital = st.session_state.get('working_capital_req', 0)
    
    st.subheader("🛠️ Model Stress Testing")
    st.write("What happens to your profit if the market shifts?")

    # 2. STRESS TEST INPUTS
    col1, col2 = st.columns(2)
    with col1:
        drop_in_sales = st.slider("Drop in Sales Volume (%)", 0, 50, 20)
        increase_in_vc = st.slider("Increase in Variable Costs (%)", 0, 30, 10)
    
    with col2:
        st.write("### Impact Analysis")
        new_vol = current_vol * (1 - drop_in_sales/100)
        new_vc = vc * (1 + increase_in_vc/100)
        new_margin = price - new_vc
        new_annual_profit = (new_margin * new_vol) - (st.session_state.get('fixed_costs', 8000) * 12)
        
        st.metric("Stress-Tested Annual Profit", f"{new_annual_profit:,.2f} €", 
                  delta=f"{new_annual_profit - ((margin * current_vol) - 96000):,.2f} €", delta_color="inverse")

    st.divider()

    # 3. THE EXECUTIVE SCORECARD
    st.subheader("🏆 Executive Scorecard")
    
    # Simple Scoring Logic
    score = 0
    metrics = []

    # Check Margin
    margin_pct = (margin / price) * 100 if price > 0 else 0
    if margin_pct > 40: 
        score += 25
        metrics.append("✅ Healthy Contribution Margin")
    else: metrics.append("❌ Low Margin Structure")

    # Check Liquidity (CCC)
    ccc = st.session_state.get('inventory_days', 0) + st.session_state.get('ar_days', 0) - st.session_state.get('payables_days', 0)
    if ccc < 45: 
        score += 25
        metrics.append("✅ Efficient Cash Cycle")
    else: metrics.append("❌ Cash Locked in Operations")

    # Check Survival (Runway)
    if st.session_state.get('safety_margin', 0) > 15:
        score += 25
        metrics.append("✅ Sustainable Scale")
    else: metrics.append("❌ Dangerous Break-even Proximity")

    # Check Unit Economics
    if st.session_state.get('ltv_cac_ratio', 0) > 3:
        score += 25
        metrics.append("✅ Scalable Unit Economics")
    else: metrics.append("❌ Fragile Customer ROI")

    # 4. FINAL DISPLAY
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Business Health Score", f"{score}/100")
        if score <= 25: st.error("CRITICAL RISK")
        elif score <= 50: st.warning("FRAGILE")
        elif score <= 75: st.info("STABLE")
        else: st.success("ELITE")

    with c2:
        st.write("### Key Strategic Signals")
        for m in metrics:
            st.write(m)

    

    st.divider()

    # 5. THE COLD ROADMAP
    st.subheader("📍 The Cold Roadmap")
    if score < 50:
        st.error("""
        **Priority 1: Survival.** Do not spend on marketing. Your structural deficit will only grow. 
        Focus on raising Prices or slashing Fixed Costs immediately.
        """)
    elif score < 80:
        st.warning("""
        **Priority 2: Optimization.** Optimize your Cash Conversion Cycle to release liquidity. 
        Work on Retention (Churn) to improve your LTV.
        """)
    else:
        st.success("""
        **Priority 3: Scaling.** You have a 'License to Grow'. 
        Aggressively increase CAC spend to capture market share.
        """)

    st.divider()
    
    # 6. RESET OR EXPORT
    if st.button("🔄 Restart Analysis", use_container_width=True):
        st.session_state.flow_step = 0
        st.session_state.mode = "home"
        st.rerun()

    st.caption("Managers' Lab | Analytical Decision Support System | v2.0")
