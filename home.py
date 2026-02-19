import streamlit as st

# 1. Αρχικοποίηση του βήματος (αν δεν υπάρχει)
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 0  # 0 σημαίνει Αρχική Σελίδα

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔓 Free Tools")
    st.caption("Για τον κυρ-Βαγγέλη (Quick Checks)")
    # Εδώ μπορείς να έχεις τα 3 free εργαλεία πάντα διαθέσιμα
    free_choice = st.radio("Γρήγορη Πρόσβαση:", ["Αρχική", "Κόστος Μονάδας", "Ημέρες Πίστωσης", "Απόθεμα"])

# --- MAIN LOGIC ---

# Αν ο χρήστης επιλέξει κάτι από το sidebar, μηδενίζουμε το Path για να πάει εκεί
if free_choice != "Αρχική":
    st.session_state.flow_step = -1 # Ειδική τιμή για ελεύθερη πλοήγηση

# CASE 0: Αρχική Σελίδα (The Hook)
if st.session_state.flow_step == 0 and free_choice == "Αρχική":
    st.title("🧪 Managers’ Lab")
    st.markdown("""
    ### Οδηγός Επιβίωσης & Λήψης Αποφάσεων
    
    Αυτό δεν είναι ένα απλό κομπιουτεράκι. Είναι μια **διαδρομή απόφασης**.
    Ο κυρ-Βαγγέλης ξέρει τα νούμερα, αλλά εσύ πρέπει να δείξεις αν η επιχείρηση **αντέχει**.
    """)
    
    # 

    st.info("💡 Η διαδρομή είναι κλειδωμένη: Πρώτα η Επιβίωση, μετά η Στρατηγική.")

    if st.button("Ξεκίνα τη Δομημένη Διαδρομή (Survival Engine)", type="primary"):
        st.session_state.flow_step = 1
        st.rerun()

# CASE 1: Το πρώτο βήμα της διαδρομής (Survival)
elif st.session_state.flow_step == 1:
    st.header("Βήμα 1: Survival Anchor")
    # Εδώ καλείς τη συνάρτηση από το resilience_app
    st.write("Εδώ εξετάζουμε αν το σύστημα αντέχει σοκ.")
    
    if st.button("Επόμενο Βήμα: Structural Pressure"):
        st.session_state.flow_step = 2
        st.rerun()

# CASE -1: Ελεύθερα Εργαλεία (Για τον κυρ-Βαγγέλη)
elif st.session_state.flow_step == -1:
    if free_choice == "Κόστος Μονάδας":
        st.subheader("Υπολογισμός Κόστους")
        # call your function: show_unit_cost_app()
    elif free_choice == "Ημέρες Πίστωσης":
        st.subheader("Ποιος μου χρωστάει")
        # call your function: show_credit_days_calculator()
