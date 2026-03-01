from tools.open_app import open_app
from tools.email import read_recent_emails, send_email
from tools.reminder import set_reminder, show_reminders
from llm_client import summarize_text
from tools.web_search import web_search

# FILE OPS
from tools.file_ops import (
    create_file,
    read_file,
    write_file,
    delete_file,
    create_folder,
    summarize_file
)

# SYSTEM CONTROL
from tools.system_control import (
    volume_up,
    volume_down,
    mute,
    unmute,   # ← ADDED
    brightness_up,
    brightness_down,
    screenshot,
    shutdown_pc,
    restart_pc,
    lock_screen
)


def execute_tool(tool_name, args):

    # ---------- OPEN APPS ----------
    if tool_name == "open_app":
        return open_app(**args)

    # ---------- EMAIL ----------
    elif tool_name == "read_recent_emails":
        return read_recent_emails(
            limit=args.get("limit", 5),
            summarize=args.get("summarize", False),
            llm=summarize_text
        )

    elif tool_name == "send_email":
        return send_email(**args)

    # ---------- REMINDERS ----------
    elif tool_name == "set_reminder":
        return set_reminder(
            task=args.get("task"),
            time=args.get("time")
        )

    elif tool_name == "show_reminders":
        return show_reminders()

    # ---------- CLOCK ----------
    elif tool_name in ["open_clock", "set_timer", "set_alarm", "start_stopwatch"]:
        return open_app(app_name="clock")

    # ---------- WEB SEARCH ----------
    elif tool_name == "web_search":
        return web_search(**args)

    # ---------- FILE OPS ----------
    elif tool_name == "create_file":
        return create_file(**args)

    elif tool_name == "read_file":
        return read_file(**args)

    elif tool_name == "write_file":
        return write_file(**args)

    elif tool_name == "delete_file":
        return delete_file(**args)

    elif tool_name == "create_folder":
        return create_folder(**args)

    elif tool_name == "summarize_file":
        return summarize_file(
            path=args.get("path"),
            llm=summarize_text
        )

    # ---------- SYSTEM CONTROL ----------
    elif tool_name == "volume_up":
        return volume_up()

    elif tool_name == "volume_down":
        return volume_down()

    elif tool_name == "mute":
        return mute()

    elif tool_name == "unmute":
        return unmute()

    elif tool_name == "brightness_up":
        return brightness_up()

    elif tool_name == "brightness_down":
        return brightness_down()

    elif tool_name == "screenshot":
        return screenshot()

    elif tool_name == "shutdown_pc":
        return shutdown_pc()

    elif tool_name == "restart_pc":
        return restart_pc()

    elif tool_name == "lock_screen":
        return lock_screen()

    return "Tool not found"