import streamlit as st

def calculate_unit_costs(
    sales_regular,
    sales_overtime,
    raw_material_cost,
    operating_cost_regular,
    operating_cost_overtime,
    labor_cost_regular,
    labor_cost_overtime,
):
    total_units = sales_regular + sales_overtime
    total_cost = (
        raw_material_cost +
        operating_cost_regular +
        operating_cost_overtime +
        labor_cost_regular +
        labor_cost_overtime
    )

    avg_cost_total = total_cost / total_units if total_units != 0 else 0

    avg_cost_regular = (
        (labor_cost_regular / sales_regular) +
        (operating_cost_regular / sales_regular) +
        (raw_material_cost / total_units)
        if sales_regular != 0 else 0
    )

    avg_cost_overtime = (
        (labor_cost_overtime / sales_overtime) +
        (operating_cost_overtime / sales_overtime) +
        (raw_material_cost / total_units)
        if sales_overtime != 0 else 0
    )

    return avg_cost_total, avg_cost_regular, avg_cost_overtime


def show_unit_cost_app():
    st.header("📦 Unit Production Cost Analysis")
    st.caption(
        "Υπολογισμός μοναδιαίου κόστους παραγωγής, με διάκριση "
        "μεταξύ κανονικού ωραρίου και υπερωριών."
    )

    # ================= INPUTS =================
    with st.form("unit_cost_form"):
        st.subheader("📊 Παραγωγή (μονάδες)")

        col1, col2 = st.columns(2)
        with col1:
            sales_regular = st.number_input(
                "Παραγωγή σε κανονικό ωράριο (μονάδες / ημέρα)",
                value=1000
            )
        with col2:
            sales_overtime = st.number_input(
                "Παραγωγή σε υπερωρίες (μονάδες / ημέρα)",
                value=100
            )

        st.subheader("💸 Κόστος Πρώτων Υλών")
        raw_material_cost = st.number_input(
            "Συνολικό ημερήσιο κόστος πρώτων υλών (€)",
            value=1500.0
        )

        st.subheader("🏭 Λειτουργικό & Εργατικό Κόστος")

        col3, col4 = st.columns(2)
        with col3:
            operating_cost_regular = st.number_input(
                "Λειτουργικό κόστος (κανονικό ωράριο) (€)",
                value=4000.0
            )
            labor_cost_regular = st.number_input(
                "Εργατικό κόστος (κανονικό ωράριο) (€)",
                value=8000.0
            )

        with col4:
            operating_cost_overtime = st.number_input(
                "Λειτουργικό κόστος (υπερωρίες) (€)",
                value=400.0
            )
            labor_cost_overtime = st.number_input(
                "Εργατικό κόστος (υπερωρίες) (€)",
                value=1200.0
            )

        submitted = st.form_submit_button("📐 Υπολογισμός Κόστους")

    # ================= RESULTS =================
    if submitted:
        avg_total, avg_regular, avg_overtime = calculate_unit_costs(
            sales_regular,
            sales_overtime,
            raw_material_cost,
            operating_cost_regular,
            operating_cost_overtime,
            labor_cost_regular,
            labor_cost_overtime
        )

        st.markdown("---")
        st.subheader("🧮 Αποτελέσματα Κόστους")

        r1, r2, r3 = st.columns(3)
        r1.metric(
            "Μέσο Μοναδιαίο Κόστος (σύνολο)",
            f"{avg_total:.2f} €"
        )
        r2.metric(
            "Μοναδιαίο Κόστος – Κανονικό Ωράριο",
            f"{avg_regular:.2f} €"
        )
        r3.metric(
            "Μοναδιαίο Κόστος – Υπερωρίες",
            f"{avg_overtime:.2f} €"
        )

        st.markdown(
            "ℹ️ **Ερμηνεία:** Το κόστος πρώτων υλών κατανέμεται σε όλες τις μονάδες, "
            "ενώ το εργατικό και λειτουργικό κόστος επιβαρύνει ξεχωριστά "
            "την κανονική παραγωγή και τις υπερωρίες."
        )
