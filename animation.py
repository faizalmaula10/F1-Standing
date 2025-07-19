import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ─── Streamlit Page Setup ─────────────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="F1 Driver Standings Animation")

# ─── Load & Prepare Data ──────────────────────────────────────────────────────
df = pd.read_excel("data_f1_fix.xlsx", engine="openpyxl")

# Drivers to include
drivers = [
    'Max Verstappen', 'Lando Norris', 'Oscar Piastri',
    'Lewis Hamilton', 'George Russell', 'Carlos Sainz', 'Charles Leclerc'
]
df = df[df['Driver'].isin(drivers)]

# Truncate race names for display
df['Race'] = df['Race'].apply(lambda x: x if len(x) <= 10 else x[:10] + '…')

# Unique race order
races = list(df.sort_values('Round')['Race'].unique())
num_races = len(races)

# ─── Driver Styles & Images ───────────────────────────────────────────────────
driver_colors = {
    'Max Verstappen': '#213448',
    'Lando Norris':   '#EB5B00',
    'Oscar Piastri':  '#EB5B00',
    'Lewis Hamilton': '#819A91',
    'George Russell': '#819A91',
    'Carlos Sainz':   '#DC3C22',
    'Charles Leclerc':'#DC3C22'
}

driver_images = {
    'Max Verstappen': 'https://a.espncdn.com/combiner/i?img=/i/headshots/rpm/players/full/4665.png',
    'Lando Norris':   'https://a.espncdn.com/combiner/i?img=/i/headshots/rpm/players/full/5579.png',
    'Oscar Piastri':  'https://a.espncdn.com/combiner/i?img=/i/headshots/rpm/players/full/5752.png',
    'Lewis Hamilton': 'https://a.espncdn.com/i/headshots/rpm/players/full/868.png',
    'George Russell': 'https://a.espncdn.com/combiner/i?img=/i/headshots/rpm/players/full/5503.png&w=350&h=254',
    'Carlos Sainz':   'https://a.espncdn.com/combiner/i?img=/i/headshots/rpm/players/full/4686.png',
    'Charles Leclerc':'https://a.espncdn.com/combiner/i?img=/i/headshots/rpm/players/full/5498.png'
}

# ─── Sidebar Controls ─────────────────────────────────────────────────────────
st.sidebar.title("🎮 Race Animation Control")
play = st.sidebar.button("▶️ Play Full Season")
selected_race_idx = st.sidebar.slider("Select Race Round", 1, num_races, 1, key="race_slider")

# ─── Driver Images Sidebar (Static) ───────────────────────────────────────────
st.sidebar.markdown("### Drivers")
for drv in drivers:
    st.sidebar.image(driver_images[drv], width=150, caption=drv)

# ─── Chart-Drawing Function ──────────────────────────────────────────────────
def draw_chart(upto_idx):
    current = races[:upto_idx]
    dff = df[df['Race'].isin(current)]
    
    # base line chart
    fig = px.line(
        dff,
        x="Race", y="Standing",
        color="Driver",
        line_group="Driver",
        markers=True,
        category_orders={"Race": races},
        color_discrete_map=driver_colors
    )
    fig.update_layout(
        width=1800, height=700,
        yaxis=dict(autorange='reversed', title="Standing (1 = Best)"),
        xaxis=dict(title="Race", tickangle=45),
        title="🏁 F1 Driver Standings Progression",
        margin=dict(l=60, r=300, t=80, b=80),
        font=dict(size=16),
        legend=dict(font=dict(size=14))
    )
    
    # annotate total points at final point of each driver
    if upto_idx > 0:
        last_race = current[-1]
        for drv in drivers:
            row = df[(df['Driver']==drv) & (df['Race']==last_race)]
            if not row.empty:
                y = row['Standing'].values[0]
                pts = row['TotalPoints'].values[0]
                fig.add_annotation(
                    x=last_race, y=y,
                    text=f"{int(pts)} pts",
                    showarrow=False,
                    font=dict(size=14, color='black'),
                    bgcolor='white',
                    bordercolor='black',
                    borderwidth=1,
                    borderpad=4,
                    xanchor='left', yanchor='middle'
                )

    return fig

# ─── Main Display ─────────────────────────────────────────────────────────────
placeholder = st.empty()

if play:
    for i in range(1, num_races+1):
        fig = draw_chart(i)
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.4)
else:
    fig = draw_chart(selected_race_idx)
    placeholder.plotly_chart(fig, use_container_width=True)
