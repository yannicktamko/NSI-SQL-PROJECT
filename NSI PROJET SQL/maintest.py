import sqlite3
import kivy
import ast
kivy.require('2.2.1')
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
import pyautogui
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image as PlatypusImage, PageBreak



connexion = sqlite3.connect('database.db')
# Récupération d'un curseur
c = connexion.cursor()
# Remplissage d'une table
# c.execute("""INSERT INTO client VALUES ("Foster", 'Max', 1,"mdp1"),("Tamko", 'Yannick', 2,'mdp2'),("Sempels", 'Maxime', 3,'mdp3');""")
clients = c.execute("SELECT * FROM client")
clients = clients.fetchall()
connexion.commit()

################################----------------------------------------------------

KV = """

ScreenManager:
    id: sm
    Screen:
        name: "ecran1"
        MDRectangleFlatButton:
            text: "Se connecter"
            text_color: 1,1,1,1
            md_bg_color: 0.4392156862745098, 0.5058823529411764, 0.6
            pos_hint: {'center_x': .6, 'center_y': .40}
            on_release: app.login_screen()
                    

        MDRectangleFlatButton:
            text: "Creer un compte"
            text_color: 1,1,1,1
            md_bg_color: 0.4392156862745098, 0.5058823529411764, 0.6
            pos_hint: {'center_x': .4, 'center_y': .40}
            on_release: sm.current = "ecran3"

        MDTextField:
            id: prenom
            hint_text: "prenom"
            mode: "rectangle"
            pos_hint: {'center_x': .5, 'center_y': .7}
            size_hint: 0.60, 0.1

        MDTextField:
            id: mdp
            hint_text: "Mot de passe"
            mode: "rectangle"
            pos_hint: {'center_x': .5, 'center_y': .55}
            size_hint: 0.60, 0.1

        MDTextField:
            id: nom
            hint_text: "Nom"
            mode: "rectangle"
            pos_hint: {'center_x': .5, 'center_y': .85}
            size_hint: 0.60, 0.1
            
    Screen:
        name: "ecran2"
        MDFloatLayout:

            MDRaisedButton:
                text: "Selectionner votre date d'arrrivee"
                id: arrivee
                pos_hint: {'center_x': .25, 'center_y': .5}
                on_release: app.show_arrivee_picker()

            MDRaisedButton:
                text: "Selectionner votre date de depart"
                id: depart
                pos_hint: {'center_x': .75, 'center_y': .5}
                on_release: app.show_depart_picker()

            MDRaisedButton:
                id: transport
                text: "Choisissez votre moyen de transport"
                pos_hint: {"center_x": .25, "center_y": .7}
                on_release: app.transport.open()

            MDRaisedButton:
                text: "Précédant"
                pos_hint: {'center_x': .10, 'center_y': .25}
                on_release: sm.current = "ecran1"


            MDRaisedButton:
                text: "Telecharger le récapitulatif"
                pos_hint: {'center_x': .85, 'center_y': .25}
                on_release: app.creer_recapitulatif(self.root.ids.destination.text ,photo_ville, [self.root.ids.arrivee.text,self.root.ids.depart.text,50], path_carte, activites)

            MDLabel:
                id: welcome_label
                text: "Réservez votre voyage !"
                pos_hint: {'center_x': .90, 'center_y': .90}
                color: 0.4392156862745098, 0.5058823529411764, 0.6
            
            MDRaisedButton:
                id: destination
                text: "Choisissez votre destination"
                pos_hint: {"center_x": .75, "center_y": .7}
                on_release: app.menu.open()

            MDRaisedButton:
                id: logement
                text: "Choisissez votre logement"
                pos_hint: {"center_x": .75, "center_y": .6}
                on_release: app.logement.open()
            
            MDRaisedButton:
                id: activites
                text: "Choisissez le motif de ce voyage"
                pos_hint: {"center_x": .25, "center_y": .6}
                on_release: app.activites.open()
                

    Screen:
        name: "ecran3"
        MDRectangleFlatButton:
            text: "Creer le compte"
            text_color: 1,1,1,1
            md_bg_color: 0.4392156862745098, 0.5058823529411764, 0.6
            pos_hint: {'center_x': .5, 'center_y': .25}
            on_release: app.signin_screen()

        MDRectangleFlatButton:
            text: "Retournez vers l'ecran de connexion"
            text_color: 1,1,1,1
            md_bg_color: 0.4392156862745098, 0.5058823529411764, 0.6
            pos_hint: {'center_x': .20, 'center_y': .10}
            on_release: sm.current = "ecran1"
        

        MDTextField:
            id: prenom_cree
            hint_text: "prenom"
            mode: "rectangle"
            pos_hint: {'center_x': .5, 'center_y': .7}
            size_hint: 0.60, 0.1

        MDTextField:
            id: mdp_cree
            hint_text: "Mot de passe"
            mode: "rectangle"
            pos_hint: {'center_x': .5, 'center_y': .55}
            size_hint: 0.60, 0.1

        MDTextField:
            id: nom_cree
            hint_text: "Nom"
            mode: "rectangle"
            pos_hint: {'center_x': .5, 'center_y': .85}
            size_hint: 0.60, 0.1
        
        MDTextField:
            id: mdp_confirm
            hint_text: "Confirmez mot de passe"
            mode: "rectangle"
            pos_hint: {'center_x': .5, 'center_y': .4}
            size_hint: 0.60, 0.1


        
       

"""

################################----------------------------------------------------

class MonAppli(MDApp):

    title = "Mon appli"
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)
    
    def set_item(self, text__item):
            self.root.ids.destination.text = text__item
            self.menu.dismiss()
    
    def set_item1(self, text__item):
            self.root.ids.transport.text = text__item
            self.transport.dismiss()
    
    def set_item2(self, text__item):
            self.root.ids.logement.text = text__item
            self.transport.dismiss()
    
    def set_item3(self, text__item):
            self.root.ids.activites.text = text__item
            self.transport.dismiss()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.screen = Builder.load_string(KV)
        menu_items = [{ "viewclass": "OneLineListItem", "text": "Paris", "on_release": lambda x="Paris": self.set_item(x)}, { "viewclass": "OneLineListItem", "text": "Londres", "on_release": lambda x="Londres": self.set_item(x)},{ "viewclass": "OneLineListItem", "text": "Tokyo", "on_release": lambda x="Tokyo": self.set_item(x)},{ "viewclass": "OneLineListItem", "text": "Liverpool", "on_release": lambda x="Liverpool": self.set_item(x)},{ "viewclass": "OneLineListItem", "text": "Lloret del mar","on_release": lambda x="Lloret del Mar": self.set_item(x)},{ "viewclass": "OneLineListItem", "text": "Singapoure", "on_release": lambda x="Singapoure": self.set_item(x)},{ "viewclass": "OneLineListItem", "text": "Dubai", "on_release": lambda x="Dubai": self.set_item(x)},{ "viewclass": "OneLineListItem", "text": "Besançon", "on_release": lambda x="Besançon": self.set_item(x)},{ "viewclass": "OneLineListItem", "text": "Madagascar", "on_release": lambda x="Madagascar": self.set_item(x)} ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.destination, items=menu_items, width_mult=4
        )
        transport = [{ "viewclass": "OneLineListItem", "text": "Avion", "on_release": lambda x="Avion": self.set_item1(x)}, { "viewclass": "OneLineListItem", "text": "Train", "on_release": lambda x="Train": self.set_item1(x)},{ "viewclass": "OneLineListItem", "text": "Bus", "on_release": lambda x="Bus": self.set_item1(x)}]
        self.transport = MDDropdownMenu(
            caller=self.screen.ids.transport, items=transport, width_mult=4
        )
        logement = [{ "viewclass": "OneLineListItem", "text": "Camping Les Boubous", "on_release": lambda x="Camping les Boubous": self.set_item2(x)}, { "viewclass": "OneLineListItem", "text": "Motel Transilvanie", "on_release": lambda x="Motel Transilvanie": self.set_item2(x)},{ "viewclass": "OneLineListItem", "text": "Ibis Hotel", "on_release": lambda x="Ibis Hotel": self.set_item2(x)}, { "viewclass": "OneLineListItem", "text": "Grand Hotel", "on_release": lambda x="Grand Hotel": self.set_item2(x)}]
        self.logement = MDDropdownMenu(
            caller=self.screen.ids.logement, items=logement, width_mult=4
        )
        activites = [{ "viewclass": "OneLineListItem", "text": "Voyage d'affaires", "on_release": lambda x="Voyage d'affaires": self.set_item3(x)}, { "viewclass": "OneLineListItem", "text": "Escapade amoureuse", "on_release": lambda x="Escapade amoureuse": self.set_item3(x)},{ "viewclass": "OneLineListItem", "text": "Vacances en famille", "on_release": lambda x="Vacances en famille": self.set_item3(x)}, { "viewclass": "OneLineListItem", "text": "Fuir votre femme", "on_release": lambda x="Fuir votre femme": self.set_item3(x)}]
        self.activites = MDDropdownMenu(
            caller=self.screen.ids.activites, items=activites, width_mult=4
        )

    def login_screen(self):
        clients = c.execute("SELECT * FROM client").fetchall()
        connexion.commit()
        self.nom = self.root.ids.nom.text
        self.prenom = self.root.ids.prenom.text
        self.mdp = self.root.ids.mdp.text
        index = 0
        str_info = ""
        bon_index = 0

        for elem in clients:
            if elem[0].upper() == self.nom.upper() and elem[1].upper() == self.prenom.upper():
                str_info = "Username existant "
                if elem[3].upper() == self.mdp.upper():
                    str_info += "et bon mdp"
                    bon_index = index
                else:
                    str_info += "mais mauvais mdp"
            else:
                if "existant" not in str_info:
                    str_info = "username non existant"
            index += 1

        #pyautogui.alert(str_info)

        if str_info == "Username existant et bon mdp":
            #print(self.root.ids.sm.current_screen)
            self.root.current = "ecran2"
            return clients[bon_index]

    def signin_screen(self):
        last_id=clients[-1][2]
        nom_cree = self.root.ids.nom_cree.text
        prenom_cree = self.root.ids.prenom_cree.text
        mdp_cree = self.root.ids.mdp_cree.text
        mdp_confirm = self.root.ids.mdp_confirm.text
        if mdp_cree!=mdp_confirm:   
            """pyautogui.alert('Les mots de passes ne concordent pas')"""
        if nom_cree!=None and prenom_cree!=None and mdp_cree!=None and mdp_cree==mdp_confirm:
            c.execute(f"""INSERT INTO client
            VALUES ('{nom_cree}', '{prenom_cree}', '{str(int(last_id)+1)}','{mdp_cree}')""")
            connexion.commit()
            #pyautogui.alert('Le compte a bien été crée')
            self.root.current = "ecran1"
        
    def on_save_arrivee(self, instance, value, date_range):
       #nvalue=c.execute(f"""SELECT reservations.date
#FROM reservations
#JOIN client ON reservations.id_client = client.id_client
#  WHERE client.prenom = {self.root.ids.prenom.text} """)

        #self.root.ids.arrivee.text = self.reverse_date_formatter(nvalue)
        self.date_arrive=str(value)
        self.root.ids.arrivee.text = str(value)

    def on_save_depart(self, instance, value, date_range):
        #nvalue = c.execute("""SELECT reservations.date
        #FROM reservations
        #JOIN client ON reservations.id_client = client.id_client
        #WHERE client.prenom = 'Maxime'""")
        """nvalue = nvalue.fetchone()
        nvalue = nvalue[0]
        nvalue = ast.literal_eval(nvalue)[1]
        print(nvalue)
        #self.root.ids.depart.text = self.reverse_date_formatter(nvalue)"""
        self.date_depart=str(value)
        self.root.ids.depart.text = str(value)
    
    
    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_arrivee_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_arrivee, on_cancel=self.on_cancel)
        date_dialog.open()

    def show_depart_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_depart, on_cancel=self.on_cancel)
        date_dialog.open()

    def new_date_formater(self,old_format):
        """Passe d'une liste de la forme [“10-02-2024”,”10-02-2024”,50]
        à une liste de la forme [(10,2,2024),(18,2,24),50]
        """
        assert type(old_format) == list

        a = old_format[0].split("-")
        b = old_format[1].split("-")
        t = (int(a[0]), int(a[1]), int(a[2]))
        t2 = (int(b[0]), int(b[1]), int(b[2]))
        return [t, t2, old_format[2]]

    def reverse_date_formatter(self,date_tuple):
        """
        Passe d'un tuple de la forme (10, 2, 2025) à une chaîne de la forme "10-02-2025"
        """
        assert type(date_tuple) == tuple and len(date_tuple) == 3

        # Convertir le tuple en une chaîne au format "jour-mois-année"
        date_str = f"{date_tuple[0]:02d}-{date_tuple[1]:02d}-{date_tuple[2]:04d}"
        return date_str

    def dates_bon_str(self, dates):
        mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
        return f"Du {dates[0][0]} {mois[dates[0][1]-1]} {dates[0][2]} au {dates[1][0]} {mois[dates[1][1]-1]} {dates[1][2]}"
    
    def creer_recapitulatif(self, choix_ville,photo_ville, dates, path_carte, activites):
        prix_total=dates[2]
        c = canvas.Canvas(f"{choix_ville}_recapitulatif.pdf", pagesize=letter)
        # Page 1: Titre et image de fond
        c.drawInlineImage(photo_ville, 0, 0, width=letter[0], height=letter[1])
        c.setFont("Helvetica-Bold", 30)
        PlatypusImage("for_construction/fond_blanc.JPG", width=800, height=280).drawOn(c, 0, 700)
        c.drawString(22, 750, f"Visite de {choix_ville}")
        c.drawString(22, 710, self.dates_bon_str(dates))

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

    #choix_ville= self.root.ids.destination.text
    photo_ville="for_construction/img_villes/img_paris.jpeg"
    #dates= [self.root.ids.arrivee.text,self.root.ids.depart.text,50] #le troisieme représente le prix des vols
    path_carte="for_construction/img_carte_test.jpg"
    activites={"Jour 1":["Bateau Mouche sur la Seine","for_construction/img_act/croisiere_bateau_mouche_paris.jpg",40,
                            "Visite Tour Eiffel guidée","for_construction/img_act/visite_tour_eiffel.jpg",40],
                "Jour 2":["Traverse champs elysées","for_construction/img_act/champs_elysee.jpeg",0],
        }

################################----------------------------------------------------




if __name__ == '__main__':
    MonAppli().run()