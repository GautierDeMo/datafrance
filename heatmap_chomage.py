import folium
import pandas as pd 

# On récupère nos tableeaux
df_chomage = pd.read_csv("dataset\\chomage.csv")
df_villes = pd.read_csv("dataset\\infos.csv")


# On enleve les villes ayant "nc" comme latitude et longitude
df_villes = df_villes[df_villes.Latitude != "nc"]
df_villes = df_villes[df_villes.Longitude != "nc"]
villes = df_villes.ville.unique()

def color_rate(taux):
    if taux <7.8:
        return "#FBD976"
    elif 7.8 <= taux < 8.3:
        return "#FEB24C"
    elif 8.3 <= taux < 8.8:
        return "#FC8C3C"
    elif 8.8 <= taux < 9.2:
        return "#F84F38"
    elif 9.2 <= taux < 9.6:
        return "#E43932"
    elif 9.6 <= taux < 10.5:
        return "#BE2E28"
    elif taux >= 10.5:
        return "#801F27"
    

#for annee in range(2004,2017):

for annee in range(2004,2017):
    map = folium.Map(location= [46.1076707,3.6705597], zoom_start=6.2)
    fgv = folium.FeatureGroup(name= "Taux de chomage")
    for ville in villes:
        try:
            print(ville)
            latitude = df_villes[df_villes["ville"] == ville]["Latitude"].iloc[0]
            longitude = df_villes[df_villes["ville"] == ville]["Longitude"].iloc[0]

            taux = df_chomage[df_chomage["ville"] ==ville][str(annee)].iloc[0]
            fgv.add_child(folium.CircleMarker(location= [latitude, longitude], radius=1, fill_color= color_rate(taux), color= color_rate(taux), fill_opacity= 0.7))
        except:
            continue

        map.add_child(fgv)

    legend_html = """
        <div style="position: fixed;
                    bottom:50px; left: 50px; width: 15%; height: 300px;
                    border:2px solid grey; z-index:9999; font-size:12px;
                    padding: 20px;
                    ">&nbsp; Taux de chomage en France <br> <br>
                    <i class="fa fa-square fa-2x"
                                style="color: #FBD976"></i>&nbsp; Moins de 7.8 % &nbsp; <br>
                    <i class="fa fa-square fa-2x"
                                style="color: #FEB24C"></i>&nbsp; entre 7.8 et 8.3 % &nbsp; <br>
                    <i class="fa fa-square fa-2x"
                                style="color: #FC8C3C"></i>&nbsp; entre 8.3 et 8.8 % &nbsp; <br>
                    <i class="fa fa-square fa-2x"
                                style="color: #F84F38"></i>&nbsp; entre 8.8 et 9.2 % &nbsp; <br>
                    <i class="fa fa-square fa-2x"
                                style="color: #E43932"></i>&nbsp; entre 9.2 et 9.6 % &nbsp; <br>
                    <i class="fa fa-square fa-2x"
                                style="color: #BE2E28"></i>&nbsp; entre 9.6 et 10.5 % &nbsp; <br>
                    <i class="fa fa-square fa-2x"
                                style="color: #801F27"></i>&nbsp; plus de 10.5 % &nbsp; <br>
                """
map.get_root().html.add_child(folium.Element(legend_html))
map.save("maps\\france_chomage_" + str(annee) +".html")