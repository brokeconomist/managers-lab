import streamlit as st

def show_unit_cost_app():
    st.header("📊 Industrial Unit Cost Calculator")
    st.info("Analyze the components of your Variable Cost. Use 'Sync to Core' to update all other tools.")

    # 1. LOAD CURRENT STATE
    if 'variable_cost' not in st.session_state:
        st.session_state.variable_cost = 12.0

    st.subheader("Cost Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛠 Direct Costs")
        raw_materials = st.number_input("Raw Materials per unit (€)", min_value=0.0, value=st.session_state.variable_cost * 0.7)
        labor_cost = st.number_input("Direct Labor per unit (€)", min_value=0.0, value=st.session_state.variable_cost * 0.2)
        
    with col2:
        st.markdown("### ⚡ Variable Overheads")
        energy_cost = st.number_input("Energy/Utilities per unit (€)", min_value=0.0, value=st.session_state.variable_cost * 0.05)
        packaging_shipping = st.number_input("Packaging & Shipping (€)", min_value=0.0, value=st.session_state.variable_cost * 0.05)

    # 2. CALCULATE TOTAL VC
    total_vc = raw_materials + labor_cost + energy_cost + packaging_shipping
    
    st.divider()
    
    # 3. ANALYSIS & SYNC
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.metric("Calculated Variable Cost", f"{total_vc:.2f} €", 
                  delta=f"{total_vc - st.session_state.variable_cost:.2f} € vs Global",
                  delta_color="inverse")
    
    with c2:
        if st.button("🔄 Sync to Shared Core", use_container_width=True):
            st.session_state.variable_cost = total_vc
            st.success("Global Variable Cost Updated!")
            st.rerun()

    # 4. VISUALIZATION OF COST STRUCTURE
    st.write("### Cost Structure Analysis")
    cost_data = {
        "Raw Materials": raw_materials,
        "Labor": labor_cost,
        "Energy": energy_cost,
        "Logistics": packaging_shipping
    }
    
    # Απλή μπάρα ποσοστών
    if total_vc > 0:
        for label, value in cost_data.items():
            pct = value / total_vc
            st.write(f"**{label}:** {value:.2f}€ ({pct:.1%})")
            st.progress(pct)

    st.divider()
    st.caption("Tip: If raw material prices increase, update them here and sync. Your Break-Even and Survival Margin will adjust automatically.")
