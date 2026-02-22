import streamlit as st
import plotly.graph_objects as go

def run_step():
    st.header("📉 Stage 1: Break-Even Analysis")
    st.info("Calculates the minimum volume needed to cover all variable and fixed costs.")

    # 1. DYNAMIC SYNC FROM STAGE 0
    # Note: Using 'fixed_cost' (singular) to match your Stage 0 code
    price = st.session_state.get('price', 0.0)
    variable_cost = st.session_state.get('variable_cost', 0.0)
    current_volume = st.session_state.get('volume', 0.0)
    
    # Check for Price/Volume to avoid calculation errors
    if price <= 0 or current_volume <= 0:
        st.warning("⚠️ Baseline data missing. Please return to Stage 0.")
        if st.button("⬅️ Back to Stage 0"):
            st.session_state.flow_step = 0
            st.rerun()
        return

    # 2. FIXED COSTS INPUT (Linked to Stage 0)
    st.subheader("Annual Fixed Costs")
    
    # We use a unique key 'fixed_cost_input' but default its value 
    # to the one stored in session_state.fixed_cost
    fixed_cost = st.number_input(
        "Total Annual Fixed Costs (€)", 
        min_value=0.0, 
        value=float(st.session_state.get('fixed_cost', 50000.0)),
        step=1000.0,
        key="fixed_cost_sync"
    )
    
    # Update the global session state so other stages see the change
    st.session_state.fixed_cost = fixed_cost

    # 3. BREAK-EVEN CALCULATIONS
    unit_contribution = price - variable_cost
    
    if unit_contribution > 0:
        be_units = fixed_cost / unit_contribution
        be_revenue = be_units * price
    else:
        be_units = 0
        be_revenue = 0

    # 4. RESULTS DISPLAY
    st.divider()
    res1, res2, res3 = st.columns(3)
    
    with res1:
        st.metric("Break-Even Units", f"{be_units:,.0f}")
    with res2:
        st.metric("Break-Even Revenue", f"{be_revenue:,.2f} €")
    with res3:
        safety_margin = ((current_volume - be_units) / current_volume * 100) if current_volume > 0 else 0
        st.metric("Margin of Safety", f"{safety_margin:.1f}%", 
                  delta=f"{current_volume - be_units:,.0f} units surplus")

    # 5. VISUALIZATION
    
    
    max_x = int(max(be_units, current_volume) * 1.5)
    if max_x == 0: max_x = 100
    x_vals = list(range(0, max_x, max(1, max_x // 20)))
    rev_y = [x * price for x in x_vals]
    costs_y = [fixed_cost + (x * variable_cost) for x in x_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=rev_y, name='Total Revenue', line=dict(color='#00CC96')))
    fig.add_trace(go.Scatter(x=x_vals, y=costs_y, name='Total Costs', line=dict(color='#EF553B')))
    fig.add_vline(x=be_units, line_dash="dash", line_color="white", annotation_text="Break-Even Point")
    
    fig.update_layout(title="Annual Break-Even Chart", xaxis_title="Units", yaxis_title="Euros", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # 6. NAVIGATION
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Back to Calibration"):
            st.session_state.flow_step = 0
            st.rerun()
    with nav2:
        if st.button("Proceed to Stage 2 ➡️", type="primary"):
            st.session_state.flow_step = 2
            st.rerun()
