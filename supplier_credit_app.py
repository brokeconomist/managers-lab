import streamlit as st
import pandas as pd

# -----------------------
# Calculation Engine
# -----------------------

def calculate_supplier_credit_gain(
    supplier_credit_days,
    discount_pct,
    clients_pct,
    current_sales,
    unit_price,
    total_unit_cost,
    interest_rate_pct
):
    discount = discount_pct / 100
    clients = clients_pct / 100
    interest_rate = interest_rate_pct / 100

    # Gain from taking the early payment discount
    discount_gain = current_sales * discount * clients

    # Opportunity cost: The interest we would have earned if we kept the money for the credit period
    average_cost_ratio = total_unit_cost / unit_price
    
    # Formula logic: Volume of capital * cost ratio * (days/365) * interest rate
    credit_benefit = (
        (current_sales / (365 / supplier_credit_days)) * average_cost_ratio
        - ((current_sales * (1 - clients)) / (365 / supplier_credit_days)) * average_cost_ratio
    ) * interest_rate

    net_gain = discount_gain - credit_benefit
    return discount_gain, credit_benefit, net_gain

# -----------------------
# UI Logic
# -----------------------

def show_supplier_credit_analysis():
    st.header("🏦 Supplier Credit vs. Early Payment Discount")
    st.write("Determine the optimal payment strategy: Leverage supplier credit or secure early payment discounts?")

    # SIDEBAR: Financial Variables
    with st.sidebar:
        st.subheader("Supplier Terms")
        s_credit_days = st.number_input("Credit Period (Days)", value=60)
        s_discount = st.number_input("Early Payment Discount (%)", value=2.0)
        
        st.divider()
        st.subheader("Operational Data")
        c_sales = st.number_input("Annual Sales (€)", value=2000000.0, step=10000.0)
        u_price = st.number_input("Unit Selling Price (€)", value=20.0)
        u_cost = st.number_input("Unit Total Cost (€)", value=18.0)
        
        st.divider()
        st.subheader("Financial Context")
        c_pay_pct = st.slider("% of Business Paid in Cash", 0, 100, 50)
        wacc = st.number_input("Cost of Capital (WACC %)", value=10.0)
        
        run = st.button("Analyze Financial Impact")

    # MAIN SCREEN: Strategic Results
    if run:
        discount_gain, credit_cost, net_gain = calculate_supplier_credit_gain(
            s_credit_days, s_discount, c_pay_pct,
            c_sales, u_price, u_cost, wacc
        )

        # 1. Executive Summary Metrics
        st.subheader("📊 Strategic Indifference Point")
        
        # Effective Annual Interest Rate (EAR) of the discount
        # Approx formula: (Discount % / (1 - Discount %)) * (365 / Credit Days)
        approx_ear = (s_discount/100 / (1 - s_discount/100)) * (365 / s_credit_days) * 100

        c1, c2, c3 = st.columns(3)
        c1.metric("Net Economic Gain", f"€ {net_gain:,.0f}")
        c2.metric("Discount Annualized Rate", f"{approx_ear:.1f}%")
        c3.metric("Company WACC", f"{wacc:.1f}%")

        # 2. Decision Matrix
        st.divider()
        st.subheader("🧠 Tactical Assessment")
        
        
        
        if net_gain > 0:
            st.success(f"✅ **PAY EARLY:** The annualized discount ({approx_ear:.1f}%) is higher than your cost of capital ({wacc:.1f}%). Paying early creates value.")
        else:
            st.error(f"❌ **USE CREDIT:** The supplier credit is 'cheaper' than the cost of funding the early payment. Maximize your DSO.")

        # 3. Detailed Breakdown Table
        st.divider()
        st.subheader("📈 Scenario Components")
        
        breakdown_df = pd.DataFrame({
            "Financial Component": ["Gross Savings from Discount", "Lost Interest (Credit Opportunity Cost)", "Net Strategic Impact"],
            "Amount (€)": [f"€ {discount_gain:,.2f}", f"€ {credit_cost:,.2f}", f"€ {net_gain:,.2f}"]
        })
        st.table(breakdown_df)

        # 4. Critical Insight
        st.info(f"""
        **Analytical Perspective:** By paying early, you are essentially 'lending' money back to your supplier in exchange for {s_discount}%. 
        This is only rational if the **Internal Rate of Return (IRR)** of this discount exceeds your **WACC**. 
        In this scenario, your IRR is {approx_ear:.1f}%.
        """)

if __name__ == "__main__":
    show_supplier_credit_analysis()


