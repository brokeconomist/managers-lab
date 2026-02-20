import streamlit as st

def show_home():
    # 1. HEADER & PHILOSOPHY
    st.title("🧪 Managers' Lab")
    st.markdown("""
    **A decision laboratory for managers.** This is not a dashboard. It's a simulator to test
    what must be true for a decision to work — and what breaks when it doesn't.
    """)

    st.divider()

    # 2. SYSTEM HEALTH INDEX (The Cold Truth)
    try:
        price         = st.session_state.price
        volume        = st.session_state.volume
        variable_cost = st.session_state.variable_cost
        fixed_cost    = st.session_state.fixed_cost

        # ── FIX 1: Guard against price = 0 (division by zero) ──
        if price <= 0:
            st.warning("⚠️ Price is 0 or negative — Health Index cannot be calculated.")
        else:
            revenue       = price * volume
            contribution  = price - variable_cost
            margin        = contribution / price

            ccc = (
                st.session_state.ar_days
                + st.session_state.inventory_days
                - st.session_state.payables_days
            )

            # ── FIX 2: Guard against contribution = 0 (division by zero in break-even) ──
            if contribution <= 0:
                st.warning("⚠️ Contribution margin ≤ 0 — Break-even cannot be calculated.")
            else:
                breakeven     = fixed_cost / contribution
                safety_margin = (volume / breakeven) - 1 if breakeven > 0 else float('inf')

                st.subheader("🏥 System Health Index")
                col1, col2, col3 = st.columns(3)

                with col1:
                    color = "green" if margin > 0.3 else "orange" if margin > 0.15 else "red"
                    st.metric("Profitability (Gross)", f"{margin:.1%}")
                    st.caption(f":{color}[Targeting {price}€ / unit]")

                with col2:
                    color = "green" if ccc < 45 else "orange" if ccc < 90 else "red"
                    st.metric("Liquidity Gap", f"{int(ccc)} Days")
                    st.caption(f":{color}[Cash Conversion Cycle]")

                with col3:
                    color = "green" if safety_margin > 0.2 else "orange" if safety_margin > 0 else "red"
                    st.metric("Survival Margin", f"{safety_margin:.1%}")
                    st.caption(f":{color}[Distance from Break-even]")

    except Exception as e:
        st.error(f"System State error: {e}. Please refresh the app.")

    st.divider()
    st.markdown("**Direct Access to Decision Modules:**")

    # 3. DECISION BUTTONS (Navigation)
    def go_to(tool_name: str):
        st.session_state.mode = "library"
        st.session_state.selected_tool = tool_name
        st.rerun()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 📈 Pricing & Viability")
        if st.button("Break-Even Shift Analysis", use_container_width=True):
            go_to("Break-Even Shift Analysis")
        if st.button("Loss Threshold Analysis", use_container_width=True):
            go_to("Loss Threshold Analysis")

    with col_b:
        st.markdown("### 💰 Cash & Finance")
        if st.button("Cash Cycle Calculator", use_container_width=True):
            go_to("Cash Cycle Calculator")
        if st.button("Credit Policy Analysis", use_container_width=True):
            go_to("Credit Policy Analysis")

    st.markdown("### 📦 Operations")
    col_c, col_d = st.columns(2)
    with col_c:
        if st.button("Unit Cost Calculator", use_container_width=True):
            go_to("Unit Cost Calculator")
    with col_d:
        if st.button("Inventory Turnover Analysis", use_container_width=True):
            go_to("Inventory Turnover Analysis")

    st.divider()

    # 4. FOOTER
    st.caption("🧪 Managers' Lab v2.0 | Shared Core Architecture")
