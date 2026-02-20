import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🧪 Managers’ Lab")
        st.caption("Analytical Rigor · 365-Day Cycle")
        
        if st.button("🏠 Back to Home"):
            st.session_state.mode = "home"
            st.rerun()
            
        st.divider()
        
        # Mode Selection
        st.subheader("Navigation Mode")
        mode_choice = st.radio(
            "Select Approach:",
            ["🧭 Structured Path", "📚 Tool Library"],
            index=0 if st.session_state.mode == "path" else 1,
            label_visibility="collapsed"
        )
        
        # Update session state based on radio selection
        if mode_choice == "🧭 Structured Path":
            st.session_state.mode = "path"
        else:
            st.session_state.mode = "library"

        st.divider()
        
        # Progress Indicator (Only for Path Mode)
        if st.session_state.mode == "path":
            st.subheader("Progress")
            progress = st.session_state.flow_step / 5
            st.progress(progress)
            st.caption(f"Stage {st.session_state.flow_step} of 5")βψ
