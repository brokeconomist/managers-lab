# discount_npv_ui.py
import streamlit as st
from discount_npv_logic import calculate_discount_npv
from utils import format_number_gr, format_percentage_gr

def show_discount_npv_ui():
    st.title("Cash Discount NPV Analysis")

    with st.form("discount_npv_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_sales = st.number_input("Current Sales (€)", value=1000.0, step=100.0)
            extra_sales = st.number_input("Extra Sales from Discount (€)", value=250.0, step=50.0)
            discount_trial = st.number_input("Proposed Discount (%)", value=2.0, step=0.1) / 100
            prc_clients_take_disc = st.number_input("% of Customers Accepting Discount", value=40.0, step=1.0) / 100
            days_clients_take_discount = st.number_input("Payment Days for Discount Customers", value=60, step=1)

        with col2:
            days_clients_no_discount = st.number_input("Payment Days for Non-Discount Customers", value=120, step=1)
            new_days_cash_payment = st.number_input("New Cash Payment Days for Discount", value=10, step=1)
            cogs = st.number_input("Cost of Goods Sold (€)", value=800.0, step=100.0)
            wacc = st.number_input("Capital Cost (WACC %)", value=20.0, step=0.1) / 100
            avg_days_pay_suppliers = st.number_input("Average Supplier Payment Days", value=30, step=1)

        submitted = st.form_submit_button("Calculate")

    if submitted:
        results = calculate_discount_npv(
            current_sales,
            extra_sales,
            discount_trial,
            prc_clients_take_disc,
            days_clients_take_discount,
            days_clients_no_discount,
            new_days_cash_payment,
            cogs,
            wacc,
            avg_days_pay_suppliers
        )

        st.subheader("Results")
        st.write(f"Average Collection Period (Current): {results['avg_current_collection_days']} days")
        st.write(f"Current Receivables: {format_number_gr(results['current_receivables'])} €")
        st.write(f"New Average Collection Period: {results['new_avg_collection_period']} days")
        st.write(f"New Receivables: {format_number_gr(results['new_receivables'])} €")
        st.write(f"Released Capital: {format_number_gr(results['free_capital'])} €")
        st.write(f"Profit from Extra Sales: {format_number_gr(results['profit_from_extra_sales'])} €")
        st.write(f"Profit from Released Capital: {format_number_gr(results['profit_from_free_capital'])} €")
        st.write(f"Discount Cost: {format_number_gr(results['discount_cost'])} €")
        st.markdown("---")
        st.write(f"💰 **Net Present Value (NPV): {format_number_gr(results['npv'])} €**")
        st.write(f"📉 **Maximum Discount (Break-Even NPV): {format_percentage_gr(results['max_discount'])}**")
        st.write(f"📈 **Optimal Discount: {format_percentage_gr(results['optimum_discount'])}**")
