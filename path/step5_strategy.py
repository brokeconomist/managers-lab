import streamlit as st
import pandas as pd

def run_step():
    st.header("🏁 Stage 5: Strategic Stress Test & QSPM")
    st.info("The final diagnostic. Testing business resilience and selecting the optimal strategy.")

    # 1. CORE DATA SYNC
    p = st.session_state.get('price', 0.0)
    vc = st.session_state.get('variable_cost', 0.0)
    q = st.session_state.get('volume', 0.0)
    margin = p - vc
    
    st.subheader("🛠️ Model Stress Testing")
    
    # 2. STRESS TEST
    col1, col2 = st.columns(2)
    with col1:
        drop_sales = st.slider("Drop in Sales Volume (%)", 0, 50, 20)
        inc_costs = st.slider("Increase in Costs (%)", 0, 30, 10)
    
    with col2:
        stressed_q = q * (1 - drop_sales/100)
        stressed_margin = p - (vc * (1 + inc_costs/100))
        # Annual baseline (approx 8000€ monthly burn from Stage 4)
        stressed_annual_profit = (stressed_margin * stressed_q) - (96000)
        st.metric("Stress-Tested Profit", f"{stressed_annual_profit:,.2f} €", delta_color="inverse")

    st.divider()

    # 3. QSPM (Quantitative Strategic Planning Matrix)
    st.subheader("🎯 QSPM: Strategic Selection")
    st.write("Evaluate which move is mathematically superior based on your current health.")

    # Simplified QSPM Data
    factors = {
        "Market Growth": 0.20,
        "Competitive Rivalry": 0.15,
        "Operating Margin": 0.30,
        "Cash Liquidity": 0.20,
        "Brand Equity": 0.15
    }

    # Scores for two strategies: A (Scale) vs B (Efficiency)
    # If Margin/Health is low, Efficiency should score higher
    health_score = st.session_state.get('health_score', 50) # Inferred from previous steps
    
    qspm_data = []
    for factor, weight in factors.items():
        # Logic: If health is low, Efficiency (B) gets higher attractiveness scores
        att_a = 2 if health_score < 40 else 4  # Scaling Attractiveness
        att_b = 4 if health_score < 40 else 2  # Efficiency Attractiveness
        qspm_data.append({
            "Key Factor": factor,
            "Weight": weight,
            "Scale (AS)": att_a,
            "Scale (TAS)": weight * att_a,
            "Efficiency (AS)": att_b,
            "Efficiency (TAS)": weight * att_b
        })

    df_qspm = pd.DataFrame(qspm_data)
    st.table(df_qspm)

    total_a = df_qspm["Scale (TAS)"].sum()
    total_b = df_qspm["Efficiency (TAS)"].sum()

    

    c1, c2 = st.columns(2)
    c1.metric("Strategy A: Scaling TAS", f"{total_a:.2f}")
    c2.metric("Strategy B: Efficiency TAS", f"{total_b:.2f}")

    # 4. FINAL VERDICT
    st.divider()
    if total_b > total_a:
        st.warning("⚖️ **Decision:** The QSPM suggests **Efficiency First**. Your structural risks are too high to justify aggressive scaling.")
    else:
        st.success("🚀 **Decision:** The QSPM suggests **Aggressive Scaling**. Your fundamentals are strong enough to capture market share.")

    st.divider()
    if st.button("🔄 Restart Lab Analysis"):
        st.session_state.flow_step = 0
        st.rerun()
