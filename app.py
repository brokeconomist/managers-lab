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

# Render sidebar to handle navigation state updates
render_sidebar()

# --- 4. ROUTING LOGIC (The Brain of the OS) ---
mode = st.session_state.get("mode", "home")

if mode == "home":
    show_home()

elif mode == "path":
    step = st.session_state.get("flow_step", 0)
    
    # Progress indicator for Path mode (Steps 1-5)
    if step > 0:
        st.info(f"📍 Path Progress: Stage {step} of 5")

    # Step Routing
    if step == 0:
        from path.step0_calibration import run_step
        run_step()
    elif step == 1:
        from path.step1_survival import run_step
        run_step()
    elif step == 2:
        from path.cash_cycle import run_step
        run_step()
    elif step == 3:
        from path.step3_unit_economics import run_step
        run_step()
    elif step == 4:
        from path.step4_sustainability import run_step
        run_step()
    elif step == 5:
        from path.step5_strategy import run_step
        run_step()
    else:
        st.warning("Unknown Step. Returning to Calibration.")
        st.session_state.flow_step = 0
        st.rerun()

elif mode == "library":
    from ui.library import show_library
    show_library()

elif mode == "about":
    from ui.about import show_about
    show_about()

# 5. FOOTER (Sidebar bottom)
st.sidebar.divider()
st.sidebar.caption("v2.0.1 | Shared Core | 365-Day Cycle")
