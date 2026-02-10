import pandas as pd 
import csv

df_chomage = pd.read_csv('dataset\\chomage.csv')

departements = ['0'+ str(i) if len(str(i)) == 1 else str(i) for i in range(1,96)]

villes = df_chomage.ville

colonnes = ['departement','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']
tableau_chomage_moyenne = pd.DataFrame(columns = colonnes)
tableau_chomage_moyenne.to_csv('dataset\\moyenne_chomage.csv', index=False)

with open('dataset\\moyenne_chomage.csv', 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= colonnes, lineterminator = '\n')
    for dpt in departements: # 01 -> 02
        dico = {e: '' for e in colonnes}
        dico['departement'] = dpt
        for annee in range(2004,2017):
            dico[str(annee)] = df_chomage[df_chomage.ville.str.contains(dpt)][str(annee)].mean()

        writer.writerow(dico)
        print(dpt)