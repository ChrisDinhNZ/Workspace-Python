'''
Description: A simple class to monitor button or switch via a GPIO input.
'''

from gpiozero import Button

class ButtonMonitor:
   def __init__(self, input_pin, name, observer):
      self.button = Button(input_pin)
      self.button_name = name
      self.observer = observer

      self.button.when_pressed = self.button_pressed

   def button_pressed(self):
      if self.observer is None:
         pass  # No observer so do nothing
      else:
         self.observer.handle_button_pressed(self.button_name)
