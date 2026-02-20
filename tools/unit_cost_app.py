import streamlit as st
import pandas as pd

def calculate_unit_costs(sales_regular, sales_overtime, raw_material_cost, operating_cost_regular, operating_cost_overtime, labor_cost_regular, labor_cost_overtime):
    total_units = sales_regular + sales_overtime
    total_cost = (raw_material_cost + operating_cost_regular + operating_cost_overtime + labor_cost_regular + labor_cost_overtime)
    avg_cost_total = total_cost / total_units if total_units != 0 else 0

    avg_cost_regular = ((labor_cost_regular / sales_regular) + (operating_cost_regular / sales_regular) + (raw_material_cost / total_units)) if sales_regular != 0 else 0
    avg_cost_overtime = ((labor_cost_overtime / sales_overtime) + (operating_cost_overtime / sales_overtime) + (raw_material_cost / total_units)) if sales_overtime != 0 else 0

    return avg_cost_total, avg_cost_regular, avg_cost_overtime

def show_unit_cost_app():
    st.header("📦 Unit Production Cost Calculator")
    st.caption("Stage 3: Deep dive into unit economics using global data.")

    # 1. SYNC WITH GLOBAL STATE
    # Αν ο χρήστης δεν έχει περάσει από το Break-Even, ορίζουμε defaults
    if "global_units" not in st.session_state: st.session_state.global_units = 1000
    if "global_price" not in st.session_state: st.session_state.global_price = 20.0
    if "global_vc" not in st.session_state: st.session_state.global_vc = 12.0

    # 2. INPUTS (Διαβάζουν από το Session State)
    with st.sidebar:
        st.subheader("Production Volume")
        # Εδώ το Regular Units τραβάει την τιμή από το global_units
        s_reg = st.number_input("Regular Units Produced", value=int(st.session_state.global_units), min_value=1)
        s_ot = st.number_input("Overtime Units Produced", value=0, min_value=0)
        
        st.divider()
        st.subheader("Variable & Fixed Costs")
        # Το Raw Material Cost υπολογίζεται αυτόματα ως πρόταση (Units * Global Variable Cost)
        suggested_rm = s_reg * st.session_state.global_vc
        rm_cost = st.number_input("Total Raw Material Cost (€)", value=float(suggested_rm))
        
        st.markdown("**Operating Expenses**")
        op_reg = st.number_input("Regular Operating Cost (€)", value=4000.0)
        op_ot = st.number_input("Overtime Operating Cost (€)", value=0.0)
        
        st.markdown("**Labor Expenses**")
        lab_reg = st.number_input("Regular Labor Cost (€)", value=8000.0)
        lab_ot = st.number_input("Overtime Labor Cost (€)", value=0.0)

        st.divider()
        # Η τιμή πώλησης έρχεται επίσης από το Global State
        sell_price = st.number_input("Target Selling Price (€/unit)", value=float(st.session_state.global_price))
        
        run_calc = st.button("Execute Cost Analysis")

    # 3. Εμφάνιση ειδοποίησης αν τα δεδομένα ήρθαν από το προηγούμενο στάδιο
    st.info(f"Using global parameters: **{s_reg} units** at **{sell_price} €/unit** (Target).")

    if run_calc:
        avg_total, avg_reg, avg_ot = calculate_unit_costs(s_reg, s_ot, rm_cost, op_reg, op_ot, lab_reg, lab_ot)

        # RESULTS SECTION
        st.subheader("📊 Cost Metrics")
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg. Total Cost", f"{avg_total:.2f} €")
        c2.metric("Regular Unit Cost", f"{avg_reg:.2f} €")
        
        # Ενημέρωση του Global Variable Cost αν ο χρήστης βρήκε ακριβέστερο νούμερο εδώ
        st.session_state.global_vc = avg_reg

        # ... (υπόλοιπος κώδικας για Margin Analysis και Table όπως πριν) ...
        st.write(f"**Current Margin:** {sell_price - avg_reg:.2f} €")
        
        #
