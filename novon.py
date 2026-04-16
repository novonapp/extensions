import os
import sys
import json
import subprocess
import shlex

# ANSI Color Codes (Novon Purple Theme)
CLR_P = "\033[38;5;135m"  # Primary Purple
CLR_P2 = "\033[38;5;93m"  # Deep Purple
CLR_P3 = "\033[38;5;171m" # Accent Purple
CLR_G = "\033[92m"        # Success Green
CLR_Y = "\033[93m"        # Warning Yellow
CLR_R = "\033[91m"        # Error Red
CLR_B = "\033[1m"         # Bold
CLR_0 = "\033[0m"         # Reset

LOGO = fr"""{CLR_P}{CLR_B}
  _   _  ______      ______  _   _ 
 | \ | |/ __ \ \    / / __ \| \ | |
 |  \| | |  | \ \  / / |  | |  \| |
 | . ` | |  | |\ \/ /| |  | | . ` |
 | |\  | |__| | \  / | |__| | |\  |
 |_| \_|\____/   \/   \____/|_| \_|
                                   
      EXTENSION MANAGEMENT SHELL
{CLR_0}"""

CONFIG_PATH = "novon_config.json"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

def show_help():
    print(f"\n{CLR_P}{CLR_B}Available Commands:{CLR_0}")
    print(f"  {CLR_P3}bundle{CLR_0}         Run the extension bundling process")
    print(f"  {CLR_P3}config{CLR_0}         View current project configuration")
    print(f"  {CLR_P3}set <key> <val>{CLR_0}   Change a setting (e.g. org_name or branch)")
    print(f"  {CLR_P3}list{CLR_0}           List detected extensions")
    print(f"  {CLR_P3}help{CLR_0}           Show this help message")
    print(f"  {CLR_P3}exit / quit{CLR_0}    Exit the Novon Shell")

def run_bundle(extra_args):
    if "--upgrade" not in extra_args and "--no-upgrade" not in extra_args:
        choice = input(f"{CLR_Y}? Do you want to automatically upgrade extension versions? (y/n): {CLR_0}").strip().lower()
        if choice == 'y':
            extra_args.append("--upgrade")
        else:
            extra_args.append("--no-upgrade")

    print(f"{CLR_P}[i] Starting Novon Bundler...{CLR_0}")
    cmd = [sys.executable, "bundle_extensions.py"] + extra_args
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    for line in process.stdout:
        print(line, end="")
    
    process.wait()
    if process.returncode == 0:
        print(f"\n{CLR_G}>>> Bundling completed successfully.{CLR_0}")
    else:
        print(f"\n{CLR_R}>>> Bundling failed with exit code {process.returncode}.{CLR_0}")

def show_config():
    config = load_config()
    print(f"{CLR_P}{CLR_B}Current Configuration:{CLR_0}")
    if not config:
        print(f"{CLR_Y}No config found. Run bundle to initialize.{CLR_0}")
        return
    for k, v in config.items():
        print(f"  {CLR_P3}{k:15}:{CLR_0} {v}")
    
    print(f"\n{CLR_B}Tip:{CLR_0} {CLR_P}org_name{CLR_0} can be your GitHub Organization or your personal Username.")

def set_config(key, value):
    config = load_config()
    if not config:
        print(f"{CLR_R}Error: Config file not found. Run bundle once to initialize.{CLR_0}")
        return
    
    if key not in config:
        print(f"{CLR_Y}Warning: Key '{key}' is not a standard config key.{CLR_0}")
    
    config[key] = value
    save_config(config)
    print(f"{CLR_G}Successfully set {key} to {value}{CLR_0}")

def list_extensions():
    extensions = [d for d in os.listdir(".") 
                 if os.path.isdir(d) and d.startswith("com.novon.")]
    print(f"{CLR_P}{CLR_B}Detected Extensions:{CLR_0}")
    for ext in extensions:
        print(f"  {CLR_P3}-{CLR_0} {ext}")

def handle_command(cmd_line):
    if not cmd_line.strip():
        return True

    try:
        parts = shlex.split(cmd_line)
    except ValueError as e:
        print(f"{CLR_R}Parsing error: {e}{CLR_0}")
        return True

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in ["exit", "quit", ":q"]:
        return False
    elif cmd == "bundle":
        run_bundle(args)
    elif cmd == "config":
        show_config()
    elif cmd == "set":
        if len(args) < 2:
            print(f"{CLR_R}Usage: set <key> <value>{CLR_0}")
        else:
            set_config(args[0], args[1])
    elif cmd == "list":
        list_extensions()
    elif cmd == "help":
        show_help()
    elif cmd == "clear" or cmd == "cls":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(LOGO)
    else:
        print(f"{CLR_R}Unknown command: {cmd}{CLR_0}")
        show_help()
    
    return True

def shell_mode():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(LOGO)
    print(f"{CLR_Y}Welcome back, Developer. Type 'help' for commands.{CLR_0}")
    
    while True:
        try:
            prompt = f"\n{CLR_P2}novon{CLR_0} {CLR_P3}>{CLR_0} "
            cmd_line = input(prompt).strip()
            if not handle_command(cmd_line):
                print(f"{CLR_P}Stay creative. Goodbye!{CLR_0}")
                break
        except EOFError:
            print(f"\n{CLR_P}Goodbye!{CLR_0}")
            break
        except KeyboardInterrupt:
            print(f"\n{CLR_Y}Use 'exit' to quit.{CLR_0}")

def main():
    # If arguments are passed, run in one-shot mode
    if len(sys.argv) > 1:
        cmd_line = " ".join(sys.argv[1:])
        handle_command(cmd_line)
    else:
        # Otherwise, enter interactive shell
        shell_mode()

if __name__ == "__main__":
    main()
