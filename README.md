 |==================================================> DAMMY X11 TOOL

A 1-file Termux tool to Install, Start, Stop + Fully Uninstall XFCE Desktop with Termux-X11. 
No D-Bus spam. No ghost X11 left behind.

---

### **1. Requirements / What to Download First**

You need 2 things on Android before running:

1.  **Termux** from F-Droid  
    `Google Play version is outdated. Use F-Droid only.`  
    https://f-droid.org/packages/com.termux/

2.  **Termux:X11** APK from GitHub  
    This is the actual display server. The script will install the `termux-x11-nightly` package, but you still need the Android app.  
    https://github.com/termux/termux-x11/releases

Storage: ~800MB free for XFCE + deps.

---

### **2. Install & Run**

```bash
pkg update -y
pkg install python git -y
git clone https://github.com/princethuth/Dammy-xfce4-X11View.git
cd Dammy-xfce4-X11View
python Dammy-X11.py
