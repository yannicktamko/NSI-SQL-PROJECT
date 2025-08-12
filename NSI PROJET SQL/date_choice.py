from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu

KV = '''
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
        text: "Précédant"
        pos_hint: {'center_x': .10, 'center_y': .25}


    MDRaisedButton:
        text: "Suivant"
        pos_hint: {'center_x': .90, 'center_y': .25}

    MDRaisedButton:
        id: destination
        text: "Choisir votre destination"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.menu.open()
    
    MDRaisedButton:
        id: transport
        text: "Choisissez votre moyen de transport"
        pos_hint: {"center_x": .5, "center_y": .7}
        on_release: app.transport.open()
    
    MDLabel:
        text: "Commencez la reservation de votre voyage !"
        pos_hint: {'center_x': .8, 'center_y': .75}
        color: 0.4392156862745098, 0.5058823529411764, 0.6
'''


class Dates(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.screen = Builder.load_string(KV)
        tab = ['Paris', 'New York', 'Tokyo', 'London', 'Liverpool' , 'Lloret del Mar', 'Singapoure', 'Dubai', 'Besançon', 'Madaagascar']
        menu_items = [{ "viewclass": "OneLineListItem", "text": "Paris"}, { "viewclass": "OneLineListItem", "text": "London"},{ "viewclass": "OneLineListItem", "text": "Tokyo"},{ "viewclass": "OneLineListItem", "text": "Liverpool"},{ "viewclass": "OneLineListItem", "text": "Lloret del mar"},{ "viewclass": "OneLineListItem", "text": "Singapoure"},{ "viewclass": "OneLineListItem", "text": "Dubai"},{ "viewclass": "OneLineListItem", "text": "Besançon"},{ "viewclass": "OneLineListItem", "text": "Madagascar"} ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.destination, items=menu_items, width_mult=4
        )
        transport = [{ "viewclass": "OneLineListItem", "text": "Avion"}, { "viewclass": "OneLineListItem", "text": "Train"},{ "viewclass": "OneLineListItem", "text": "Bus"}]
        self.transport = MDDropdownMenu(
            caller=self.screen.ids.transport, items=transport, width_mult=4
        )


    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def on_save_arrivee(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        self.root.ids.arrivee.text = str(value)
        
        
    def on_save_depart(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        
        self.root.ids.depart.text = str(value)
    
    def on_save_destination(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        
        self.root.ids.destination.text = str(value)
    
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
        #arrivee = f"{date_dialog._date_label_text}"
        #depart = f"{date_dialog.year}" + "-" + f"{date_dialog.month}" +  "-" + f"{date_dialog.day}"



Dates().run()


