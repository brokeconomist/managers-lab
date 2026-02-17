import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. Υπολογιστική Μηχανή (Internal Logic) ---
def get_clv_timeline(purchases, price, cost, marketing, retention, discount, churn, realization, risk_p, cac):
    cm = (purchases * (price - cost)) - marketing
    adj_disc = discount + risk_p
    cum_npv = -cac
    data = []
    payback = None
    
    for t in range(1, int(retention) + 1):
        survival = (1 - churn) ** t
        # Discounted Cash Flow formula
        flow = (cm * realization * survival) / ((1 + adj_disc) ** t)
        cum_npv += flow
        data.append({"Year": t, "Cumulative_NPV": cum_npv})
        if cum_npv >= 0 and payback is None:
            payback = t
    return pd.DataFrame(data), cum_npv, payback

# --- 2. Η Κύρια Συνάρτηση (Exported to app.py) ---
def show_clv_calculator():
    st.title("👥 Strategic CLV & Scenario Planner")
    st.markdown("""
    Αυτό το εργαλείο συγκρίνει δύο επιχειρηματικά σενάρια για να αναδείξει πώς μικρές αλλαγές στο 
    **Churn** ή στην **Τιμή** επηρεάζουν την τελική αξία της επιχείρησης.
    """)
    st.divider()

    # --- Sidebar Inputs ---
    with st.sidebar:
        st.header("📊 Σενάριο Α (Current)")
        p_a = st.number_input("Purchases/Year (A)", value=10.0)
        pr_a = st.number_input("Price (A) $", value=100.0)
        cac_a = st.number_input("Acquisition Cost (A) $", value=150.0)
        ch_a = st.number_input("Churn Rate (A) %", value=0.05)

        st.header("🚀 Σενάριο Β (Target)")
        p_b = st.number_input("Purchases/Year (B)", value=10.0)
        pr_b = st.number_input("Price (B) $", value=110.0)
        cac_b = st.number_input("Acquisition Cost (B) $", value=150.0)
        ch_b = st.number_input("Churn Rate (B) %", value=0.03)

        st.divider()
        ret = st.slider("Retention Horizon (Years)", 1, 15, 5)
        # Σταθερές παραμέτρων
        cost, mkt, disc, real, risk_p = 60.0, 20.0, 0.08, 0.90, 0.03
        run = st.button("Generate Comparison Report")

    if run:
        # Εκτέλεση Υπολογισμών
        df_a, final_a, pb_a = get_clv_timeline(p_a, pr_a, cost, mkt, ret, disc, ch_a, real, risk_p, cac_a)
        df_b, final_b, pb_b = get_clv_timeline(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)

        # --- Οπτικοποίηση: Cumulative NPV Comparison ---
        st.subheader("📉 Σύγκριση Κερδοφορίας (Cash Flow Timeline)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_a['Year'], y=df_a['Cumulative_NPV'], name='Σενάριο Α (Current)', line=dict(color='#EF553B', dash='dash')))
        fig.add_trace(go.Scatter(x=df_b['Year'], y=df_b['Cumulative_NPV'], name='Σενάριο Β (Optimized)', line=dict(color='#00CC96', width=4)))
        fig.add_hline(y=0, line_dash="dot", line_color="black")
        
        st.plotly_chart(fig, use_container_width=True)
        

        # --- Ανάλυση & Εξηγήσεις ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Executive Summary")
            st.write(f"""
            **1. Value Gap:** Η βελτιστοποίηση του μοντέλου προσφέρει επιπλέον **${final_b - final_a:,.2f}** ανά πελάτη.
            **2. Payback Period:** - Σενάριο Α: Απόσβεση σε **{pb_a if pb_a else '>'+str(ret)} έτη**.
            - Σενάριο Β: Απόσβεση σε **{pb_b if pb_b else '>'+str(ret)} έτη**.
            """)
            
            ltv_a = (final_a + cac_a) / cac_a if cac_a > 0 else 0
            ltv_b = (final_b + cac_b) / cac_b if cac_b > 0 else 0
            
            st.metric("Βελτίωση LTV/CAC Ratio", f"{ltv_b:.2f}x", f"{ltv_b - ltv_a:.2f}x")
            

        with col2:
            st.subheader("💡 Τι σημαίνουν αυτά τα νούμερα;")
            with st.expander("Τι είναι το Payback Period;", expanded=True):
                st.write("""
                Είναι ο χρόνος που απαιτείται για να καλύψει ο πελάτης το κόστος απόκτησής του (CAC). 
                Όσο πιο γρήγορα η γραμμή περάσει το μηδέν, τόσο λιγότερο κεφάλαιο κίνησης χρειάζεται η επιχείρηση.
                """)
            
            with st.expander("Γιατί το Risk-Adjusted CLV είναι χαμηλότερο;"):
                st.write(f"""
                Factor-In: Έχουμε συμπεριλάβει **Churn ({ch_a*100}%)** και **Realization ({real*100}%)**. 
                Αυτό σημαίνει ότι υπολογίζουμε την "ψυχρή αλήθεια": ότι κάποιοι πελάτες θα φύγουν και κάποια έσοδα 
                δεν θα εισπραχθούν ποτέ.
                """)

        # --- Πίνακας Δεδομένων ---
        st.subheader("📊 Συγκριτικός Πίνακας Metrics")
        comparison_df = pd.DataFrame({
            "Metric": ["Net Lifetime Value", "Payback Period", "LTV/CAC Ratio", "Risk Exposure"],
            "Scenario A": [f"${final_a:,.2f}", f"{pb_a} Yrs", f"{ltv_a:.2f}x", "High"],
            "Scenario B": [f"${final_b:,.2f}", f"{pb_b} Yrs", f"{ltv_b:.2f}x", "Low"]
        })
        st.table(comparison_df)

# Boilerplate για αυτόνομη εκτέλεση
if __name__ == "__main__":
    show_clv_calculator()
