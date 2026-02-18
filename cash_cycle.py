import streamlit as st

def run_cash_cycle_app():
    st.header("💧 Cash Conversion Cycle (CCC) Analysis")
    st.caption("Strategic assessment of working capital efficiency and liquidity timing.")

    # SIDEBAR: Input Parameters
    with st.sidebar:
        st.header("Inventory Components")
        raw_materials_days = st.number_input(
            "Raw Materials (Days)", min_value=0, value=76, step=1
        )
        processing_days = st.number_input(
            "Production / Processing (Days)", min_value=0, value=37, step=1
        )
        finished_goods_days = st.number_input(
            "Finished Goods (Days)", min_value=0, value=42, step=1
        )

        st.divider()
        st.header("Credit Components")
        receivables_days = st.number_input(
            "Accounts Receivable (Days)", min_value=0, value=73, step=1
        )
        payables_days = st.number_input(
            "Accounts Payable (Days)", min_value=0, value=61, step=1
        )
        
        run_analysis = st.button("Calculate Cycle")

    # MAIN AREA: Logic & Results
    st.markdown(
        """
        The CCC measures the **time (in days)** your capital remains illiquid—locked between 
        disbursing cash to suppliers and collecting cash from sales.
        """
    )

    

    # Calculations
    # Operating Cycle = Inventory Days + Receivable Days
    inventory_days_total = raw_materials_days + processing_days + finished_goods_days
    operating_cycle = inventory_days_total + receivables_days
    cash_conversion_cycle = operating_cycle - payables_days

    if run_analysis:
        st.divider()
        st.subheader("🧮 Results & Metrics")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.metric("Inventory Period", f"{inventory_days_total} Days")
            st.caption("Total time in stock/production.")
            
        with col_res2:
            st.metric("Operating Cycle", f"{operating_cycle} Days")
            st.caption("Total time from order to payment.")

        with col_res3:
            st.metric("Cash Cycle (CCC)", f"{cash_conversion_cycle} Days", delta=None)
            st.caption("Self-financing requirement.")

        # Analytical Insight
        st.divider()
        st.subheader("🧠 Managerial Verdict")
        
        if cash_conversion_cycle > 150:
            st.error(
                f"**Critical Liquidity Pressure:** The business must self-finance operations for **{cash_conversion_cycle} days**. "
                "High dependency on external credit lines. Consider optimizing raw material safety stocks or accelerating collections."
            )
        elif cash_conversion_cycle < 60:
            st.success(
                f"**High Efficiency:** With a cycle of **{cash_conversion_cycle} days**, working capital turnover is fast. "
                "The business generates cash rapidly from its operations, reducing the need for debt."
            )
        else:
            st.warning(
                f"**Moderate Pressure:** A cycle of **{cash_conversion_cycle} days** is standard for many industries, "
                "but potential for cash liberation exists in shortening the processing phase."
            )

        # Strategic Breakdown Table
        st.subheader("📈 Strategic Breakdown")
        st.table({
            "Phase": ["Inventory Storage", "Production Time", "Sales Collection", "Supplier Credit (Offset)"],
            "Days": [raw_materials_days + finished_goods_days, processing_days, receivables_days, -payables_days]
        })

    else:
        st.info("👈 Adjust the cycle components in the sidebar and click 'Calculate Cycle'.")

if __name__ == "__main__":
    run_cash_cycle_app()
