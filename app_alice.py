from kivy.clock import Clock

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
import threading

from kivy.app import App
from kivy.uix.label import Label
import alice_server


class SampleLayout(GridLayout):

    def __init__(self, **kwargs):
        self.al = None
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

        self.n_label = Label(text=str(3))
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

        self.run_b = Button(text="run")
        self.run_b.bind(on_press=self.run)
        self.add_widget(self.run_b)
        run_cl = Button(text="run")
        run_cl.bind(on_press=self.run_cl)
        self.add_widget(run_cl)



    def do_the_loop(self):
        self.event = Clock.schedule_interval(self.to_be_called, 0.5)

    def to_be_called(self, dt):
        self.n_label.text = str(self.al.num)
        if self.al.num > 200:
            Clock.unschedule(self.event)
            self.run_b.disabled = False


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
        instance.disabled = True
        self.al = alice_server.AliceServer()
        self.al.L = self.slider_l
        self.al.K = self.slider_k
        self.al.N = self.slider_n
        # self.do_the_loop()
        t = threading.Thread(target=self.al.run)
        t.daemon = True
        t.start()

    def run_cl(self, instance):
        pass

class MyApp(App):

    def build(self):
        return SampleLayout()



if __name__ == '__main__':
    MyApp().run()

