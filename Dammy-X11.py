#!/usr/bin/env python3
import os
import sys
import signal
import time

PREFIX = "/data/data/com.termux/files/usr"
PID_FILE = os.path.expanduser("~/.x11.pid")
LAUNCHER = "startxfce.sh"

def show_banner():
    os.system("clear")
    banner = """
####################################################
# Encrypted by: Dammy-Tool                         #
# Whatsapp: +2349038303472                         #
# Github: https://github.com/Princethuth           #
####################################################

 █▀▀▀█▄   ▄▀▀▀█▄  █▄  ▄█  █▄  ▄█ ▀█  █▀
 █   █ █ █▀   ▀█  █▀▄▀▄█  █▀▄▀▄█   ▀█▀ 
 █   █ █ █▄▄▄▄▄█  █  █ █  █  █ █    █  
 █▄▄▄█▀  █     █  █    █  █    █    █  
 ▀▀▀▀    ▀     ▀  ▀    ▀  ▀    ▀    ▀  
       -= Auto Detect ToolName for the code. =-
"""
    print(banner)

def run(cmd): 
    os.system(cmd)

def kill_old():
    print("[*] Killing any old X11/XFCE/D-Bus instances...")
    run("pkill -9 startxfce4 2>/dev/null")
    run("pkill -9 termux-x11 2>/dev/null")
    run("pkill -9 dbus-launch 2>/dev/null")
    run("pkill -9 dbus-daemon 2>/dev/null")
    run(f"rm -rf {PREFIX}/tmp/.X11-unix {PREFIX}/tmp/runtime-* {PREFIX}/var/run/dbus/*")
    if os.path.exists(PID_FILE): 
        try: os.remove(PID_FILE)
        except: pass

def install_and_start():
    kill_old()
    
    print("[1/5] Update + Enable X11 repo first...")
    run("pkg update -y")
    run("pkg install -y x11-repo termux-services") 

    print("[2/5] Installing X11 + XFCE...")
    run("pkg install -y termux-x11-nightly xfce4 xfce4-session dbus")

    print("[3/5] Creating launcher script...")
    # NOTICE: We completely unset DBUS environment variables for the parent shell 
    # and keep it strictly contained inside this temporary script execution block.
    script = f"""#!/data/data/com.termux/files/usr/bin/zsh
export DISPLAY=:0
export NO_AT_BRIDGE=1
export XDG_RUNTIME_DIR={PREFIX}/tmp
mkdir -p {PREFIX}/tmp

if [ ! -f {PREFIX}/var/lib/dbus/machine-id ]; then
    dbus-uuidgen --ensure
fi

echo "[*] Starting X11 server on :0 ..."
termux-x11 :0 -ac &
echo $! > {PID_FILE}
sleep 2

echo ">>> IMPORTANT: Open the Termux:X11 app on your phone NOW <<<"
sleep 2

echo "[*] Launching D-Bus and XFCE internally..."
dbus-launch --exit-with-session startxfce4
"""
    with open(LAUNCHER, "w") as f: 
        f.write(script)
    run("chmod +x " + LAUNCHER)

    print("[4/5] Running launcher...")
    # Executing via a clean environment execution command to completely shield your main Termux shell
    run(f"env -u DBUS_SESSION_BUS_ADDRESS -u DISPLAY ./{LAUNCHER}")

def stop_and_uninstall():
    print("[+] Stopping + Full Cleanup...")
    kill_old()
    print("[+] Removing packages...")
    run("pkg uninstall -y xfce4 xfce4-session dbus termux-x11-nightly termux-services x11-repo")
    run("rm -f " + LAUNCHER)
    
    print("[+] Cleaning and resetting global environment variables...")
    # Scrub any accidental leaks out of system profiles completely
    run("sed -i '/DBUS_SESSION_BUS_ADDRESS/d' ~/.bashrc 2>/dev/null")
    run("sed -i '/DBUS_SESSION_BUS_ADDRESS/d' ~/.zshrc 2>/dev/null")
    run("sed -i '/DISPLAY/d' ~/.bashrc 2>/dev/null")
    run("sed -i '/DISPLAY/d' ~/.zshrc 2>/dev/null")
    
    # Completely strip live session values out of active process memory
    os.environ.pop("DBUS_SESSION_BUS_ADDRESS", None)
    os.environ.pop("DISPLAY", None)
    os.environ.pop("XDG_RUNTIME_DIR", None)
        
    print("[+] Termux environment restored to default safely.")

def main():
    # Instantly wipe environmental traces the second your script launches
    os.environ.pop("DBUS_SESSION_BUS_ADDRESS", None)
    os.environ.pop("DISPLAY", None)
    
    while True:
        show_banner()
        print("=== Termux XFCE Manager v4 ===")
        print("1. Install Deps + Start XFCE")
        print("2. Stop XFCE + Uninstall Everything")
        print("3. Exit")
        try:
            c = input("Select: ").strip()
            if c == "1": 
                install_and_start()
                input("\nPress Enter to return to menu...")
            elif c == "2": 
                if input("This will remove all X11/XFCE. Sure? y/N: ").lower() == "y": 
                    stop_and_uninstall()
                    input("\nPress Enter to return to menu...")
            elif c == "3": 
                print("Exiting tool. Goodbye!")
                break
            else:
                print("Invalid choice")
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            print("\nExiting tool.")
            break

if __name__ == "__main__":
    main()

