[app]
title = descargatube
package.name = descargatube
package.domain = org.morris
version = 1.1

# Icono — debe ser PNG para Android (convierte icon.ico a icon.png antes de compilar)
icon.filename = icon.png

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

# yt-dlp se instala como paquete Python puro; ffmpeg NO se incluye en Android
# porque no existe como binario del sistema. El postprocesamiento a MP3
# queda deshabilitado automáticamente en Android (ver main.py).
requirements = python3,kivy==2.3.0,yt-dlp

# Orientación
orientation = portrait

# ── Permisos Android ─────────────────────────────────────────────────────────
# Añadimos permisos de almacenamiento para intentar guardar en la carpeta pública "Download"
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# ── SDK / NDK ─────────────────────────────────────────────────────────────────
android.api = 33
android.minapi = 26
android.ndk = 25b
android.ndk_api = 26
fullscreen = 0

# Aceptar licencias automáticamente durante el build
android.accept_sdk_license = True

# Arquitecturas
android.archs = arm64-v8a,armeabi-v7a

# Rama de python-for-android (stable)
p4a.branch = master

# ── Opciones de build ─────────────────────────────────────────────────────────
[buildozer]
log_level = 2
warn_on_root = 1