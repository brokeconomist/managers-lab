import streamlit as st
import pandas as pd
import plotly.express as px

# --- Helper functions ---
def parse_number_en(number_str):
    return float(number_str)

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

    purchases_str = st.text_input("Expected purchases per period (e.g., year)", "10")
    price_str = st.text_input("Price per purchase ($)", "100")
    cost_str = st.text_input("Cost per purchase ($)", "60")
    marketing_str = st.text_input("Marketing cost per period ($)", "20")
    retention_str = st.text_input("Estimated customer retention (years)", "5")
    discount_str = st.text_input("Discount rate (e.g., 0.05 for 5%)", "0.05")

    purchases = parse_number_en(purchases_str)
    price = parse_number_en(price_str)
    cost = parse_number_en(cost_str)
    marketing = parse_number_en(marketing_str)
    retention = parse_number_en(retention_str)
    discount = parse_number_en(discount_str)

    if None in [purchases, price, cost, marketing, retention, discount]:
        st.error("Please enter valid numbers in all fields.")
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
