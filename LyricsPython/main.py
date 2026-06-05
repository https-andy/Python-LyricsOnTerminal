import time

import pylrc
import sounddevice as sd
import soundfile as sf

from pyfiglet import Figlet
from rich.live import Live
from rich.panel import Panel
from rich.box import DOUBLE

# =====================
# CONFIG
# =====================

AUDIO_FILE = "payphone.wav"
LYRICS_FILE = "letra.lrc"

TYPE_SPEED = 0.1

# =====================
# LETRA
# =====================

with open(LYRICS_FILE, "r", encoding="utf-8") as f:
    lyrics = pylrc.parse(f.read())

# =====================
# AUDIO
# =====================

data, fs = sf.read(AUDIO_FILE)

# =====================
# ASCII FONT
# =====================

figlet = Figlet(font="small")

# =====================
# REPRODUCCIÓN
# =====================

sd.play(data, fs)

start_time = time.time()

history = []

with Live(
    refresh_per_second=30,
    screen=False,
) as live:

    for line in lyrics:

        while time.time() - start_time < line.time:
            time.sleep(1.5)

        current = ""

        for char in line.text:

            current += char

            # ASCII DEL TEXTO ACTUAL
            ascii_text = figlet.renderText(current)

            content = ""

            # ASCII GIGANTE CON EFECTO MÁQUINA
            content += f"[hot_pink]{ascii_text}[/hot_pink]\n"

            # HISTORIAL DE VERSOS
            if history:

                content += "\n"

                for previous in history[-3:]:
                    content += f"{previous}\n"

            content += f"\n[bold white]{current}█[/bold white]"

            live.update(
                Panel(
                    content,
                    border_style="hot_pink",
                    box=DOUBLE
                )
            )

            time.sleep(TYPE_SPEED)

        history.append(line.text)

if line == lyrics[-1]:
    time.sleep(5)

sd.wait()