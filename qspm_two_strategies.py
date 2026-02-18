import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def normalize_weights(weights):
    total = sum(weights)
    if total == 0:
        return weights
    return [w / total for w in weights]

# -------------------------------------------------
# MAIN UI
# -------------------------------------------------
def show_qspm_tool():
    st.header("🧭 QSPM – Quantitative Strategic Planning Matrix")
    st.caption("Structured comparison of alternative strategic paths based on weighted attractiveness.")

    # -------------------------------------------------
    # SIDEBAR: CONFIGURATION
    # -------------------------------------------------
    with st.sidebar:
        st.subheader("Decision Setup")
        strategy_A = st.text_input("Strategy A Name", value="Market Expansion")
        strategy_B = st.text_input("Strategy B Name", value="Product Innovation")
        
        st.divider()
        num_criteria = st.number_input(
            "Number of Strategic Criteria",
            min_value=2, max_value=12, value=5, step=1
        )
        st.info("Assign weights based on relative importance (e.g., 1-10) and scores based on attractiveness (1-4).")

    # -------------------------------------------------
    # CORE PHILOSOPHY
    # -------------------------------------------------
    st.markdown("""
    > This matrix quantifies **managerial judgment**. It doesn't replace the decision-maker; 
    > it reveals which strategy is most consistent with your own priorities.
    """)

    

    # -------------------------------------------------
    # CRITERIA INPUT SECTION
    # -------------------------------------------------
    st.subheader("1️⃣ Strategic Criteria & Scoring")
    
    criteria, weights, score_A, score_B = [], [], [], []

    # Table-like Header
    h1, h2, h3, h4 = st.columns([3, 1, 1, 1])
    h1.markdown("**Criterion**")
    h2.markdown("**Weight**")
    h3.markdown(f"**{strategy_A}**")
    h4.markdown(f"**{strategy_B}**")

    for i in range(num_criteria):
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        with c1:
            crit = st.text_input(f"c_n_{i}", value=f"Factor {i+1}", label_visibility="collapsed")
        with c2:
            w = st.number_input(f"w_{i}", min_value=0.0, max_value=10.0, value=1.0, step=0.5, label_visibility="collapsed")
        with c3:
            s_a = st.number_input(f"sa_{i}", min_value=1, max_value=4, value=2, label_visibility="collapsed")
        with c4:
            s_b = st.number_input(f"sb_{i}", min_value=1, max_value=4, value=2, label_visibility="collapsed")
        
        criteria.append(crit)
        weights.append(w)
        score_A.append(s_a)
        score_B.append(s_b)

    # -------------------------------------------------
    # CALCULATIONS
    # -------------------------------------------------
    norm_weights = normalize_weights(weights)
    weighted_A = [norm_weights[i] * score_A[i] for i in range(num_criteria)]
    weighted_B = [norm_weights[i] * score_B[i] for i in range(num_criteria)]
    total_A = sum(weighted_A)
    total_B = sum(weighted_B)

    # -------------------------------------------------
    # RESULTS & VISUALS
    # -------------------------------------------------
    st.divider()
    st.subheader("2️⃣ Analytical Comparison")

    col_m1, col_m2 = st.columns(2)
    col_m1.metric(f"Score: {strategy_A}", f"{total_A:.2f}")
    col_m2.metric(f"Score: {strategy_B}", f"{total_B:.2f}", 
                  delta=f"{total_B - total_A:.2f}" if total_B != total_A else None)

    # Comparison Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(criteria))
    width = 0.35
    
    ax.bar(x - width/2, weighted_A, width, label=strategy_A, color='#1f77b4')
    ax.bar(x + width/2, weighted_B, width, label=strategy_B, color='#ff7f0e')
    
    ax.set_ylabel('Weighted Attractiveness')
    ax.set_title('Contribution per Criterion')
    ax.set_xticks(x)
    ax.set_xticklabels(criteria, rotation=45, ha='right')
    ax.legend()
    st.pyplot(fig)

    # -------------------------------------------------
    # INTERPRETATION
    # -------------------------------------------------
    st.divider()
    st.subheader("3️⃣ Strategic Verdict")

    if abs(total_A - total_B) < 0.1:
        st.info("⚖️ **Indifference Point:** Both strategies are almost equally attractive. Re-evaluate the weights of the most critical factors.")
    elif total_A > total_B:
        st.success(f"🏆 **Dominant Path:** {strategy_A} appears more aligned with your strategic priorities.")
    else:
        st.success(f"🏆 **Dominant Path:** {strategy_B} appears more aligned with your strategic priorities.")

    with st.expander("View Full QSPM Data Table"):
        df = pd.DataFrame({
            "Criterion": criteria,
            "Raw Weight": weights,
            "Normalized Weight": norm_weights,
            f"{strategy_A} Score": score_A,
            f"{strategy_A} Weighted": weighted_A,
            f"{strategy_B} Score": score_B,
            f"{strategy_B} Weighted": weighted_B,
        })
        st.dataframe(df.style.format({
            "Normalized Weight": "{:.2f}",
            f"{strategy_A} Weighted": "{:.2f}",
            f"{strategy_B} Weighted": "{:.2f}",
        }))

if __name__ == "__main__":
    show_qspm_tool()
