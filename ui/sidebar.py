import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🧪 Managers’ Lab")
        st.caption("Strategic Decision Support")
        
        st.divider()

        # Κουμπί Home
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.mode = "home"
            st.session_state.selected_tool = None
            st.rerun()
            
        st.divider()
        st.subheader("Navigation")

        # Κουμπί Library
        if st.button("📚 Tool Library", use_container_width=True):
            st.session_state.mode = "library"
            st.session_state.selected_tool = None
            st.rerun()

        # Κουμπί Path
        if st.button("🧭 Structured Path (5 Stages)", use_container_width=True):
            st.session_state.mode = "path"
            st.session_state.flow_step = 1
            st.session_state.selected_tool = None
            st.rerun()

        # Progress Bar μόνο αν είμαστε σε Path mode
        if st.session_state.get('mode') == "path":
            st.divider()
            step = st.session_state.get('flow_step', 1)
            st.caption(f"Path Progress: Stage {step} of 5")
            st.progress(step / 5)

        st.divider()
        # Cold Analysis Note
        st.caption("Analytical focus: Efficiency, Stability, & Survival Margin.")
