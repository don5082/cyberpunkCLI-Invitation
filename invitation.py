import itertools
import sys
import time
from logging import WARNING, error

from click import style
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.theme import Theme
from rich.align import Align
import pyfiglet

# ANSI escape codes (colors)

GREEN = "\033[32m"
MAIN_TEXT = "\033[38;2;117;174;155m"
TITLE_TEXT = "\033[38;2;48;140;135m"
BACKGROUND = "\033[38;2;14;16;37m"
WARNING_TEXT = "\033[38;2;191;0;53m"
RESET = "\033[0m"

TYPING_SPEED = 0.1

# Define a custom cyberpunk color palette
cyber_theme = Theme({
    "neon_green": "bold #00ff66",
    "neon_pink": "bold #ff007f",
    "neon_blue": "bold #00e5ff",
    "cyber_yellow": "bold #ffe600",
    "dim_gray": "dim white",
    "background": "bold #0e1025",
    "main_text": "bold #75ae9b",
    "title_text": "bold #308C87",
    "warning_text": "bold #bf0035"
})

valid_selections = ["whatisthenetwork", "cyberindex", "dog", "entries", "help"]


console = Console(theme=cyber_theme)

BANNER_TITLE = f""" {MAIN_TEXT}
 ██████  ██    ██ ████████  ████████ ████████  ████████  ██     ██ ██    ██ ██    ██ 
██    ██  ██  ██  ██     ██ ██       ██     ██ ██     ██ ██     ██ ███   ██ ██   ██ 
██         ████   ██     ██ ██       ██     ██ ██     ██ ██     ██ ████  ██ ██  ██   
██          ██    ████████  ██████   ████████  ████████  ██     ██ ██ ██ ██ █████    
██          ██    ██     ██ ██       ██   ██   ██        ██     ██ ██  ████ ██  ██   
██    ██    ██    ██     ██ ██       ██    ██  ██        ██     ██ ██   ███ ██   ██  
 ██████     ██    ████████  ████████ ██     ██ ██         ███████  ██    ██ ██    ██ 
{RESET}
"""

GLITCH_SEQ = ["█▓▒░░▒▓██▓▒░░░▒▒▓▓██████▓▓▒▒░░░▒▒▓▓████▓▓▒▒░░░░▒▒▓███▓▓▒▒░░░░▒▒▓▓██████▓▓▓██████▓▓▒▒░░░▒▒▓▓█████▓▓▒▒░░░░▒",
              "████▓▓▒▒░░▒▒▓▓████████████▓▓▒▒░░░░▒▒▓▓██████▓▓▒▒░░████▓▓▒▒░░░░▒▒▓▓█████░░▒▒▓▓██████▓▓▒▒░░░░▒▒▓▓█████████▓",
              "░░▒▒▓▓██████▓▓▒▒░░░░▒▒▓▓██████▓▓▒▒░░░░▒▒▓▓██████▓▓▒▒░▒▒▓▓██████▓▓▒▒░░░░▒▒▓▓████░▒▒▓▓██████▓▓▒▒░░░░▒▒▓▓███",
              "▓▓████████▓▓▒▒░░░░▒▒▓██████▓▓▒▒░░█████▓▓▒▒░░░░▒▒▓█████▓▓▒▒░░░░▒▒▓▓██████▓▓▒▒░░░░▒▒▓▓██████▓▓▒▒░░░░▒▒▓▓███",
              "▒░░░▒▒▓▓████▓▓▒▒░░░░▒▒▓▓██████▓▓▒▒░░░▒▒▓▓███░░░▒▒▓▓█████▓▓▒▒░░░░▒▒▓▓██░░░▒▒▓▓███████░░░▒▒▓▓█████▓▓▒▒░░███"]

FAKE_ERROR_STACKTRACE = [
    f"{WARNING_TEXT} CRITICAL SYSTEM FAULT: Cyberdeck Kernel Panic (Error Code 0x8004100E){RESET} \n",
    f"{MAIN_TEXT} Traceback (most recent neural link call):{RESET}\n",
    f"  File {TITLE_TEXT} \"/net/subroutines/security_gate.py\"{RESET} , line 142, in {MAIN_TEXT} verify_clearance{RESET} \n",
    f"    auth_token = cipher.decrypt(user_input, key=NETWORK_KEY)\n",
    f"  File {TITLE_TEXT} \"/net/crypto/cipher_suite.py\"{RESET} , line 88, in {MAIN_TEXT} decrypt{RESET} \n",
    f"    raise DecryptionError(\"Payload signature corrupted during transmission\")\n",
    f"{WARNING_TEXT} DecryptionError{RESET} : Payload signature mismatch or missing neural token.\n",
    f"  File {TITLE_TEXT} \"/kernel/neural_link.py\"{RESET} , line 301, in {MAIN_TEXT} jack_in{RESET} \n",
    f"    sys.hardware_bus.pulse(voltage=120, target=\"cortex_implants\")\n",
    f"{WARNING_TEXT} HardwareFault{RESET} : Overvoltage spike detected in optic interface.\n",
    f"{WARNING_TEXT} [!] EMERGENCY DUMP WRITTEN TO /var/log/ice_breach.dmp{RESET} \n",
    f"{MAIN_TEXT} [SYS_OVERRIDE] Process crashed with {RESET}{WARNING_TEXT}error{RESET}{MAIN_TEXT} code {RESET}{TITLE_TEXT}1{RESET}{MAIN_TEXT} ...{RESET} \n\n"
]


def apply_block_gradient(text: str, font: str = "block") -> str:
    # Generate standard block ASCII text
    raw_art = pyfiglet.figlet_format(text, font=font)

    # Map solid borders and blocks to your custom cyberpunk block characters
    gradient_art = (
        raw_art.replace("█", "█")
        .replace("#", "█")
    )
    return gradient_art

def glitch_animation(glitch_time, delay=0.05):
    start = time.perf_counter()
    time_elapsed = -1

    glitch = itertools.cycle(GLITCH_SEQ)

    while time_elapsed < glitch_time:
        sys.stdout.write(f"\r\033[K{GREEN}{next(glitch)}   {RESET}")
        sys.stdout.flush()
        time.sleep(delay)
        now = time.perf_counter()
        time_elapsed = now - start
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()

def load_animation(loading_time, style="neon_green", delay=0.08):
    start = time.perf_counter()
    spinner = itertools.cycle(['⠁⠀⠀', '⠉⠀⠀', '⠉⠁⠀', '⠉⠉⠀', '⠈⠉⠁', '⠀⠉⠉', '⠀⠈⠙', '⠀⠀⠛', '⠀⠐⠚', '⠀⠒⠒', '⠐⠒⠂', '⠰⠒⠀',
                               '⠰⠆⠀', '⠰⠤⠀', '⠠⠤⠄', '⠀⠤⠤', '⠀⠠⢤', '⠀⠀⣤', '⠀⢀⣠', '⠀⣀⣀', '⢀⣀⡀', '⣀⣀⠀', '⣄⡀⠀', '⣆⠀⠀', '⡇⠀⠀',
                               '⡧⠀⠀', '⡷⠀⠀', '⣕⠄⠀', '⢷⠄⠀', '⡾⠠⠀', '⡥⢑⠄', '⢃⡪⠡', '⢊⡲⠡', '⢄⠬⠲', '⠡⢈⠔', '⠢⠠⠠', '⠀⠐⡀', '⠀⠀⢀'])
    time_elapsed = -1

    while time_elapsed < loading_time:
        sys.stdout.write(f"\r\033[K{GREEN}{next(spinner)}   {RESET}")
        sys.stdout.flush()
        time.sleep(delay)
        now = time.perf_counter()
        time_elapsed = now - start
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()

def boot_animation(text, style="main_text", delay=0.01, newline=True):
    """Simulates a typing terminal effect."""
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(delay)
    if newline:
        console.print()

def write_error():
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    for string in FAKE_ERROR_STACKTRACE:
        sys.stdout.write(string)
        sys.stdout.flush()
    time.sleep(1)

def erase_text(char_count, delay=0.03):
    """Simulates backspacing characters out one by one."""
    for _ in range(char_count):
        sys.stdout.write("\b \b")
        sys.stdout.flush()
        time.sleep(delay)

def main():
    console.clear()

    # Boot sequence animation

    time.sleep(1)

    boot_animation("[SYS_INIT] Establishing secure link...", style="dim_gray")
    load_animation(1, style="dim_gray")
    time.sleep(1)
    boot_animation("[ACCESS GRANTED] Decrypting event payload...", style="neon_blue")
    time.sleep(1)
    boot_animation("Please enter your alias: ")
    name = input()

    boot_animation(f"Hello {name}. \n\nType 'help' to see a list of commands")

    answer = input()

    wrong_answer_allowance = 3

    while wrong_answer_allowance > 0:
        if wrong_answer_allowance != 3:
            boot_animation(f"\nType 'help' to see a list of commands")
            answer = input()

        if answer.lower().strip() == 'help':
            boot_animation("""Available commands: \n
          \twhatisthenetwork    - tells you more about what the Network is\n
          \tcyberindex         - get the cyber crime live status\n
          \tdog                 - try and find out\n
          \tentries             - get all article entries\n
          \thelp                - this command, displays all current commands\n
          """, delay=.005)
            selection = input()
            while not selection.lower().strip() in valid_selections:
                boot_animation(f"{selection} is not a valid selection, {name}")
                selection = input()
            boot_animation(f"fetching {selection}")
            load_animation(3)
            break

        else:
            wrong_answer_allowance -= 1
            if wrong_answer_allowance == 2:
                boot_animation(f"That was not a valid entry.")
                boot_animation(f"Do not fail this task again.", style="warning_text")
            elif wrong_answer_allowance == 1:
                boot_animation(f"INCORRECT. THIS IS YOUR FINAL WARNING", style="warning_text")
            elif wrong_answer_allowance == 0:
                boot_animation(f"Your inadherance is a threat to the network. Do not resist.")
                boot_animation("TERMINATION", style="warning_text")
                boot_animation("commencing immediately.")
                # print_eye()
                input("DISCONNECTED: press enter to close window...")
                quit()



    glitch_animation(2.5)
    write_error()

    time.sleep(5)
    load_animation(3)

    boot_animation("Are you afraid of ", style="main_text", delay=TYPING_SPEED, newline=False)
    boot_animation("ARTIFICIAL INTELLIGENCE ", style="warning_text", delay=TYPING_SPEED, newline=False)
    boot_animation("taking over the world?\n", delay=TYPING_SPEED)
    ominous_txt = "You have to be"
    time.sleep(1)
    load_animation(2)
    boot_animation(ominous_txt, newline=False, delay=TYPING_SPEED)
    time.sleep(.5)
    erase_text(len(ominous_txt), delay=0.03)
    boot_animation("You don't have to be", delay=TYPING_SPEED)
    time.sleep(1)
    boot_animation(":)", delay=TYPING_SPEED * 2)
    time.sleep(1)


    # ASCII Header
    # console.print(apply_block_gradient("CyberPunk", font='banner3'), style="title_text")
    sys.stdout.write(BANNER_TITLE)
    sys.stdout.flush()

    boot_animation("\t TALK TO CREATIVES,\n")
    boot_animation("\t ARTIST, AND \t WRITERS ABOUT \t\t THE ", newline=False)
    boot_animation("END OF THE WORLD\n", style="warning_text")
    boot_animation("\t 3121 16TH ST, SAN FRANCISCO, CA 94103\n\n\t APRIL 4, 2027\n\t\t AT 7:00 PM\n\n")
    time.sleep(3)
    load_animation(3)
    boot_animation(" We will see you there", delay=TYPING_SPEED)

    # Event Details Box
    # invite_details = (
    #     "[neon_blue]LOCATION:[/] The Underdeck Club (Sector 7G)\n"
    #     "[neon_blue]DATE/TIME:[/] Saturday, Nov 14 @ 22:00 HRS\n"
    #     "[neon_blue]DRESS CODE:[/] Techwear / Neon / Cyperpunk\n"
    #     "[neon_blue]NETWORK KEY:[/] 0x8F92-CYBER-PARTY\n\n"
    #     "[cyber_yellow]MISSION:[/] Synthwave beats, neural-link gaming, and specialized drinks."
    # )
    #
    # panel = Panel(
    #     invite_details,
    #     title="[neon_green]⚡ EXCLUSIVE ACCESS PERMIT ⚡[/neon_green]",
    #     subtitle="[dim_gray]DO NOT TRANSMIT OUTSIDE THE NETWORK[/dim_gray]",
    #     border_style="cyber_yellow",
    #     padding=(1, 2)
    # )
    # console.print(panel)
    # console.print()
    #
    # # Interactive RSVP
    # rsvp = Prompt.ask(
    #     "[neon_green]Will you jack into the event network?[/neon_green]",
    #     choices=["yes", "no", "maybe"],
    #     default="yes"
    # )
    #
    # if rsvp == "yes":
    #     alias = Prompt.ask("[neon_blue]Enter your handle/alias[/neon_blue]")
    #     console.print(f"\n[neon_green]✓ ACCESS CONFIRMED. Coordinates locked for Agent {alias}.[/neon_green]\n")
    # elif rsvp == "maybe":
    #     console.print("\n[cyber_yellow]⚠ STATUS PENDING. Signal locked until further update.[/cyber_yellow]\n")
    # else:
    #     console.print("\n[neon_pink]✖ ACCESS DENIED. Terminal self-destructing... (Just kidding!).[/neon_pink]\n")
    #
    input("Press Enter to disconnect and delete your device trace...")


if __name__ == "__main__":
    main()