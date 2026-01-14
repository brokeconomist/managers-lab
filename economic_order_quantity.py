import streamlit as st
import math

def format_number_en(num, decimals=0):
    """
    Format numbers with commas as thousand separators and dot as decimal separator.
    Example: 1234567.89 -> '1,234,567.89'
    """
    return f"{num:,.{decimals}f}"

def format_percentage_en(num):
    """
    Format decimal as percentage string with 2 decimals.
    """
    return f"{num * 100:.2f}%"

def show_economic_order_quantity():
    st.title("📦 Economic Order Quantity (EOQ)")

    # --- Input ---
    q = st.number_input("Unit Price (q)", value=30.0, format="%.2f")
    M = st.number_input("Demand for the Period (M)", value=10000, step=100)
    kf = st.number_input("Fixed Ordering Cost per Order (kf)", value=600.0, format="%.2f")
    r = st.number_input("Percentage Discount (%)", value=0.0, format="%.2f") / 100
    annual_interest = st.number_input("Annual Interest Rate", value=0.05, format="%.4f")
    storage_cost_rate = st.number_input("Storage Cost Rate (%)", value=3.0, format="%.2f") / 100

    # --- Calculations ---
    KV = M * q                          # Total merchandise cost
    i = annual_interest                 # Interest
    j = i + storage_cost_rate           # Total storage cost rate
    KL = j * KV                          # Storage and interest cost

    if r == 0:
        B = math.sqrt((2 * M * kf) / (q * j)) if j != 0 else 0
    else:
        B = math.sqrt((2 * M * kf) / (storage_cost_rate + (1 - r) * kf))  # adjusted for discount

    orders = M / B if B != 0 else 0
    KF = orders * kf
    K = KF + KL

    # --- Output ---
    st.subheader("📊 Results")
    st.write(f"**Total Procurement Cost (K):** {format_number_en(K, 0)} €")
    st.write(f"**Fixed Ordering Cost (KF):** {format_number_en(KF, 0)} €")
    st.write(f"**Merchandise Cost for Demand (KV):** {format_number_en(KV, 0)} €")
    st.write(f"**Storage and Interest Cost (KL):** {format_number_en(KL, 0)} €")
    st.write(f"**Interest Rate (i):** {format_percentage_en(i)}")
    st.write(f"**Total Storage Cost Rate (j):** {format_percentage_en(j)}")
    st.write(f"**Optimal Order Quantity (B):** {format_number_en(B, 0)} units")
    st.write(f"**Number of Orders in Period:** {format_number_en(orders, 2)}")
