import streamlit as st

def show_home():

    st.title("🧪 Managers’ Lab")

    st.markdown("""
    A decision laboratory for managers.

    Not a dashboard.  
    Not a reporting or forecasting tool.

    Managers’ Lab exists to test **what must be true** for a decision to work —
    and what breaks when it doesn’t.

    The tools are already built.  
    Judgment is yours.
    """)

    st.divider()

    st.subheader("Start with the decision")

    st.markdown("""
    Choose the type of decision you are trying to make.
    Each path exposes the assumptions, constraints, and trade-offs involved.
    """)

    # --- CENTRAL DECISION MENU ---
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 💲 Pricing & Viability")
            st.markdown("""
            Decisions about pricing, margins, and feasibility.

            Typical questions:
            - At what volume does this work?
            - How sensitive is profit to price or cost changes?
            - What breaks first?
            """)
            st.caption("Tools: Break-even, pricing pressure, cost sensitivity")

        with st.container(border=True):
            st.markdown("### 👥 Customer Economics")
            st.markdown("""
            Decisions about customer value and demand structure.

            Typical questions:
            - Is this customer base worth growing?
            - How fragile is CLV?
            - What happens under substitution or complementarity?
            """)
            st.caption("Tools: CLV, substitution, complementary products")

    with col2:
        with st.container(border=True):
            st.markdown("### 💰 Cash & Financing")
            st.markdown("""
            Decisions about liquidity and funding.

            Typical questions:
            - Will this decision create cash stress?
            - How long can we finance operations internally?
            - What credit policy is sustainable?
            """)
            st.caption("Tools: cash cycle, credit policy, financing needs")

        with st.container(border=True):
            st.markdown("### ⚙️ Cost Structure & Operations")
            st.markdown("""
            Decisions about efficiency and operational scale.

            Typical questions:
            - How does unit cost evolve with volume?
            - Where do bottlenecks appear?
            - What is the operational break point?
            """)
            st.caption("Tools: unit cost, EOQ, turnover, working capital")

    st.divider()

    st.markdown("""
    ### How to use the Lab

    Use the sidebar to open a specific tool once you know
    **which decision frame you are operating in**.

    Focus on **tolerance**, not forecasts.  
    Small changes compound structurally.
    """)

    st.info("If this is your first visit, start with **Getting Started** to understand the decision logic.")

    st.markdown(
        """
        <br>
        **Contact**  
        For feedback, questions, or collaboration:  
        ✉️ <a href="mailto:brokeconomist@gmail.com">brokeconomist@gmail.com</a>
        """,
        unsafe_allow_html=True
    )

