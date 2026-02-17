import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def get_clv_timeline(purchases, price, cost, marketing, retention, discount, churn, realization, risk_p, cac):
    cm = (purchases * (price - cost)) - marketing
    adj_disc = discount + risk_p
    cum_npv = -cac
    data = []
    payback = None
    
    for t in range(1, int(retention) + 1):
        survival = (1 - churn) ** t
        flow = (cm * realization * survival) / ((1 + adj_disc) ** t)
        cum_npv += flow
        data.append({"Year": t, "Cumulative_NPV": cum_npv})
        if cum_npv >= 0 and payback is None:
            payback = t
    return pd.DataFrame(data), cum_npv, payback

def show_clv_calculator():
    st.header("👥 Strategic CLV & Scenario Comparison")
    st.write("Ανάλυση της αξίας του πελάτη με συνυπολογισμό κινδύνου (Risk-Adjusted) και σύγκριση σεναρίων.")

    # Sidebar για τις παραμέτρους
    st.sidebar.subheader("⚙️ Παράμετροι Ανάλυσης")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Σενάριο Α (Current)")
        p_a = st.number_input("Purchases/Year (A)", value=10.0, key="pa")
        pr_a = st.number_input("Price (A) $", value=100.0, key="pra")
        cac_a = st.number_input("CAC (A) $", value=150.0, key="caca")
        ch_a = st.number_input("Churn Rate (A) %", value=0.05, step=0.01, key="cha")

    with col2:
        st.subheader("🚀 Σενάριο Β (Target)")
        p_b = st.number_input("Purchases/Year (B)", value=10.0, key="pb")
        pr_b = st.number_input("Price (B) $", value=110.0, key="prb")
        cac_b = st.number_input("CAC (B) $", value=150.0, key="cacb")
        ch_b = st.number_input("Churn Rate (B) %", value=0.03, step=0.01, key="chb")

    # Σταθερές ρίσκου
    cost, mkt, disc, real, risk_p = 60.0, 20.0, 0.08, 0.90, 0.03
    ret = 5 # Ορίζοντας 5ετίας

    if st.button("Calculate & Compare"):
        df_a, final_a, pb_a = get_clv_timeline(p_a, pr_a, cost, mkt, ret, disc, ch_a, real, risk_p, cac_a)
        df_b, final_b, pb_b = get_clv_timeline(p_b, pr_b, cost, mkt, ret, disc, ch_b, real, risk_p, cac_b)

        # Γράφημα
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_a['Year'], y=df_a['Cumulative_NPV'], name='Σενάριο Α', line=dict(color='#EF553B', dash='dash')))
        fig.add_trace(go.Scatter(x=df_b['Year'], y=df_b['Cumulative_NPV'], name='Σενάριο Β', line=dict(color='#00CC96', width=4)))
        fig.add_hline(y=0, line_dash="dot", line_color="white")
        st.plotly_chart(fig, use_container_width=True)
        

        # Εξηγήσεις
        st.subheader("💡 Στρατηγική Ερμηνεία")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.info(f"""
            **Value Gap:** Η διαφορά μεταξύ των σεναρίων είναι **${final_b - final_a:,.2f}** ανά πελάτη.
            
            **Payback Period:**
            - Σενάριο Α: {pb_a if pb_a else '>5'} έτη.
            - Σενάριο Β: {pb_b if pb_b else '>5'} έτη.
            """)
            

        with info_col2:
            st.warning(f"""
            **Risk-Adjusted CLV:** Τα νούμερα αυτά δεν είναι απλά έσοδα. Είναι η καθαρή παρούσα αξία αφού αφαιρέσουμε το ρίσκο απώλειας πελάτη (Churn) και το κόστος κεφαλαίου.
            """)

        # Πίνακας
        st.table(pd.DataFrame({
            "Metric": ["Risk-Adjusted CLV", "Payback Year", "LTV/CAC Ratio"],
            "Scenario A": [f"${final_a:,.2f}", pb_a, f"{(final_a+cac_a)/cac_a:.2f}x"],
            "Scenario B": [f"${final_b:,.2f}", pb_b, f"{(final_b+cac_b)/cac_b:.2f}x"]
        }))
