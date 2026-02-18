import streamlit as st
import pandas as pd

# -----------------------------------------
# LOGIC
# -----------------------------------------
def calculate_weighted_average(amounts, credit_days):
    total_amount = sum(amounts)
    if total_amount == 0:
        return 0, 0.0

    weighted_sum = sum(a * d for a, d in zip(amounts, credit_days))
    weighted_avg = weighted_sum / total_amount
    return total_amount, weighted_avg

# -----------------------------------------
# UI
# -----------------------------------------
def show_credit_days_calculator():
    st.header("📅 Weighted Average Credit Days")
    st.caption("Strategic assessment of receivables based on exposure volume, not just customer count.")

    # SIDEBAR: Control the number of categories
    with st.sidebar:
        st.subheader("Configuration")
        num_categories = st.number_input(
            "Number of customer categories",
            min_value=1, max_value=15, value=4
        )
        st.divider()
        st.info("The weighted average provides a more accurate picture of liquidity risk than a simple average.")

    # INPUT AREA
    st.subheader("📥 Input Data")
    
    names = []
    customers = []
    amounts = []
    credit_days = []

    # Header Row
    h1, h2, h3, h4 = st.columns([2, 1, 2, 1])
    h1.markdown("**Category Name**")
    h2.markdown("**Cust. #**")
    h3.markdown("**Amount (€)**")
    h4.markdown("**Days**")

    for i in range(num_categories):
        c1, c2, c3, c4 = st.columns([2, 1, 2, 1])
        
        names.append(c1.text_input(f"n_{i}", value=f"Segment {i+1}", label_visibility="collapsed"))
        customers.append(c2.number_input(f"c_{i}", min_value=0, step=1, label_visibility="collapsed"))
        amounts.append(c3.number_input(f"a_{i}", min_value=0.0, step=1000.0, label_visibility="collapsed"))
        credit_days.append(c4.number_input(f"d_{i}", min_value=0, step=1, label_visibility="collapsed"))

    st.divider()

    if st.button("📊 Calculate Weighted Metrics", type="primary"):
        total_amount, weighted_avg = calculate_weighted_average(amounts, credit_days)

        if total_amount == 0:
            st.error("⚠️ Please enter at least one amount to perform the calculation.")
            return

        # RESULTS
        st.subheader("📈 Financial Results")
        m1, m2, m3 = st.columns(3)

        m1.metric("Total Receivables", f"€ {total_amount:,.0f}".replace(",", "."))
        m2.metric("Weighted Avg. Days", f"{weighted_avg:.1f} Days")
        
        # Simple average for comparison
        active_segments = [d for a, d in zip(amounts, credit_days) if a > 0]
        simple_avg = sum(active_segments) / len(active_segments) if active_segments else 0
        m3.metric("Simple Average", f"{simple_avg:.1f} Days", delta=f"{weighted_avg - simple_avg:.1f} Bias")

        

        # ANALYTICAL TABLE
        st.subheader("📋 Exposure Analysis")
        
        data = []
        for n, c, a, d in zip(names, customers, amounts, credit_days):
            if a > 0:
                weight = (a / total_amount) * 100
                data.append({
                    "Category": n,
                    "Customers": c,
                    "Amount (€)": a,
                    "Credit Days": d,
                    "Weight (%)": f"{weight:.1f}%"
                })
        
        df = pd.DataFrame(data)
        st.table(df)

        # Managerial Insight
        st.divider()
        st.markdown("### 🧠 Strategic Observation")
        highest_debt_idx = amounts.index(max(amounts))
        
        if credit_days[highest_debt_idx] > weighted_avg:
            st.warning(f"**Concentration Risk:** Your largest exposure (**{names[highest_debt_idx]}**) has credit terms longer than your weighted average. This significantly delays your cash inflows.")
        else:
            st.success(f"**Liquidity Control:** Your highest value segments are paying faster than the average, which is positive for cash flow stability.")

if __name__ == "__main__":
    show_credit_days_calculator()
