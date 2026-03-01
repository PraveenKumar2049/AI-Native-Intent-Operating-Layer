DANGEROUS_TOOLS = [
    "shutdown_pc",
    "restart_pc",
    "delete_file",
    "send_email"
]

def requires_confirmation(tool_name):
    return tool_name in DANGEROUS_TOOLS