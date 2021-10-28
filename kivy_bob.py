import re
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import bob_client
import threading
from plyer import filechooser
from kivy.graphics import Color, Rectangle


class ClientLayout(GridLayout):
    def __init__(self, **kwargs):
        self.bob = bob_client.BobClient()
        super(ClientLayout, self).__init__(**kwargs)
        self.cols = 2
        self.machine_details_layout = GridLayout(cols=2)
        self.n_label = Label(text="Inputs per one \nhidden neuron [N]", halign='center', valign='middle')
        self.k_label = Label(text="Neurons in \nhidden layer [K]", halign='center', valign='middle')
        self.l_label = Label(text="Weights range {-L, L}")
        self.bits_len_label = Label(text="Key length [bits]")
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
        self.bind_button = Button(text="Connect to server")
        self.read_config_button = Button(text="Get settings", disabled=True)
        self.create_bits_button = Button(text="Create random bits", disabled=True)
        self.import_bits_button = Button(text="Import bits", disabled=True)
        self.run_machine_button = Button(text="START", disabled=True, bold=True)
        self.reset_button = Button(text="RESET", disabled=True, bold=True)

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
        self.buttons_layout.add_widget(self.reset_button)
        self.reset_button.bind(on_press=self.on_reset)

        self.add_widget(self.buttons_layout)

        self.bits_editor_layout = GridLayout(cols=3)

        self.ber_label = Label(text="QBER [%]")
        self.ber_value = Label(text="0")
        self.ber_slider = Slider(min=0, max=10, value=0, disabled=True)
        self.ber_slider.bind(value=self.on_ber_slider)

        self.choose_label = Label(text="BER TYPE")
        self.random_button = Button(text="RANDOM", disabled=True)
        self.random_button.bind(on_press=self.random_bits_create)
        self.block_button = Button(text="BLOCK", disabled=True)
        self.block_button.bind(on_press=self.block_bits_create)

        self.bits_editor_layout.add_widget(self.ber_label)
        self.bits_editor_layout.add_widget(self.ber_value)
        self.bits_editor_layout.add_widget(self.ber_slider)
        self.bits_editor_layout.add_widget(self.choose_label)
        self.bits_editor_layout.add_widget(self.random_button)
        self.bits_editor_layout.add_widget(self.block_button)

        self.add_widget(self.bits_editor_layout)

        self.bits_layout = GridLayout(cols=1, padding=5)
        self.bits_label_all = TextInput(text='111', disabled=False, cursor=(0, 0))
        self.bits_layout.add_widget(self.bits_label_all)
        self.add_widget(self.bits_layout)
        with self.bits_layout.canvas.before:
            Color(0, 0, 0, 1)

            self.rect = Rectangle(pos=self.bits_layout.pos, size=self.bits_layout.size)
        self.bits_layout.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def random_bits_create(self, instance):
        self.random_button.background_normal = instance.background_down
        self.block_button.background_normal = 'atlas://data/images/defaulttheme/button'
        self.bob.bits.type = 'random'
        self.bits_label_all.text = str(self.bob.bits.bits)

    def block_bits_create(self, instance):
        self.block_button.background_normal = instance.background_down
        self.random_button.background_normal = 'atlas://data/images/defaulttheme/button'
        self.bob.bits.type = 'block'
        self.bits_label_all.text = str(self.bob.bits.bits)

    def on_reset(self, instance):
        self.bob = bob_client.BobClient()
        self.n_value.text = str(self.bob.N)
        self.k_value.text = str(self.bob.K)
        self.l_value.text = str(self.bob.L)
        self.bits_len_value.text = str(self.bob.bits_length)
        self.bind_button.disabled = False
        self.read_config_button.disabled = True
        self.create_bits_button.disabled = True
        self.import_bits_button.disabled = True
        self.run_machine_button.disabled = True
        self.reset_button.disabled = True
        with self.bits_layout.canvas.before:
            Color(0, 0, 0, 1)
            self.bits_layout.canvas.before.remove(self.rect)
            self.rect = Rectangle(pos=self.bits_layout.pos, size=self.bits_layout.size)

        self.bits_layout.bind(pos=self.update_rect, size=self.update_rect)

    def on_import_bits(self, instance):
        path = filechooser.open_file(title="Pick a txt file..",
                                     filters=[("Text files", "*.txt")])[0]

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
                if self.bob.connected == True:
                    self.popup_window.dismiss()
                    return True
                else:
                    self.bind_button.disabled = False
                    self.read_config_button.disabled = True
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
        self.run_machine_button.disabled = False
        self.bob.create_random_bits()
        self.bits_label_all.text = str(self.bob.bits.bits)

    def on_run_machine(self, instance):
        self.bob.create_machine()
        self.show_run_popup()
        self.run_thread = threading.Thread(target=self.bob.run_TPM_machine)
        self.run_thread.daemon = True
        self.run_thread.start()
        close_popup_thread = threading.Thread(target=self.close_run_popup)
        close_popup_thread.daemon = True
        close_popup_thread.start()
        self.reset_button.disabled = False

    def close_run_popup(self):
        while True:
            if not self.run_thread.is_alive():
                self.popup_window.dismiss()
                self.bits_label_all.text = str(self.bob.bits.bits)
                if self.bob.success:
                    with self.bits_layout.canvas.before:
                        Color(0, 1, 0, 1)
                        self.bits_layout.canvas.before.remove(self.rect)
                        self.rect = Rectangle(pos=self.bits_layout.pos, size=self.bits_layout.size)
                else:
                    with self.bits_layout.canvas.before:
                        Color(1, 0, 0, 1)
                        self.bits_layout.canvas.before.remove(self.rect)
                        self.rect = Rectangle(pos=self.bits_layout.pos, size=self.bits_layout.size)
                self.bits_layout.bind(pos=self.update_rect, size=self.update_rect)
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
