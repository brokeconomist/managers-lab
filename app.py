import streamlit as st

# --- Imports των εργαλείων σου ---
from home import show_home
from start_here import show_start_here
from break_even_shift_calculator import show_break_even_shift_calculator
from unit_cost_app import show_unit_cost_app
from credit_days_calculator import show_credit_days_calculator
from inventory_turnover_calculator import show_inventory_turnover_calculator
from pricing_power_radar import show_pricing_power_radar
from qspm_two_strategies import show_qspm_tool
# Φέρε και το νέο Resilience Map που φτιάξαμε
from financial_resilience_app import show_resilience_map 

# ----------------------------------------
# 1. Κατηγοριοποίηση (Free vs Premium)
# ----------------------------------------
# Εδώ είναι το "δόλωμα" για τον κυρ-Βαγγέλη και το "χρυσάφι" για τον γιο
free_tools = {
    "📊 Βασικά Εργαλεία (Free)": [
        ("Υπολογισμός Κόστους Μονάδας", show_unit_cost_app),
        ("Ημέρες Πίστωσης (Ποιος χρωστάει)", show_credit_days_calculator),
        ("Ταχύτητα Αποθέματος", show_inventory_turnover_calculator),
        ("Break-Even Analysis", show_break_even_shift_calculator),
    ]
}

premium_tools = {
    "🛡️ Survival Engine (Premium)": [
        ("Financial Resilience Map", show_resilience_map),
        ("QSPM – Στρατηγική Επιλογή", show_qspm_tool),
        ("Pricing Power Radar", show_pricing_power_radar),
    ]
}

# ----------------------------------------
# 2. Session State & Access Control
# ----------------------------------------
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False # Ξεκινάει ως Free

if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "🏠 Home"

# ----------------------------------------
# 3. Sidebar (Tablet Optimized)
# ----------------------------------------
st.sidebar.title("🧪 Managers’ Lab")

# FREE SECTION (Για τον πατέρα)
st.sidebar.subheader("🆓 Ελεύθερη Χρήση")
for name, func in free_tools["📊 Βασικά Εργαλεία (Free)"]:
    if st.sidebar.button(name, key=f"free_{name}"):
        st.session_state.selected_tool = name

st.sidebar.divider()

# PREMIUM SECTION (Για τον γιο)
st.sidebar.subheader("💎 Survival Engine")
if not st.session_state.is_premium:
    st.sidebar.info("🔓 Ξεκλείδωσε την πλήρη στρατηγική ανάλυση (7 ημέρες - 10€)")
    if st.sidebar.button("Unlock All Tools", type="primary"):
        st.session_state.is_premium = True # Εδώ θα έμπαινε η πληρωμή
        st.rerun()

for name, func in premium_tools["🛡️ Survival Engine (Premium)"]:
    # Αν δεν είναι premium, δείξε λουκέτο
    label = name if st.session_state.is_premium else f"🔒 {name}"
    if st.sidebar.button(label, key=f"prem_{name}"):
        if st.session_state.is_premium:
            st.session_state.selected_tool = name
        else:
            st.session_state.selected_tool = "Unlock_Page"

# ----------------------------------------
# 4. Render Logic
# ----------------------------------------

# Αρχική Σελίδα
if st.session_state.selected_tool == "🏠 Home":
    show_home() # Το κείμενο που έχεις ήδη για το Decision Path

# Σελίδα Πληρωμής / Teaser
elif st.session_state.selected_tool == "Unlock_Page":
    st.title("🛡️ Ξεκλείδωσε το Survival Engine")
    st.markdown("""
    ### Ο κυρ-Βαγγέλης ξέρει τα νούμερα. Εσύ ξέρεις τη Στρατηγική;
    
    Για να πείσεις τον πατέρα σου ότι η επιχείρηση χρειάζεται **επιστημονική διοίκηση**, πρέπει να του δείξεις τι θα γίνει αν η αγορά αλλάξει αύριο.
    
    **Με το Premium Access ξεκλειδώνεις:**
    1. **Financial Resilience Map:** Το στίγμα της εταιρείας στον χάρτη επιβίωσης.
    2. **Stress Test Simulator:** Τι συμβαίνει στο ταμείο αν πέσει ο τζίρος 20%.
    3. **Strategy Comparison (QSPM):** Για να παίρνεις αποφάσεις με δεδομένα, όχι με το "ένστικτο".
    
    **Κόστος:** 10€ για 7 ημέρες. Κατέβασε τα PDF, δείξε τα στον πατέρα σου, γίνε ο επόμενος Leader.
    """)
    
    
    
    if st.button("Απόκτησε Πρόσβαση Τώρα"):
        st.session_state.is_premium = True
        st.success("Η πρόσβαση ενεργοποιήθηκε!")
        st.rerun()

# Φόρτωση των εργαλείων
else:
    # Ψάξε στα Free
    for name, func in free_tools["📊 Βασικά Εργαλεία (Free)"]:
        if name == st.session_state.selected_tool:
            func()
    
    # Ψάξε στα Premium
    for name, func in premium_tools["🛡️ Survival Engine (Premium)"]:
        if name == st.session_state.selected_tool:
            func()

# ----------------------------------------
# Footer (Quick Exit)
# ----------------------------------------
if st.session_state.selected_tool != "🏠 Home":
    if st.sidebar.button("🏠 Επιστροφή στην Αρχική"):
        st.session_state.selected_tool = "🏠 Home"
        st.rerun()
