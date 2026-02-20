import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    st.header("📅 Weighted Average Credit Days & Pareto Analysis")
    st.caption("Strategic assessment of receivables volume and collection concentration.")

    with st.sidebar:
        st.subheader("Configuration")
        num_categories = st.number_input("Number of customer categories", min_value=1, max_value=15, value=5)
        st.divider()
        st.info("Pareto Analysis (80/20) helps identify which key accounts dominate your credit exposure.")

    st.subheader("📥 Input Data")
    names, customers, amounts, credit_days = [], [], [], []

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

    if st.button("📊 Run Analytical Engine", type="primary"):
        total_amount, weighted_avg = calculate_weighted_average(amounts, credit_days)

        if total_amount == 0:
            st.error("⚠️ Enter values to generate analysis.")
            return

        # 1. CORE METRICS
        st.divider()
        m1, m2 = st.columns(2)
        m1.metric("Total Receivables", f"€ {total_amount:,.0f}".replace(",", "."))
        m2.metric("Weighted Avg. Days", f"{weighted_avg:.1f} Days")

        # 2. PARETO DATA PREPARATION
        df = pd.DataFrame({
            "Category": names,
            "Amount": amounts,
            "Days": credit_days
        }).sort_values(by="Amount", ascending=False)

        df["Weight %"] = (df["Amount"] / total_amount) * 100
        df["Cumulative %"] = df["Weight %"].cumsum()

        # 3. PARETO CHART
        st.subheader("📈 Pareto Exposure Chart")
        st.caption("Identify the 'Vital Few' segments that constitute the majority of your debt.")
        
        
        
        fig, ax1 = plt.subplots(figsize=(10, 5))
        # Bar chart
        ax1.bar(df["Category"], df["Amount"], color="#1f77b4", label="Debt Amount")
        ax1.set_ylabel("Debt Amount (€)")
        
        # Cumulative line
        ax2 = ax1.twinx()
        ax2.plot(df["Category"], df["Cumulative %"], color="#d62728", marker="D", ms=7, label="Cumulative %")
        ax2.axhline(y=80, color='gray', linestyle='--') # 80% threshold
        ax2.set_ylabel("Cumulative Percentage (%)")
        ax2.set_ylim(0, 110)

        plt.title("Receivables Concentration (Pareto)")
        st.pyplot(fig)

        # 4. PARETO TABLE
        st.subheader("📋 Concentration Table")
        st.table(df.style.format({"Amount": "{:,.0f} €", "Weight %": "{:.1f}%", "Cumulative %": "{:.1f}%"}))

        # 5. MANAGERIAL VERDICT
        st.divider()
        key_segments = df[df["Cumulative %"] <= 85]["Category"].tolist()
        
        st.markdown("### 🧠 Strategic Verdict")
        st.write(f"The following segments constitute **over 80%** of your total exposure: **{', '.join(key_segments)}**.")
        
        # Checking if high-volume customers pay late
        avg_days_top = df[df["Cumulative %"] <= 85]["Days"].mean()
        if avg_days_top > weighted_avg:
            st.error(f"⚠️ **High-Risk Concentration:** Your core debtors (top 80%) have a collection period ({avg_days_top:.1f} days) higher than the average. Your liquidity is overly dependent on these specific accounts.")
        else:
            st.success("✅ **Balanced Risk:** Your primary debtors have collection terms that align with or are faster than your average.")

if __name__ == "__main__":
    show_credit_days_calculator()
