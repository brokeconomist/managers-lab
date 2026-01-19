import streamlit as st
from discount_npv_logic import calculate_discount_npv
from utils import format_number_gr, format_percentage_gr

def show_discount_npv_ui():
    st.header("💳 Cash Discount – NPV Analysis")
    st.caption("Αξιολόγηση έκπτωσης με βάση την αξία του χρήματος στον χρόνο")

    # ---------- INPUTS ----------
    with st.form("discount_npv_form"):
        st.subheader("📈 Πωλήσεις")
        col1, col2 = st.columns(2)

        with col1:
            current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0, step=100.0)
            extra_sales = st.number_input("Επιπλέον Πωλήσεις από Έκπτωση (€)", value=250.0, step=50.0)

        with col2:
            discount_trial = st.number_input("Προτεινόμενη Έκπτωση (%)", value=2.0, step=0.1) / 100
            prc_clients_take_disc = st.number_input(
                "Πελάτες που παίρνουν έκπτωση (%)", value=40.0
            ) / 100

        st.subheader("⏱️ Όροι Πίστωσης")
        col3, col4 = st.columns(2)

        with col3:
            days_clients_take_discount = st.number_input(
                "Ημέρες πληρωμής (με έκπτωση)", value=60
            )
            new_days_cash_payment = st.number_input(
                "Νέες ημέρες πληρωμής (cash)", value=10
            )

        with col4:
            days_clients_no_discount = st.number_input(
                "Ημέρες πληρωμής (χωρίς έκπτωση)", value=120
            )
            avg_days_pay_suppliers = st.number_input(
                "Ημέρες πληρωμής προμηθευτών", value=30
            )

        st.subheader("💸 Κόστος Κεφαλαίου")
        col5, col6 = st.columns(2)

        with col5:
            cogs = st.number_input("COGS (€)", value=800.0)

        with col6:
            wacc = st.number_input("Κόστος Κεφαλαίου (WACC %)", value=20.0) / 100

        submitted = st.form_submit_button("📊 Υπολογισμός")

    # ---------- RESULTS ----------
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

        st.markdown("---")
        st.subheader("📊 Κύκλος Είσπραξης")

        r1, r2, r3 = st.columns(3)
        r1.metric("Τρέχων ACP", f"{results['avg_current_collection_days']} ημέρες")
        r2.metric("Νέος ACP", f"{results['new_avg_collection_period']} ημέρες")
        r3.metric("Απελευθερωμένο Κεφάλαιο", format_number_gr(results['free_capital']))

        st.subheader("💰 Οικονομική Επίδραση")
        r4, r5, r6 = st.columns(3)
        r4.metric("Κέρδος από Πωλήσεις", format_number_gr(results['profit_from_extra_sales']))
        r5.metric("Κέρδος από Κεφάλαιο", format_number_gr(results['profit_from_free_capital']))
        r6.metric("Κόστος Έκπτωσης", format_number_gr(results['discount_cost']))

        st.markdown("---")
        st.metric("📌 Καθαρή Παρούσα Αξία (NPV)", format_number_gr(results["npv"]))

        if results["npv"] > 0:
            st.success("✅ Η πολιτική έκπτωσης δημιουργεί αξία")
        else:
            st.error("❌ Η πολιτική έκπτωσης καταστρέφει αξία")

        with st.expander("📉 Όρια & Βελτιστοποίηση"):
            st.write(f"Μέγιστη Έκπτωση (NPV = 0): {format_percentage_gr(results['max_discount'])}")
            st.write(f"Βέλτιστη Έκπτωση: {format_percentage_gr(results['optimum_discount'])}")
