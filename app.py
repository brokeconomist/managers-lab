import streamlit as st

# 1. PAGE SETUP
# Configure the global appearance and browser tab metadata.
st.set_page_config(
    page_title="Managers' Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. INITIALIZATION & SHARED CORE
from core.system_state import initialize_system_state

# This initializes all session keys: Baseline Status, Financials, and UI State.
# Default starting point: mode="home", flow_step=0, baseline_locked=False.
initialize_system_state()

# 3. UI COMPONENTS
from ui.sidebar import render_sidebar
from ui.home import show_home

# Render the persistent navigation sidebar.
render_sidebar()

# 4. ROUTING LOGIC
# The application flow is determined by the 'mode' and 'flow_step' keys.
mode = st.session_state.get("mode", "home")

if mode == "home":
    # Adaptive Home: Displays 'Entry Mode' (Calibration required) 
    # or 'Control Center' (Dashboard) based on baseline_locked status.
    show_home()

elif mode == "path":
    # ANALYSIS MODE: A structured 5-stage journey through business economics.
    step = st.session_state.get("flow_step", 0)
    
    # Progress indicator for user orientation.
    st.info(f"📍 Current Stage: {step} of 5")

    # Dynamic Path Routing based on the current step.
    if step == 0:
        # System Initialization & Baseline Definition.
        from path.step0_calibration import run_step
        run_step()
    elif step == 1:
        # Survival Anchor: Cash reserves and Burn Rate analysis.
        from path.step1_survival import run_step
        run_step()
    elif step == 2:
        # Cash Flow Optimization: Timing and Liquidity.
        from path.step2_cash import run_step
        run_step()
    elif step == 3:
        # Unit Economics: Margin optimization and Pricing sensitivity.
        from path.step3_unit_economics import run_step
        run_step()
    elif step == 4:
        # Sustainability: Long-term growth and debt-servicing capacity.
        from path.step4_sustainability import run_step
        run_step()
    elif step == 5:
        # Strategy: Valuation and Exit readiness.
        from path.step5_strategy import run_step
        run_step()

elif mode == "library":
    # TOOL LIBRARY: Direct access to specific financial simulators.
    from ui.library import show_library
    show_library()

# 5. FOOTER
# Sidebar versioning and architecture info.
st.sidebar.divider()
st.sidebar.caption("v2.0 | Shared Core Architecture | 365-Day Calc")
