import streamlit as st

def run_cash_cycle_app():
    st.header("💧 Cash Conversion Cycle")
    st.caption(
        "Measures how long your business finances operations before cash comes back in."
    )

    st.markdown(
        """
        This tool shows **how many days your capital is tied up** between paying suppliers  
        and collecting cash from customers.

        > A long cash cycle does **not** mean low profitability —  
        > it means **higher financing pressure**.
        """
    )

    st.markdown("---")

    # =================================================
    # INVENTORY SECTION
    # =================================================
    st.subheader("📦 Inventory & Production Time")
    st.caption("Time during which money is locked inside materials and production.")

    col1, col2 = st.columns(2)

    with col1:
        raw_materials_days = st.number_input(
            "Raw Materials Inventory Days",
            min_value=0,
            value=76,
            step=1
        )
        st.caption(
            "Average number of days raw materials stay in storage before entering production."
        )

        processing_days = st.number_input(
            "Production / Processing Days",
            min_value=0,
            value=37,
            step=1
        )
        st.caption(
            "Time required to convert raw materials into finished products."
        )

    with col2:
        finished_goods_days = st.number_input(
            "Finished Goods Inventory Days",
            min_value=0,
            value=42,
            step=1
        )
        st.caption(
            "Average days finished products remain in inventory before being sold."
        )

    st.markdown("---")

    # =================================================
    # CREDIT SECTION
    # =================================================
    st.subheader("💳 Credit Terms")
    st.caption("Timing differences between cash inflows and outflows.")

    col3, col4 = st.columns(2)

    with col3:
        receivables_days = st.number_input(
            "Accounts Receivable Days",
            min_value=0,
            value=73,
            step=1
        )
        st.caption(
            "Average number of days customers take to pay after the sale."
        )

    with col4:
        payables_days = st.number_input(
            "Accounts Payable Days",
            min_value=0,
            value=61,
            step=1
        )
        st.caption(
            "Average number of days you take to pay suppliers."
        )

    # =================================================
    # CALCULATION
    # =================================================
    cash_conversion_cycle = (
        raw_materials_days
        + processing_days
        + finished_goods_days
        + receivables_days
        - payables_days
    )

    st.markdown("---")

    # =================================================
    # RESULTS
    # =================================================
    st.subheader("🧮 Result")

    st.metric(
        label="Total Cash Conversion Cycle",
        value=f"{cash_conversion_cycle} days"
    )

    st.markdown(
        """
        **Interpretation**  
        This is the number of days your business must **self-finance operations**
        before cash returns from customers.
        """
    )

    # =================================================
    # DECISION GUIDANCE
    # =================================================
    if cash_conversion_cycle > 150:
        st.error(
            "🔴 Very long cash cycle.\n\n"
            "The business is highly dependent on external financing. "
            "Inventory reduction, faster collections, or longer supplier credit should be examined."
        )

    elif cash_conversion_cycle < 60:
        st.success(
            "🟢 Short and efficient cash cycle.\n\n"
            "Working capital pressure is low. "
            "The business converts operations into cash quickly."
        )

    else:
        st.warning(
            "🟠 Moderate cash cycle.\n\n"
            "The business operates within a normal range, "
            "but improvements in inventory or credit terms could free cash."
        )

    st.markdown("---")

    st.caption(
        "⚠️ This tool focuses on **liquidity timing**, not profitability. "
        "A profitable company can still fail if the cash cycle is too long."
    )
