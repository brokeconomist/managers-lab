import streamlit as st
import pandas as pd

def run_step():
    st.header("🏁 Stage 5: Strategic Stress Test & Interactive QSPM")
    
    # 1. CORE DATA SYNC
    p = st.session_state.get('price', 0.0)
    vc = st.session_state.get('variable_cost', 0.0)
    q = st.session_state.get('volume', 0.0)
    liquidity_drain_annual = st.session_state.get('liquidity_drain', 0.0)
    
    # 2. STRESS TEST (Analytical Resilience)
    st.subheader("🛠️ Model Stress Testing")
    col1, col2 = st.columns(2)
    with col1:
        drop_sales = st.slider("Drop in Sales Volume (%)", 0, 50, 20)
    with col2:
        inc_costs = st.slider("Increase in Variable Costs (%)", 0, 30, 10)
    
    # Annual Calculation including the Slow-Stock Penalty
    total_annual_burn = (7000.0 * 12) + 12000.0 # Standard Baseline
    stressed_q = q * (1 - drop_sales/100)
    stressed_vc = vc * (1 + inc_costs/100)
    stressed_profit = ((p - stressed_vc) * stressed_q) - total_annual_burn - liquidity_drain_annual
    
    st.metric("Stress-Tested Annual Profit", f"{stressed_profit:,.2f} €", delta_color="inverse")
    st.caption(f"Includes -{liquidity_drain_annual:,.2f} € penalty for slow-moving inventory.")

    st.divider()

    # 3. INTERACTIVE QSPM
    st.subheader("🎯 Custom QSPM: Strategic Selection")
    st.write("Define your weights and rate the attractiveness of each strategy.")

    # User-Defined Weights
    with st.expander("⚖️ Edit Strategic Weights (Must sum to 1.0)", expanded=True):
        c1, c2, c3 = st.columns(3)
        w_margin = c1.slider("Profit Margin Weight", 0.0, 0.5, 0.3)
        w_growth = c2.slider("Market Growth Weight", 0.0, 0.5, 0.2)
        w_liquidity = c3.slider("Cash Liquidity Weight", 0.0, 0.5, 0.3)
        
        c4, c5 = st.columns(2)
        w_rivalry = c4.slider("Competitive Rivalry Weight", 0.0, 0.5, 0.1)
        w_brand = c5.slider("Brand Equity Weight", 0.0, 0.5, 0.1)
        
        total_w = w_margin + w_growth + w_liquidity + w_rivalry + w_brand
        st.write(f"**Total Weight Sum: {total_w:.2f}**")
        if round(total_w, 2) != 1.0:
            st.warning("⚠️ Adjust weights to sum to 1.0 for a valid QSPM analysis.")

    # User-Defined Attractiveness Scores
    st.write("### Rate Strategy Attractiveness (1 = Low, 4 = High)")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Strategy A: Aggressive Scaling**")
        as_a_margin = st.selectbox("Margin Match (A)", [1,2,3,4], index=1, key="q_a1")
        as_a_liquidity = st.selectbox("Liquidity Match (A)", [1,2,3,4], index=0, key="q_a2")

    with col_b:
        st.markdown("**Strategy B: Efficiency First**")
        as_b_margin = st.selectbox("Margin Match (B)", [1,2,3,4], index=3, key="q_b1")
        as_b_liquidity = st.selectbox("Liquidity Match (B)", [1,2,3,4], index=3, key="q_b2")

    # QSPM Table Generation
    factors = [
        ("Operating Margin", w_margin, as_a_margin, as_b_margin),
        ("Market Growth", w_growth, 4, 2), # Static example for growth
        ("Cash Liquidity", w_liquidity, as_a_liquidity, as_b_liquidity),
        ("Competitive Rivalry", w_rivalry, 2, 3),
        ("Brand Equity", w_brand, 3, 2)
    ]

    qspm_list = []
    for f, w, as_a, as_b in factors:
        qspm_list.append({
            "Key Factor": f,
            "Weight": w,
            "Scale (AS)": as_a, "Scale (TAS)": w * as_a,
            "Efficiency (AS)": as_b, "Efficiency (TAS)": w * as_b
        })

    df_qspm = pd.DataFrame(qspm_list)
    st.table(df_qspm)

    

    # 4. FINAL VERDICT
    total_tas_a = df_qspm["Scale (TAS)"].sum()
    total_tas_b = df_qspm["Efficiency (TAS)"].sum()
    
    st.divider()
    res_a, res_b = st.columns(2)
    res_a.metric("Scaling Score (TAS)", f"{total_tas_a:.2f}")
    res_b.metric("Efficiency Score (TAS)", f"{total_tas_b:.2f}")

    if total_tas_a > total_tas_b:
        st.success("🚀 **The QSPM favors SCALING.** Your priorities suggest growth is the way forward.")
    else:
        st.warning("⚖️ **The QSPM favors EFFICIENCY.** Risk mitigation and stock rotation should be your focus.")

    if st.button("🔄 Restart Lab Analysis", use_container_width=True):
        st.session_state.flow_step = 0
        st.rerun()
