import streamlit as st

def show_library():
    st.title("📚 Tool Library")
    st.markdown("Direct access to all operational and strategic calculators.")
    
    # Κατηγοριοποίηση για ευκολία στο tablet
    category = st.selectbox("Select Category", ["Operations", "Finance", "Strategy"])
    
    if category == "Operations":
        tool = st.radio("Select Tool", ["Unit Cost", "Inventory Velocity"])
        if tool == "Unit Cost":
            from tools.unit_cost_app import show_unit_cost_app
            show_unit_cost_app()
        # κλπ...

    elif category == "Finance":
        # Αντίστοιχα imports για cash cycle, credit κλπ.
        pass
