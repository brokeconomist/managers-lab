import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# CALCULATION LOGIC
# -------------------------------------------------
def analyze_resilience(profit, assets, current_assets, current_liabilities):
    roa = (profit / assets) * 100 if assets > 0 else 0
    current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
    return round(roa, 2), round(current_ratio, 2)

# -------------------------------------------------
# UI INTERFACE
# -------------------------------------------------
def show_resilience_map():
    st.header("🛡️ Financial Resilience & Shock Absorption Map")
    st.caption("Mapping the system's ability to absorb economic shocks without collapsing.")

    with st.sidebar:
        st.subheader("Core Financials")
        net_profit = st.number_input("Net Annual Profit (€)", value=50000.0)
        total_assets = st.number_input("Total Assets (€)", value=500000.0)
        
        st.divider()
        st.subheader("Liquidity Profile")
        c_assets = st.number_input("Current Assets (€)", value=120000.0)
        c_liabilities = st.number_input("Current Liabilities (€)", value=80000.0)
        
        run_map = st.button("Map System Position")

    # Resilience Logic
    roa, c_ratio = analyze_resilience(net_profit, total_assets, c_assets, c_liabilities)

    st.subheader("📍 Strategic Position")
    
    # 2x2 Resilience Matrix Plot
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Set Axis Limits (Standardized)
    ax.set_xlim(0, 4)  # Current Ratio Axis
    ax.set_ylim(-10, 30) # ROA Axis
    
    # Draw Quadrants
    ax.axhline(10, color='black', linewidth=1, linestyle='--') # Profitability Threshold
    ax.axvline(1.5, color='black', linewidth=1, linestyle='--') # Liquidity Threshold
    
    # Label Quadrants
    ax.text(0.5, 25, "Growth Trap\n(High Profit / Low Cash)", fontsize=10, color='orange', alpha=0.7)
    ax.text(2.5, 25, "The Fortress\n(High Profit / High Cash)", fontsize=10, color='green', alpha=0.7)
    ax.text(0.5, -5, "Danger Zone\n(Critical Vulnerability)", fontsize=10, color='red', alpha=0.7)
    ax.text(2.5, -5, "Safe Storage\n(Low Efficiency)", fontsize=10, color='blue', alpha=0.7)

    # Plot Current Position
    ax.scatter(c_ratio, roa, color='red', s=200, edgecolors='black', zorder=5)
    ax.annotate(f"Current State\n(CR: {c_ratio}, ROA: {roa}%)", (c_ratio, roa), 
                textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')

    ax.set_xlabel("Liquidity Buffer (Current Ratio)")
    ax.set_ylabel("Efficiency (Return on Assets %)")
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

    

    # ANALYTICAL VERDICT
    st.divider()
    st.subheader("🧠 Shock Absorption Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**System Status:**")
        if c_ratio < 1.0:
            st.error("🔴 **Technical Insolvency Risk:** The system cannot cover short-term shocks. Any delay in receivables will trigger a crisis.")
        elif c_ratio < 1.5:
            st.warning("🟠 **Low Buffer:** You are operating 'lean'. Good for efficiency, but vulnerable to market volatility.")
        else:
            st.success("🟢 **High Buffer:** The system can absorb significant shocks (e.g., loss of a major client) without immediate failure.")

    with col2:
        st.write("**Efficiency Status:**")
        if roa > 15:
            st.success("🟢 **High Performance:** The system generates ample internal capital to fuel its own survival.")
        elif roa > 5:
            st.info("🔵 **Moderate Performance:** Stable, but requires external financing for rapid expansion.")
        else:
            st.error("🔴 **Value Destruction:** The system is stagnant. Survival depends purely on cash reserves, not on operational strength.")

    # Shock Scenario Simulation
    st.divider()
    st.subheader("🌪️ Stress Test Simulation")
    shock_pct = st.slider("Simulate Revenue/Cash Drop (%)", 0, 50, 20)
    
    new_c_ratio = (c_assets * (1 - shock_pct/100)) / c_liabilities
    st.write(f"In the event of a **{shock_pct}%** sudden cash shock, your liquidity buffer would drop from **{c_ratio}** to **{new_c_ratio:.2f}**.")
    
    if new_c_ratio < 1:
        st.error("❌ **System Failure:** Under this scenario, the business would be unable to meet its obligations.")
    else:
        st.success("✔️ **System Survival:** The business survives the shock, though with reduced maneuverability.")

if __name__ == "__main__":
    show_resilience_map()
