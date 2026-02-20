import streamlit as st
from decimal import Decimal, getcontext
import pandas as pd

# --- CALCULATION LOGIC (Preserving your exact logic) ---
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

    # Threshold & Optimum Calculations
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
        "new_avg_collection_period": round(new_avg_collection_period, 2),
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
    st.info("Analyze the trade-off between margin loss (discount) and cash acceleration.")

    # 1. PARAMETERS IN COLUMNS (To avoid sidebar menu conflict)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Core Financials")
        # Τραβάμε τα defaults από το session_state αν υπάρχουν
        cur_p = st.session_state.get('price', 1.0)
        cur_q = st.session_state.get('volume', 1000.0)
        cur_sales = cur_p * cur_q
        
        current_sales = st.number_input("Current Annual Sales (€)", value=float(cur_sales))
        extra_sales = st.number_input("Extra Sales from Discount (€)", value=cur_sales * 0.1)
        cogs = st.number_input("Total COGS (€)", value=cur_sales * 0.7)
        wacc = st.number_input("Cost of Capital / WACC (%)", value=15.0) / 100

    with col2:
        st.subheader("🎯 Discount Strategy")
        discount_trial = st.number_input("Proposed Discount (%)", value=2.0) / 100
        prc_clients_take_disc = st.number_input("% Revenue Expected to Take Discount", value=40.0) / 100
        new_days_cash_payment = st.number_input("Target Discount Days (e.g., 10 days)", value=10)
        avg_days_pay_suppliers = st.number_input("Supplier Payment Days", value=30)

    st.divider()
    st.subheader("📊 Current Receivable Segmentation")
    s1, s2, s3 = st.columns(3)
    with s1:
        fast_pct = st.number_input("Fast Payers (%)", value=30.0) / 100
        fast_dso = st.number_input("Fast DSO (days)", value=45)
    with s2:
        med_pct = st.number_input("Med Payers (%)", value=40.0) / 100
        med_dso = st.number_input("Med DSO (days)", value=75)
    with s3:
        slow_pct = st.number_input("Slow Payers (%)", value=30.0) / 100
        slow_dso = st.number_input("Slow DSO (days)", value=120)

    allocation_mode = st.radio("Targeting Logic", ["Proportional", "Slow Payers First", "Fast Payers First"], horizontal=True)

    if st.button("🚀 Calculate Policy Impact", use_container_width=True):
        if abs((fast_pct + med_pct + slow_pct) - 1.0) > 0.01:
            st.error("Segmentation must sum to 100%.")
            return

        # Segmentation Logic
        segments = [{"pct": fast_pct, "dso": fast_dso}, {"pct": med_pct, "dso": med_dso}, {"pct": slow_pct, "dso": slow_dso}]
        if allocation_mode == "Slow Payers First": segments.sort(key=lambda x: x["dso"], reverse=True)
        elif allocation_mode == "Fast Payers First": segments.sort(key=lambda x: x["dso"])

        remaining = prc_clients_take_disc
        weighted_take_dso = 0
        weighted_no_take_dso = 0
        for seg in segments:
            take = min(seg["pct"], remaining)
            weighted_take_dso += take * seg["dso"]
            weighted_no_take_dso += (seg["pct"] - take) * seg["dso"]
            remaining -= take

        eff_take = weighted_take_dso / prc_clients_take_disc if prc_clients_take_disc > 0 else 0
        eff_no_take = weighted_no_take_dso / (1 - prc_clients_take_disc) if prc_clients_take_disc < 1 else 0

        res = calculate_discount_npv(current_sales, extra_sales, discount_trial, prc_clients_take_disc, 
                                     eff_take, eff_no_take, new_days_cash_payment, cogs, wacc, avg_days_pay_suppliers)

        # RESULTS
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("DSO Shift", f"{res['avg_current_collection_days']} → {res['new_avg_collection_period']}", f"{res['new_avg_collection_period'] - res['avg_current_collection_days']:.1f} days")
        m2.metric("Cash Released", f"{res['free_capital']:,.2f} €")
        m3.metric("NPV Outcome", f"{res['npv']:,.2f} €", delta="Value Creation" if res['npv']>0 else "Value Loss")

        # Visual Breakdown
        b1, b2 = st.columns(2)
        with b1:
            st.write("### 💎 Gains")
            st.write(f"Capital Yield: {res['profit_from_free_capital']:,.2f} €")
            st.write(f"Extra Margin: {res['profit_from_extra_sales']:,.2f} €")
        with b2:
            st.write("### 📉 Costs")
            st.write(f"Discount Cost: {res['discount_cost']:,.2f} €")
            st.error(f"Net Result: {res['npv']:,.2f} €")

        st.divider()
        st.subheader("🧠 Threshold Analysis")
        st.table(pd.DataFrame({
            "Indicator": ["Max Sustainable Discount", "Mathematically Optimal Discount"],
            "Value": [f"{res['max_discount']}%", f"{res['optimum_discount']}%"]
        }))
        
        if res['npv'] > 0:
            st.success("✅ **Verdict:** The policy is financially sound. The benefit of liquidity outweighs the margin cost.")
        else:
            st.error("❌ **Verdict:** Reject policy. The discount is too expensive compared to your cost of capital.")
