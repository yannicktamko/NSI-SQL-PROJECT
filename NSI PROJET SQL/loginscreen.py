
import sqlite3
import kivy
kivy.require('2.2.1')
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex
from kivymd.uix.pickers import MDDatePicker

connexion = sqlite3.connect('database.db')

# Récupération d'un curseur
c = connexion.cursor()

# Remplissage d'une table
# c.execute("""INSERT INTO client VALUES ("Foster", 'Max', 1,"mdp1"),("Tamko", 'Yannick', 2,'mdp2'),("Sempels", 'Maxime', 3,'mdp3');""")

clients = c.execute("SELECT * FROM client")
clients = clients.fetchall()

connexion.commit()


KV = '''
Screen:

     MDRectangleFlatButton:
        text: "Se connecter"
        text_color: 1,1,1,1
        md_bg_color: 0, 194, 0, 0.8
        pos_hint: {'center_x': .6, 'center_y': .40}
        on_release: app.login_screen()
                
    MDRaisedButton:
        text: "Suivant"
        pos_hint: {'center_x': .90, 'center_y': .25}
        on_release: app.vers_ecran("ecran2")

    MDRectangleFlatButton:
        text: "Creer un compte"
        text_color: 1,1,1,1
        md_bg_color: 0, 194, 0, 0.8
        pos_hint: {'center_x': .4, 'center_y': .40}
        on_release: app.vers_ecran("ecran3")

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

        
    '''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def login_screen(self):
        #demande le nom, prenom et mdp, si les 3 représente bien un client alors renvoi le tuple d'info du client actuel(pr l'instant, mais avec l'id client ducoup)
        #A FAIRE: création du user si il est pas dedans
        self.nom = self.root.ids.nom.text
        self.prenom = self.root.ids.prenom.text
        self.mdp = self.root.ids.mdp.text
        index = 0
        str_info=""
        bon_index=0
        for elem in clients:
            if elem[0].upper()==self.nom.upper() and elem[1].upper()==self.prenom.upper():# and elem[3].upper()==mdp.upper():
                str_info="Username existant "
                if elem[3].upper()==self.mdp.upper():
                    str_info+="et bon mdp"
                    bon_index=index
                else:
                    str_info+="mais mauvais mdp"
            else:
                if "existant" not in str_info:
                    str_info="username non existant"#A CREER
            index+=1
        print(str_info)
        if str_info=="Username existant et bon mdp":
            return clients[bon_index] 


MainApp().run