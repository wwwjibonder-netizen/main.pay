[app]
title = QR Face Attendance
package.name = qroutandface
package.domain = org.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,spec
version = 0.1
requirements = python3,kivy,opencv-python,pyzbar,requests,jpeg,png
orientation = portrait
osx.kivy_version = 2.1.0
fullscreen = 0
android.permissions = CAMERA, INTERNET
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = armeabi-v7a, arm64-v8a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
