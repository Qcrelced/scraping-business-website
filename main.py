from modules import nav_google


def main():
    print("Choisissez votre choix")
    print("1 : Scrape la liste d'urls")
    print("2 : Scrape une ville")
    choice = str(input("choice : "))
    while choice != "1" and choice != "2":
        choice = str(input("choice : "))
    match choice:
        case "1":
            villes = [
                 "Perpignan", "Canet-en-Roussillon", "Saint-Estève", "Saint-Cyprien", "Argelès-sur-Mer",
                "Cabestany", "Pia", "Saint-Laurent-de-la-Salanque", "Elne", "Rivesaltes", "Thuir",
                "Le Soler", "Céret", "Bompas", "Toulouges", "Canohès", "Prades", "Le Barcarès",
                "Saleilles", "Ille-sur-Têt", "Pollestres", "Le Boulou", "Sainte-Marie-la-Mer",
                "Banyuls-sur-Mer", "Claira", "Bages", "Millas", "Villeneuve-de-la-Raho", "Port-Vendres",
                "Pézilla-la-Rivière", "Torreilles", "Alénya", "Salses-le-Château", "Amélie-les-Bains-Palalda",
                "Espira-de-l'Agly", "Saint-André", "Sorède", "Villelongue-de-la-Salanque", "Latour-Bas-Elne",
                "Saint-Hippolyte", "Palau-del-Vidre", "Saint-Féliu-d'Avall", "Saint-Génis-des-Fontaines",
                "Ponteilla", "Saint-Nazaire", "Arles-sur-Tech", "Baixas", "Maureillas-las-Illas",
                "Corneilla-del-Vercol", "Saint-Laurent-de-Cerdans", "Montesquieu-des-Albères",
                "Villelongue-dels-Monts", "Vernet-les-Bains", "Collioure", "Laroque-des-Albères", "Vinça",
                "Tresserre", "Llupia", "Saint-Paul-de-Fenouillet", "Corbère", "Brouilla", "Trouillas",
                "Prats-de-Mollo-la-Preste", "Banyuls-dels-Aspres", "Saint-Féliu-d'Amont", "Reynès", "Le Tech",
                "Oms", "Fourques", "Calmeilles", "Montauriol", "Les Cluses", "Saint-Jean-Pla-de-Corts",
                "Saint-Jean-Lasseille", "Villemolaque", "Passa", "Vivès", "Terrats", "Caixas", "Tordères",
                "Llauro", "Montbolo", "Serralongue", "Saint-Marsal", "Saint-Michel-de-Llotes", "Corsavy",
                "Olette", "Souanyas", "Nyer", "Jujols", "Canaveilles", "Thuès-Entre-Valls", "Ayguatébia-Talau",
                "Oreilla", "Escaro", "Sahorre", "Fuilla", "Py", "Casteil", "Villefranche-de-Conflent",
                "Corneilla-de-Conflent", "Serdinya", "Joch", "Eus", "Molitg-les-Bains", "Mosset", "Campôme",
                "Catllar", "Taurinya", "Clara", "Ria-Sirach", "Los Masos", "Fillols", "Roda de Ter", "Marquixanes",
                "Rabouillet", "Saint-Arnac", "Fenouillet", "Gincla", "Sournia", "Le Vivier", "Pézilla-de-Conflent",
                "Trilla", "Ansignan", "Caudiès-de-Fenouillèdes", "Fosse", "Maury", "Saint-Paul-de-Fenouillet",
                "Saint-Martin", "Lesquerde", "Lansac", "Caramany", "Rasiguères", "Latour-de-France", "Planèzes",
                "Tautavel", "Vingrau", "Cases-de-Pène", "Opoul-Périllos", "Estagel", "Montner", "Bélesta",
                "Cassagnes", "Calce", "Villeneuve-la-Rivière", "Pezilla-la-Rivière", "Baho", "Saint-Estève",
                "Toulouges", "Ponteilla", "Llupia", "Pollestres", "Bages", "Villemolaque", "Saint-Féliu-d'Avall",
                "Saleilles"
            ]
            for ville in villes:
                nav_google.search(ville)
        case "2":
            nav_google.search(str(input("Votre ville à scraper : ")))


main()
