import streamlit as st

def show_home():
    # --- Page title ---
    st.title("🧪 Managers’ Lab")
    
    # --- Short description ---
    st.markdown(
        """
        Welcome to Managers’ Lab — your interactive toolkit for financial analysis, 
        decision support, and business modeling.  
        Explore, experiment, and make data-driven decisions with practical tools.
        """
    )

    # --- Main categories overview ---
    st.subheader("Tool Categories")
    
    st.markdown("""
    - **Getting Started**: Step-by-step guides to begin using the Lab.  
    - **Break-Even & Pricing**: Analyze costs, margins, and pricing impact.  
    - **Customer Value**: Evaluate CLV, substitution, and complementary products.  
    - **Finance & Cash Flow**: Manage cash cycles, credit policies, and loans.  
    - **Cost & Profit**: Estimate unit costs, gross profit, and NPV.  
    - **Inventory & Operations**: Calculate EOQ, turnover, and credit days.
    """)
    
    # --- Quick start instruction ---
    st.subheader("Getting Started")
    st.markdown(
        """
        Use the sidebar to select a category and tool.  
        Each tool comes with step-by-step instructions and examples.  
        Your data stays local — experiment freely!
        """
    )

    # Optional: add a separator or note
    st.markdown("---")
    st.info("Tip: Start with 'Getting Started' if this is your first visit.")
