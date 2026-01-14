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
    st.title("📦 Unit Production Cost Calculator")

    st.header("Input Data")

    sales_regular = st.number_input("Daily Sales (units – regular hours)", value=1000)
    sales_overtime = st.number_input("Daily Sales (units – overtime)", value=100)
    raw_material_cost = st.number_input("Daily Raw Material Cost (€)", value=1500.0)
    operating_cost_regular = st.number_input("Operating Cost (regular hours) (€)", value=4000.0)
    operating_cost_overtime = st.number_input("Operating Cost (overtime) (€)", value=400.0)
    labor_cost_regular = st.number_input("Labor Cost (regular hours) (€)", value=8000.0)
    labor_cost_overtime = st.number_input("Labor Cost (overtime) (€)", value=1200.0)

    if st.button("Calculate Costs"):
        avg_total, avg_regular, avg_overtime = calculate_unit_costs(
            sales_regular,
            sales_overtime,
            raw_material_cost,
            operating_cost_regular,
            operating_cost_overtime,
            labor_cost_regular,
            labor_cost_overtime
        )

        st.subheader("Results:")
        st.metric("🔹 Average Unit Cost (Total)", f"{avg_total:.2f} €")
        st.metric("🟢 Unit Cost (Regular Hours)", f"{avg_regular:.2f} €")
        st.metric("🕐 Unit Cost (Overtime Hours)", f"{avg_overtime:.2f} €")
