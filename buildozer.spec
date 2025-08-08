[app]

# (str) Title of your application
title = RSS Reader

# (str) Package name (no spaces or special chars)
package.name = rssreader

# (str) Package domain (needed for android/ios packaging)
package.domain = org.yourname

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy

# (str) Application version
version = 0.1

# (int) Target Android API
android.api = 33

# (int) Minimum API your app will support
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 25b

# (str) Build Tools version
android.build_tools = 33.0.2

# (str) SDK path (must match GitHub Actions workflow)
android.sdk_path = ~/.buildozer/android/platform/android-sdk

# (str) NDK path (must match GitHub Actions workflow)
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0
