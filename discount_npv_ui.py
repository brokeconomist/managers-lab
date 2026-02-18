import streamlit as st
from decimal import Decimal, getcontext
import pandas as pd

# --- CALCULATION LOGIC (UNCHANGED) ---
def calculate_discount_npv(
    current_sales, extra_sales, discount_trial, prc_clients_take_disc,
    days_curently_paying_clients_take_discount, days_curently_paying_clients_not_take_discount,
    new_days_payment_clients_take_disc, cogs, wacc, avg_days_pay_suppliers
):
    getcontext().prec = 20

    prc_clients_not_take_disc = 1 - prc_clients_take_disc
    avg_current_collection_days = (
        prc_clients_take_disc * days_curently_paying_clients_take_discount +
        prc_clients_not_take_disc * days_curently_paying_clients_not_take_discount
    )
    current_receivables = current_sales * avg_current_collection_days / 365

    total_sales = current_sales + extra_sales
    prcnt_new_policy = ((current_sales * prc_clients_take_disc) + extra_sales) / total_sales
    prcnt_old_policy = 1 - prcnt_new_policy

    new_avg_collection_period = (
        prcnt_new_policy * new_days_payment_clients_take_disc +
        prcnt_old_policy * days_curently_paying_clients_not_take_discount
    )
    new_receivables = total_sales * new_avg_collection_period / 365
    free_capital = current_receivables - new_receivables

    profit_from_extra_sales = extra_sales * (1 - cogs / current_sales)
    profit_from_free_capital = free_capital * wacc
    discount_cost = total_sales * prcnt_new_policy * discount_trial

    i = wacc / 365

    inflow = (
        total_sales * prcnt_new_policy * (1 - discount_trial) /
        ((1 + i) ** new_days_payment_clients_take_disc)
    )
    inflow += total_sales * prcnt_old_policy / ((1 + i) ** days_curently_paying_clients_not_take_discount)

    outflow = (
        (cogs / current_sales) * (extra_sales / current_sales) * current_sales /
        ((1 + i) ** avg_days_pay_suppliers)
    )
    outflow += current_sales / ((1 + i) ** avg_current_collection_days)

    npv = inflow - outflow

    max_discount = 1 - (
        (1 + i) ** (new_days_payment_clients_take_disc - days_curently_paying_clients_not_take_discount) * (
            (1 - 1 / prcnt_new_policy) + (
                (1 + i) ** (days_curently_paying_clients_not_take_discount - avg_current_collection_days) +
                (cogs / current_sales) * (extra_sales / current_sales) *
                (1 + i) ** (days_curently_paying_clients_not_take_discount - avg_days_pay_suppliers)
            ) / (prcnt_new_policy * (1 + extra_sales / current_sales))
        )
    )

    optimum_discount = (1 - ((1 + i) ** (new_days_payment_clients_take_disc - avg_current_collection_days))) / 2

    return {
        "avg_current_collection_days": round(avg_current_collection_days, 2),
        "current_receivables": round(current_receivables, 2),
        "prcnt_new_policy": round(prcnt_new_policy, 4),
        "prcnt_old_policy": round(prcnt_old_policy, 4),
        "new_avg_collection_period": round(new_avg_collection_period, 2),
        "new_receivables": round(new_receivables, 2),
        "free_capital": round(free_capital, 2),
        "profit_from_extra_sales": round(profit_from_extra_sales, 2),
        "profit_from_free_capital": round(profit_from_free_capital, 2),
        "discount_cost": round(discount_cost, 2),
        "npv": round(npv, 2),
        "max_discount": round(max_discount * 100, 2),
        "optimum_discount": round(optimum_discount * 100, 2),
    }

# --- UI ---
def show_discount_npv_ui():
    st.header("💳 Cash Discount – Strategic NPV Analysis")
    st.write("Analyze how early payment discounts affect Liquidity, DSO, and Net Present Value.")

    # SIDEBAR: Parameters
    with st.sidebar:
        st.subheader("📈 Core Financials")
        current_sales = st.number_input("Current Annual Sales ($)", value=1000.0)
        extra_sales = st.number_input("Extra Sales from Discount ($)", value=250.0)
        cogs = st.number_input("Total COGS ($)", value=800.0)
        wacc = st.number_input("WACC (%)", value=20.0) / 100

        st.divider()
        st.subheader("🎯 Discount Strategy")
        discount_trial = st.number_input("Proposed Discount (%)", value=2.0) / 100
        prc_clients_take_disc = st.number_input("% Revenue Taking Discount", value=40.0) / 100
        new_days_cash_payment = st.number_input("Target Discount Days", value=10)
        avg_days_pay_suppliers = st.number_input("Supplier Payment Days", value=30)

        st.divider()
        st.subheader("📊 Revenue Segmentation")
        fast_pct = st.number_input("Fast Payers (%)", value=30.0) / 100
        fast_dso = st.number_input("Fast DSO (days)", value=60)
        
        med_pct = st.number_input("Medium Payers (%)", value=40.0) / 100
        med_dso = st.number_input("Medium DSO (days)", value=90)
        
        slow_pct = st.number_input("Slow Payers (%)", value=30.0) / 100
        slow_dso = st.number_input("Slow DSO (days)", value=120)

        allocation_mode = st.radio(
            "Targeting Strategy",
            ["Proportional", "Slow Payers First", "Fast Payers First"]
        )

        run = st.button("Calculate Policy Impact")

    # MAIN SCREEN
    if run:
        # Validate Segmentation
        if abs((fast_pct + med_pct + slow_pct) - 1.0) > 0.01:
            st.error("Revenue segmentation must sum to 100%. Check sidebar.")
            return

        # Logic for weighted DSO calculation
        segments = [
            {"pct": fast_pct, "dso": fast_dso},
            {"pct": med_pct, "dso": med_dso},
            {"pct": slow_pct, "dso": slow_dso},
        ]
        if allocation_mode == "Slow Payers First":
            segments.sort(key=lambda x: x["dso"], reverse=True)
        elif allocation_mode == "Fast Payers First":
            segments.sort(key=lambda x: x["dso"])

        remaining = prc_clients_take_disc
        weighted_take_dso = 0
        weighted_no_take_dso = 0

        for seg in segments:
            take_from_seg = min(seg["pct"], remaining)
            not_take_from_seg = seg["pct"] - take_from_seg
            weighted_take_dso += take_from_seg * seg["dso"]
            weighted_no_take_dso += not_take_from_seg * seg["dso"]
            remaining -= take_from_seg

        effective_days_take = weighted_take_dso / prc_clients_take_disc if prc_clients_take_disc > 0 else 0
        effective_days_no_take = weighted_no_take_dso / (1 - prc_clients_take_disc) if prc_clients_take_disc < 1 else 0

        results = calculate_discount_npv(
            current_sales, extra_sales, discount_trial, prc_clients_take_disc,
            effective_days_take, effective_days_no_take,
            new_days_cash_payment, cogs, wacc, avg_days_pay_suppliers
        )

        # 1. Executive Summary Metrics
        st.subheader("📊 Policy Efficiency Indicators")
        m1, m2, m3 = st.columns(3)
        m1.metric("DSO Improvement", f"{results['avg_current_collection_days']} → {results['new_avg_collection_period']}", 
                  f"{results['new_avg_collection_period'] - results['avg_current_collection_days']:.1f} days")
        m2.metric("Capital Released", f"${results['free_capital']:,.2f}")
        m3.metric("Incremental Sales Profit", f"${results['profit_from_extra_sales']:,.2f}")

        # 2. Financial Components (T-Account Style)
        st.divider()
        st.subheader("💰 Cash Flow Components")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.write("**Gains (+)**")
            st.success(f"Released Capital Yield: ${results['profit_from_free_capital']:,.2f}")
            st.success(f"Extra Sales Margin: ${results['profit_from_extra_sales']:,.2f}")
        
        with c2:
            st.write("**Costs (-)**")
            st.error(f"Cost of Discounts: ${results['discount_cost']:,.2f}")
        
        with c3:
            st.write("**Net Result**")
            npv_color = "green" if results['npv'] > 0 else "red"
            st.markdown(f"<h3 style='color:{npv_color};'>NPV: ${results['npv']:,.2f}</h3>", unsafe_allow_html=True)

        # 3. Decision Visuals
        st.divider()
        st.subheader("🧠 Strategic Decision Support")
        
        
        
        if results['npv'] > 0:
            st.success("✅ **Value Creator:** The discount policy improves the cash cycle enough to justify the margin loss.")
        else:
            st.error("❌ **Value Destroyer:** The cost of the discount outweighs the benefit of faster collection and extra sales.")

        # 4. Optimization Table
        st.subheader("📉 Structural Thresholds")
        st.table(pd.DataFrame({
            "Metric": ["Max Sustainable Discount", "Mathematically Optimal Discount"],
            "Value": [f"{results['max_discount']}%", f"{results['optimum_discount']}%"]
        }))
        
        st.info("""
        **Analytical Note:** Max Sustainable Discount is the point where NPV = 0. 
        Beyond this percentage, you are paying more for the cash than it costs you to borrow it (WACC).
        """)

if __name__ == "__main__":
    show_discount_npv_ui()
