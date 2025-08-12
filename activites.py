
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
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex


connexion = sqlite3.connect('database.db')

# Récupération d'un curseur
c = connexion.cursor()

# Remplissage d'une table
# c.execute("""INSERT INTO client VALUES ("Foster", 'Max', 1,"mdp1"),("Tamko", 'Yannick', 2,'mdp2'),("Sempels", 'Maxime', 3,'mdp3');""")

clients = c.execute("SELECT * FROM client")
clients = clients.fetchall()

connexion.commit()


KV = '''
ShowcaseScreen:
    name: 'ScreenManager'
    fullscreen: True

    BoxLayout:
        size_hint_y: None
        height: '48dp'

        Spinner:
            text: 'Default transition'
            values: ('SlideTransition', 'SwapTransition', 'FadeTransition', 'WipeTransition')
            on_text: sm.transition = Factory.get(self.text)()

    ScreenManager:
        id: sm

        <Screen1> :
            name: "ecran1"
            MDRectangleFlatButton:
                text: "Se connecter"
                text_color: 1,1,1,1
                md_bg_color: 0.4392156862745098, 0.5058823529411764, 0.6
                pos_hint: {'center_x': .6, 'center_y': .40}
                on_release: app.login_screen()
                        
            MDRaisedButton:
                text: "Suivant"
                pos_hint: {'center_x': .90, 'center_y': .25}
                on_release: sm.current = "ecran2"

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

        <Screen2> :
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
                    pos_hint: {"center_x": .5, "center_y": .7}
                    on_release: app.transport.open()

                MDRaisedButton:
                    text: "Précédant"
                    pos_hint: {'center_x': .10, 'center_y': .25}
                    on_release: app.vers_ecran("ecran1")


                MDRaisedButton:
                    text: "Suivant"
                    pos_hint: {'center_x': .90, 'center_y': .25}
                    on_release: app.vers_ecran("ecran3")

                MDLabel:
                    text: "Choisissez vos dates de voyage"
                    pos_hint: {'center_x': .85, 'center_y': .75}
                    color: 0.4392156862745098, 0.5058823529411764, 0.6
                
                MDRaisedButton:
                    id: destination
                    text: "Choisir votre destination"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.menu.open()

        <Screen3>
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
                on_release: app.vers_ecran("ecran1")
            

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


        
Screen: 
    ScreenManager:
        id: screen_manager
        Screen1:
        Screen2:
        Screen3:
        
    '''

################################----------------------------------------------------

class Screen1(Screen) :
    pass
class Screen2(Screen) :
    pass
class Screen3(Screen):
    pass

################################----------------------------------------------------


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
    
    def vers_ecran(self,ecran):
        self.root.ids.screen_manager.current = ecran
        if ecran=="ecran1":
            self.root.ids.screen_manager.transition.direction = "right"    
        else:
            self.root.ids.screen_manager.transition.direction = "left"  


    


MainApp().run()