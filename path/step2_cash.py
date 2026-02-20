import streamlit as st
from tools.cash_cycle import run_cash_cycle_app
from tools.cash_fragility_index import show_cash_fragility_index

def run_step():
    st.header("Stage 2: Cash Pressure")
    st.markdown("""
    **Objective:** Audit the liquidity engine. 
    Profit is an opinion; Cash is a fact. We analyze the Cash Cycle and Fragility.
    """)
    
    show_cash_fragility_index()
    st.divider()
    run_cash_cycle_app()
    
    st.divider()
    if st.button("Stage 2 Complete → Move to Unit Economics"):
        st.session_state.flow_step = 3
        st.rerun()
