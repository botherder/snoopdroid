Snoopdroid
==========

Snoopdroid is a simple utility to automate the process of extracting installed apps from an Android phone using the [Android Debug Bridge](https://developer.android.com/studio/command-line/adb). Optionally, Snoopdroid is able to lookup the extracted packages on various online services in order to attempt to immediately recognize any known malicious apps.

<p align="center"><img src="/img/snoopdroid.png?raw=true"/></p>

Installation on Debian GNU/Linux
--------------------------------

In order to run Snoopdroid on Debian you will need to install the following dependencies:

```
apt install python3 python3-pip python3-dev build-essential libssl-dev libffi-dev swig android-sdk-platform-tools
```

Make sure to generate your adb keys with:

```
adb keygen ~/.android/adbkey
```

You can then install Snoopdroid with pip3:

```
pip3 install rsa
pip3 install snoopdroid
```

Installation on Mac
-------------------

Running Snoopdroid on Mac requires Xcode and [homebrew](https://brew.sh) to be installed.

In order to install adb and other dependencies use:

```
brew install openssl swig libusb python3
brew install homebrew/cask/android-platform-tools
```

Make sure to generate your adb keys:

```
mkdir $HOME/.android
adb keygen $HOME/.android/adbkey
adb pubkey $HOME/.android/adbkey > $HOME/.android/adbkey.pub
```

You can now install Snoopdroid with pip3:

```
pip3 install rsa
pip3 install snoopdroid
```

How to use
----------

In order to use Snoopdroid you need to connect your Android device to your computer. You will then need to [enable USB debugging](https://developer.android.com/studio/debug/dev-options#enable) on the Android device.

If this is the first time you connect to this device, you will need to approve the authentication keys through a prompt that will appear on your Android device.

You can now launch Snoopdroid simply with `snoopdroid`. At each run, Snoopdroid will generate a new acquisition folder containing all the extracted APKs in the current working directory. You can change the base folder using:

```
snoopdroid --storage /path/to/folder
```

Optionally, you can decide to enable lookups of the SHA256 hash of all the extracted APKs on [VirusTotal](https://www.virustotal.com) and/or [Koodous](https://www.koodous.com). While these lookups do not provide any conclusive assessment on all of the extracted APKs, they might highlight any known malicious ones.

```
snoopdroid --virustotal
snoopdroid --koodous
```

Or, to launch all available lookups:

```
snoopdroid --all
```
