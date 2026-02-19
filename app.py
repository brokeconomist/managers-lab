import streamlit as st

# 1. ΕΙΣΑΓΩΓΗ ΤΩΝ ΕΡΓΑΛΕΙΩΝ
try:
    from unit_cost_app import show_unit_cost_app
    from credit_days_calculator import show_credit_days_calculator
    from inventory_turnover_calculator import show_inventory_turnover_calculator
    from financial_resilience_app import show_resilience_map
    from qspm_two_strategies import show_qspm_tool
except ImportError as e:
    st.error(f"Λείπει αρχείο: {e}")

# --- SETTINGS & STYLE ---
st.set_page_config(page_title="Managers’ Lab", page_icon="🧪", layout="wide")

# CSS για Tablet-Friendly περιβάλλον
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.8em; font-weight: bold; border: 1px solid #d1d1d1; }
    .stMetric { background-color: #ffffff; border: 1px solid #e0e0e0; padding: 10px; border-radius: 10px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#f8f9fa, #e9ecef); }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "Home"
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧪 Managers’ Lab")
    
    if st.sidebar.button("🏠 Αρχική Σελίδα"):
        st.session_state.selected_tool = "Home"
    
    st.divider()
    st.subheader("👴 Εργαλεία για τον Πατέρα (Free)")
    # ΔΙΟΡΘΩΜΕΝΗ ΣΥΝΤΑΞΗ ΕΔΩ
    if st.sidebar.button("📊 Κόστος Μονάδας"): 
        st.session_state.selected_tool = "UnitCost"
    if st.sidebar.button("📅 Ποιος Χρωστάει (Credit)"): 
        st.session_state.selected_tool = "CreditDays"
    if st.sidebar.button("📦 Ταχύτητα Αποθέματος"): 
        st.session_state.selected_tool = "Inventory"
    
    st.divider()
    st.subheader("👨‍💼 Για τον Διάδοχο (Premium)")
    
    res_label = "🛡️ Survival Map" if st.session_state.is_premium else "🔒 Survival Map"
    qspm_label = "🧭 Στρατηγική QSPM" if st.session_state.is_premium else "🔒 Στρατηγική QSPM"
    
    if st.sidebar.button(res_label): 
        st.session_state.selected_tool = "Resilience"
    if st.sidebar.button(qspm_label): 
        st.session_state.selected_tool = "QSPM"
    
    if not st.session_state.is_premium:
        st.info("Unlock Survival Engine (10€)")
        if st.sidebar.button("🔓 Ξεκλείδωμα Τώρα", type="primary"):
            st.session_state.is_premium = True
            st.rerun()

# --- MAIN RENDER LOGIC ---

if st.session_state.selected_tool == "Home":
    st.title("🧪 Managers’ Lab")
    st.markdown("""
    ### Οδηγός Επιβίωσης & Λήψης Αποφάσεων
    
    Εδώ δεν κάνουμε απλή λογιστική. Εδώ χαρτογραφούμε την αντοχή της επιχείρησης στα σοκ της αγοράς.
    
    **Πώς να ξεκινήσεις:**
    1. Χρησιμοποίησε τα **δωρεάν εργαλεία** για να ελέγξεις τα καθημερινά σου έξοδα και εισπράξεις.
    2. Ξεκλείδωσε το **Survival Engine** για να δεις αν η επιχείρηση θα αντέξει μια κρίση ή αν το επόμενο βήμα σου είναι ασφαλές.
    """)
    
    

    st.divider()
    c1, c2 = st.columns(2)
    c1.info("**Για τον κυρ-Βαγγέλη:** Εστίασε στο Κόστος και την Αποθήκη. Τα νούμερα που ξέρεις, σε γράφημα.")
    c2.success("**Για τον Γιο:** Εστίασε στη Ρευστότητα και τη Στρατηγική. Απόδειξε ότι ξέρεις να διοικείς με δεδομένα.")

elif st.session_state.selected_tool == "UnitCost":
    show_unit_cost_app()

elif st.session_state.selected_tool == "CreditDays":
    show_credit_days_calculator()

elif st.session_state.selected_tool == "Inventory":
    show_inventory_turnover_calculator()

elif st.session_state.selected_tool in ["Resilience", "QSPM"]:
    if not st.session_state.is_premium:
        st.title("🛡️ Survival Engine (Locked)")
        st.markdown("""
        ### Γιατί ο γιος πρέπει να το ξεκλειδώσει;
        
        Ο κυρ-Βαγγέλης έχει το ένστικτο, εσύ όμως χρειάζεσαι την **απόδειξη**. 
        Με το 7-ήμερο Unlock μπορείς να του δείξεις:
        - **Τον Χάρτη Επιβίωσης:** Πού βρίσκεται η εταιρεία σε σχέση με τον κίνδυνο.
        - **Stress Test:** Τι θα συμβεί αν αύριο οι πελάτες πληρώσουν 15 μέρες αργότερα.
        - **Σύγκριση Στρατηγικής:** Γιατί η "ιδέα σου" είναι οικονομικά καλύτερη.
        """)
        
        if st.button("Unlock All Tools for 7 Days (10€)", type="primary"):
            st.session_state.is_premium = True
            st.rerun()
    else:
        if st.session_state.selected_tool == "Resilience":
            show_resilience_map()
        else:
            show_qspm_tool()

# FOOTER
st.divider()
st.caption("Managers’ Lab · Built for Managers, Trusted by Founders.")
