import streamlit as st
import pandas as pd

# -------------------------------------------------
# Calculation Logic
# -------------------------------------------------
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

    # Unit Cost Regular
    avg_cost_regular = (
        (labor_cost_regular / sales_regular) +
        (operating_cost_regular / sales_regular) +
        (raw_material_cost / total_units)
        if sales_regular != 0 else 0
    )

    # Unit Cost Overtime
    avg_cost_overtime = (
        (labor_cost_overtime / sales_overtime) +
        (operating_cost_overtime / sales_overtime) +
        (raw_material_cost / total_units)
        if sales_overtime != 0 else 0
    )

    return avg_cost_total, avg_cost_regular, avg_cost_overtime

# -------------------------------------------------
# UI Interface
# -------------------------------------------------
def show_unit_cost_app():
    st.header("📦 Unit Production Cost Calculator")
    st.caption("Detailed cost breakdown between regular and overtime production cycles.")

    # SIDEBAR: Inputs
    with st.sidebar:
        st.subheader("Production Volume")
        sales_regular = st.number_input("Regular Units Produced", value=1000)
        sales_overtime = st.number_input("Overtime Units Produced", value=100)
        
        st.divider()
        st.subheader("Variable & Fixed Costs")
        raw_material_cost = st.number_input("Total Raw Material Cost (€)", value=1500.0)
        
        st.label("Operating Costs")
        operating_reg = st.number_input("Regular Operating Cost (€)", value=4000.0)
        operating_ot = st.number_input("Overtime Operating Cost (€)", value=400.0)
        
        st.label("Labor Costs")
        labor_reg = st.number_input("Regular Labor Cost (€)", value=8000.0)
        labor_ot = st.number_input("Overtime Labor Cost (€)", value=1200.0)

        st.divider()
        selling_price = st.number_input("Target Selling Price (€/unit)", value=20.0)
        
        run_calc = st.button("Execute Cost Analysis")

    if run_calc:
        # Calculations
        avg_total, avg_regular, avg_overtime = calculate_unit_costs(
            sales_regular, sales_overtime, raw_material_cost,
            operating_reg, operating_ot, labor_reg, labor_ot
        )

        # RESULTS SECTION
        st.subheader("📊 Cost Metrics")
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Avg. Total Cost", f"{avg_total:.2f} €")
        col2.metric("Regular Unit Cost", f"{avg_regular:.2f} €")
        col3.metric("Overtime Unit Cost", f"{avg_overtime:.2f} €", 
                   delta=f"{((avg_overtime/avg_regular)-1)*100:.1f}% Increase" if avg_regular != 0 else None,
                   delta_color="inverse")

        st.divider()

        # MARGIN ANALYSIS (New Feature)
        st.subheader("💡 Managerial Insights")
        
        margin_reg = selling_price - avg_regular
        margin_ot = selling_price - avg_overtime
        
        c_m1, c_m2 = st.columns(2)
        c_m1.write(f"**Margin (Regular):** {margin_reg:.2f} € / unit")
        c_m2.write(f"**Margin (Overtime):** {margin_ot:.2f} € / unit")

        

        if avg_overtime > selling_price:
            st.error(f"⚠️ **Warning:** Overtime unit cost ({avg_overtime:.2f} €) exceeds selling price. Additional orders are currently generating losses.")
        elif avg_overtime > avg_regular:
            st.warning(f"ℹ️ **Observation:** Overtime production is profitable but reduces unit margin by {avg_overtime - avg_regular:.2f} € compared to regular hours.")
        else:
            st.success("✅ **Efficiency Note:** Overtime production is highly efficient and maintains healthy margins.")

        # Breakdown Table
        st.subheader("📈 Detailed Expense Breakdown")
        breakdown_df = pd.DataFrame({
            "Cost Category": ["Labor", "Operating", "Materials (allocated)"],
            "Regular Unit (€)": [labor_reg/sales_regular, operating_reg/sales_regular, raw_material_cost/(sales_regular+sales_overtime)],
            "Overtime Unit (€)": [labor_ot/sales_overtime if sales_overtime > 0 else 0, 
                                  operating_ot/sales_overtime if sales_overtime > 0 else 0, 
                                  raw_material_cost/(sales_regular+sales_overtime)]
        })
        st.table(breakdown_df)
    else:
        st.info("👈 Enter production and cost data in the sidebar and click 'Execute'.")

if __name__ == "__main__":
    show_unit_cost_app()
