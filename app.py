import streamlit as st

# 1. SETUP ΣΕΛΙΔΑΣ
st.set_page_config(page_title="Managers’ Lab", layout="wide")

# 2. INITIALIZATION
if "mode" not in st.session_state:
    st.session_state.mode = "home"
if "flow_step" not in st.session_state:
    st.session_state.flow_step = 1

# 3. IMPORT UI COMPONENTS
from ui.sidebar import render_sidebar
from ui.home import show_home

# Εμφάνιση Sidebar
render_sidebar()

# 4. ROUTING (Δρομολόγηση)
if st.session_state.mode == "home":
    show_home()

elif st.session_state.mode == "path":
    # Structured Journey
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
    from ui.library import show_library
    show_library()
