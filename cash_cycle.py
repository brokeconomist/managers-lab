import streamlit as st

def run_cash_cycle_app():
    st.title("📊 Cash Conversion Cycle Calculator")
    st.markdown("""
Fill in the fields below to calculate the **overall cash conversion cycle** of your business.
""")

    # --- User Inputs ---
    col1, col2 = st.columns(2)

    with col1:
        raw_materials_days = st.number_input("📦 Raw Materials Inventory Days", min_value=0, value=76, step=1)
        processing_days = st.number_input("🏭 Production / Processing Days", min_value=0, value=37, step=1)
        finished_goods_days = st.number_input("📦 Finished Goods Inventory Days", min_value=0, value=42, step=1)

    with col2:
        receivables_days = st.number_input("💰 Accounts Receivable Days", min_value=0, value=73, step=1)
        payables_days = st.number_input("🧾 Accounts Payable Days", min_value=0, value=61, step=1)

    # --- Calculation ---
    cash_conversion_cycle = (
        raw_materials_days +
        processing_days +
        finished_goods_days +
        receivables_days -
        payables_days
    )

    # --- Results ---
    st.markdown("---")
    st.subheader("🧮 Calculation Results")
    st.metric(label="📆 Total Cash Conversion Cycle (days)", value=f"{cash_conversion_cycle} days")

    # --- Evaluation ---
    if cash_conversion_cycle > 150:
        st.warning("⚠️ Cash cycle is very long. Consider reducing inventory or improving credit terms.")
    elif cash_conversion_cycle < 60:
        st.success("✅ Cash cycle is short and efficient.")
    else:
        st.info("ℹ️ Cash cycle is within normal range.")

    st.markdown("---")
    st.caption("🔧 This tool is based on standard financial management analysis and checks the net duration of tied-up resources.")
