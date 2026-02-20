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
        s_reg = st.number_input("Regular Units Produced", value=1000, min_value=1)
        s_ot = st.number_input("Overtime Units Produced", value=100, min_value=0)
        
        st.divider()
        st.subheader("Variable & Fixed Costs")
        rm_cost = st.number_input("Total Raw Material Cost (€)", value=1500.0)
        
        # Using markdown for bold headers in sidebar
        st.markdown("**Operating Expenses**")
        op_reg = st.number_input("Regular Operating Cost (€)", value=4000.0)
        op_ot = st.number_input("Overtime Operating Cost (€)", value=400.0)
        
        st.markdown("**Labor Expenses**")
        lab_reg = st.number_input("Regular Labor Cost (€)", value=8000.0)
        lab_ot = st.number_input("Overtime Labor Cost (€)", value=1200.0)

        st.divider()
        sell_price = st.number_input("Target Selling Price (€/unit)", value=20.0)
        
        run_calc = st.button("Execute Cost Analysis")

    if run_calc:
        # Calculations using the engine
        avg_total, avg_reg, avg_ot = calculate_unit_costs(
            s_reg, s_ot, rm_cost, op_reg, op_ot, lab_reg, lab_ot
        )

        # RESULTS SECTION
        st.subheader("📊 Cost Metrics")
        c1, c2, c3 = st.columns(3)
        
        c1.metric("Avg. Total Cost", f"{avg_total:.2f} €")
        c2.metric("Regular Unit Cost", f"{avg_reg:.2f} €")
        
        # Logic for overtime metric delta
        ot_delta = None
        if avg_reg > 0 and s_ot > 0:
            ot_delta = f"{((avg_ot/avg_reg)-1)*100:.1f}% vs Reg"
            
        c3.metric("Overtime Unit Cost", f"{avg_ot:.2f} €", 
                   delta=ot_delta,
                   delta_color="inverse")

        st.divider()

        # MARGIN ANALYSIS
        st.subheader("💡 Managerial Insights")
        
        m_reg = sell_price - avg_reg
        m_ot = sell_price - avg_ot if s_ot > 0 else 0
        
        col_m1, col_m2 = st.columns(2)
        col_m1.write(f"**Margin (Regular):** {m_reg:.2f} € / unit")
        if s_ot > 0:
            col_m2.write(f"**Margin (Overtime):** {m_ot:.2f} € / unit")
        else:
            col_m2.write("**Margin (Overtime):** N/A")

        

        if s_ot > 0:
            if avg_ot > sell_price:
                st.error(f"❌ **Loss Alert:** Overtime cost ({avg_ot:.2f} €) is higher than Selling Price. Stop OT or increase price.")
            elif avg_ot > avg_reg:
                st.warning(f"⚠️ **Margin Compression:** Overtime is profitable but costs {avg_ot - avg_reg:.2f} € more per unit than regular hours.")
            else:
                st.success("✅ **Optimal Efficiency:** Overtime production is currently cost-effective.")

        # Breakdown Table
        st.subheader("📈 Detailed Breakdown per Unit")
        total_v = s_reg + s_ot
        
        data = {
            "Category": ["Labor", "Operating", "Materials"],
            "Regular (€)": [lab_reg/s_reg, op_reg/s_reg, rm_cost/total_v],
            "Overtime (€)": [lab_ot/s_ot if s_ot > 0 else 0, op_ot/s_ot if s_ot > 0 else 0, rm_cost/total_v]
        }
        st.table(pd.DataFrame(data))
    else:
        st.info("👈 Enter production data in the sidebar and click 'Execute'.")
