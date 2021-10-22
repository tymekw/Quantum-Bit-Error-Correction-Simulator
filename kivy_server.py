import re

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import alice_server
import threading
from plyer import filechooser


class ServerLayout(GridLayout):
    def __init__(self, **kwargs):
        self.alice = alice_server.AliceServer()
        super(ServerLayout, self).__init__(**kwargs)
        self.cols = 2
        self.machine_details_layout = GridLayout(cols=2)
        self.n_label = Label(text="N value")
        self.k_label = Label(text="K value")
        self.l_label = Label(text="L value")
        self.n_value = Label(text=str(self.alice.N))
        self.k_value = Label(text=str(self.alice.K))
        self.l_value = Label(text=str(self.alice.L))

        self.bits_label = Label(text="bits length")
        self.seed_label = Label(text="write seed")
        self.bits_value = Label(text="256")

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
        self.N_grid_layout = GridLayout(rows=1)
        self.K_grid_layout = GridLayout(rows=1)
        # self.n_slider = Slider(min=1, max=100, value=10)
        # self.n_slider.bind(value=self.on_slider_n)
        # self.k_slider = Slider(min=1, max=100, value=10)
        # self.k_slider.bind(value=self.on_slider_k)
        self.l_slider = Slider(min=1, max=100, value=2)
        self.l_slider.bind(value=self.on_slider_l)
        self.bits_slider = Slider(min=1, max=10000, value=1000)
        self.bits_slider.bind(value=self.on_slider_bits)
        self.seed_text_field = TextInput(text='Write your seed')

        # self.machine_sliders_text_layout.add_widget(self.n_slider)
        # self.machine_sliders_text_layout.add_widget(self.k_slider)

        # for i in range(0,10):
        #     self.N_grid_layout.add_widget(Button(text=str(i)))

        self.machine_sliders_text_layout.add_widget(self.N_grid_layout)
        self.machine_sliders_text_layout.add_widget(self.K_grid_layout)
        self.machine_sliders_text_layout.add_widget(self.l_slider)
        self.machine_sliders_text_layout.add_widget(self.bits_slider)
        self.machine_sliders_text_layout.add_widget(self.seed_text_field)

        self.add_widget(self.machine_sliders_text_layout)

        self.buttons_layout = GridLayout(cols=2)
        self.bind_button = Button(text="Bind with client")
        # self.bind_button.bind(on_press=self.on_bind)
        self.create_bits_button = Button(text="Create random bits")
        self.create_bits_button.bind(on_press=self.on_create_bits)

        self.import_bits_button = Button(text="Import bits", disabled=False)
        self.import_bits_button.bind(on_press=self.on_import_bits)

        self.send_machine_config_button = Button(text="Send machine config", disabled=True)
        self.send_machine_config_button.bind(on_press=self.on_send_config)
        self.run_machine_button = Button(text="Run machine", disabled=True)
        self.run_machine_button.bind(on_press=self.on_run_machine)

        # self.buttons_layout.add_widget(self.bind_button)
        self.buttons_layout.add_widget(self.create_bits_button)
        self.buttons_layout.add_widget(self.import_bits_button)
        self.buttons_layout.add_widget(self.send_machine_config_button)
        self.buttons_layout.add_widget(self.run_machine_button)

        self.add_widget(self.buttons_layout)

        self.bits_layout = GridLayout(cols=1)
        self.bits_label_all = TextInput(text='111', disabled=False, cursor=(0, 0))
        self.bits_layout.add_widget(self.bits_label_all)
        self.add_widget(self.bits_layout)
        self.on_bind(self.bind_button)

    def on_import_bits(self, instance):
        self.remove_n_k_buttons()
        path = filechooser.open_file(title="Pick a txt file..",
                                     filters=[("Text files", "*.txt")])[0]
        # print(path)
        with open(path, 'r') as f:
            lines = f.readline()

        if re.match(r'^[01]*$', lines):
            self.alice.bits.bits = lines
            self.bits_label_all.text = str(self.alice.bits.bits)
            self.alice.create_machine()
            possible_nk = self.alice.get_factors_list()
            print(possible_nk)
            for i, j in possible_nk:
                self.N_grid_layout.add_widget(Button(text=str(i), on_press=self.handle_new_n))
                self.K_grid_layout.add_widget(Button(text=str(j), on_press=self.handle_new_k))
            self.n_value.text = str(self.alice.N)
            self.k_value.text = str(self.alice.K)
            self.bits_slider.value = str(len(self.alice.bits.bits))
            self.bits_slider.disabled = True
            self.l_slider.disabled = True
            self.create_bits_button.disabled = True
            self.import_bits_button.disabled = True
            self.send_machine_config_button.disabled = False
        else:
            self.bits_label_all.text = "Choose file containing only '1' and '0'"




    def on_slider_n(self, instance, value):
        self.n_value.text = str(int(value))
        self.alice.set_N(int(value))

    def on_slider_k(self, instance, value):
        self.k_value.text = str(int(value))
        self.alice.set_K(int(value))

    def on_slider_l(self, instance, value):
        self.l_value.text = str(int(value))
        self.alice.set_L(int(value))

    def on_slider_bits(self, instance, value):
        self.bits_value.text = str(int(value))
        self.alice.set_bits_length(int(value))

    def on_bind(self, instance):
        instance.disabled = True
        # self.send_machine_config_button.disabled = False
        # self.show_bind_popup()
        self.bind_thread = threading.Thread(target=self.alice.bind)
        self.bind_thread.daemon = True
        self.bind_thread.start()
        # close_popup_thread = threading.Thread(target=self.close_bid_popup)
        # close_popup_thread.daemon = True
        # close_popup_thread.start()

    def close_bid_popup(self):
        while True:
            if not self.bind_thread.is_alive():
                self.popup_window.dismiss()
                return True

    def show_bind_popup(self):
        self.popup_window = Popup(title="waiting", size_hint=(None, None), size=(400, 400),
                                  auto_dismiss=False)
        self.popup_window.open()

    def on_create_bits(self, instance):
        self.remove_n_k_buttons()
        self.alice.set_seed(self.seed_text_field.text)
        self.alice.generate_bits()
        self.bits_label_all.text = str(self.alice.bits.bits)
        self.alice.create_machine()
        possible_nk = self.alice.get_factors_list()
        print(possible_nk)
        for i, j in possible_nk:
            self.N_grid_layout.add_widget(Button(text=str(i), on_press=self.handle_new_n))
            self.K_grid_layout.add_widget(Button(text=str(j), on_press=self.handle_new_k))
        for b in self.N_grid_layout.children:
            if b.text == str(self.alice.N):
                b.background_normal = b.background_down
        for b in self.K_grid_layout.children:
            if b.text ==  str(self.alice.K):
                b.background_normal = b.background_down
        self.n_value.text = str(self.alice.N)
        self.k_value.text = str(self.alice.K)
        self.send_machine_config_button.disabled = False
        self.import_bits_button.disabled = True

    def remove_n_k_buttons(self):
        self.N_grid_layout.clear_widgets()
        self.K_grid_layout.clear_widgets()
        for b in self.N_grid_layout.children:
            self.N_grid_layout.remove_widget(b)
        for b in self.K_grid_layout.children:
            self.K_grid_layout.remove_widget(b)

    def get_possible_k(self, given_n):
        for n, k in self.alice.get_factors_list():
            if n == given_n:
                return k

    def get_possible_n(self, given_k):
        for n, k in self.alice.get_factors_list():
            if k == given_k:
                return n

    def handle_new_n(self, instance):
        self.reset_buttons()
        instance.background_normal = instance.background_down
        self.alice.N = int(instance.text)
        self.alice.K = self.get_possible_k(int(instance.text))
        for button in self.K_grid_layout.children:
            if button.text == str(self.alice.K):
                button.background_normal = instance.background_down
        self.n_value.text = str(self.alice.N)
        self.k_value.text = str(self.alice.K)
        self.alice.change_machine_config()
        print(self.alice.W)
        print(self.alice.aliceTPM.W)

    def handle_new_k(self, instance):
        self.reset_buttons()
        instance.background_normal = instance.background_down
        self.alice.K = int(instance.text)
        self.alice.N = self.get_possible_k(int(instance.text))
        for button in self.N_grid_layout.children:
            if button.text == str(self.alice.N):
                button.background_normal = instance.background_down
        self.n_value.text = str(self.alice.N)
        self.k_value.text = str(self.alice.K)
        self.alice.change_machine_config()
        print(self.alice.W)
        print(self.alice.aliceTPM.W)

    def reset_buttons(self):
        for button in self.N_grid_layout.children:
            button.background_normal = 'atlas://data/images/defaulttheme/button'
        for button in self.K_grid_layout.children:
            button.background_normal = 'atlas://data/images/defaulttheme/button'

    def on_send_config(self, instance):
        # self.n_slider.disabled = True
        # self.k_slider.disabled = True
        self.l_slider.disabled = True
        self.bits_slider.disabled = True
        self.seed_text_field.disabled = True
        # self.create_bits_button.disabled = True
        instance.disabled = True
        self.run_machine_button.disabled = False
        self.show_send_popup()
        self.send_config_thread = threading.Thread(target=self.alice.send_machine_config)
        self.send_config_thread.daemon = True
        self.send_config_thread.start()
        close_popup_thread = threading.Thread(target=self.close_send_popup)
        close_popup_thread.daemon = True
        close_popup_thread.start()

    def close_send_popup(self):
        while True:
            if not self.send_config_thread.is_alive():
                self.popup_window.dismiss()
                return True

    def show_send_popup(self):
        self.popup_window = Popup(title="waiting", size_hint=(None, None), size=(400, 400),
                                  auto_dismiss=False)
        self.popup_window.open()

    def on_run_machine(self, instance):
        self.show_run_popup()
        self.run_thread = threading.Thread(target=self.alice.run_machine)
        self.run_thread.daemon = True
        self.run_thread.start()
        close_popup_thread = threading.Thread(target=self.close_run_popup)
        close_popup_thread.daemon = True
        close_popup_thread.start()

    def close_run_popup(self):
        while True:
            if not self.run_thread.is_alive():
                self.popup_window.dismiss()
                self.bits_label_all.text = str(self.alice.bits.bits)
                self.bits_label_all.disabled = False
                # self.n_slider.disabled = False
                # self.k_slider.disabled = False
                self.l_slider.disabled = False
                self.bits_slider.disabled = False
                self.seed_text_field.disabled = False
                self.create_bits_button.disabled = False
                # self.bind_button.disabled = False
                self.run_machine_button.disabled = False
                self.send_machine_config_button.disabled = False
                return True

    def show_run_popup(self):
        self.popup_window = Popup(title="running machine", size_hint=(None, None), size=(400, 400),
                                  auto_dismiss=False)
        self.popup_window.open()


class ServerApp(App):
    def build(self):
        return ServerLayout()


if __name__ == '__main__':
    main = threading.Thread(target=ServerApp().run())
