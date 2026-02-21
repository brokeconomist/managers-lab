import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🧪 Managers’ Lab")
        st.caption("Strategic Decision Support")
        
        st.divider()

        # Home Button
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.mode = "home"
            st.session_state.selected_tool = None
            st.rerun()
            
        st.divider()
        st.subheader("Navigation")

        # Tool Library Button
        if st.button("📚 Tool Library", use_container_width=True):
            st.session_state.mode = "library"
            st.session_state.selected_tool = None
            st.rerun()

        # Structured Path Button
        # Logic: If not locked, start at Stage 0. If locked, resume/start at Stage 1.
        if st.button("🧭 Structured Path", use_container_width=True):
            st.session_state.mode = "path"
            if not st.session_state.get('baseline_locked', False):
                st.session_state.flow_step = 0
            else:
                st.session_state.flow_step = 1
            st.session_state.selected_tool = None
            st.rerun()

        # Progress Bar (Visible only in Path mode)
        if st.session_state.get('mode') == "path":
            step = st.session_state.get('flow_step', 0)
            if step > 0:  # Only show progress for Analysis Stages 1-5
                st.divider()
                st.caption(f"Analysis Progress: Stage {step} of 5")
                st.progress(step / 5)

        # Support & Information Section
        st.divider()
        if st.button("ℹ️ About & Support", use_container_width=True):
            st.session_state.mode = "about"
            st.session_state.selected_tool = None
            st.rerun()

        # Cold Analysis Footer Note
        st.divider()
        st.caption("Analytical focus: Efficiency, Stability, & Survival Margin.")
        st.caption("System Version: 2.0.1")
