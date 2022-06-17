import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.base import runTouchApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import sqlite3
from kivy.uix.label import Label
import io
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
import requests
import json

connection = sqlite3.connect('KittyDex.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS KittyDex
              (Prop TEXT, Nom TEXT, Model BLOB, Rang INT, S INT, PrixEur INT, OPrixBTC INT, OPrixETH INT, OPrixLTC INT, PrixBTC INT, PrixETH INT, PrixLTC INT, Attk INT, Pv INT, Crt INT, Char INT)''')
user = None


class PopupWindow(Widget):
	def btn(self):
		popFun()


class P(FloatLayout):
	pass

def popFun():
	show = P()
	window = Popup(title = "popup", content = show,
				size_hint = (None, None), size = (300, 300))
	window.open()


class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def validate(self):

        demail = self.email.text        
        dpwd = self.pwd.text
        global user

        
        if (demail not in users['Email'].unique() and dpwd not in users['Password'].unique()) or (len(demail) == 0) or (len(dpwd) == 0):
            popFun()
        else:
                xemail = users.index[users['Email']==self.email.text].tolist()
                xpwd = users.index[users['Password']==self.pwd.text].tolist()
                if xemail != xpwd:
                    popFun()
                else:  
                    user = users.loc[xemail]                     
                        
			
                    sm.current = 'logdata'

            
                    self.email.text = ""
                    self.pwd.text = ""



class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    bod = ObjectProperty(None)
    wallet = ObjectProperty(None)
    def signupbtn(self):

		
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text, self.bod.text, self.wallet.text]],
							columns = ['Name', 'Email', 'Password', 'BOD', 'wallet'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():

				
                user.to_csv('login.csv', mode = 'a', header = False, index = False)
                sm.current = 'login'
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
            else:
			
                popFun()

class logDataWindow(Screen):
    pass


class galleryWindow(Screen):
    view = ObjectProperty(None)
    
    def button_pressed(self, btn):
        
        global user
        id = btn.text
        x = cursor.execute("SELECT * from KittyDex WHERE Nom=?", (id,))
        y = x.fetchall()
        
        
        blob_data = y[0][2]
        
        data = io.BytesIO(blob_data)
        im = CoreImage(data, ext="png").texture
        
               
        layout = FloatLayout()
        closeButton = Button(text = "Retour", size_hint = (0.1, 0.1), pos = (715, 10) )
        layout.add_widget(closeButton)  
        img = Image(texture=im, size_hint = (1, 1), pos = (-250, 150))
        layout.add_widget(img)
        Rang = Label(text = 'Rang : ' + str(y[0][3]), size_hint = (1, 1), pos = (100,250))
        layout.add_widget(Rang)
        Sexe = Label(text = 'Sexe : ' + str(y[0][4]), size_hint = (1, 1), pos = (175,250))
        layout.add_widget(Sexe)
        Attk = Label(text = 'Attk : ' + str(y[0][12]), size_hint = (1, 1), pos = (100,200))
        layout.add_widget(Attk)
        Pv = Label(text = 'Pv : ' + str(y[0][13]), size_hint = (1, 1), pos = (175,200))
        layout.add_widget(Pv)
        Crt = Label(text = 'Crt : ' + str(y[0][14]), size_hint = (1, 1), pos = (100,150))
        layout.add_widget(Crt)
        Char = Label(text = 'Char : ' + str(y[0][15]), size_hint = (1, 1), pos = (175,150))
        layout.add_widget(Char)
        Prix = Label(text = 'Prix : ' + str(y[0][5]) + '€', size_hint = (1, 1), pos = (-300,-50))
        layout.add_widget(Prix)
        Wallet = Label(text = 'Portefeuille : ' + str(user['wallet'].iat[0]) + '€', size_hint = (1, 1), pos = (200,300))
        layout.add_widget(Wallet)
  
        key = "https://api.binance.com/api/v3/ticker/price?symbol="
          
        url = key+'BTCEUR' 
        BTC = requests.get(url)
        BTC = BTC.json()
        VBTC = y[0][5] / float(BTC['price'])
        vb = VBTC - y[0][6]
        
        Lbtc = Label(text = 'valeur en Bitcoin : ' + str(VBTC) + ' BTC', size_hint = (1, 1), pos = (-200,-100))
        layout.add_widget(Lbtc)
        
        url = key+'ETHEUR' 
        ETH = requests.get(url)
        ETH = ETH.json()
        VETH = y[0][5] / float(ETH['price'])
        ve = VETH - y[0][7]
        
        Leth = Label(text = 'valeur en Ethereum : ' + str(VETH) + ' ETH', size_hint = (1, 1), pos = (-200,-150))
        layout.add_widget(Leth)
        
        url = key+'LTCEUR' 
        LTC = requests.get(url)
        LTC = LTC.json()
        VLTC = y[0][5] / float(LTC['price'])
        vl = VLTC - y[0][8]
        
        Lltc = Label(text = 'valeur en Litecoin : ' + str(VLTC) + ' LTC', size_hint = (1, 1), pos = (-200,-200))
        layout.add_widget(Lltc)
        
        vbtc = Label(text = 'variation depuis l achat : ' + str(vb) + '€', size_hint = (1, 1), pos = (200,-100))
        layout.add_widget(vbtc)
        
        veth = Label(text = 'variation depuis l achat : ' + str(ve) + '€', size_hint = (1, 1), pos = (200,-150))
        layout.add_widget(veth)
        
        vltc = Label(text = 'variation depuis l achat : ' + str(vl) + '€', size_hint = (1, 1), pos = (200,-200))
        layout.add_widget(vltc)
        
        

        popup = Popup(title =btn.text,
                      content = layout)  
        popup.open()   
  

        closeButton.bind(on_press = popup.dismiss) 
    
    def on_enter(self):
        global user

        id = user['Email'].iat[0]
        x = cursor.execute("SELECT * from KittyDex WHERE Prop=?", (id,))

        y = x.fetchall()
        l = len(y)
        base = ["element {}".format(i) for i in range(l)]
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        i = 0
        for element in base:
            nom = y[i][1]            
            layout.add_widget(Button(on_press=self.button_pressed, text=nom, size=(50, 50), size_hint=(1, None),
                                     background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1)))
            i+=1
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(layout)
        self.view.add_widget(scrollview)

    def on_leave(self):
        self.view.remove_widget(self.view.children[0])
        
    def create_scrollview(self, dt):
        pass    
    
    def __init__(self, **kwargs):
        super(galleryWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.create_scrollview)
        
    

class buyWindow(Screen):
    view = ObjectProperty(None)
    
    def buy(self, btn):
        global user
    
    def button_pressed(self, btn):
        
        global user
        id = btn.text
        x = cursor.execute("SELECT * from KittyDex WHERE Nom=?", (id,))
        y = x.fetchall()
        
        
        blob_data = y[0][2]
        
        data = io.BytesIO(blob_data)
        im = CoreImage(data, ext="png").texture
        
                
        layout = FloatLayout()
        closeButton = Button(text = "Retour", size_hint = (0.1, 0.1), pos = (715, 10) )
        layout.add_widget(closeButton)  
        img = Image(texture=im, size_hint = (1, 1), pos = (-250, 150))
        layout.add_widget(img)
        Rang = Label(text = 'Rang : ' + str(y[0][3]), size_hint = (1, 1), pos = (100,250))
        layout.add_widget(Rang)
        Sexe = Label(text = 'Sexe : ' + str(y[0][4]), size_hint = (1, 1), pos = (175,250))
        layout.add_widget(Sexe)
        Attk = Label(text = 'Attk : ' + str(y[0][12]), size_hint = (1, 1), pos = (100,200))
        layout.add_widget(Attk)
        Pv = Label(text = 'Pv : ' + str(y[0][13]), size_hint = (1, 1), pos = (175,200))
        layout.add_widget(Pv)
        Crt = Label(text = 'Crt : ' + str(y[0][14]), size_hint = (1, 1), pos = (100,150))
        layout.add_widget(Crt)
        Char = Label(text = 'Char : ' + str(y[0][15]), size_hint = (1, 1), pos = (175,150))
        layout.add_widget(Char)
        Prix = Label(text = 'Prix : ' + str(y[0][5]) + '€', size_hint = (1, 1), pos = (-300,-50))
        layout.add_widget(Prix)
        Wallet = Label(text = 'Portefeuille : ' + str(user['wallet'].iat[0]) + '€', size_hint = (1, 1), pos = (200,300))
        layout.add_widget(Wallet)
  
        key = "https://api.binance.com/api/v3/ticker/price?symbol="
          
        url = key+'BTCEUR' 
        BTC = requests.get(url)
        BTC = BTC.json()
        VBTC = y[0][5] / float(BTC['price'])

        Lbtc = Label(text = 'valeur en Bitcoin : ' + str(VBTC) + ' BTC', size_hint = (1, 1), pos = (-200,-100))
        layout.add_widget(Lbtc)
        
        url = key+'ETHEUR' 
        ETH = requests.get(url)
        ETH = ETH.json()
        VETH = y[0][5] / float(ETH['price'])
        
        Leth = Label(text = 'valeur en Ethereum : ' + str(VETH) + ' ETH', size_hint = (1, 1), pos = (-200,-150))
        layout.add_widget(Leth)
        
        url = key+'LTCEUR' 
        LTC = requests.get(url)
        LTC = LTC.json()
        VLTC = y[0][5] / float(LTC['price'])
        
        Lltc = Label(text = 'valeur en Litecoin : ' + str(VLTC) + ' LTC', size_hint = (1, 1), pos = (-200,-200))
        layout.add_widget(Lltc)
                
        Bbutton = Button(text = 'Acheter' , size_hint = (0.1, 0.1), pos = (350, 10) )
        layout.add_widget(Bbutton)
        
        popup = Popup(title =btn.text,
                      content = layout)  
        popup.open()   
  
        closeButton.bind(on_press = popup.dismiss) 
        Bbutton.bind(on_press = self.buy)
    
    def on_enter(self):
        global user
        id = user['Email'].iat[0]
        x = cursor.execute("SELECT * from KittyDex WHERE Prop!=?", (id,))
        y = x.fetchall()
        l = len(y)
        i = 0
        base = ["element {}".format(i) for i in range(l)]
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        i = 0
        for element in base:
            nom = y[i][1]            
            layout.add_widget(Button(on_press=self.button_pressed, text=nom, size=(50, 50), size_hint=(1, None),
                                     background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1)))
            i+=1
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(layout)
        self.view.add_widget(scrollview)

    def on_leave(self):
        self.view.remove_widget(self.view.children[0])
        
    def create_scrollview(self, dt):
        pass    

    def __init__(self, **kwargs):
        super(buyWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.create_scrollview)

class sellWindow(Screen):
    view = ObjectProperty(None)
    
    def sell(self, btn):
        global user
    
    def button_pressed(self, btn):
        
        global user
        id = btn.text
        x = cursor.execute("SELECT * from KittyDex WHERE Nom=?", (id,))
        y = x.fetchall()
        
        
        blob_data = y[0][2]
        
        data = io.BytesIO(blob_data)
        im = CoreImage(data, ext="png").texture
        
                
        layout = FloatLayout()
        closeButton = Button(text = "Retour", size_hint = (0.1, 0.1), pos = (715, 10) )
        layout.add_widget(closeButton)  
        img = Image(texture=im, size_hint = (1, 1), pos = (-250, 150))
        layout.add_widget(img)
        Rang = Label(text = 'Rang : ' + str(y[0][3]), size_hint = (1, 1), pos = (100,250))
        layout.add_widget(Rang)
        Sexe = Label(text = 'Sexe : ' + str(y[0][4]), size_hint = (1, 1), pos = (175,250))
        layout.add_widget(Sexe)
        Attk = Label(text = 'Attk : ' + str(y[0][12]), size_hint = (1, 1), pos = (100,200))
        layout.add_widget(Attk)
        Pv = Label(text = 'Pv : ' + str(y[0][13]), size_hint = (1, 1), pos = (175,200))
        layout.add_widget(Pv)
        Crt = Label(text = 'Crt : ' + str(y[0][14]), size_hint = (1, 1), pos = (100,150))
        layout.add_widget(Crt)
        Char = Label(text = 'Char : ' + str(y[0][15]), size_hint = (1, 1), pos = (175,150))
        layout.add_widget(Char)
        Prix = Label(text = 'Prix : ' + str(y[0][5]) + '€', size_hint = (1, 1), pos = (-300,-50))
        layout.add_widget(Prix)
        Wallet = Label(text = 'Portefeuille : ' + str(user['wallet'].iat[0]) + '€', size_hint = (1, 1), pos = (200,300))
        layout.add_widget(Wallet)
  
        key = "https://api.binance.com/api/v3/ticker/price?symbol="
          
        url = key+'BTCEUR' 
        BTC = requests.get(url)
        BTC = BTC.json()
        VBTC = y[0][5] / float(BTC['price'])
        vb = VBTC - y[0][6]
        
        Lbtc = Label(text = 'valeur en Bitcoin : ' + str(VBTC) + ' BTC', size_hint = (1, 1), pos = (-200,-100))
        layout.add_widget(Lbtc)
        
        url = key+'ETHEUR' 
        ETH = requests.get(url)
        ETH = ETH.json()
        VETH = y[0][5] / float(ETH['price'])
        ve = VETH - y[0][7]
        
        Leth = Label(text = 'valeur en Ethereum : ' + str(VETH) + ' ETH', size_hint = (1, 1), pos = (-200,-150))
        layout.add_widget(Leth)
        
        url = key+'LTCEUR' 
        LTC = requests.get(url)
        LTC = LTC.json()
        VLTC = y[0][5] / float(LTC['price'])
        vl = VLTC - y[0][8]
        
        Lltc = Label(text = 'valeur en Litecoin : ' + str(VLTC) + ' LTC', size_hint = (1, 1), pos = (-200,-200))
        layout.add_widget(Lltc)
        
        vbtc = Label(text = 'variation depuis l achat : ' + str(vb) + '€', size_hint = (1, 1), pos = (200,-100))
        layout.add_widget(vbtc)
        
        veth = Label(text = 'variation depuis l achat : ' + str(ve) + '€', size_hint = (1, 1), pos = (200,-150))
        layout.add_widget(veth)
        
        vltc = Label(text = 'variation depuis l achat : ' + str(vl) + '€', size_hint = (1, 1), pos = (200,-200))
        layout.add_widget(vltc)
        
        Bbutton = Button(text = 'Acheter' , size_hint = (0.1, 0.1), pos = (350, 10) )
        layout.add_widget(Bbutton)
        
        popup = Popup(title =btn.text,
                      content = layout)  
        popup.open()   
  
        closeButton.bind(on_press = popup.dismiss) 
    
        Bbutton.bind(on_press = self.sell)
    
    def on_enter(self):
        global user
        id = user['Email'].iat[0]
        x = cursor.execute("SELECT * from KittyDex WHERE Prop=?", (id,))
        y = x.fetchall()
        l = len(y)
        base = ["element {}".format(i) for i in range(l)]
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        i = 0
        for element in base:
            nom = y[i][1]            
            layout.add_widget(Button(on_press=self.button_pressed, text=nom, size=(50, 50), size_hint=(1, None),
                                     background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1)))
            i+=1
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(layout)
        self.view.add_widget(scrollview)

    def on_leave(self):
        self.view.remove_widget(self.view.children[0])
        
    def create_scrollview(self, dt):
        pass    

    def __init__(self, **kwargs):
        super(sellWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.create_scrollview)


class windowManager(ScreenManager):
	pass

kv = Builder.load_file('login.kv')
sm = windowManager()

users=pd.read_csv('login.csv')

sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(galleryWindow(name='gallery'))
sm.add_widget(buyWindow(name='buy'))
sm.add_widget(sellWindow(name='sell'))

class loginMain(App):
	def build(self):
		return sm



if __name__=="__main__":
	loginMain().run()

connection.commit()
connection.close()