import streamlit as st
import plotly.graph_objects as go

def run_step():
    st.header("📉 Stage 1: Break-Even Analysis")
    st.info("Calculates the minimum volume needed to cover all variable and fixed costs.")

    # 1. ΔΥΝΑΜΙΚΟΣ ΣΥΓΧΡΟΝΙΣΜΟΣ (Εδώ είναι η λύση)
    # Διαβάζουμε ΠΑΝΤΑ τις τρέχουσες τιμές από το Stage 0
    price = st.session_state.get('price', 0.0)
    variable_cost = st.session_state.get('variable_cost', 0.0)
    current_volume = st.session_state.get('volume', 0.0)
    
    # 2. ΕΛΕΓΧΟΣ ΔΕΔΟΜΕΝΩΝ
    if price == 0 or current_volume == 0:
        st.warning("⚠️ Παρακαλώ επέστρεψε στο Stage 0 και όρισε Τιμή, Μεταβλητό Κόστος και Όγκο Πωλήσεων.")
        if st.button("⬅️ Επιστροφή στο Stage 0"):
            st.session_state.flow_step = 0
            st.rerun()
        return

    # 3. INPUTS ΓΙΑ ΣΤΑΘΕΡΑ ΕΞΟΔΑ (Fixed Costs)
    st.subheader("Σταθερά Έξοδα (Annual Fixed Costs)")
    col1, col2 = st.columns(2)
    with col1:
        fixed_costs = st.number_input("Συνολικά Ετήσια Σταθερά Έξοδα (€)", 
                                      min_value=0.0, 
                                      value=st.session_state.get('fixed_costs', 50000.0),
                                      step=1000.0)
        st.session_state.fixed_costs = fixed_costs

    # 4. ΥΠΟΛΟΓΙΣΜΟΣ BREAK-EVEN
    unit_contribution = price - variable_cost
    
    if unit_contribution > 0:
        be_units = fixed_costs / unit_contribution
        be_revenue = be_units * price
    else:
        be_units = 0
        be_revenue = 0

    # 5. ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ
    st.divider()
    res1, res2, res3 = st.columns(3)
    
    with res1:
        st.metric("Break-Even Units", f"{be_units:,.0f} units")
    with res2:
        st.metric("Break-Even Revenue", f"{be_revenue:,.2f} €")
    with res3:
        # Margin of Safety (Πόσο μακριά είμαστε από το σημείο μηδέν)
        safety_margin = ((current_volume - be_units) / current_volume * 100) if current_volume > 0 else 0
        st.metric("Margin of Safety", f"{safety_margin:.1f}%", 
                  delta=f"{current_volume - be_units:,.0f} units",
                  delta_color="normal" if safety_margin > 0 else "inverse")

    # 6. ΟΠΤΙΚΟΠΟΙΗΣΗ (Chart)
    # Δημιουργία δεδομένων για το γράφημα με βάση το current_volume
    max_x = int(max(be_units, current_volume) * 1.5)
    x_vals = list(range(0, max_x, max(1, max_x // 20)))
    rev_y = [x * price for x in x_vals]
    costs_y = [fixed_costs + (x * variable_cost) for x in x_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=rev_y, name='Total Revenue', line=dict(color='#00CC96')))
    fig.add_trace(go.Scatter(x=x_vals, y=costs_y, name='Total Costs', line=dict(color='#EF553B')))
    fig.add_vline(x=be_units, line_dash="dash", line_color="white", annotation_text="Break-Even")
    
    fig.update_layout(title="Break-Even Chart", xaxis_title="Units", yaxis_title="Euros", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # 7. NAVIGATION
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        if st.button("⬅️ Stage 0 (Calibration)"):
            st.session_state.flow_step = 0
            st.rerun()
    with col_n2:
        if st.button("Stage 2 (Cash Cycle) ➡️", type="primary"):
            st.session_state.flow_step = 2
            st.rerun()
