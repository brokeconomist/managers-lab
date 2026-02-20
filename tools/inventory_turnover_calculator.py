import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# Logic Functions
# -------------------------------------------------
def calculate_turnover(avg_inv, usage_val):
    if usage_val == 0:
        return 0
    # Χρήση 365 ημερών βάσει των οδηγιών σου
    return round((avg_inv * 365) / usage_val, 2)

# -------------------------------------------------
# UI Interface
# -------------------------------------------------
def show_inventory_turnover_calculator():
    st.header("📦 Inventory Turnover & Pareto Analysis")
    st.caption("Identify slow-moving items and capital concentration in your warehouse.")

    # SIDEBAR: Settings
    with st.sidebar:
        st.subheader("Configuration")
        method = st.radio(
            "Calculation Basis",
            ["📊 Quantity-Based", "💶 Value-Based"]
        )
        num_items = st.number_input("Number of Products", min_value=1, max_value=20, value=5)
        
        st.divider()
        st.info("Value-Based analysis is recommended for identifying where your cash is 'trapped'.")

    # INPUT AREA
    st.subheader("📥 Inventory Data")
    
    col_names = ["Product Name", "Avg. Inventory", "Annual Sales/COGS"]
    if method == "📊 Quantity-Based":
        input_labels = ["Name", "Avg. Units", "Units Sold"]
    else:
        input_labels = ["Name", "Avg. Value (€)", "COGS (€)"]

    data_list = []
    
    # Header Row
    h1, h2, h3 = st.columns([2, 1, 1])
    h1.markdown(f"**{input_labels[0]}**")
    h2.markdown(f"**{input_labels[1]}**")
    h3.markdown(f"**{input_labels[2]}**")

    for i in range(num_items):
        c1, c2, c3 = st.columns([2, 1, 1])
        name = c1.text_input(f"n_{i}", value=f"Item {i+1}", label_visibility="collapsed")
        avg_inv = c2.number_input(f"inv_{i}", min_value=0.0, step=10.0, label_visibility="collapsed")
        usage = c3.number_input(f"usage_{i}", min_value=0.0, step=100.0, label_visibility="collapsed")
        data_list.append({"Name": name, "AvgInventory": avg_inv, "Usage": usage})

    st.divider()

    if st.button("📊 Run Inventory Analysis", type="primary"):
        df = pd.DataFrame(data_list)
        
        # Calculate Turnover Days for each item
        df["Turnover Days"] = df.apply(lambda x: calculate_turnover(x["AvgInventory"], x["Usage"]), axis=1)
        
        # 1. SUMMARY METRICS
        total_inv = df["AvgInventory"].sum()
        total_usage = df["Usage"].sum()
        weighted_avg_days = calculate_turnover(total_inv, total_usage)

        m1, m2 = st.columns(2)
        label_inv = "Total Inventory Value" if "Value" in method else "Total Units in Stock"
        m1.metric(label_inv, f"{total_inv:,.0f}")
        m2.metric("Weighted Avg. Turnover", f"{weighted_avg_days} Days")

        # 2. PARETO ANALYSIS (Based on Inventory Amount)
        # Θέλουμε να δούμε ποια προϊόντα αποτελούν το μεγαλύτερο μέρος του αποθέματος
        df_pareto = df.sort_values(by="AvgInventory", ascending=False).copy()
        df_pareto["Weight %"] = (df_pareto["AvgInventory"] / total_inv * 100) if total_inv > 0 else 0
        df_pareto["Cumulative %"] = df_pareto["Weight %"].cumsum()

        st.subheader("📈 Pareto Analysis: Capital Concentration")
        st.caption("The chart shows which items represent the largest share of your inventory investment.")

        

        fig, ax1 = plt.subplots(figsize=(10, 5))
        ax1.bar(df_pareto["Name"], df_pareto["AvgInventory"], color="#2ca02c", label="Inventory Amount")
        ax1.set_ylabel("Inventory Amount")
        
        ax2 = ax1.twinx()
        ax2.plot(df_pareto["Name"], df_pareto["Cumulative %"], color="#d62728", marker="o", label="Cumulative %")
        ax2.axhline(y=80, color='black', linestyle='--', alpha=0.5)
        ax2.set_ylim(0, 110)
        ax2.set_ylabel("Cumulative %")
        
        st.pyplot(fig)

        # 3. DETAILED DATA TABLE
        st.subheader("📋 Analytical Breakdown")
        st.table(df_pareto.style.format({
            "AvgInventory": "{:,.2f}",
            "Usage": "{:,.2f}",
            "Weight %": "{:.1f}%",
            "Cumulative %": "{:.1f}%",
            "Turnover Days": "{:.1f}"
        }))

        # 4. MANAGERIAL VERDICT (Pareto Insight)
        st.divider()
        st.subheader("🧠 Managerial Verdict")
        
        # Identify "A" category items (Top 80% of investment)
        a_items = df_pareto[df_pareto["Cumulative %"] <= 85]["Name"].tolist()
        
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            st.write("**Key Investment Focus:**")
            st.write(f"The following items represent ~80% of your inventory: **{', '.join(a_items)}**.")
        
        with col_v2:
            # Check for "Dead Stock" candidates
            slow_movers = df_pareto[df_pareto["Turnover Days"] > (weighted_avg_days * 1.5)]["Name"].tolist()
            if slow_movers:
                st.warning(f"**Slow-Moving Alert:** These items have a turnover rate 50% slower than average: **{', '.join(slow_movers)}**.")
            else:
                st.success("**Turnover Balance:** No significant slow-movers detected relative to average.")

if __name__ == "__main__":
    show_inventory_turnover_calculator()
