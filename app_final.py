import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

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
df = df[df['MP'] > 0].drop_duplicates()
df = df.dropna(subset=['Player', 'Pos', 'Nation'])

df['Gls_per_MP'] = df['Gls'] / df['MP']
df['Ast_per_MP'] = df['Ast'] / df['MP']
df['Min_per_MP'] = df['Min'] / df['MP']

if '90s' not in df.columns:
    df['90s'] = df['MP']
df["Gls_90"] = df["Gls"] / df["90s"]
df["Ast_90"] = df["Ast"] / df["90s"]

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


tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "Performances", "Comparaisons", "Répartition", "Détails",
    "Nations & Performance", "Ligues",
    "Exploration", "Visualisations", "Comparaisons Joueurs", "Matrice"
])

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
    st.title("Répartition des postes et classements")
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
    st.subheader("Détails des statistiques sélectionnées")
    st.dataframe(
        filtered_df[['Player', 'Pos', 'MP', 'Gls', 'Ast', 'Min', 'Gls_per_MP', 'Ast_per_MP', 'Min_per_MP']],
        use_container_width=True
    )

with tab5:
    st.subheader("Top 10 des Nations")
    top_nations = df['Nation'].value_counts().head(10)
    fig7, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_nations.index, y=top_nations.values, ax=ax1, palette="Spectral")
    ax1.set_xlabel("Nation")
    ax1.set_ylabel("Nombre de joueurs")
    plt.xticks(rotation=45)
    st.pyplot(fig7)

    st.subheader("Joueurs les plus performants")

    col1, col2 = st.columns(2)
    with col1:
        postes_selectionnes = st.multiselect(
            "1. Choisir les postes", options=df["Pos"].unique(), default=['FW', 'MF']
        )
    with col2:
        min_minutes = st.slider(
            "2. Filtrer par minutes jouées",
            min_value=0,
            max_value=int(df["Min"].max()),
            value=(500, int(df["Min"].max())),
            step=1
        )

    df_filtre = df[df["Pos"].isin(postes_selectionnes)]
    df_filtre = df_filtre[df_filtre["Min"].between(min_minutes[0], min_minutes[1])]

    st.subheader("Buts/90 min (X) vs Passes décisives/90 min (Y)")
    fig8, ax2 = plt.subplots(figsize=(10, 6))
    taille_points = (df_filtre["Min"] / df["Min"].max() * 500) + 20
    ax2.scatter(
        df_filtre["Gls_90"],
        df_filtre["Ast_90"],
        s=taille_points,
        c=pd.factorize(df_filtre["Pos"])[0],
        cmap="viridis",
        alpha=0.7
    )
    ax2.set_xlabel("Buts par 90 min")
    ax2.set_ylabel("Passes décisives par 90 min")
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig8)

    if not df_filtre.empty:
        df_filtre["Total_Efficacite_90"] = df_filtre["Gls_90"] + df_filtre["Ast_90"]
        top5 = df_filtre.sort_values("Total_Efficacite_90", ascending=False).head(5)
        st.subheader("Top 5 joueurs les plus performants")
        st.dataframe(
            top5[["Player", "Pos", "Squad", "Gls_90", "Ast_90", "90s"]].rename(columns={
                "Player": "Joueur",
                "Squad": "Équipe",
                "Gls_90": "Buts/90",
                "Ast_90": "PD/90",
                "90s": "Matchs Joués"
            }).reset_index(drop=True),
            use_container_width=True
        )

with tab6:
    st.subheader("Comparaison des Ligues")
    st.caption("Analyse des taux offensifs moyens (buts et passes décisives par 90 min).")

    df_reguliers = df[df["90s"] >= 10]
    ligue_stats = df_reguliers.groupby("Comp").agg(
        Moy_Buts=("Gls_90", "mean"),
        Moy_PD=("Ast_90", "mean")
    ).reset_index().rename(columns={"Comp": "Ligue"})

    ligue_long = ligue_stats.melt(
        id_vars="Ligue",
        var_name="Statistique",
        value_name="Moyenne_par_90"
    )

    fig9, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=ligue_long,
        y="Ligue",
        x="Moyenne_par_90",
        hue="Statistique",
        ax=ax3,
        palette="flare",
        errorbar=None
    )
    ax3.set_xlabel("Taux moyen par 90 minutes")
    ax3.set_ylabel("")
    st.pyplot(fig9)

with tab7:
    st.header("Exploration générale des joueurs")
    sub = df.sample(n=min(15, len(df)), random_state=1)

    st.subheader("Aperçu aléatoire des données")
    st.dataframe(sub, use_container_width=True)

    fig_hist, ax = plt.subplots(figsize=(8, 5))
    ax.hist(sub["MP"], bins=10, color="skyblue", edgecolor="black")
    ax.set_title("Histogramme des matches joués")
    ax.set_xlabel("Matches joués (MP)")
    ax.set_ylabel("Nombre de joueurs")
    st.pyplot(fig_hist)
    plt.close(fig_hist)

    st.subheader("Visualisation 3D des joueurs")
    fig3d = px.scatter_3d(
        sub, x="Pos", y="MP", z="Gls", color="Nation", size="MP", hover_data=["Player"]
    )
    st.plotly_chart(fig3d, use_container_width=True)

with tab8:
    st.header("Visualisations avancées")

    st.subheader("Distribution des passes décisives par position")
    st.plotly_chart(px.violin(df, x="Pos", y="G+A", color="Pos"), use_container_width=True)

    st.subheader("Répartition des buts par position")
    st.plotly_chart(px.box(df, x="Pos", y="Gls", color="Pos"), use_container_width=True)

    st.subheader("Buts par joueur")
    st.plotly_chart(px.bar(df.head(30), x="Player", y="Gls", color="Pos"), use_container_width=True)

    st.subheader("Passes décisives par joueur")
    st.plotly_chart(px.line(df.head(30), x="Player", y="G+A", color="Pos"), use_container_width=True)

    st.subheader("Répartition des buts par position")
    st.plotly_chart(px.pie(df, names="Pos", values="Gls"), use_container_width=True)


with tab9:
    st.header("Comparaison des joueurs sélectionnés")
    comp_players = st.multiselect("Choisis les joueurs à comparer", df["Player"].unique())

    if comp_players:
        comp = df[df["Player"].isin(comp_players)]
        st.dataframe(comp, use_container_width=True)

        st.plotly_chart(
            px.bar(comp, x="Player", y=["Gls", "Ast"], barmode="group", title="Comparaison Buts et Passes"),
            use_container_width=True,
        )

        st.plotly_chart(
            px.bar(comp, x="Player", y="G+A", color="Pos", title="Comparaison des G+A"),
            use_container_width=True,
        )

        st.plotly_chart(
            px.scatter(
                comp, x="MP", y="G+A", color="Pos", size="Gls",
                hover_data=["Player"], title="Performance globale"
            ),
            use_container_width=True,
        )
    else:
        st.info("Sélectionne un ou plusieurs joueurs pour afficher la comparaison.")

with tab10:
    st.header("Matrice de dispersion des statistiques")
    st.plotly_chart(
        px.scatter_matrix(df, dimensions=["MP", "Gls", "Ast", "G+A"], color="Pos"),
        use_container_width=True
    )