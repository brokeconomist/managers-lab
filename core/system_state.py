import streamlit as st

def initialize_system_state():
    """Αρχικοποίηση των 5 Πυλώνων του Συστήματος στο Session State"""
    
    # 1️⃣ Revenue Engine
    if 'price' not in st.session_state: st.session_state.price = 20.0
    if 'volume' not in st.session_state: st.session_state.volume = 1000
    
    # 2️⃣ Cost Structure
    if 'variable_cost' not in st.session_state: st.session_state.variable_cost = 12.0
    if 'fixed_cost' not in st.session_state: st.session_state.fixed_cost = 5000.0
    
    # 3️⃣ Time & Cash Pressure
    if 'ar_days' not in st.session_state: st.session_state.ar_days = 45
    if 'inventory_days' not in st.session_state: st.session_state.inventory_days = 60
    if 'payables_days' not in st.session_state: st.session_state.payables_days = 30
    
    # 4️⃣ Capital & Financing
    if 'debt' not in st.session_state: st.session_state.debt = 20000.0
    if 'interest_rate' not in st.session_state: st.session_state.interest_rate = 0.05
    
    # 5️⃣ Durability
    if 'retention_rate' not in st.session_state: st.session_state.retention_rate = 0.85
