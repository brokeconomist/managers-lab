import streamlit as st
import pandas as pd
import plotly.express as px

# --- Helper functions ---
def parse_number_en(number_str):
    try:
        return float(number_str.replace(',', ''))
    except:
        return None

def format_number_en(number, decimals=2):
    return f"{number:,.{decimals}f}"

def format_percentage_en(number, decimals=1):
    return f"{number*100:.{decimals}f}%"


# --- CLV Calculation ---
def calculate_clv_discounted(
    purchases_per_period,
    price_per_purchase,
    cost_per_purchase,
    marketing_cost_per_period,
    retention_years,
    discount_rate
):
    try:
        net_margin_per_period = (purchases_per_period * (price_per_purchase - cost_per_purchase)) - marketing_cost_per_period
        if discount_rate == 0:
            clv = net_margin_per_period * retention_years
        else:
            discount_factor = (1 - (1 + discount_rate) ** (-retention_years)) / discount_rate
            clv = net_margin_per_period * discount_factor
        return clv
    except Exception:
        return None


# --- Tornado Chart Data ---
def tornado_data(clv_base, params, delta=0.1):
    results = []
    for key, value in params.items():
        if value is None or value == 0:
            continue
        params_plus = params.copy()
        params_plus[key] = value * (1 + delta)
        clv_plus = calculate_clv_discounted(**params_plus)

        params_minus = params.copy()
        params_minus[key] = value * (1 - delta)
        clv_minus = calculate_clv_discounted(**params_minus)

        pct_plus = ((clv_plus - clv_base) / clv_base) * 100 if clv_base != 0 else 0
        pct_minus = ((clv_minus - clv_base) / clv_base) * 100 if clv_base != 0 else 0

        results.append({
            "Parameter": key,
            "Change": f"+{int(delta*100)}%",
            "Impact (%)": pct_plus
        })
        results.append({
            "Parameter": key,
            "Change": f"-{int(delta*100)}%",
            "Impact (%)": pct_minus
        })

    mapping = {
        "purchases_per_period": "Purchases per Period",
        "price_per_purchase": "Price per Purchase",
        "cost_per_purchase": "Cost per Purchase",
        "marketing_cost_per_period": "Marketing Cost per Period",
        "retention_years": "Customer Retention (Years)",
        "discount_rate": "Discount Rate"
    }

    df = pd.DataFrame(results)
    df["Parameter"] = df["Parameter"].map(mapping)
    return df


# --- Streamlit UI ---
def show_clv_calculator():
    st.title("👥 Customer Lifetime Value (CLV) Calculator — Discounted")

    st.markdown(
        "Calculate the **net present value of a customer** and explore how changes in your assumptions impact it."
    )

    with st.form("clv_form"):
        purchases_input = st.text_input("Expected purchases per period", "10")
        st.caption("Number of purchases your average customer makes in one period (e.g., per year).")

        price_input = st.text_input("Price per purchase ($)", "100")
        st.caption("The price at which you sell one unit or service to a customer per purchase.")

        cost_input = st.text_input("Cost per purchase ($)", "60")
        st.caption("Direct cost per purchase. Includes production, delivery, and any variable cost incurred per sale.")

        marketing_input = st.text_input("Marketing cost per period ($)", "20")
        st.caption("Average marketing cost allocated per customer per period (ads, campaigns, promotions).")

        retention_input = st.text_input("Estimated customer retention (years)", "5")
        st.caption("Average duration a customer stays active and keeps buying from you.")

        discount_input = st.text_input("Discount rate (e.g., 0.05 for 5%)", "0.05")
        st.caption("Time value of money — how much future cash flows are discounted to present value.")

        submitted = st.form_submit_button("Calculate CLV")

    if submitted:
        purchases = parse_number_en(purchases_input)
        price = parse_number_en(price_input)
        cost = parse_number_en(cost_input)
        marketing = parse_number_en(marketing_input)
        retention = parse_number_en(retention_input)
        discount = parse_number_en(discount_input)

        if None in [purchases, price, cost, marketing, retention, discount]:
            st.error("⚠️ Please enter valid numbers in all fields.")
            return

        clv = calculate_clv_discounted(
            purchases_per_period=purchases,
            price_per_purchase=price,
            cost_per_purchase=cost,
            marketing_cost_per_period=marketing,
            retention_years=retention,
            discount_rate=discount,
        )

        if clv is None:
            st.error("Error in calculation. Check input values.")
            return

        st.success(f"Estimated Net Present Value of Customer: {format_number_en(clv)} $")

        # Tornado Chart
        st.subheader("📊 Sensitivity Analysis (Tornado Chart)")

        params = {
            "purchases_per_period": purchases,
            "price_per_purchase": price,
            "cost_per_purchase": cost,
            "marketing_cost_per_period": marketing,
            "retention_years": retention,
            "discount_rate": discount,
        }

        df_tornado = tornado_data(clv, params, delta=0.1)

        fig = px.bar(
            df_tornado,
            x="Impact (%)",
            y="Parameter",
            color="Change",
            orientation="h",
            title="CLV Sensitivity to Parameter Changes",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
