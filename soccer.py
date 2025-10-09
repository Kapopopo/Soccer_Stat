import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title(" Statistiques des joueurs de football")
st.write("Application simple avec recherche et comparaisons visuelles")

#  Chargement des données 
data = pd.read_csv("top5-players.csv")

#  Sélection des joueurs pour comparaison 
players = st.multiselect("👥 Choisis les joueurs à comparer", data["Player"].unique())

# --- Sous-échantillon pour les graphiques globaux ---
sub = data.sample(n=min(15, len(data)), random_state=1)

# --- Tableau d'aperçu ---
st.subheader("Aperçu des données")
st.dataframe(sub)

# --- Histogramme des matches joués ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(sub["MP"], bins=10, color="skyblue", edgecolor="black")
ax.set_title("Histogramme des matches joués")
ax.set_xlabel("Matches joués (MP)")
ax.set_ylabel("Nombre de joueurs")
st.pyplot(fig)
plt.close(fig)

# --- Graphique 3D ---
st.subheader("Visualisation 3D des joueurs")
fig3d = px.scatter_3d(sub, x="Pos", y="MP", z="Gls", color="Nation", size="MP", hover_data=["Player"])
st.plotly_chart(fig3d, use_container_width=True)

# Graphique violon 
st.subheader("Distribution des passes décisives par position")
st.plotly_chart(px.violin(sub, x="Pos", y="G+A", color="Pos"), use_container_width=True)

#  Boîte à moustaches 
st.subheader(" Répartition des buts par position")
st.plotly_chart(px.box(sub, x="Pos", y="Gls", color="Pos"), use_container_width=True)

#  Barres : buts par joueur 
st.subheader("Buts par joueur")
st.plotly_chart(px.bar(sub, x="Player", y="Gls", color="Pos"), use_container_width=True)

#  Ligne : passes décisives 
st.subheader(" Passes décisives par joueur")
st.plotly_chart(px.line(sub, x="Player", y="G+A", color="Pos"), use_container_width=True)

# camembert : répartition des buts 
st.subheader("Répartition des buts par position")
st.plotly_chart(px.pie(sub, names="Pos", values="Gls"), use_container_width=True)

#  Matrice de dispersion
st.subheader("Matrice de dispersion des statistiques")
st.plotly_chart(px.scatter_matrix(sub, dimensions=["MP", "Gls", "Ast", "G+A"], color="Pos"), use_container_width=True)

#  COMPARAISON DES JOUEURS   
if players:
    st.subheader(" Comparaison des joueurs sélectionnés")
    comp = data[data["Player"].isin(players)]
    st.dataframe(comp)

    # Comparaison visuelle (buts + passes)
    st.plotly_chart(px.bar(comp, x="Player", y=["Gls", "Ast"], barmode="group", title="Comparaison des Buts et Passes"), use_container_width=True)

    # Comparaison G+A
    st.plotly_chart(px.bar(comp, x="Player", y="G+A", color="Pos", title="Comparaison des G+A"), use_container_width=True)

    # Comparaison multi-axes
    st.plotly_chart(px.scatter(comp, x="MP", y="G+A", color="Pos", size="Gls", hover_data=["Player"], title="Performance globale"), use_container_width=True)
else:
    st.info("Sélectionne un ou plusieurs joueurs pour afficher la comparaison.")
