import folium
import pandas as pd 

# On recupere les tableaux necessaires
df = pd.read_csv('dataset\\elections.csv')
df_candidats = pd.read_csv('dataset\\candidats_2019.csv')
df_infos = pd.read_csv('dataset\\infos.csv')

# On enleve les villes ayant 'nc' comme latitude et longitude
df_infos = df_infos[df_infos.Latitude != 'nc']
df_infos = df_infos[df_infos.Longitude != 'nc']

candidats = df_candidats.candidat
df["Gagnant"] = df[candidats].idxmax(axis=1)

villes = df_infos.ville.unique()

# FOnction qui fixe la couleur en fonction du candidat
def color_rate(candidat):
    if candidat == "Nathalie LOISEAU":
        return '#EFC29D'
    elif candidat == "Jordan BARDELLA":
        return "#1C435C"
    elif candidat == "François-Xavier BELLAMY":
        return "#9AD2F6"
    elif candidat == "Yannick JADOT":
        return "#91BAFB"
    elif candidat == "Benoît HAMON":
        return "#560836"
    elif candidat == "Manon AUBRY": 
        return "#EF9E9E"
    elif candidat == "Raphaël GLUCKSMANN":
        return "#E97DBD"
    elif candidat == "Nicolas DUPONT-AIGNAN":
        return "#69A0FA"

map = folium.Map(location= [46.1076707,3.6705597], zoom_start=6.2, tiles='CartoDB dark_matter')
fgv = folium.FeatureGroup(name= "Resultats des elections 2019")

for ville in villes:
    try:
        latitude = df_infos[df_infos['ville'] == ville]['Latitude'].iloc[0]
        longitude = df_infos[df_infos['ville'] == ville]['Longitude'].iloc[0]
        gagnant = df[df['ville'] == ville]['Gagnant'].iloc[0]
        fgv.add_child(folium.CircleMarker(location= [latitude, longitude],
                                            radius= 1,
                                            fill_color= color_rate(gagnant),
                                            color= color_rate(gagnant),
                                            fill_opacity= 0.7))
        map.add_child(fgv)
        print(ville)
    except:
        continue

map.save('maps\\france_elections_2019.html')