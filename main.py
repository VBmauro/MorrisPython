import threading
import os

import yt_dlp

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.animation import Animation

# ── Fondo ─────────────────────────────────────────────
Window.clearcolor = (0.10, 0.10, 0.13, 1)

# ── Directorio descarga ──────────────────────────────
if platform == "android":
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path, app_storage_path

    request_permissions([
        Permission.INTERNET,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])

    try:
        BASE_DIR = os.path.join(primary_external_storage_path(), "Download", "DescargaTube")
    except:
        BASE_DIR = os.path.join(app_storage_path(), "DescargaTube")
else:
    BASE_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "DescargaTube")

os.makedirs(BASE_DIR, exist_ok=True)

# ── Logger ───────────────────────────────────────────
class YDL_Logger:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(msg)


class DownloaderUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        self._downloading = False
        self.format = None

        # ── Título ─────────────────────────────
        self.title = Label(
            text="Descarga Tube PRO",
            font_size=28,
            bold=True,
            size_hint=(1, .12)
        )
        self.add_widget(self.title)

        # ── Input ──────────────────────────────
        self.url_input = TextInput(
            hint_text="Pega enlace de YouTube, Facebook, TikTok o Instagram",
            multiline=False,
            size_hint=(1, .12),
            background_color=(0.2,0.2,0.25,1),
            foreground_color=(1,1,1,1)
        )
        self.add_widget(self.url_input)

        # ── Botones PEGAR / LIMPIAR ───────────
        top_buttons = BoxLayout(size_hint=(1,.10), spacing=10)

        self.btn_paste = Button(text="PEGAR")
        self.btn_paste.bind(on_press=self.paste_link)

        self.btn_clear = Button(text="LIMPIAR")
        self.btn_clear.bind(on_press=self.clear_link)

        top_buttons.add_widget(self.btn_paste)
        top_buttons.add_widget(self.btn_clear)
        self.add_widget(top_buttons)

        # ── Iconos ────────────────────────────
        icons_layout = BoxLayout(size_hint=(1,.15), spacing=15)

        icons_layout.add_widget(Image(source="youtube.png"))
        icons_layout.add_widget(Image(source="facebook.png"))
        icons_layout.add_widget(Image(source="tiktok.png"))
        icons_layout.add_widget(Image(source="instagram.png"))

        self.add_widget(icons_layout)

        # ── Formato ───────────────────────────
        fmt_layout = BoxLayout(size_hint=(1,.12), spacing=10)

        self.btn_mp4 = Button(text="MP4 Video")
        self.btn_mp4.bind(on_press=self.select_mp4)

        self.btn_mp3 = Button(text="Audio")
        self.btn_mp3.bind(on_press=self.select_mp3)

        fmt_layout.add_widget(self.btn_mp4)
        fmt_layout.add_widget(self.btn_mp3)
        self.add_widget(fmt_layout)

        # ── Botón DESCARGAR GRANDE ────────────
        self.btn_download = Button(
            text="DESCARGAR",
            size_hint=(1,.16),
            font_size=26,
            bold=True,
            background_color=(0.1,0.65,0.3,1)
        )
        self.btn_download.bind(on_press=self.start_download)
        self.add_widget(self.btn_download)

        # ── Progreso ──────────────────────────
        self.progress = ProgressBar(max=100, value=0, size_hint=(1,.08))
        self.add_widget(self.progress)

        # ── Estado ────────────────────────────
        self.status = Label(text="Esperando enlace...", size_hint=(1,.12))
        self.add_widget(self.status)

        # ── Firma ─────────────────────────────
        self.signature = Label(
            text="By Morris",
            size_hint=(1,.07),
            color=(1,0.3,0.3,1)
        )
        self.add_widget(self.signature)

    # ── Funciones UI ────────────────────────
    def paste_link(self, instance):
        from kivy.core.clipboard import Clipboard
        self.url_input.text = Clipboard.paste()

    def clear_link(self, instance):
        self.url_input.text = ""
        self._set_status("Campo limpiado")

    def select_mp4(self, instance):
        self.format = "mp4"
        self._animate_button(instance)
        self._set_status("Formato MP4 seleccionado")

    def select_mp3(self, instance):
        self.format = "mp3"
        self._animate_button(instance)
        self._set_status("Formato Audio seleccionado")

    def start_download(self, instance):
        if self._downloading:
            return

        url = self.url_input.text.strip()
        if not url or not self.format:
            self._set_status("Falta enlace o formato")
            return

        self._downloading = True
        self.btn_download.disabled = True
        self.progress.value = 0
        self._set_status("Iniciando descarga...")

        threading.Thread(
            target=self._download_media,
            args=(url,self.format),
            daemon=True
        ).start()

    # ── MOTOR DE DESCARGA (NO TOCADO) ───────
    def _download_media(self, url, format_type):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(BASE_DIR, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'logger': YDL_Logger(),
                'retries': 5
            }

            if format_type == "mp4":
                ydl_opts['format'] = 'best'
            else:
                ydl_opts['format'] = 'bestaudio/best'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except Exception as e:
            Clock.schedule_once(lambda dt: self._set_status(f"Error: {str(e)[:80]}"))
        finally:
            Clock.schedule_once(lambda dt: self._unlock_ui())

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes',0)
            if total:
                pct = downloaded/total*100
                Clock.schedule_once(lambda dt:self._update_progress(pct))
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt:self._finish_download())

    def _update_progress(self,pct):
        self.progress.value = pct
        self._set_status(f"Descargando {int(pct)}%")

    def _finish_download(self):
        self.progress.value = 100
        self._set_status("Descarga completada")

    def _unlock_ui(self):
        self._downloading=False
        self.btn_download.disabled=False

    def _set_status(self,text):
        self.status.text=text

    def _animate_button(self, btn):
        anim = Animation(size_hint=(1.1,1.1), duration=0.1) + Animation(size_hint=(1,1), duration=0.1)
        anim.start(btn)


class DownloaderApp(App):
    def build(self):
        self.title="Descarga Tube PRO"
        return DownloaderUI()


if __name__=="__main__":
    DownloaderApp().run()