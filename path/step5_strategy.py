import streamlit as st
from tools.qspm_two_strategies import show_qspm_tool

def run_step():
    st.header("Stage 5: Strategic Decision")
    st.markdown("""
    **Objective:** Quantitative Strategy Selection. 
    Based on all previous data, we compare two distinct paths to find the structural winner.
    """)
    
    show_qspm_tool()
    
    st.divider()
    st.success("🏁 Audit Complete. You have reached the end of the Structured Decision Path.")
    if st.button("Return to Home"):
        st.session_state.mode = "home"
        st.session_state.flow_step = 1
        st.rerun()
