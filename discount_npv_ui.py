import streamlit as st
from discount_npv_logic import calculate_discount_npv
from utils import format_number_gr, format_percentage_gr

def show_discount_npv_ui():
    st.header("💳 Cash Discount – NPV Analysis")
    st.caption("Αξιολόγηση έκπτωσης με βάση την αξία του χρήματος στον χρόνο")

    # ===== Sidebar Inputs =====
    st.sidebar.subheader("📈 Πωλήσεις")
    current_sales = st.sidebar.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0, step=100.0)
    extra_sales = st.sidebar.number_input("Επιπλέον Πωλήσεις από Έκπτωση (€)", value=250.0, step=50.0)

    st.sidebar.subheader("🎯 Έκπτωση & Πελάτες")
    discount_trial = st.sidebar.number_input("Προτεινόμενη Έκπτωση (%)", value=2.0, step=0.1) / 100
    prc_clients_take_disc = st.sidebar.number_input("Πελάτες που παίρνουν έκπτωση (%)", value=40.0) / 100

    st.sidebar.subheader("⏱️ Ημέρες Πίστωσης")
    days_clients_take_discount = st.sidebar.number_input("Ημέρες πληρωμής (με έκπτωση)", value=60)
    days_clients_no_discount = st.sidebar.number_input("Ημέρες πληρωμής (χωρίς έκπτωση)", value=120)
    new_days_cash_payment = st.sidebar.number_input("Νέες ημέρες πληρωμής (cash)", value=10)

    st.sidebar.subheader("💸 Κόστος & Χρηματοδότηση")
    cogs = st.sidebar.number_input("COGS (€)", value=800.0)
    wacc = st.sidebar.number_input("Κόστος Κεφαλαίου (WACC %)", value=20.0) / 100
    avg_days_pay_suppliers = st.sidebar.number_input("Ημέρες πληρωμής προμηθευτών", value=30)

    if st.sidebar.button("Υπολογισμός"):
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

        st.subheader("📊 Κύκλος Είσπραξης")
        col1, col2, col3 = st.columns(3)
        col1.metric("Τρέχων ACP", f"{results['avg_current_collection_days']} ημέρες")
        col2.metric("Νέος ACP", f"{results['new_avg_collection_period']} ημέρες")
        col3.metric("Απελευθερωμένο Κεφάλαιο", format_number_gr(results['free_capital']))

        st.subheader("💰 Οικονομική Επίδραση")
        col4, col5, col6 = st.columns(3)
        col4.metric("Κέρδος από Πωλήσεις", format_number_gr(results['profit_from_extra_sales']))
        col5.metric("Κέρδος από Κεφάλαιο", format_number_gr(results['profit_from_free_capital']))
        col6.metric("Κόστος Έκπτωσης", format_number_gr(results['discount_cost']))

        st.markdown("---")
        st.metric(
            "📌 Καθαρή Παρούσα Αξία (NPV)",
            format_number_gr(results["npv"])
        )

        if results["npv"] > 0:
            st.success("✅ Η πολιτική έκπτωσης δημιουργεί αξία")
        else:
            st.error("❌ Η πολιτική έκπτωσης καταστρέφει αξία")

        with st.expander("📉 Όρια & Βελτιστοποίηση"):
            st.write(f"Μέγιστη Έκπτωση (NPV = 0): {format_percentage_gr(results['max_discount'])}")
            st.write(f"Βέλτιστη Έκπτωση: {format_percentage_gr(results['optimum_discount'])}")
