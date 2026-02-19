import streamlit as st

# 1. ΕΙΣΑΓΩΓΗ ΤΩΝ ΕΡΓΑΛΕΙΩΝ (Βεβαιώσου ότι τα ονόματα των αρχείων είναι σωστά)
# Αν κάποιο αρχείο λείπει, το Streamlit θα βγάλει σφάλμα - απλά κάνε comment τη γραμμή
try:
    from unit_cost_app import show_unit_cost_app
    from credit_days_calculator import show_credit_days_calculator
    from inventory_turnover_calculator import show_inventory_turnover_calculator
    from financial_resilience_app import show_resilience_map
    from qspm_two_strategies import show_qspm_tool
    from pricing_power_radar import show_pricing_power_radar
except ImportError as e:
    st.error(f"Missing file: {e}")

# --- SETTINGS & STYLE ---
st.set_page_config(page_title="Managers’ Lab", page_icon="🧪", layout="wide")

# CSS για να φαίνεται σαν Pro App στο tablet
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; margin-bottom: 10px; }
    .stAlert { border-radius: 10px; }
    .main { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "Home"
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# --- SIDEBAR (Η "Βιτρίνα") ---
with st.sidebar:
    st.title("🧪 Managers’ Lab")
    
    if st.button("🏠 Αρχική Σελίδα"):
        st.session_state.selected_tool = "Home"
    
    st.divider()
    st.subheader("👴 Για τον Κυρ-Βαγγέλη (Free)")
    if st.button("📊 Κόστος Μονάδας"): st.session_state.selected_tool = "UnitCost"
    if st.button("📅 Ποιος Χρωστάει (Credit)"); st.session_state.selected_tool = "CreditDays"
    if st.button("📦 Ταχύτητα Αποθέματος"): st.session_state.selected_tool = "Inventory"
    
    st.divider()
    st.subheader("👨‍💼 Για τον Διάδοχο (Premium)")
    # Ένδειξη κλειδώματος
    res_label = "🛡️ Survival Map" if st.session_state.is_premium else "🔒 Survival Map"
    qspm_label = "🧭 Στρατηγική QSPM" if st.session_state.is_premium else "🔒 Στρατηγική QSPM"
    
    if st.button(res_label): st.session_state.selected_tool = "Resilience"
    if st.button(qspm_label): st.session_state.selected_tool = "QSPM"
    
    if not st.session_state.is_premium:
        st.warning("Ξεκλείδωσε το Survival Engine για 7 ημέρες")
        if st.button("🔓 Unlock All (10€)"):
            st.session_state.is_premium = True
            st.rerun()

# --- MAIN RENDER LOGIC ---

# 1. HOME PAGE
if st.session_state.selected_tool == "Home":
    st.title("🧪 Managers’ Lab")
    st.subheader("A structured decision laboratory for managers.")
    
    st.markdown("""
    Αυτό δεν είναι ένα απλό λογιστικό φύλλο. Είναι ο **Οδηγός Επιβίωσης** της επιχείρησης.
    
    - **Ο Κυρ-Βαγγέλης** χρησιμοποιεί την εμπειρία του.
    - **Ο Διάδοχος** χρησιμοποιεί το Lab για να αποδείξει τι αντέχει η επιχείρηση.
    """)
    
    

    st.info("💡 Ξεκίνα από τα Free εργαλεία στο πλάι ή ξεκλείδωσε το 'Survival Engine' για πλήρη ανάλυση.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Survival", "Phase 1")
    with col2:
        st.metric("Structure", "Phase 2")
    with col3:
        st.metric("Strategy", "Phase 3")

# 2. FREE TOOLS
elif st.session_state.selected_tool == "UnitCost":
    show_unit_cost_app()
elif st.session_state.selected_tool == "CreditDays":
    show_credit_days_calculator()
elif st.session_state.selected_tool == "Inventory":
    show_inventory_turnover_calculator()

# 3. PREMIUM TOOLS (With Paywall Check)
elif st.session_state.selected_tool in ["Resilience", "QSPM"]:
    if not st.session_state.is_premium:
        st.title("🛡️ Survival Engine (Locked)")
        st.markdown("""
        ### Γιατί να το ξεκλειδώσεις;
        Ο πατέρας σου ξέρει τα νούμερα στο κεφάλι του. Εσύ πρέπει να του δείξεις τον **Χάρτη Επιβίωσης**.
        
        **Τι θα πάρεις με το 7-ήμερο Unlock:**
        - **Resilience Map:** Δες αν η εταιρεία "σκάει" σε ένα σοκ 20% στην αγορά.
        - **Strategy Comparison:** Σύγκρινε δύο δρόμους (π.χ. Επέκταση vs Οικονομία) με νούμερα.
        - **Professional Reports:** Δείξε στο tablet γραφήματα που δεν αμφισβητούνται.
        
        **Κόστος:** 10€ (Μία φορά - Πρόσβαση για 7 ημέρες)
        """)
        
        if st.button("Ενεργοποίηση Πρόσβασης Τώρα"):
            st.session_state.is_premium = True
            st.rerun()
    else:
        # Αν είναι premium, δείξε το εργαλείο
        if st.session_state.selected_tool == "Resilience":
            show_resilience_map()
        else:
            show_qspm_tool()

# FOOTER
st.divider()
st.caption("Managers’ Lab · Built for the Next Generation of Decision Makers.")
