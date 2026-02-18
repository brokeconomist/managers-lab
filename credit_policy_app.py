import streamlit as st

# -------------------------------------------------
# Formatting Helpers
# -------------------------------------------------
def format_currency(value, decimals=2):
    try:
        formatted = f"{value:,.{decimals}f}"
        return f"€ {formatted}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return f"€ {value}"

# -------------------------------------------------
# MAIN APP
# -------------------------------------------------
def show_credit_policy_analysis():
    st.header("🧾 Credit Policy Impact (Accounting View)")
    st.write("Quantitative assessment of loosening credit terms to drive volume.")

    # SIDEBAR: Strategic Inputs
    with st.sidebar:
        st.header("📍 Policy Parameters")
        
        with st.expander("Current State", expanded=True):
            current_sales = st.number_input("Annual Sales (€)", value=20000000.0)
            current_cash_pct = st.slider("Current Cash Sales (%)", 0, 100, 50) / 100
            current_credit_days = st.number_input("Current Credit Days", value=60)
        
        with st.expander("Proposed Change", expanded=True):
            sales_inc_pct = st.slider("Expected Sales Increase (%)", 0, 100, 20) / 100
            new_cash_pct = st.slider("New Cash Sales (%)", 0, 100, 20) / 100
            new_credit_days = st.number_input("New Credit Days", value=90)
            bad_debt_pct = st.slider("Expected Bad Debts (%)", 0.0, 20.0, 2.0) / 100

        with st.expander("Cost Structure", expanded=False):
            unit_price = st.number_input("Unit Selling Price (€)", value=20.0)
            total_unit_cost = st.number_input("Total Unit Cost (€)", value=18.0)
            variable_unit_cost = st.number_input("Variable Unit Cost (€)", value=14.0)
            wacc = st.number_input("Cost of Capital (%)", value=10.0) / 100

        run = st.button("Calculate Policy Impact")

    # MAIN SCREEN: Analysis
    if not run:
        st.info("💡 Adjust the policy parameters in the sidebar and click 'Calculate' to see the impact on operating profit.")
        return

    # --- CALCULATION LOGIC ---
    base_units = current_sales / unit_price
    increased_units = base_units * sales_inc_pct
    total_new_units = base_units + increased_units

    # 1. Incremental Profit
    profit_increase = increased_units * (unit_price - variable_unit_cost)

    # 2. Capital Lock-up Cost
    avg_cost_per_unit = (
        (base_units * total_unit_cost) + (increased_units * variable_unit_cost)
    ) / total_new_units

    current_credit_sales = current_sales * (1 - current_cash_pct)
    new_credit_sales = (current_sales * (1 + sales_inc_pct)) * (1 - new_cash_pct)

    capital_in_receivables_new = (new_credit_sales / (365 / new_credit_days)) * (avg_cost_per_unit / unit_price)
    capital_in_receivables_old = (current_credit_sales / (365 / current_credit_days)) * (total_unit_cost / unit_price)
    
    financial_cost = (capital_in_receivables_new - capital_in_receivables_old) * wacc

    # 3. Risk Cost
    bad_debts_cost = (current_sales * (1 + sales_inc_pct)) * bad_debt_pct

    # Final Result
    total_extra_costs = financial_cost + bad_debts_cost
    net_impact = profit_increase - total_extra_costs

    # --- DISPLAY RESULTS ---
    st.divider()
    st.subheader("📊 Decision Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Incremental Profit", format_currency(profit_increase))
    col2.metric("Extra Risk & Funding", format_currency(total_extra_costs), delta_color="inverse")
    col3.metric("Net Operational Impact", format_currency(net_impact))

    

    st.divider()
    st.subheader("🧠 Cold Analysis Verdict")

    if net_impact > 0:
        st.success(f"✅ **GO:** The credit expansion is justified. For every €1 of extra cost, you generate €{profit_increase/total_extra_costs:.2f} in margin.")
    else:
        st.error("❌ **NO-GO:** Loosening credit destroys value. The financing of the 'float' and the default risk outweigh the gains from volume.")

    with st.expander("View Detailed Cost Breakdown"):
        st.write(f"**Capital Tied in Receivables (New):** {format_currency(capital_in_receivables_new)}")
        st.write(f"**Capital Tied in Receivables (Old):** {format_currency(capital_in_receivables_old)}")
        st.write(f"**Annual Opportunity Cost of Capital:** {format_currency(financial_cost)}")
        st.write(f"**Projected Bad Debt Expense:** {format_currency(bad_debts_cost)}")

    st.caption("ℹ️ Accounting View: This model assumes linear costs and fixed default rates across the new sales volume.")

if __name__ == "__main__":
    show_credit_policy_analysis()

