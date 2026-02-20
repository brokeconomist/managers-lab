import streamlit as st
from tools.unit_cost_app import show_unit_cost_app
from tools.inventory_turnover_calculator import show_inventory_turnover_calculator

def run_step():
    st.header("Stage 3: Unit Economics")
    st.markdown("""
    **Objective:** Verify the core transaction. 
    If the unit cost is misunderstood, growth only accelerates failure.
    """)
    
    show_unit_cost_app()
    st.divider()
    show_inventory_turnover_calculator()
    
    st.divider()
    st.warning("⚠️ Operational audit complete. Next stages involve Strategic Durability.")
    if st.button("Proceed to Strategic Analysis"):
        st.session_state.flow_step = 4
        st.rerun()
