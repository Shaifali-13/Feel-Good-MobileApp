from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from hoverable import HoverBehavior
import json, glob, random
from datetime import datetime
from pathlib import Path

Builder.load_file('design.kv')

class LoginScreen(Screen):
    
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self, uname, pword):

        with open("users.json", 'r') as file:
            users = json.load(file) 
            #users will be a dictionary containing all the data 
            #in users.json file
        
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        
        else:
            self.ids.login_wrong.text = "Wrong username or password!"
    
    def forgot_password(self):
        self.manager.current = "forgotPassword"
            



class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    def add_user(self, uname, pword):

        with open("users.json") as file:
            users = json.load(file)

            users[uname] = {'username': uname, 
            'password': pword, 
            'date_created': 
            datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            }
        
        with open("users.json", 'w') as file:
            json.dump(users, file)
        
        self.manager.current = "sign_up_success_screen"


class SignUpSuccessScreen(Screen):
    def login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    def logout(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
    
    def get_quotes(self, feels):

        feels = feels.lower()

        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename
                            in available_feelings]

        
        if feels in available_feelings:
            with open("quotes//{feels}.txt", encoding="UTF-8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class ForgotPasswordScreen(Screen):
    def change_password(self, uname, new_pword):

        with open("users.json") as file:
            users = json.load(file)
        
        users[uname] = {'username': uname, 
        'password': new_pword,
        'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        if users[uname]['username'] == uname:
            with open("users.json", 'w') as file:
                users[uname]['password'] = new_pword
                json.dump(users, file)
            
            self.ids.password_status.text = "Password changed successfully!"
            import time
            time.sleep(1)
            self.manager.transition.direction = "right"
            self.manager.current = "login_screen"
        
        else:
            self.ids.password_status.text = "Error! Please Try again!"
   

class MainApp(App):

    def build(self):
        return RootWidget()  #it's the object, not the class hence used()
    

if __name__ == "__main__":
    MainApp().run()