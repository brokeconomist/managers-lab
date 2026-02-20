import streamlit as st
from tools.break_even_shift_calculator import show_break_even_shift_calculator

def run_step():
    st.header("Stage 1: Survival Anchor")
    st.markdown("""
    **Objective:** Identify the structural limit of the business. 
    Before looking at profits, we must know how much "room" we have if the market shifts.
    """)
    
    show_break_even_shift_calculator()
    
    st.divider()
    if st.button("Stage 1 Complete → Move to Cash Pressure"):
        st.session_state.flow_step = 2
        st.rerun()
