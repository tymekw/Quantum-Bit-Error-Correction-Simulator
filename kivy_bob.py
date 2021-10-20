import re

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import bob_client
import threading
from plyer import filechooser


class ClientLayout(GridLayout):
    def __init__(self, **kwargs):
        self.bob = bob_client.BobClient()
        super(ClientLayout, self).__init__(**kwargs)
        self.cols = 2
        self.machine_details_layout = GridLayout(cols=2)
        self.n_label = Label(text="N value")
        self.k_label = Label(text="K value")
        self.l_label = Label(text="L value")
        self.bits_len_label = Label(text="Bits length")
        self.n_value = Label(text=str(self.bob.N))
        self.k_value = Label(text=str(self.bob.K))
        self.l_value = Label(text=str(self.bob.L))
        self.bits_len_value = Label(text=str(self.bob.bits_length))

        self.machine_details_layout.add_widget(self.n_label)
        self.machine_details_layout.add_widget(self.n_value)
        self.machine_details_layout.add_widget(self.k_label)
        self.machine_details_layout.add_widget(self.k_value)
        self.machine_details_layout.add_widget(self.l_label)
        self.machine_details_layout.add_widget(self.l_value)
        self.machine_details_layout.add_widget(self.bits_len_label)
        self.machine_details_layout.add_widget(self.bits_len_value)

        self.add_widget(self.machine_details_layout)

        self.buttons_layout = GridLayout(cols=2)
        self.bind_button = Button(text="Bind with server")
        self.read_config_button = Button(text="Read machine config", disabled=True)
        self.create_bits_button = Button(text="Create random bits", disabled=True)
        self.import_bits_button = Button(text="Import bits", disabled=True)
        self.run_machine_button = Button(text="Run machine", disabled=True)

        self.buttons_layout.add_widget(self.bind_button)
        self.bind_button.bind(on_press=self.on_bind)
        self.buttons_layout.add_widget(self.read_config_button)
        self.read_config_button.bind(on_press=self.on_read_config)
        self.buttons_layout.add_widget(self.create_bits_button)
        self.create_bits_button.bind(on_press=self.on_create_bits)
        self.buttons_layout.add_widget(self.import_bits_button)
        self.import_bits_button.bind(on_press=self.on_import_bits)
        self.buttons_layout.add_widget(self.run_machine_button)
        self.run_machine_button.bind(on_press=self.on_run_machine)

        self.add_widget(self.buttons_layout)

        self.bits_editor_layout = GridLayout(cols=3)

        self.ber_label = Label(text="BER")
        self.ber_value = Label(text="0")
        self.ber_slider = Slider(min=0, max=10, value=0, disabled=True)
        self.ber_slider.bind(value=self.on_ber_slider)

        self.choose_label = Label(text="Choose BER version")
        self.random_button = Button(text="RANDOM", disabled=True)
        self.block_button = Button(text="BLOCK", disabled=True)

        self.bits_editor_layout.add_widget(self.ber_label)
        self.bits_editor_layout.add_widget(self.ber_value)
        self.bits_editor_layout.add_widget(self.ber_slider)
        self.bits_editor_layout.add_widget(self.choose_label)
        self.bits_editor_layout.add_widget(self.random_button)
        self.bits_editor_layout.add_widget(self.block_button)

        self.add_widget(self.bits_editor_layout)

        self.bits_layout = GridLayout(cols=1)
        self.bits_label_all = TextInput(text='111', disabled=False, cursor=(0, 0))
        self.bits_layout.add_widget(self.bits_label_all)
        self.add_widget(self.bits_layout)

    def on_import_bits(self, instance):
        # self.remove_n_k_buttons()
        path = filechooser.open_file(title="Pick a txt file..",
                                     filters=[("Text files", "*.txt")])[0]
        # print(path)
        with open(path, 'r') as f:
            lines = f.readline()
        if re.match(r'^[01]*$', lines):
            self.bob.bits.bits = lines
            self.bits_label_all.text = str(self.bob.bits.bits)
            self.bits_len_value = len(self.bob.bits.bits)
            if len(self.bob.bits.bits) != self.bob.bits_length:
                self.bits_label_all.text = "choose bits with proper length: {}".format(self.bob.bits_length)
            else:
                self.run_machine_button.disabled = False
                self.create_bits_button.disabled = True
                self.import_bits_button.disabled = True
        else:
            self.bits_label_all.text = "Choose file containing only '0' and '1'"
        # self..create_machine()
        # possible_nk = self.alice.get_factors_list()
        # print(possible_nk)
        # for i, j in possible_nk:
        #     self.N_grid_layout.add_widget(Button(text=str(i), on_press=self.handle_new_n))
        #     self.K_grid_layout.add_widget(Button(text=str(j), on_press=self.handle_new_k))
        # self.n_value.text = str(self.alice.N)
        # self.k_value.text = str(self.alice.K)
        # self.bits_slider.value = str(len(self.alice.bits.bits))
        # self.bits_slider.disabled = True
        # self.l_slider.disabled = True
        # self.create_bits_button.disabled = True
        # self.import_bits_button.disabled = True

    def on_ber_slider(self, instance, value):
        self.ber_value.text = str(int(value))
        self.bob.bits.BER = int(value)

    def on_bind(self, instance):
        instance.disabled = True
        self.read_config_button.disabled = False
        self.show_bind_popup()
        self.bind_thread = threading.Thread(target=self.bob.bind)
        self.bind_thread.daemon = True
        self.bind_thread.start()
        close_popup_thread = threading.Thread(target=self.close_bind_popup)
        close_popup_thread.daemon = True
        close_popup_thread.start()

    def close_bind_popup(self):
        while True:
            if not self.bind_thread.is_alive():
                self.popup_window.dismiss()
                return True

    def show_bind_popup(self):
        self.popup_window = Popup(title="waiting", size_hint=(None, None), size=(400, 400),
                                  auto_dismiss=False)
        self.popup_window.open()

    def on_read_config(self, instance):
        instance.disabled = True
        self.create_bits_button.disabled = False
        self.import_bits_button.disabled = False
        self.ber_slider.disabled = False
        self.random_button.disabled = False
        self.block_button.disabled = False
        self.show_read_popup()
        self.read_config_thread = threading.Thread(target=self.bob.receive_machine_config)
        self.read_config_thread.deamon = True
        self.read_config_thread.start()
        close_popup_thread = threading.Thread(target=self.close_read_popup)
        close_popup_thread.daemon = True
        close_popup_thread.start()


    def close_read_popup(self):
        while True:
            if not self.read_config_thread.is_alive():
                self.popup_window.dismiss()
                self.n_value.text = str(self.bob.N)
                self.k_value.text = str(self.bob.K)
                self.l_value.text = str(self.bob.L)
                self.bits_len_value.text = str(self.bob.bits_length)
                return True

    def show_read_popup(self):
        self.popup_window = Popup(title="waiting", size_hint=(None, None), size=(400, 400),
                                  auto_dismiss=False)
        self.popup_window.open()

    def on_create_bits(self, instance):
        self.create_bits_button.disabled = True
        self.run_machine_button.disabled = False
        self.bob.create_random_bits()
        self.bits_label_all.text = str(self.bob.bits.bits)

    def on_run_machine(self, instance):
        self.bob.create_machine()
        self.show_run_popup() # ToDo
        self.run_thread = threading.Thread(target=self.bob.run_TPM_machine)
        self.run_thread.daemon = True
        self.run_thread.start()
        close_popup_thread = threading.Thread(target=self.close_run_popup)  # ToDo
        close_popup_thread.daemon = True
        close_popup_thread.start()

    def close_run_popup(self):
        while True:
            if not self.run_thread.is_alive():
                self.popup_window.dismiss()
                self.bits_label_all.text = str(self.bob.bits.bits)
                return True

    def show_run_popup(self):
        self.popup_window = Popup(title="running machine", size_hint=(None, None), size=(400, 400),
                                  auto_dismiss=False)
        self.popup_window.open()

class ClientApp(App):
    def build(self):
        return ClientLayout()


if __name__ == '__main__':
    main = threading.Thread(target=ClientApp().run())
