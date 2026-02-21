import streamlit as st

# 1. PAGE SETUP
st.set_page_config(
    page_title="Managers' Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. INITIALIZATION & SHARED CORE
from core.system_state import initialize_system_state
initialize_system_state()

# 3. UI COMPONENTS
from ui.sidebar import render_sidebar
from ui.home import show_home

# We render the sidebar first so it can update the session_state
render_sidebar()

# --- 4. ROUTING LOGIC (app.py) ---
mode = st.session_state.get("mode", "home")

if mode == "home":
    show_home()

elif mode == "path":
    step = st.session_state.get("flow_step", 0)
    if step == 0:
        from path.step0_calibration import run_step
        run_step()
    else:
        st.info(f"📍 Analysis Stage: {step} of 5")
        if step == 1:
            from path.step1_survival import run_step
            run_step()
        # ... τα υπόλοιπα steps ...

elif mode == "library":
    from ui.library import show_library
    show_library()

# ΑΥΤΟ ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ ΕΔΩ - ΤΕΡΜΑ ΑΡΙΣΤΕΡΑ ΣΤΗΝ ΙΔΙΑ ΓΡΑΜΜΗ ΜΕ ΤΑ ΑΛΛΑ ELIF
elif mode == "about":
    from ui.about import show_about
    show_about()

# 5. FOOTER
st.sidebar.divider()
st.sidebar.caption("v2.0 | Shared Core Architecture | 365-Day Calc")
