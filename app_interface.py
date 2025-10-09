import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard Foot", layout="wide")

st.markdown(
    """
    <h1 style="text-align:center; color:#1E3D55;">Tableau de bord des statistiques footballistiques</h1>
    <p style="text-align:center; color:gray;">Analyse interactive des performances des joueurs</p>
    <hr style="border:1px solid #ddd;">
    """,
    unsafe_allow_html=True
)

df = pd.read_csv('data/foot-cleans.csv')
df = df[df['MP'] > 0]

df['Gls_per_MP'] = df['Gls'] / df['MP']
df['Ast_per_MP'] = df['Ast'] / df['MP']
df['Min_per_MP'] = df['Min'] / df['MP']

st.sidebar.header("Filtres")
positions = df['Pos'].unique()
selected_pos = st.sidebar.multiselect("Positions", positions, default=positions)

players = df['Player'].unique()
selected_players = st.sidebar.multiselect("Joueurs", players, default=players[:10])
filtered_df = df[(df['Pos'].isin(selected_pos)) & (df['Player'].isin(selected_players))]

sort_by = st.sidebar.selectbox("Trier par", ['Gls_per_MP', 'Ast_per_MP', 'Min_per_MP'])
ascending = st.sidebar.checkbox("Tri ascendant", value=False)
filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

col1, col2, col3 = st.columns(3)
col1.metric("Moy. Buts/Match", f"{filtered_df['Gls_per_MP'].mean():.2f}")
col2.metric("Moy. Assists/Match", f"{filtered_df['Ast_per_MP'].mean():.2f}")
col3.metric("Moy. Minutes/Match", f"{filtered_df['Min_per_MP'].mean():.0f}")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Performances", "Comparaisons", "Répartition", "Détails"])

with tab1:
    colA, colB = st.columns(2)

    with colA:
        fig1 = px.bar(filtered_df, x='Player', y='Gls_per_MP', color='Pos',
                      title="Buts par match", labels={'Gls_per_MP': 'Buts/Match'})
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = px.bar(filtered_df, x='Player', y='Ast_per_MP', color='Pos',
                      title="Passes décisives par match", labels={'Ast_per_MP': 'Assists/Match'})
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    colC, colD = st.columns(2)

    with colC:
        fig3 = px.scatter(filtered_df, x='Gls', y='Ast', size='MP', color='Pos',
                          hover_name='Player', title="Corrélation Buts vs Assists")
        st.plotly_chart(fig3, use_container_width=True)

    with colD:
        fig4 = px.scatter(filtered_df, x='Min_per_MP', y='Gls_per_MP', color='Pos',
                          title="Minutes jouées vs Buts par match")
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.markdown("Répartition des postes et classements")

    colE, colF = st.columns(2)

    with colE:
        pos_counts = filtered_df['Pos'].value_counts().reset_index()
        pos_counts.columns = ['Position', 'Nombre de joueurs']
        fig5 = px.pie(pos_counts, names='Position', values='Nombre de joueurs',
                      title="Répartition des postes")
        st.plotly_chart(fig5, use_container_width=True)

    with colF:
        top_scorers = df.sort_values(by='Gls', ascending=False).head(10)
        fig6 = px.bar(top_scorers, x='Player', y='Gls', color='Pos',
                      title="Top 10 buteurs", labels={'Gls': 'Buts'})
        st.plotly_chart(fig6, use_container_width=True)

with tab4:
    st.markdown("Détails des statistiques sélectionnées")
    st.dataframe(
        filtered_df[['Player', 'Pos', 'MP', 'Gls', 'Ast', 'Min', 'Gls_per_MP', 'Ast_per_MP', 'Min_per_MP']],
        use_container_width=True
    )
