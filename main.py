
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
        text: "Creer le compte"
        text_color: 1,1,1,1
        md_bg_color: 0.4392156862745098, 0.5058823529411764, 0.6
        pos_hint: {'center_x': .5, 'center_y': .25}
        on_release: app.signin_screen()

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

        
    '''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def signin_screen(self):
        last_id=clients[-1][2]
        nom_cree = self.root.ids.nom_cree.text
        prenom_cree = self.root.ids.prenom_cree.text
        mdp_cree = self.root.ids.mdp_cree.text
        mdp_confirm = self.root.ids.mdp_confirm.text
        if mdp_cree!=mdp_confirm:
            return Builder.load_string("""
                                       MDLabel:
                                        text: "Les mots de passe ne sont pas les memes"
                                        color: 0.4392156862745098, 0.5058823529411764, 0.6
                                        pos_hint: {'center_x': .5, 'center_y': .4}
                                        """)
        else:
            if nom_cree!=None and prenom_cree!=None and mdp_cree!=None:
                #a_ajoute=f"('{nom}', '{prenom}', '{str(int(last_id)+1)}','{mdp}')"
                #print(a_ajoute)
                c.execute(f"""INSERT INTO client
                VALUES ('{nom_cree}', '{prenom_cree}', '{str(int(last_id)+1)}','{mdp_cree}')""")
                connexion.commit()

if __name__ == "__main__":
    MainApp().run
    
    
