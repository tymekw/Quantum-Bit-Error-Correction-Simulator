import kivy

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
import threading
import subprocess
kivy.require('2.0.0')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
import alice_server


class SampleLayout(GridLayout):

    def __init__(self, **kwargs):
        self.slider_n = 0
        self.slider_k = 0
        self.slider_l = 0
        super(SampleLayout, self).__init__(**kwargs)
        self.cols = 3
        n = Slider(min=0, max=100, value=25)
        n.bind(value=self.on_slider_val_n)
        k = Slider(min=0, max=100, value=25)
        k.bind(value=self.on_slider_val_k)
        l = Slider(min=0, max=100, value=25)
        l.bind(value=self.on_slider_val_l)

        self.n_label = Label(text="0")
        self.k_label = Label(text="0")
        self.l_label = Label(text="0")
        self.add_widget(Label(text="N"))
        self.add_widget(n)
        self.add_widget(self.n_label)
        self.add_widget(Label(text="K"))
        self.add_widget(k)
        self.add_widget(self.k_label)
        self.add_widget(Label(text="L"))
        self.add_widget(l)
        self.add_widget(self.l_label)

        run = Button(text="run")
        run.bind(on_press=self.run)
        self.add_widget(run)
        run_cl = Button(text="run")
        run_cl.bind(on_press=self.run_cl)
        self.add_widget(run_cl)

    def on_slider_val_n(self, instance, val):
        self.n_label.text = str(val)
        self.slider_n = int(val)

    def on_slider_val_k(self, instance, val):
        self.k_label.text = str(val)
        self.slider_k = int(val)

    def on_slider_val_l(self, instance, val):
        self.l_label.text = str(val)
        self.slider_l = int(val)

    def run(self, instance):
        t = threading.Thread(alice_server.run(self.slider_n, self.slider_k, self.slider_l))

    def run_cl(self, instance):
        # t1 = threading.Thread(bob_client.run()).start()
        pass

class MyApp(App):

    def build(self):
        return SampleLayout()
    # label = Label(text='Hello world')


if __name__ == '__main__':
    threading.Thread(MyApp().run())

