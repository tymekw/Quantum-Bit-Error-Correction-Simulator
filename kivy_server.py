from kivy.clock import Clock

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
import threading

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import alice_server


class ServerLayout(GridLayout):
    def __init__(self, **kwargs):
        super(ServerLayout, self).__init__(**kwargs)
        self.cols = 2
        self.machine_details_layout = GridLayout(cols=2)
        self.n_label = Label(text="N value")
        self.k_label = Label(text="K value")
        self.l_label = Label(text="L value")
        self.n_value = Label(text="10")
        self.k_value = Label(text="10")
        self.l_value = Label(text="10")

        self.bits_label = Label(text="bits length")
        self.seed_label = Label(text="write seed")
        self.bits_value = Label(text="100")

        self.machine_details_layout.add_widget(self.n_label)
        self.machine_details_layout.add_widget(self.n_value)
        self.machine_details_layout.add_widget(self.k_label)
        self.machine_details_layout.add_widget(self.k_value)
        self.machine_details_layout.add_widget(self.l_label)
        self.machine_details_layout.add_widget(self.l_value)

        self.machine_details_layout.add_widget(self.bits_label)
        self.machine_details_layout.add_widget(self.bits_value)
        self.machine_details_layout.add_widget(self.seed_label)

        self.add_widget(self.machine_details_layout)

        self.machine_sliders_text_layout = GridLayout(cols=1)
        self.n_slider = Slider(min=0, max=100, value=50)
        self.n_slider.bind(value=self.on_slider_n)
        self.k_slider = Slider(min=0, max=100, value=50)
        self.k_slider.bind(value=self.on_slider_k)
        self.l_slider = Slider(min=0, max=100, value=50)
        self.l_slider.bind(value=self.on_slider_l)
        self.bits_slider = Slider(min=0, max=10000, value=100)
        self.bits_slider.bind(value=self.on_slider_bits)
        self.seed_text_field = TextInput(text='Write your seed')

        self.machine_sliders_text_layout.add_widget(self.n_slider)
        self.machine_sliders_text_layout.add_widget(self.k_slider)
        self.machine_sliders_text_layout.add_widget(self.l_slider)
        self.machine_sliders_text_layout.add_widget(self.bits_slider)
        self.machine_sliders_text_layout.add_widget(self.seed_text_field)

        self.add_widget(self.machine_sliders_text_layout)

        self.buttons_layout = GridLayout(cols=2)
        self.bind_button = Button(text="Bind with client")
        # self.bind_button.bind(on_press=self.function)
        self.create_bits_button = Button(text="Create random bits")
        # self.create_bits_button.bind(on_press=self.function)
        self.import_bits_button = Button(text="Import bits")
        # self.import_bits_button.bind(on_press=self.function)
        self.send_machine_config_button = Button(text="Send machine config")
        # self.send_machine_config_button.bind(on_press=self.function)
        self.run_machine_button = Button(text="Run machine")
        # self.run_machine_button.bind(on_press=self.function)

        self.buttons_layout.add_widget(self.bind_button)
        self.buttons_layout.add_widget(self.create_bits_button)
        self.buttons_layout.add_widget(self.import_bits_button)
        self.buttons_layout.add_widget(self.send_machine_config_button)
        self.buttons_layout.add_widget(self.run_machine_button)

        self.add_widget(self.buttons_layout)

    def on_slider_n(self, instance, value):
        self.n_value.text = str(int(value))

    def on_slider_k(self, instance, value):
        self.k_value.text = str(int(value))

    def on_slider_l(self, instance, value):
        self.l_value.text = str(int(value))

    def on_slider_bits(self, instance, value):
        self.bits_value.text = str(int(value))


class ServerApp(App):
    def build(self):
        return ServerLayout()


if __name__ == '__main__':
    ServerApp().run()
