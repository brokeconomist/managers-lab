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

elif mode == "path":
    step = st.session_state.get("flow_step", 0)
    
    if step == 0:
        from path.step0_calibration import run_step
        run_step()
    else:
        # Progress indicator for Analysis stages
        st.info(f"📍 Analysis Stage: {step} of 5")
        
        if step == 1:
            from path.step1_survival import run_step
            run_step()
        elif step == 2:
            # ΑΥΤΟ ΠΡΕΠΕΙ ΝΑ ΥΠΑΡΧΕΙ ΓΙΑ ΝΑ ΕΜΦΑΝΙΣΤΕΙ ΤΟ ΒΗΜΑ 2
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

# 5. FOOTER
st.sidebar.divider()
st.sidebar.caption("v2.0 | Shared Core Architecture | 365-Day Calc")
