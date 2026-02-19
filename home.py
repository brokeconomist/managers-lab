st.title("🧪 Managers’ Lab")

st.markdown("""
Every business decision changes structure.

Before choosing strategy,
you must understand limits.

This Lab follows one fixed path.

Survival → Pressure → Economics → Sustainability → Strategy
""")

st.divider()

if st.button("Begin Step 1 — Survival"):
    st.session_state.flow_step = 1

st.caption("The sequence cannot be skipped.")
