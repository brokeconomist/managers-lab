import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ==========================================
# LOGIC
# ==========================================

def calculate_weighted_average(amounts, credit_days):
    """
    Weighted average credit days.
    Each category's days are weighted by the AMOUNT owed (not customer count).

    Formula: Σ(amount × days) / Σ(amount)
    """
    total_amount = sum(amounts)
    if total_amount == 0:
        return 0.0, 0.0

    weighted_sum = sum(a * d for a, d in zip(amounts, credit_days))
    weighted_avg = weighted_sum / total_amount

    return round(total_amount, 2), round(weighted_avg, 2)


def calculate_simple_average(credit_days):
    """Simple (unweighted) average — for comparison only."""
    active = [d for d in credit_days if d > 0]
    if not active:
        return 0.0
    return round(sum(active) / len(active), 2)


# ==========================================
# VISUALIZATION
# ==========================================

def plot_credit_days_chart(names, amounts, credit_days, weighted_avg, simple_avg, currency='€'):
    """
    Bar chart: each category's credit days as bars.
    Bar width scales with the amount owed — thicker = bigger debt.
    Two reference lines: weighted avg (correct) vs simple avg (wrong).
    """
    max_amt = max(amounts) if max(amounts) > 0 else 1
    widths = [max(0.15, (a / max_amt) * 0.7) for a in amounts]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=names,
        y=credit_days,
        width=widths,
        marker_color='#4A90D9',
        text=[f"{d} days\n{currency}{a:,.0f}" for d, a in zip(credit_days, amounts)],
        textposition='outside',
        hovertemplate='%{x}<br>Days: %{y}<br>Amount: ' + currency + '<extra></extra>'
    ))

    fig.add_hline(
        y=weighted_avg,
        line_dash="solid",
        line_color="#E67E22",
        line_width=3,
        annotation_text=f"Weighted Avg: {weighted_avg} days",
        annotation_position="top right",
        annotation_font_color="#E67E22",
        annotation_font_size=13
    )

    fig.add_hline(
        y=simple_avg,
        line_dash="dash",
        line_color="#999999",
        line_width=2,
        annotation_text=f"Simple Avg: {simple_avg} days",
        annotation_position="bottom right",
        annotation_font_color="#999999",
        annotation_font_size=11
    )

    fig.update_layout(
        title="Credit Days per Category",
        xaxis_title="",
        yaxis_title="Credit Days",
        height=380,
        showlegend=False,
        yaxis=dict(rangemode='tozero')
    )

    return fig


# ==========================================
# UI
# ==========================================

def show_credit_days_calculator():
    st.set_page_config(
        page_title="Credit Days Calculator | Managers' Lab",
        layout="wide"
    )

    st.title("📅 Weighted Average Credit Days")
    st.caption(
        "Calculate the **true average credit period** across your customer categories, "
        "weighted by the **amount each group owes** — not just the number of customers."
    )

    # --- Currency ---
    currency = st.selectbox("Currency", ["EUR (€)", "USD ($)", "GBP (£)"], index=0)
    cs = currency.split('(')[1].split(')')[0]

    # --- Number of categories ---
    num_categories = st.number_input(
        "How many customer categories?",
        min_value=1, max_value=10, value=4
    )

    st.markdown("---")

    # --- Input grid: 4 columns ---
    header = st.columns([1.8, 1.2, 1.8, 1.2])
    header[0].markdown("**Category**")
    header[1].markdown("**Customers**")
    header[2].markdown(f"**Amount Owed ({cs})**")
    header[3].markdown("**Credit Days**")

    names = []
    customers = []
    amounts = []
    credit_days = []

    for i in range(num_categories):
        cols = st.columns([1.8, 1.2, 1.8, 1.2])

        with cols[0]:
            name = st.text_input(
                "Name", label_visibility="hidden",
                key=f"name_{i}",
                value=f"Category {i+1}",
                placeholder="e.g. Retail"
            )
            names.append(name)

        with cols[1]:
            cust = st.number_input(
                "Customers", label_visibility="hidden",
                key=f"cust_{i}",
                min_value=0, step=1
            )
            customers.append(cust)

        with cols[2]:
            amt = st.number_input(
                "Amount", label_visibility="hidden",
                key=f"amt_{i}",
                min_value=0.0, step=1000.0
            )
            amounts.append(amt)

        with cols[3]:
            days = st.number_input(
                "Days", label_visibility="hidden",
                key=f"days_{i}",
                min_value=0, step=1
            )
            credit_days.append(days)

    # --- Calculate ---
    st.markdown("---")

    if st.button("📊 Calculate", type="primary", use_container_width=True):

        if sum(amounts) == 0:
            st.error("⚠️ Enter at least one amount!")
            return

        total_amount, weighted_avg = calculate_weighted_average(amounts, credit_days)
        simple_avg = calculate_simple_average(credit_days)
        total_customers = sum(customers)

        # --- Results ---
        st.markdown("---")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Weighted Avg Credit Days",
            f"{weighted_avg} days",
            help="The correct average — weighted by how much each group owes"
        )

        m2.metric(
            "Simple Avg (for comparison)",
            f"{simple_avg} days",
            delta=f"{simple_avg - weighted_avg:+.1f} vs weighted",
            delta_color="inverse",
            help="Unweighted average — ignores amounts. Usually wrong for planning."
        )

        m3.metric(
            "Total Receivables",
            f"{cs}{total_amount:,.0f}",
            help="Total amount owed across all categories"
        )

        m4.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

        # --- Why they differ ---
        if abs(simple_avg - weighted_avg) > 0.5:
            st.info(
                f"💡 **Why the difference?** The simple average ({simple_avg} days) treats every category equally. "
                f"But the categories with bigger amounts pull the true average toward {weighted_avg} days. "
                f"Use **{weighted_avg} days** for cash flow planning."
            )

        # --- Chart ---
        st.markdown("---")

        active = [
            (n, c, a, d)
            for n, c, a, d in zip(names, customers, amounts, credit_days)
            if a > 0
        ]

        if active:
            a_names, a_custs, a_amts, a_days = zip(*active)
            fig = plot_credit_days_chart(
                list(a_names), list(a_amts), list(a_days),
                weighted_avg, simple_avg, cs
            )
            st.plotly_chart(fig, use_container_width=True)

        # --- Detail table ---
        st.markdown("---")

        df = pd.DataFrame({
            'Category': names,
            'Customers': customers,
            'Amount Owed': amounts,
            'Credit Days': credit_days
        })
        df = df[df['Amount Owed'] > 0].copy()
        df['% of Total'] = (df['Amount Owed'] / total_amount * 100).round(1)
        df['Contribution'] = (df['Amount Owed'] * df['Credit Days']).round(0)

        # Format amount column for display
        df_display = df.copy()
        df_display['Amount Owed'] = df_display['Amount Owed'].apply(
            lambda x: f"{cs}{x:,.0f}"
        )
        df_display['Contribution'] = df_display['Contribution'].apply(
            lambda x: f"{cs}{x:,.0f}"
        )
        df_display['% of Total'] = df_display['% of Total'].apply(
            lambda x: f"{x}%"
        )

        st.dataframe(df_display, use_container_width=True, hide_index=True)

        # --- Export ---
        st.markdown("---")

        csv = df.to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv,
            file_name="credit_days_analysis.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    show_credit_days_calculator()
