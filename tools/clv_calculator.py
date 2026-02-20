import streamlit as st

def show_clv_calculator():
    st.header("👥 Customer Lifetime Value (CLV)")
    st.info("Calculate the total worth of a customer over the whole period of their relationship with the business.")

    # 1. SYNC WITH SHARED CORE
    p = st.session_state.get('price', 20.0)
    vc = st.session_state.get('variable_cost', 12.0)
    unit_margin = p - vc
    
    st.write(f"**Unit Economics Baseline:** Margin per Unit: {unit_margin:.2f} € (Price: {p}€ - VC: {vc}€)")

    st.divider()

    # 2. CUSTOMER BEHAVIOR INPUTS
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Retention & Frequency")
        avg_purchases_year = st.number_input("Average Purchases per Year", min_value=1.0, value=4.0)
        avg_units_per_order = st.number_input("Average Units per Order", min_value=1.0, value=2.0)
        lifespan_years = st.slider("Customer Lifespan (Years)", 1, 10, 3)

    with col2:
        st.subheader("Acquisition Cost (CAC)")
        total_marketing_spend = st.number_input("Total Marketing Spend (€)", min_value=0.0, value=5000.0)
        new_customers_acquired = st.number_input("New Customers Acquired", min_value=1, value=100)
        cac = total_marketing_spend / new_customers_acquired if new_customers_acquired > 0 else 0
        st.metric("Cost per Acquisition (CAC)", f"{cac:.2f} €")

    # 3. CALCULATIONS
    # CLV = Margin per Unit * Units per Order * Frequency * Lifespan
    annual_margin_per_customer = unit_margin * avg_units_per_order * avg_purchases_year
    total_clv = annual_margin_per_customer * lifespan_years
    roi_ratio = total_clv / cac if cac > 0 else 0

    st.divider()

    # 4. RESULTS
    res1, res2, res3 = st.columns(3)
    
    with res1:
        st.metric("Gross CLV", f"{total_clv:.2f} €")
        st.caption("Total profit before CAC")

    with res2:
        net_clv = total_clv - cac
        st.metric("Net CLV (Profit)", f"{net_clv:.2f} €", delta=f"{net_clv:.2f} €")
        st.caption("Lifetime profit after CAC")

    with res3:
        color = "green" if roi_ratio > 3 else "orange" if roi_ratio > 1 else "red"
        st.metric("CLV / CAC Ratio", f"{roi_ratio:.1f}x")
        st.markdown(f"Status: :{color}[{'Strong' if roi_ratio > 3 else 'Fragile' if roi_ratio > 1 else 'Burning Cash'}]")

    st.divider()
    
    # 5. COLD ANALYSIS INSIGHT
    st.subheader("Strategic Verdict")
    if roi_ratio < 1:
        st.error(f"**Negative Unit Economics:** You are spending {cac:.2f}€ to acquire a customer who only returns {total_clv:.2f}€ in their lifetime. This is a structural leak.")
    elif roi_ratio < 3:
        st.warning("**Expansion Risk:** Your ratio is below 3x. While profitable, you may struggle to cover fixed costs and overheads as you scale.")
    else:
        st.success("**Healthy Growth:** Your CLV is more than 3x your CAC. You have a 'license to grow'—consider increasing marketing spend.")

    st.caption("Note: Calculations are based on Gross Contribution Margin. Fixed costs (rent, admin) are not included in Unit CLV.")
