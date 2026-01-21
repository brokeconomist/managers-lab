import streamlit as st
import pandas as pd

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

    st.title("🧭 QSPM – Quantitative Strategic Planning Matrix")
    st.subheader("Comparison of **two alternative strategies**")

    # -------------------------------------------------
    # EXPLANATORY TEXT (CORE PHILOSOPHY)
    # -------------------------------------------------

    st.markdown("""
    ### How to use this tool

    **What this tool does**
    - Structures a strategic comparison between **two serious alternatives**
    - Forces explicit **trade-offs**
    - Makes your **assumptions visible and testable**

    **What this tool does NOT do**
    - ❌ It does **not** forecast the market  
    - ❌ It does **not** estimate probabilities  
    - ❌ It does **not** claim objectivity  

    👉 All inputs reflect **your managerial judgment**.  
    The model does **not decide** — it only shows which strategy is
    **more consistent with your own assumptions**.

    **Why only two strategies?**
    Strategic decisions are rarely made among many options.
    In practice:
    - many ideas exist initially,
    - most are rejected qualitatively,
    - the real decision happens between **two viable paths**.

    This tool is designed for that final comparison.
    """)

    st.divider()

    # -------------------------------------------------
    # STRATEGY NAMES
    # -------------------------------------------------

    col1, col2 = st.columns(2)
    with col1:
        strategy_A = st.text_input("Strategy A name", value="Strategy A")
    with col2:
        strategy_B = st.text_input("Strategy B name", value="Strategy B")

    st.divider()

    # -------------------------------------------------
    # CRITERIA INPUT
    # -------------------------------------------------

    st.subheader("1️⃣ Strategic Criteria")

    st.markdown("""
    Define the **key factors** that influence this strategic choice.

    Typical sources:
    - Pricing & break-even analysis
    - Substitution pressure
    - Cost structure & margins
    - Market capacity constraints
    - Risk & execution capability
    """)

    num_criteria = st.number_input(
        "Number of criteria",
        min_value=2,
        max_value=10,
        value=4,
        step=1
    )

    criteria = []
    weights = []
    score_A = []
    score_B = []

    st.divider()
    st.markdown("### Criteria definition & scoring")

    for i in range(num_criteria):
        with st.container():
            st.markdown(f"**Criterion {i+1}**")

            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])

            with c1:
                crit = st.text_input(
                    f"Criterion name {i+1}",
                    value=f"Criterion {i+1}",
                    key=f"crit_{i}"
                )

            with c2:
                weight = st.number_input(
                    "Importance weight",
                    min_value=0.0,
                    max_value=10.0,
                    value=1.0,
                    step=0.5,
                    key=f"weight_{i}",
                    help="Relative importance of this criterion (managerial judgment)"
                )

            with c3:
                a_score = st.number_input(
                    f"{strategy_A} attractiveness",
                    min_value=1,
                    max_value=4,
                    value=2,
                    step=1,
                    key=f"A_{i}",
                    help="1 = poor, 4 = very attractive"
                )

            with c4:
                b_score = st.number_input(
                    f"{strategy_B} attractiveness",
                    min_value=1,
                    max_value=4,
                    value=2,
                    step=1,
                    key=f"B_{i}",
                    help="1 = poor, 4 = very attractive"
                )

            criteria.append(crit)
            weights.append(weight)
            score_A.append(a_score)
            score_B.append(b_score)

    # -------------------------------------------------
    # NORMALIZATION & CALCULATION
    # -------------------------------------------------

    norm_weights = normalize_weights(weights)

    weighted_A = [norm_weights[i] * score_A[i] for i in range(num_criteria)]
    weighted_B = [norm_weights[i] * score_B[i] for i in range(num_criteria)]

    total_A = sum(weighted_A)
    total_B = sum(weighted_B)

    # -------------------------------------------------
    # RESULTS TABLE
    # -------------------------------------------------

    st.divider()
    st.subheader("2️⃣ QSPM Results")

    df = pd.DataFrame({
        "Criterion": criteria,
        "Weight (normalized)": norm_weights,
        f"{strategy_A} score": score_A,
        f"{strategy_A} weighted": weighted_A,
        f"{strategy_B} score": score_B,
        f"{strategy_B} weighted": weighted_B,
    })

    st.dataframe(
        df.style.format({
            "Weight (normalized)": "{:.2f}",
            f"{strategy_A} weighted": "{:.2f}",
            f"{strategy_B} weighted": "{:.2f}",
        }),
        use_container_width=True
    )

    # -------------------------------------------------
    # TOTAL SCORES
    # -------------------------------------------------

    c1, c2 = st.columns(2)
    with c1:
        st.metric(f"Total Attractiveness – {strategy_A}", f"{total_A:.2f}")
    with c2:
        st.metric(f"Total Attractiveness – {strategy_B}", f"{total_B:.2f}")

    # -------------------------------------------------
    # INTERPRETATION
    # -------------------------------------------------

    st.divider()
    st.subheader("3️⃣ Interpretation")

    if total_A > total_B:
        st.success(
            f"Based on **your assumptions**, **{strategy_A}** "
            f"is more consistent with the selected criteria."
        )
    elif total_B > total_A:
        st.success(
            f"Based on **your assumptions**, **{strategy_B}** "
            f"is more consistent with the selected criteria."
        )
    else:
        st.info(
            "Both strategies appear **equally attractive** "
            "under the current assumptions."
        )

    st.markdown("""
    🔎 **Important reminder**

    If the result feels uncomfortable, ask:
    - Are the **criteria** correct?
    - Are the **weights** realistic?
    - Are the **scores honest**?

    👉 The decision remains **yours**.  
    The QSPM simply makes your reasoning explicit.
    """)
