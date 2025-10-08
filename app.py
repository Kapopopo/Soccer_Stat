import streamlit as st # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

df = pd.read_csv('cleanplayer.csv')

df = df.drop_duplicates()

df = df.dropna(subset=['Player', 'Pos', 'Nation'])

df["Gls_90"] = df["Gls"] / df["90s"]
df["Ast_90"] = df["Ast"] / df["90s"]


st.title("Analyse des 5 grands championnats (2023/2024)")


st.header("Graphique 1 : Top 10 des Nations")

top_nations = df['Nation'].value_counts().head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_nations.index, y=top_nations.values, ax=ax1, palette="Spectral")
ax1.set_xlabel("Nation")
ax1.set_ylabel("Nombre de joueurs")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.markdown("---")


st.header("Graphique 2 : Joueurs les plus performants")

col1, col2 = st.columns(2)

with col1:
    postes_selectionnes = st.multiselect(
        "1. Choisir les postes",
        options=df["Pos"].unique(),
        default=['FW', 'MF']
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

fig2, ax2 = plt.subplots(figsize=(10, 6))

taille_points = (df_filtre["Min"] / df["Min"].max() * 500) + 20

points = ax2.scatter(
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
st.pyplot(fig2)

st.subheader("Top 5 joueurs les plus performants selon les filtres")
if not df_filtre.empty:
    df_filtre["Total_Efficacite_90"] = df_filtre["Gls_90"] + df_filtre["Ast_90"]
    top5 = df_filtre.sort_values("Total_Efficacite_90", ascending=False).head(5)

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

st.markdown("---")


st.header("Graphique 3 : Comparaison des ligues")
st.caption("On regarde quelles ligues ont les meilleurs taux offensifs moyens (buts et PD / 90 min).")

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

fig3, ax3 = plt.subplots(figsize=(10, 6))
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
st.pyplot(fig3)
