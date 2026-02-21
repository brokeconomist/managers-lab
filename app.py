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

render_sidebar()

# 4. ROUTING LOGIC
mode = st.session_state.get("mode", "home")

if mode == "home":
    show_home()

elif mode == "path":
    step = st.session_state.get("flow_step", 0)
    
    if step == 0:
        # Configuration phase - No progress indicator shown yet
        from path.step0_calibration import run_step
        run_step()
    else:
        # Analysis phase - Showing progress from 1 to 5
        st.info(f"📍 Analysis Stage: {step} of 5")
        
        if step == 1:
            from path.step1_survival import run_step
            run_step()
        elif step == 2:
            from path.step2_cash import run_step
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

elif mode == "library":
    from ui.library import show_library
    show_library()

# 5. FOOTER
st.sidebar.divider()
st.sidebar.caption("v2.0 | Shared Core Architecture | 365-Day Calc")
