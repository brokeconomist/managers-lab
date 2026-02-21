import streamlit as st

def show_about():
    st.title("🧪 About Managers' Lab")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("The Methodology")
        st.write("""
        **Managers' Lab** is a Decision Engineering environment designed for small business 
        optimization. It bypasses traditional accounting narratives to focus on 
        the cold reality of cash flow, unit economics, and structural stability.
        
        The system operates on a **365-day fiscal model**, prioritizing liquidity 
        and structural stability over abstract growth metrics.
        """)
        
        st.subheader("Philosophy")
        st.info("""
        We believe that most business tragedies are predictable and preventable 
        through rigorous baseline calibration and stress-testing.
        """)

    with col2:
        st.subheader("Contact & Feedback")
        st.write("For technical issues, methodology inquiries, or feedback:")
        
        # Στοιχεία επικοινωνίας
        st.markdown("📧 **Email:** manosv@gmail.com")
        st.markdown("🌐 **Web:** [https://medium.com/@ManosV_18]")
        
        st.divider()
        st.caption("Version: 2.0.1 (Stable Build)")
        st.caption("Architecture: Shared Core OS")

    if st.button("⬅️ Back to Control Center"):
        st.session_state.mode = "home"
        st.rerun()
