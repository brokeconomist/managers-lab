import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🧪 Managers’ Lab")
        
        if st.button("🏠 Home"):
            st.session_state.mode = "home"
            st.rerun()
            
        st.divider()
        st.subheader("Navigation Mode")
        
        # Επιλογή Mode
        mode_choice = st.radio(
            "Select Approach:",
            ["🧭 Structured Path", "📚 Tool Library"],
            index=0 if st.session_state.mode == "path" else 1
        )
        
        if mode_choice == "🧭 Structured Path":
            st.session_state.mode = "path"
        else:
            st.session_state.mode = "library"

        if st.session_state.mode == "path":
            st.divider()
            st.caption(f"Progress: Stage {st.session_state.flow_step} of 5")
            st.progress(st.session_state.flow_step / 5)
