import subprocess


def open_app(app_name=None, name=None):
    if app_name:
        app = app_name.lower().strip()
    elif name:
        app = name.lower().strip()
    else:
        return "No app name provided."

    try:
        # ---------------- BASIC APPS ----------------
        if app == "notepad":
            subprocess.Popen("notepad")

        elif app == "calculator":
            subprocess.Popen("calc")

        elif app == "terminal":
            subprocess.Popen("start cmd", shell=True)

        elif app == "file explorer":
            subprocess.Popen("explorer")

        # ---------------- BROWSERS ----------------
        elif app == "chrome":
            subprocess.Popen("start chrome", shell=True)

        elif app == "firefox":
            subprocess.Popen("start firefox", shell=True)

        elif app == "brave":
            subprocess.Popen("start brave", shell=True)

        elif app == "edge" or app == "microsoft edge":
            subprocess.Popen("start msedge", shell=True)

        # ---------------- WINDOWS APPS ----------------
        elif app == "settings":
            subprocess.Popen("start ms-settings:", shell=True)

        elif app == "camera":
            subprocess.Popen("start microsoft.windows.camera:", shell=True)

        elif app == "clock":
            subprocess.Popen("start ms-clock:", shell=True)

        # ---------------- OFFICE APPS ----------------
        elif app == "word":
            subprocess.Popen("start winword", shell=True)

        elif app == "excel":
            subprocess.Popen("start excel", shell=True)

        elif app == "powerpoint":
            subprocess.Popen("start powerpnt", shell=True)

        elif app == "outlook":
            subprocess.Popen(
                r'start "" "C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"',
                shell=True
            )

        # ---------------- DEV ----------------
        elif app == "code" or app == "vscode":
            subprocess.Popen("start code", shell=True)

        # ---------------- WHATSAPP ----------------
        elif app == "whatsapp":
            subprocess.Popen(
                "start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
                shell=True
            )

        # ---------------- FALLBACK ----------------
        else:
            subprocess.Popen(f"start {app}", shell=True)

        return f"Opened {app}"

    except Exception as e:
        return f"Failed to open {app}: {e}"
