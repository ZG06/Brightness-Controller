from kivy.config import Config
# Setting the window not to be resizable
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
import os

# Setting default window size
Window.size = (dp(600), dp(300))


class MainApp(MDApp):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)
      # Loading the storage when opening the app
      self.storage = JsonStore(f'{os.path.realpath(__file__)[:-7]}storage/storage.json')
      
      self.reading_mode_state = self.storage.get('Settings')['reading_mode']

   def build(self):  
      self.title = 'Brightness Controller' # Window title
      self.icon = 'icon.png' # Window icon
      self.monitor = os.popen('xrandr -q | egrep "\sconnected"').read().split(' ')[0] # Active monitor
      self.theme_cls.theme_style = 'Dark' # Default theme style

      # Restoring settings from the previous session
      if self.root.ids.red_color.value == 100:
         if self.root.ids.green_color.value == 89:
            if self.root.ids.blue_color.value == 75:
               self.root.ids.reading_mode.active = self.reading_mode_state

   def controller(self):
      # Setting brightness and color levels after scrolling a slider
      self.brightness = f'{(self.root.ids.brightness.value/100):.2f}'
      self.R = f'{(self.root.ids.red_color.value/100):.2f}'
      self.G = f'{(self.root.ids.green_color.value/100):.2f}'
      self.B = f'{(self.root.ids.blue_color.value/100):.2f}'
      
      # Changing the screen brightness and color settings
      os.system(f'xrandr --output {self.monitor} --gamma {self.R}:{self.G}:{self.B} --brightness {self.brightness}')

      # Saving settings
      self.save_settings()

   def reading_mode(self, switchValue):
      # Turning on a reading mode if the switch is on
      if switchValue == True:
         self.root.ids.red_color.value = 100
         self.root.ids.green_color.value = 89
         self.root.ids.blue_color.value = 75
         os.system(f'xrandr --output {self.monitor} --gamma 1:0.89:0.75 --brightness {self.root.ids.brightness.value/100}')
      
      self.save_settings(switchValue)

   def save_settings(self, *args):
      # Saving brightness and color setting when closing the app
      self.storage.put(
         'Settings',
         brightness = self.root.ids.brightness.value,
         R = self.root.ids.red_color.value,
         G = self.root.ids.green_color.value,
         B = self.root.ids.blue_color.value,
         reading_mode = self.root.ids.reading_mode.active
      )

# Running the app
if __name__ == '__main__':
	MainApp().run()