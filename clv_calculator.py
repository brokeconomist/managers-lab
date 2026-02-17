import streamlit as st
import pandas as pd
import plotly.express as px
import io

# -------------------------------------------------
# 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ
# -------------------------------------------------
st.set_page_config(
    page_title="Strategic CLV Analyzer",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------
# 2. ΣΥΝΑΡΤΗΣΕΙΣ ΥΠΟΛΟΓΙΣΜΩΝ
# -------------------------------------------------
def calculate_clv_metrics(purchases, price, cost, marketing, retention, discount, churn, realization, risk_p, cac):
    cm = (purchases * (price - cost)) - marketing
    adj_discount = discount + risk_p
    clv = 0
    data = []
    cum_npv = -cac
    payback = None
    
    for t in range(1, int(retention) + 1):
        survival_prob = (1 - churn) ** t
        expected_m = cm * realization * survival_prob
        discounted_m = expected_m / ((1 + adj_discount) ** t)
        
        clv += discounted_m
        cum_npv += discounted_m
        
        data.append({
            "Year": t,
            "Net_Margin": expected_m,
            "Discounted_Flow": discounted_m,
            "Cumulative_NPV": cum_npv
        })
        
        if cum_npv >= 0 and payback is None:
            payback = t
            
    return clv - cac, payback, pd.DataFrame(data)

# -------------------------------------------------
# 3. UI & SIDEBAR
# -------------------------------------------------
def main():
    st.title("Strategic Customer Lifetime Value (CLV) Analyzer")
    st.caption("Professional Business Modeling Tool for Unit Economics")
    st.divider()

    with st.sidebar:
        st.header("⚙️ Παράμετροι Μοντέλου")
        with st.form("main_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                purchases = st.number_input("Purchases/Year", 1.0, 1000.0, 10.0)
                price = st.number_input("Price ($)", 0.0, 100000.0, 100.0)
                cost = st.number_input("Unit Cost ($)", 0.0, 100000.0, 60.0)
            with col_b:
                marketing = st.number_input("Retent. Cost ($)", 0.0, 10000.0, 20.0)
                cac = st.number_input("Acquis. Cost (CAC)", 0.0, 100000.0, 150.0)
                retention = st.slider("Horizon (Years)", 1, 20, 5)
            
            st.subheader("⚠️ Risk Factors")
            discount = st.number_input("Discount Rate", 0.0, 1.0, 0.08)
            churn = st.number_input("Churn Rate", 0.0, 1.0, 0.05)
            realization = st.number_input("Realization", 0.0, 1.0, 0.90)
            risk_p = st.number_input("Risk Premium", 0.0, 1.0, 0.03)
            
            run = st.form_submit_button("Ανάλυση & Αναφορά")

    if run:
        # Εκτέλεση Υπολογισμών
        final_clv, payback, df = calculate_clv_metrics(
            purchases, price, cost, marketing, retention, discount, churn, realization, risk_p, cac
        )
        
        ltv_total = final_clv + cac
        ratio = ltv_total / cac if cac > 0 else 0

        # 4. ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ (DASHBOARD)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Risk-Adjusted CLV", f"${final_clv:,.2f}")
        k2.metric("LTV/CAC Ratio", f"{ratio:.2f}x")
        k3.metric("Payback Period", f"{payback} Yrs" if payback else "N/A")
        
        status = "Healthy" if ratio >= 3 else "Moderate" if ratio >= 1 else "Critical"
        k4.markdown(f"**Status:** `{status}`")

        st.divider()

        # ΓΡΑΦΗΜΑΤΑ
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("Timeline of Customer Value")
            fig = px.line(df, x="Year", y="Cumulative_NPV", markers=True, 
                          title="Cumulative Net Present Value (NPV)")
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)
            

        with c2:
            st.subheader("📋 Executive Summary")
            report = f"""
            **Στρατηγική Αξιολόγηση:**
            - **Κερδοφορία:** Κάθε πελάτης αποφέρει καθαρά **${final_clv:,.2f}**.
            - **Αποδοτικότητα:** Το ratio **{ratio:.2f}x** δείχνει ότι το μοντέλο είναι **{status}**.
            - **Απόσβεση:** Χρειάζονται **{payback if payback else 'πάνω από ' + str(retention)}** έτη για να καλυφθεί το κόστος απόκτησης.
            
            **Σύσταση:**
            {"✅ Το μοντέλο είναι έτοιμο για scaling." if ratio >= 3 else "⚠️ Απαιτείται βελτίωση στο Retention ή μείωση του CAC."}
            """
            st.info(report)
            
            # DOWNLOAD DATA
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Yearly Analysis (CSV)", data=csv, 
                               file_name="clv_analysis.csv", mime="text/csv")

        # 5. COHORT COMPARISON (SENSITIVITY)
        st.subheader("🔍 Sensitivity Analysis (What-If Scenarios)")
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.write("**Scenario: -10% Churn Rate**")
            clv_opt, _, _ = calculate_clv_metrics(purchases, price, cost, marketing, retention, discount, churn * 0.9, realization, risk_p, cac)
            st.success(f"New CLV: ${clv_opt:,.2f} (Δ: {((clv_opt-final_clv)/final_clv)*100:+.1f}%)")

        with col_s2:
            st.write("**Scenario: +10% Price Increase**")
            clv_price, _, _ = calculate_clv_metrics(purchases, price * 1.1, cost, marketing, retention, discount, churn, realization, risk_p, cac)
            st.success(f"New CLV: ${clv_price:,.2f} (Δ: {((clv_price-final_clv)/final_clv)*100:+.1f}%)")

if __name__ == "__main__":
    main()
