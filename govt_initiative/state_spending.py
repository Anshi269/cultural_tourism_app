import streamlit as st
import plotly.express as px

def show(df):
    latest_year = df['Year'].max()
    state_df = df[df['Year'] == latest_year].groupby('State')['State Budget'].sum().reset_index()
    state_df = state_df.sort_values(by="State Budget", ascending=False)

    fig = px.bar(
        state_df,
        x="State",
        y="State Budget",
        title=f"Top Spending States in {latest_year}",
        labels={"State Budget": "Budget (Cr)"},
        color="State Budget"
    )
    st.plotly_chart(fig, use_container_width=True)