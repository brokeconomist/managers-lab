import streamlit as st

# -------------------------------------------------
# Formatting
# -------------------------------------------------
def format_currency(value, decimals=2):
    try:
        formatted = f"{value:,.{decimals}f}"
        return f"€ {formatted}"
    except Exception:
        return f"€ {value}"


# -------------------------------------------------
# MAIN APP
# -------------------------------------------------
def show_credit_policy_analysis():
    st.header("🧾 Credit Policy Impact (Accounting View)")
    st.caption(
        "Evaluates whether expanding customer credit increases profits "
        "using operational and accounting logic."
    )

    st.markdown(
        """
        This tool answers a **simple managerial question**:

        > *If I loosen my credit policy, will the extra sales cover  
        > the extra risk and financing cost — **without financial modeling**?*

        It is **not** a valuation tool.  
        It is a **go / no-go operating decision**.
        """
    )

    st.markdown("---")

    # =================================================
    # CURRENT POLICY
    # =================================================
    st.subheader("📍 Current Credit Policy")
    st.caption("How sales are structured today.")

    with st.form("credit_policy_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_cash = (
                st.number_input(
                    "Cash Sales (%) – Current",
                    min_value=0.0,
                    max_value=100.0,
                    value=50.0
                ) / 100
            )
            st.caption("Share of sales paid immediately.")

            current_credit_pct = (
                st.number_input(
                    "Credit Sales (%) – Current",
                    min_value=0.0,
                    max_value=100.0,
                    value=50.0
                ) / 100
            )
            st.caption("Share of sales sold on credit.")

        with col2:
            current_credit_days = st.number_input(
                "Credit Days – Current",
                min_value=0,
                value=60
            )
            st.caption("Average collection period for current credit sales.")

        st.markdown("---")

        # =================================================
        # PROPOSED POLICY
        # =================================================
        st.subheader("🆕 Proposed Credit Policy")
        st.caption("What changes you are considering.")

        col3, col4 = st.columns(2)

        with col3:
            new_cash = (
                st.number_input(
                    "Cash Sales (%) – New",
                    min_value=0.0,
                    max_value=100.0,
                    value=20.0
                ) / 100
            )
            st.caption("Expected cash share after the policy change.")

            new_credit_pct = (
                st.number_input(
                    "Credit Sales (%) – New",
                    min_value=0.0,
                    max_value=100.0,
                    value=80.0
                ) / 100
            )
            st.caption("Expected credit share after the policy change.")

        with col4:
            new_credit_days = st.number_input(
                "Credit Days – New",
                min_value=0,
                value=90
            )
            st.caption("New average collection period.")

        st.markdown("---")

        # =================================================
        # SALES & COST DATA
        # =================================================
        st.subheader("📈 Sales & Cost Structure")
        st.caption("Used to estimate incremental profit and risk.")

        sales_increase = (
            st.number_input(
                "Expected Sales Increase (%)",
                min_value=0.0,
                value=20.0
            ) / 100
        )
        st.caption("Expected volume increase due to looser credit.")

        current_sales = st.number_input(
            "Current Annual Sales (€)",
            min_value=0.0,
            value=20_000_000.0
        )

        unit_price = st.number_input(
            "Unit Selling Price (€)",
            min_value=0.01,
            value=20.0
        )

        total_unit_cost = st.number_input(
            "Total Unit Cost (€)",
            min_value=0.01,
            value=18.0
        )
        st.caption("Includes fixed + variable components.")

        variable_unit_cost = st.number_input(
            "Variable Unit Cost (€)",
            min_value=0.01,
            value=14.0
        )

        expected_bad_debts = (
            st.number_input(
                "Expected Bad Debts (%)",
                min_value=0.0,
                max_value=100.0,
                value=2.0
            ) / 100
        )
        st.caption("Estimated default rate on credit sales.")

        interest_rate = (
            st.number_input(
                "Cost of Capital (% per year)",
                min_value=0.0,
                max_value=100.0,
                value=10.0
            ) / 100
        )
        st.caption("Opportunity cost of capital tied in receivables.")

        submitted = st.form_submit_button("Run Credit Decision Check")

    # =================================================
    # CALCULATION (UNCHANGED LOGIC)
    # =================================================
    if submitted:
        base_units = current_sales / unit_price
        increased_units = base_units * sales_increase

        profit_increase = increased_units * (unit_price - variable_unit_cost)

        avg_cost_per_unit = (
            ((base_units * total_unit_cost) +
             (increased_units * variable_unit_cost))
            / (base_units + increased_units)
        )

        new_credit_sales = (current_sales * (1 + new_cash)) * new_credit_pct
        current_credit_sales = current_sales * current_cash

        capital_cost_new = (
            new_credit_sales / (360 / new_credit_days)
        ) * (avg_cost_per_unit / unit_price)

        capital_cost_current = (
            current_credit_sales / (360 / current_credit_days)
        ) * (total_unit_cost / unit_price)

        capital_cost_difference = capital_cost_new - capital_cost_current
        financial_cost = capital_cost_difference * interest_rate

        bad_debts_cost = (
            current_sales * expected_bad_debts
            + current_sales * expected_bad_debts * sales_increase
        )

        total_cost = financial_cost + bad_debts_cost
        anticipated_gain = profit_increase - total_cost

        # =================================================
        # RESULTS
        # =================================================
        st.markdown("---")
        st.subheader("📊 Decision Outcome")

        st.metric(
            "Incremental Operating Profit",
            format_currency(profit_increase)
        )

        st.metric(
            "Additional Financing & Risk Cost",
            format_currency(total_cost)
        )

        st.metric(
            "Net Impact",
            format_currency(anticipated_gain)
        )

        if anticipated_gain > 0:
            st.success(
                "✅ Credit expansion is justified **from an accounting perspective**.\n\n"
                "Additional sales cover financing costs and bad debt risk."
            )
        else:
            st.error(
                "❌ Credit expansion destroys value at the operating level.\n\n"
                "Higher risk and capital lock-up exceed the profit from extra sales."
            )

        st.caption(
            "ℹ️ This result ignores time value of money. "
            "Use the **Credit Policy – Present Value** tool for financial valuation."
        )
