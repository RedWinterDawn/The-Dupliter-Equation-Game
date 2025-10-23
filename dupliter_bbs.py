#!/usr/bin/env python3
"""
dupliter_bbs.py
Retro BBS-style terminal program for exploring the Dupliter hypothesis.
Author: Ashlan Chidester
Purpose: Educational / exploratory // interactive terminal experience Dupliter Stability Index (DSI).
"""

import math
import time
import shutil
import random
import sys

# ANSI color helpers (256-color support)
CSI = "\033["
RESET = CSI + "0m"
BOLD = CSI + "1m"

def fg(code): return f"{CSI}38;5;{code}m"

def clear():
    print(CSI + "2J" + CSI + "H", end="")

def slow_print(text, delay=0.006):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

# ASCII art: stylized Jupiter (keeps single/double quote sequences short to avoid quoting collisions)
JUPITER = r"""
                 .-''-.
              .-'  .---.  `-.
             /   .'     `.   \
            /   /  .-"-.-. \   \
           ;   ;  /  .-.  \;    ;
           |   | |  /   \  ||   |
           ;   ; | | .-. | ;'   ;
            \   \ \ `-' / /   /
             `.  `.```.'  .' .'
               `-._`---'_.-'
                    `---'
"""

BANNER = [
    f"{fg(220)}{BOLD}   ____  _   _  _     _ _ _  _   _  ___  _   _  _____{RESET}",
    f"{fg(220)}{BOLD}  |  _ \\| | | || |   (_) | \\| | | |/ _ \\| \\ | ||_   _|{RESET}",
    f"{fg(220)}{BOLD}  | | | | |_| || |    _| | .` | | | | | |  \\| |  | |  {RESET}",
    f"{fg(220)}{BOLD}  | |_| |  _  || |___| | | |\\  |_| | |_| | |\\  |  | |  {RESET}",
    f"{fg(220)}{BOLD}  |____/|_| |_||_____|_|_|_| \\_(_) |\\___/|_| \\_|  |_|  {RESET}",
]

INTRO = (
    "Connecting to DUPliter Node... BBS handshake engaged.\n"
    "Transmitting the Dupliter hypothesis — a gravitational temporal anchor.\n"
    "This simulator computes the relativistic/classical KE ratio and a pedagogical\n"
    "Dupliter Stability Index (DSI) that mixes relativistic scaling with toy\n"
    "environmental parameters: dark-matter potential and gravitational anchor strength.\n\n"
    "Note: DSI is a comparative, educational metric. Play, learn,\n"
    "and refine models responsibly.\n"
)

def headline(text):
    cols = shutil.get_terminal_size((80,20)).columns
    print(fg(81) + BOLD + text.center(cols) + RESET)

def prompt_float(prompt, default=None, minval=None, maxval=None):
    while True:
        raw = input(fg(250) + prompt + RESET + " ").strip()
        if raw == "" and default is not None:
            try:
                return float(default)
            except ValueError:
                pass
        try:
            val = float(raw)
        except ValueError:
            print(fg(208) + "Please enter a valid number (e.g., 0.1 or 0.9999)." + RESET)
            continue
        if (minval is not None and val < minval):
            print(fg(196) + f"Value too small (minimum {minval})." + RESET)
            continue
        if (maxval is not None and val > maxval):
            print(fg(196) + f"Value too large (maximum {maxval})." + RESET)
            continue
        return val

def relativistic_to_classical_ratio(beta):
    """
    Implements:
      ratio = 2*(1/sqrt(1-beta^2) - 1) / beta^2
    where beta = v/c (fraction of light speed).
    """
    if beta <= 0:
        return 0.0
    if beta >= 1:
        return float('inf')
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    numerator = 2.0 * (gamma - 1.0)
    denominator = beta * beta
    return numerator / denominator

def dupliter_stability_index(ratio, dm_factor, anchor_strength, noise=0.01):
    """
    Heuristic DSI:
      - compresses ratio via log10 to keep numeric range manageable
      - weights DM and anchor contributions
      - normalizes into a 0..100-ish scale (toy model)
    """
    r = max(ratio, 1e-12)
    log_r = math.log10(r + 1.0)
    base = (log_r * 0.6) + (math.log10(dm_factor + 1.0) * 0.25) + (math.log10(anchor_strength + 1.0) * 0.15)
    dsi = (base / (math.log10(1e6 + 1))) * 100.0
    dsi *= (1.0 + random.uniform(-noise, noise))
    return max(dsi, 0.0)

def verdict(dsi):
    if dsi >= 60:
        return ("High", fg(82) + BOLD + "Plausible Dupliter regime — strong anchor." + RESET)
    if dsi >= 30:
        return ("Moderate", fg(226) + "Marginal potential — further refinement needed." + RESET)
    if dsi > 0:
        return ("Low", fg(208) + "Unstable — insufficient parameters." + RESET)
    return ("None", fg(196) + "No Dupliter potential detected." + RESET)

def main():
    clear()
    for line in BANNER:
        print(line)
    print(fg(244) + JUPITER + RESET)
    slow_print(INTRO, delay=0.004)
    headline("DUPliter INTERACTIVE TERMINAL")
    print()

    while True:
        print(fg(153) + BOLD + "Enter parameters for an exploratory simulation (defaults provided):" + RESET)
        beta = prompt_float("Fractional velocity (v/c), 0..0.9999 (example 0.1):", default="0.1", minval=0.0, maxval=0.9999)
        dm = prompt_float("Dark-matter potential factor (dimensionless, suggested 0..10):", default="1.0", minval=0.0, maxval=1e6)
        anchor = prompt_float("Gravitational anchor strength (dimensionless, suggested 0..10):", default="1.0", minval=0.0, maxval=1e6)
        print()

        ratio = relativistic_to_classical_ratio(beta)
        dsi = dupliter_stability_index(ratio, dm, anchor)
        level, message = verdict(dsi)

        print(fg(39) + BOLD + "Computed metrics:" + RESET)
        print(f"  Relativistic / Classical KE ratio: {fg(153)}{ratio:.6g}{RESET}")
        print(f"  Dupliter Stability Index (DSI): {fg(153)}{dsi:.4f}{RESET}  — {level}")
        print("  Assessment:", message)
        print()
        print(fg(244) + "Equation used:  2*(1/√(1-β²) - 1) / β²   (β = v/c)" + RESET)
        print()

        again = input(fg(250) + "Run another simulation? (Y/n): " + RESET).strip().lower()
        if again in ("n", "no"):
            print(fg(245) + "Disconnecting from DUPliter Node. Keep hypothesizing." + RESET)
            break
        print("\n" + "-" * shutil.get_terminal_size((80,20)).columns + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + fg(245) + "Session terminated. Stay curious." + RESET)
        try:
            sys.exit(0)
        except SystemExit:
            pass

