lien = "https://www.journaldunet.com/management/ville/alboussiere/ville-07007"

ville = lien.split('/')[5]
departement = lien.split('/')[-1][-5:-3]
code_insee = lien.split('/')[-1][-5:]

print(ville)
print(departement)
print(code_insee)