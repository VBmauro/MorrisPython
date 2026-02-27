📥 Descarga Tube PRO

Descarga Tube PRO es una aplicación desarrollada con Python + Kivy + yt-dlp que permite descargar contenido multimedia desde:

✅ YouTube

✅ Facebook

✅ TikTok

✅ Instagram

La aplicación ofrece una interfaz gráfica sencilla y moderna para pegar enlaces, seleccionar formato y descargar archivos directamente en el dispositivo.

🚀 Funcionalidades

📋 Botón para pegar enlaces desde el portapapeles.

🧹 Botón para limpiar el campo del enlace.

🎬 Descarga en formato MP4 (video).

🎵 Descarga en formato Audio.

📊 Barra de progreso en tiempo real.

📱 Compatible con Android (APK) y escritorio (Linux / Windows).

🎨 Interfaz moderna con iconos de plataformas.

🛡️ Prevención de múltiples descargas simultáneas.

📂 Archivos guardados automáticamente en una carpeta dedicada.

📂 Ubicación de descargas

Los archivos se guardan en:

En Android:
/storage/emulated/0/Download/DescargaTube
En PC (Linux / Windows):
~/Downloads/DescargaTube

La carpeta se crea automáticamente si no existe.

🛠️ Tecnologías utilizadas

Python 3

Kivy (interfaz gráfica)

yt-dlp (motor de descarga)

Buildozer (para generar APK en Android)

📁 Estructura del proyecto
DescargaTube/
│
├── main.py
├── buildozer.spec
├── youtube.png
├── facebook.png
├── tiktok.png
├── instagram.png
└── README.md
▶️ Uso de la aplicación

Abre la aplicación.

Pega el enlace del video (YouTube, Facebook, TikTok o Instagram).

Selecciona el formato:

🎬 MP4 (Video)

🎵 Audio

Presiona el botón ⬇ DESCARGAR.

Observa el progreso en pantalla.

El archivo se guardará automáticamente en la carpeta DescargaTube.

⚠️ Notas importantes

La aplicación utiliza la librería yt-dlp para gestionar las descargas.

No se modifica el motor interno de descarga al cambiar la interfaz gráfica.

Es responsabilidad del usuario descargar únicamente contenido permitido por las políticas de cada plataforma.

La aplicación no almacena información personal ni realiza seguimiento del usuario.

📦 Compilación APK (Android)

Requisitos:

Linux

Python 3

Buildozer

Android SDK / NDK

Comando para compilar:

buildozer android debug

El APK se generará en la carpeta:

bin/
🧑‍💻 Autor

Desarrollado por:
Morris 😎
Proyecto educativo y personal.

📜 Licencia

Este proyecto se distribuye con fines educativos.
El uso de la aplicación debe respetar las políticas de uso de cada plataforma (YouTube, Facebook, TikTok, Instagram).
