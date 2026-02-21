import streamlit as st
import pandas as pd

def run_step():
    st.header("🏁 Stage 5: Strategic Stress Test & User-Defined QSPM")
    st.info("The final diagnostic. Set your own priorities and evaluate the optimal strategic path.")

    # 1. CORE DATA SYNC
    p = st.session_state.get('price', 0.0)
    vc = st.session_state.get('variable_cost', 0.0)
    q = st.session_state.get('volume', 0.0)
    
    st.subheader("🛠️ Model Stress Testing")
    col1, col2 = st.columns(2)
    with col1:
        drop_sales = st.slider("Drop in Sales Volume (%)", 0, 50, 20)
    with col2:
        inc_costs = st.slider("Increase in Variable Costs (%)", 0, 30, 10)
    
    # 2. QSPM: USER-DEFINED WEIGHTS
    st.divider()
    st.subheader("🎯 Custom QSPM Analysis")
    st.write("Set the importance (Weight) for each factor and rate the Attractiveness (1-4).")

    # Sidebar or Expander for Weights to keep UI clean
    with st.expander("⚖️ Edit Strategy Weights (Total must be 1.0)", expanded=True):
        c1, c2, c3 = st.columns(3)
        w_margin = c1.slider("Profit Margin Weight", 0.0, 0.5, 0.3)
        w_market = c2.slider("Market Growth Weight", 0.0, 0.5, 0.2)
        w_liquidity = c3.slider("Cash Liquidity Weight", 0.0, 0.5, 0.2)
        
        c4, c5 = st.columns(2)
        w_rivalry = c4.slider("Competitive Rivalry Weight", 0.0, 0.5, 0.15)
        w_brand = c5.slider("Brand Equity Weight", 0.0, 0.5, 0.15)
        
        total_w = w_margin + w_market + w_liquidity + w_rivalry + w_brand
        st.write(f"**Total Weight Sum: {total_w:.2f}**")
        if round(total_w, 2) != 1.0:
            st.warning("⚠️ The sum of weights should equal 1.0 for a standard QSPM.")

    # 3. ATTRACTIVENESS SCORING (User Inputs)
    st.write("### Rate Strategy Attractiveness (1 = Low, 4 = High)")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Strategy A: Aggressive Scaling**")
        as_a_margin = st.selectbox("Margin Match (A)", [1,2,3,4], index=1, key="as_a1")
        as_a_growth = st.selectbox("Growth Match (A)", [1,2,3,4], index=3, key="as_a2")

    with col_b:
        st.markdown("**Strategy B: Efficiency First**")
        as_b_margin = st.selectbox("Margin Match (B)", [1,2,3,4], index=3, key="as_b1")
        as_b_growth = st.selectbox("Growth Match (B)", [1,2,3,4], index=1, key="as_b2")

    # 4. QSPM CALCULATION TABLE
    factors = [
        ("Operating Margin", w_margin, as_a_margin, as_b_margin),
        ("Market Growth", w_market, as_a_growth, as_b_growth),
        ("Cash Liquidity", w_liquidity, 2, 4), # Fixed placeholders for logic
        ("Competitive Rivalry", w_rivalry, 3, 2),
        ("Brand Equity", w_brand, 3, 2)
    ]

    qspm_list = []
    for factor, w, as_a, as_b in factors:
        qspm_list.append({
            "Factor": factor,
            "Weight": w,
            "Scale (AS)": as_a,
            "Scale (TAS)": w * as_a,
            "Efficiency (AS)": as_b,
            "Efficiency (TAS)": w * as_b
        })

    df_qspm = pd.DataFrame(qspm_list)
    st.table(df_qspm)

    total_tas_a = df_qspm["Scale (TAS)"].sum()
    total_tas_b = df_qspm["Efficiency (TAS)"].sum()

    # 5. FINAL VERDICT
    st.divider()
    res_a, res_b = st.columns(2)
    res_a.metric("Scaling Score (TAS)", f"{total_tas_a:.2f}")
    res_b.metric("Efficiency Score (TAS)", f"{total_tas_b:.2f}")

    if total_tas_a > total_tas_b:
        st.success("🚀 **The QSPM favors SCALING.** Based on your weights, growth is the priority.")
    else:
        st.warning("⚖️ **The QSPM favors EFFICIENCY.** Based on your weights, risk mitigation is the priority.")

    if st.button("🔄 Restart Analysis"):
        st.session_state.flow_step = 0
        st.rerun()
