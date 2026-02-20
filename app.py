import streamlit as st

# 1. SETUP ΣΕΛΙΔΑΣ (Πάντα πρώτο)
st.set_page_config(
    page_title="Managers’ Lab", 
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INITIALIZATION & SHARED CORE
from core.system_state import initialize_system_state

# Αρχικοποιούμε τις 5 ομάδες μεταβλητών (Price, Volume, Costs, Days, etc.)
initialize_system_state()

if "mode" not in st.session_state:
    st.session_state.mode = "home"
if "flow_step" not in st.session_state:
    st.session_state.flow_step = 1

# 3. IMPORT UI COMPONENTS
from ui.sidebar import render_sidebar
from ui.home import show_home

# Εμφάνιση Sidebar (εδώ γίνεται η επιλογή mode: Home, Path, Library)
render_sidebar()

# 4. ROUTING (Δρομολόγηση)
# Το session_state.mode αλλάζει από το ui/sidebar.py
if st.session_state.mode == "home":
    show_home()

elif st.session_state.mode == "path":
    # Structured Journey (Το 5-Stage Path)
    st.info(f"📍 Current Stage: {st.session_state.flow_step} of 5")
    
    if st.session_state.flow_step == 1:
        from path.step1_survival import run_step
        run_step()
    elif st.session_state.flow_step == 2:
        from path.step2_cash import run_step
        run_step()
    elif st.session_state.flow_step == 3:
        from path.step3_unit_economics import run_step
        run_step()
    elif st.session_state.flow_step == 4:
        from path.step4_sustainability import run_step
        run_step()
    elif st.session_state.flow_step == 5:
        from path.step5_strategy import run_step
        run_step()

elif st.session_state.mode == "library":
    # Ελεύθερη επιλογή εργαλείων
    from ui.library import show_library
    show_library()

# 5. FOOTER (Προαιρετικό, εμφανίζεται σε όλες τις σελίδες)
st.sidebar.divider()
st.sidebar.caption("v2.0 | Shared Core Architecture")
