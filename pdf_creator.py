from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image as PlatypusImage, PageBreak


def dates_bon_str(dates):
    mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
    return f"Du {dates[0][0]} {mois[dates[0][1]-1]} {dates[0][2]} au {dates[1][0]} {mois[dates[1][1]-1]} {dates[1][2]}"

def creer_recapitulatif(choix_ville,photo_ville, dates, path_carte, activites):
    prix_total=dates[2]
    c = canvas.Canvas(f"{choix_ville}_recapitulatif.pdf", pagesize=letter)
    # Page 1: Titre et image de fond
    c.drawInlineImage(photo_ville, 0, 0, width=letter[0], height=letter[1])
    c.setFont("Helvetica-Bold", 30)
    PlatypusImage("for_construction/fond_blanc.JPG", width=800, height=280).drawOn(c, 0, 700)
    c.drawString(22, 750, f"Visite de {choix_ville}")
    c.drawString(22, 710, dates_bon_str(dates))

    #Page des activités
    for jour, activite in activites.items():
        if len(activite)==3:
            c.showPage()
            c.drawInlineImage("for_construction/arriere_plan_2.jpg", 0, 0, width=letter[0], height=letter[1])
            c.setFont("Helvetica-Bold", 30)
            nom_act=activite[0]
            path_img=activite[1]
            prix = activite[2]
            prix_total+=prix

            c.drawString(22, 620, f"{jour} ({str(prix)}€)")
            c.drawString(22, 580, nom_act)
            PlatypusImage(path_img, width=500, height=300).drawOn(c, 52, 210)
            print(nom_act,path_img,prix)

        elif len(activite)==6:
            c.showPage()
            c.drawInlineImage("for_construction/arriere_plan_2.jpg", 0, 0, width=letter[0], height=letter[1])
            c.setFont("Helvetica-Bold", 18)
            nom_act_matin = activite[0]
            path_img_matin = activite[1]
            prix_matin = activite[2]
            nom_act_aprem = activite[3]
            path_img_aprem = activite[4]
            prix_aprem = activite[5]
            prix_total+=prix_matin+prix_aprem

            c.drawString(50, 680, f"{jour} matin ({str(prix_matin)}€)")
            c.setFont("Helvetica-Bold", 18)
            c.drawString(50, 660, nom_act_matin)
            PlatypusImage(path_img_matin, width=440, height=270).drawOn(c, 50, 380)
            PlatypusImage(path_img_aprem, width=440, height=270).drawOn(c, 52, 30)
            c.drawString(50, 340, f"{jour} aprem ({str(prix_aprem)}€)")
            c.drawString(50, 320, nom_act_aprem)


    #Dernière page: Carte
    c.showPage()
    c.drawInlineImage("for_construction/arriere_plan_2.jpg", 0, 0, width=letter[0], height=letter[1])
    img = PlatypusImage(path_carte, width=500, height=270).drawOn(c, 52, 380)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(52, 680, "Récapitulatif")
    c.drawString(52, 660, "Carte du trajet:")
    c.drawString(52, 340, f"Prix total: {str(prix_total)}€")
    

    c.save()

# Exemple d'utilisation
choix_ville="Paris"
photo_ville="for_construction/img_villes/img_paris.jpeg"
dates=[(10,2,2024),(15,2,2024),400]#le troisieme représente le prix des vols
path_carte="for_construction/img_carte_test.jpg"
activites={"Jour 1":["Bateau Mouche sur la Seine","for_construction/img_act/croisiere_bateau_mouche_paris.jpg",40,
                    "Visite Tour Eiffel guidée","for_construction/img_act/visite_tour_eiffel.jpg",40],
           "Jour 2":["Traverse champs elysées","for_construction/img_act/champs_elysee.jpeg",0],
 }

creer_recapitulatif(choix_ville,photo_ville, dates, path_carte, activites)

