import streamlit as st
import pandas as pd

def show_loss_threshold_before_price_cut():
    st.header("📉 Loss Threshold Analysis")
    st.info("Calculates the required volume increase to maintain profit after a price drop.")

    # 1. SYNC WITH SHARED CORE
    # Τραβάμε τις τιμές που ορίστηκαν στο Home ή στο Survival Anchor
    p = st.session_state.get('price', 20.0)
    vc = st.session_state.get('variable_cost', 12.0)
    q = st.session_state.get('volume', 1000)
    
    current_margin_euro = p - vc
    current_margin_pct = (current_margin_euro / p) if p > 0 else 0

    # Εμφάνιση των τρεχόντων δεδομένων για επιβεβαίωση
    st.write(f"**Current Baseline:** Price: {p:.2f}€ | Unit VC: {vc:.2f}€ | Current Margin: {current_margin_pct:.1%}")

    st.divider()

    # 2. INPUTS ΓΙΑ ΤΗΝ ΕΚΠΤΩΣΗ
    col1, col2 = st.columns(2)
    with col1:
        price_cut_pct = st.slider("Proposed Price Discount (%)", 0, 50, 10) / 100
    with col2:
        st.write(f"**New Price:** {p * (1 - price_cut_pct):.2f} €")

    # 3. CALCULATIONS (The Cold Math)
    # Τύπος: Required Q Change = (Price Cut %) / (Original Margin % - Price Cut %)
    if current_margin_pct > price_cut_pct:
        req_vol_increase = price_cut_pct / (current_margin_pct - price_cut_pct)
        new_q = q * (1 + req_vol_increase)
    else:
        req_vol_increase = float('inf') # Η επιχείρηση μπαίνει μέσα σε κάθε μονάδα

    # 4. RESULTS DISPLAY
    st.subheader("Results")
    if req_vol_increase == float('inf'):
        st.error("🚨 CRITICAL: The proposed discount is equal to or higher than your current margin. You will lose money on every unit sold!")
    else:
        res1, res2 = st.columns(2)
        res1.metric("Required Volume Increase", f"+{req_vol_increase:.1%}")
        res2.metric("New Target Volume", f"{int(new_q)} units")
        
        st.warning(f"To keep the same gross profit, you must sell **{int(new_q - q)} additional units** due to the {price_cut_pct:.0%} discount.")

    # 5. SENSITIVITY TABLE
    st.write("### Discount Sensitivity Table")
    discounts = [0.02, 0.05, 0.10, 0.15, 0.20]
    data = []
    for d in discounts:
        if current_margin_pct > d:
            inc = d / (current_margin_pct - d)
            data.append({"Discount": f"{d:.0%}", "Req. Vol. Increase": f"+{inc:.1%}", "New Price": f"{p*(1-d):.2f}€"})
    
    st.table(pd.DataFrame(data))

    st.caption("Note: This analysis assumes Fixed Costs remain stable. It focuses purely on Contribution Margin protection.")
