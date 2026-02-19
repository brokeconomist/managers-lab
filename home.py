st.title("🧪 Managers’ Lab")

st.markdown("""
A structured decision laboratory for managers.

This is not a dashboard.  
This is not a reporting tool.  
This is not a forecasting engine.

Managers’ Lab follows a fixed decision path.

Every important business decision —
pricing, cost changes, credit policy, investment —
first affects survival,
then structure,
then sustainability,
and only after that, strategy.

This Lab makes you examine them in that order.
""")

st.divider()

st.markdown("""
### The Decision Path

You will move through five stages.

There are no shortcuts.
There is no skipping ahead.

The sequence is intentional.
""")

st.markdown("""
**1. Survival Anchor**  
Can the business survive small structural shifts?

**2. Structural Pressure**  
Where does cash or margin break first?

**3. Unit Economics**  
What must remain true at the operational level?

**4. Sustainability**  
Is value creation durable or fragile?

**5. Strategic Choice**  
Only after constraints are visible, comparison begins.
""")

st.divider()

st.markdown("""
You are not here to find the “right answer.”

You are here to understand:

- What must be true for this decision to work.
- How much error the system tolerates.
- Which assumption fails first.

If the numbers feel uncomfortable, the Lab is working.
""")

st.divider()

if st.button("Start Structured Decision Path"):
    st.session_state.flow_step = 1

st.caption("Advanced users may access individual tools from the sidebar.")
