import streamlit as st
import pandas as pd

def show_qspm_tool():
    st.header("🧭 QSPM – Strategy Comparison")
    st.info("Quantitative Strategic Planning Matrix: Evaluate which strategy best fits your current business reality.")

    # 1. LOAD SYSTEM CONTEXT (For Reference)
    survival = st.session_state.get('volume', 0) / (st.session_state.get('fixed_cost', 1) / (st.session_state.get('price', 1) - st.session_state.get('variable_cost', 0.1)) + 0.001) - 1
    cash_days = st.session_state.get('ar_days', 0) + st.session_state.get('inventory_days', 0) - st.session_state.get('payables_days', 0)

    st.write(f"**Current Strategic Context:** Survival Margin: {survival:.1%} | Cash Cycle: {int(cash_days)} Days")

    st.divider()

    # 2. DEFINE STRATEGIES
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        strat1_name = st.text_input("Strategy A", value="Market Expansion")
    with col_s2:
        strat2_name = st.text_input("Strategy B", value="Product Innovation")

    # 3. CRITICAL SUCCESS FACTORS (CSFs)
    # Ορίζουμε τους παράγοντες και τη βαρύτητά τους (Weight)
    factors = [
        ("Financial Stability (Cash Flow)", 0.30),
        ("Profitability (Margin)", 0.25),
        ("Market Share / Growth", 0.20),
        ("Operational Complexity", 0.15),
        ("Resource Availability", 0.10)
    ]

    st.subheader("Attractiveness Scoring (1-4)")
    st.caption("1: Not attractive | 2: Somewhat attractive | 3: Reasonably attractive | 4: Highly attractive")

    scores_a = []
    scores_b = []

    for factor, weight in factors:
        st.markdown(f"**{factor}** (Weight: {weight:.0%})")
        c1, c2 = st.columns(2)
        with c1:
            s_a = st.slider(f"Score for {strat1_name}", 1, 4, 2, key=f"a_{factor}")
            scores_a.append(s_a * weight)
        with c2:
            s_b = st.slider(f"Score for {strat2_name}", 1, 4, 2, key=f"b_{factor}")
            scores_b.append(s_b * weight)

    # 4. FINAL CALCULATION
    total_a = sum(scores_a)
    total_b = sum(scores_b)

    st.divider()

    # 5. RESULTS DISPLAY
    res_a, res_b = st.columns(2)
    with res_a:
        st.metric(f"Total Score: {strat1_name}", f"{total_a:.2f}")
    with res_b:
        st.metric(f"Total Score: {strat2_name}", f"{total_b:.2f}")

    # Strategic Verdict
    if abs(total_a - total_b) < 0.2:
        st.warning("**Strategic Stalemate:** The options are too close. Re-evaluate the weights or consider if both can be executed in phases.")
    elif total_a > total_b:
        st.success(f"**Winner: {strat1_name}** – This strategy aligns better with your success factors and current risk profile.")
    else:
        st.success(f"**Winner: {strat2_name}** – This strategy is quantitatively superior based on your scoring.")

    # 6. VISUALIZATION TABLE
    df_qspm = pd.DataFrame({
        "Factor": [f[0] for f in factors],
        "Weight": [f[1] for f in factors],
        f"{strat1_name} (Weighted)": scores_a,
        f"{strat2_name} (Weighted)": scores_b
    })
    st.table(df_qspm)
