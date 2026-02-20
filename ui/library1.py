import streamlit as st

def show_library():
    st.title("📚 Tool Library")
    st.caption("Direct access to all analytical modules.")

    # Ομαδοποίηση εργαλείων
    categories = {
        "📈 Pricing & Break-Even": [
            ("Break-Even Shift Analysis", "break_even_shift_calculator", "show_break_even_shift_calculator"),
            ("Loss Threshold Analysis", "loss_threshold", "show_loss_threshold_before_price_cut"),
            ("Pricing Power Radar", "pricing_power_radar", "show_pricing_power_radar")
        ],
        "💰 Finance & Cash Flow": [
            ("Cash Cycle Calculator", "cash_cycle", "run_cash_cycle_app"),
            ("Cash Fragility Index", "cash_fragility_index", "show_cash_fragility_index"),
            ("Credit Policy Analysis", "credit_policy_app", "show_credit_policy_analysis"),
            ("Supplier Credit Analysis", "supplier_credit_app", "show_supplier_credit_analysis"),
            ("Loan vs Leasing", "loan_vs_leasing_calculator", "loan_vs_leasing_ui")
        ],
        "👥 Customer & Strategy": [
            ("CLV Analysis", "clv_calculator", "show_clv_calculator"),
            ("QSPM Strategy Tool", "qspm_two_strategies", "show_qspm_tool"),
            ("Substitutes Sensitivity", "substitution_analysis_tool", "show_substitutes_sensitivity_tool"),
            ("Complementary Analysis", "complementary_analysis", "show_complementary_analysis")
        ],
        "📦 Operations": [
            ("Unit Cost Calculator", "unit_cost_app", "show_unit_cost_app"),
            ("Inventory Turnover", "inventory_turnover_calculator", "show_inventory_turnover_calculator"),
            ("Credit Days Calculator", "credit_days_calculator", "show_credit_days_calculator"),
            ("Discount NPV Analysis", "discount_npv_ui", "show_discount_npv_ui")
        ]
    }

    selected_cat = st.selectbox("Choose Category", list(categories.keys()))
    tool_list = categories[selected_cat]
    tool_names = [t[0] for t in tool_list]
    selected_tool_name = st.radio("Select Tool", tool_names)

    tool_data = next(t for t in tool_list if t[0] == selected_tool_name)
    file_name = tool_data[1]
    function_name = tool_data[2]

    st.divider()

    try:
        # Δυναμική φόρτωση από τον φάκελο tools
        module = __import__(f"tools.{file_name}", fromlist=[function_name])
        func = getattr(module, function_name)
        func()
    except Exception as e:
        st.error(f"Error loading: {file_name}. Check file name and function name.")
        st.info(f"Details: {e}")
