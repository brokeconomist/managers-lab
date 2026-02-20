import streamlit as st
from tools.clv_calculator import show_clv_calculator
from tools.pricing_power_radar import show_pricing_power_radar

def run_step():
    st.header("Stage 4: Structural Sustainability")
    st.markdown("""
    **Objective:** Analyze the long-term health. 
    We look at Customer Lifetime Value and your actual Pricing Power in the market.
    """)
    
    show_clv_calculator()
    st.divider()
    show_pricing_power_radar()
    
    st.divider()
    if st.button("Stage 4 Complete → Final Strategic Choice"):
        st.session_state.flow_step = 5
        st.rerun()
