[app]

title = RSS Reader
package.name = rssreader
package.domain = org.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Add these requirements:
requirements = python3,kivy,kivymd,feedparser,beautifulsoup4,pyjnius==1.6.1

version = 0.1

android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools = 33.0.2

android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b

orientation = portrait
fullscreen = 0

# Permissions needed for notifications and internet access
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,VIBRATE

# (Optional) Enable AndroidX support (recommended)
android.enable_androidx = True
android.enable_jetifier = True
