# ---------------------------------------------
# Info-Service on Raspberry Pi 
# OLED 128x64 
# IP, CPU, Temp, RAM, HDD - Info
# Draw CPU % graph
# AI: copilot
# Shell scripts for system monitoring from here:
# https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
# ---------------------------------------------

import time
import subprocess
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Initialize I2C
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Initialize OLED display (128x64 pixels)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c_bus, addr=0x3C)

# Use default PIL font
font = ImageFont.load_default()

# Graph settings
graph_width = 128
graph_height = 40
graph_y_offset = 44
values = [0] * graph_width

while True:
    # Read system information using shell commands

    # Get IP address
    IP = subprocess.check_output(
        "hostname -I | cut -d' ' -f1", shell=True
    ).decode().strip()

    # Get CPU load
    cpu_raw = subprocess.check_output(
        "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'", shell=True
    ).decode().strip()
    cpu_value = float(cpu_raw)

    # Get memory usage
    MemUsage = subprocess.check_output(
        "free -m | awk 'NR==2{printf \"%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'",
        shell=True
    ).decode().strip()

    # Get disk usage
    Disk = subprocess.check_output(
        "df -h | awk '$NF==\"/\"{printf \"%d/%dGB %s\", $3,$2,$5}'",
        shell=True
    ).decode().strip()

    # Get temperature
    temp = subprocess.check_output(
        "vcgencmd measure_temp | cut -d'=' -f2",
        shell=True
    ).decode().strip()

    # Update graph values
    values.pop(0)
    values.append(cpu_value)

    # Create image buffer
    image = Image.new("1", (display.width, display.height))
    draw = ImageDraw.Draw(image)

    # Text positions
    x = 0
    top = 0

    # Draw system info text
    draw.text((x, top), f"IP: {IP}", font=font, fill=255)
    draw.text((x, top + 10), f"CPU: {cpu_raw}  Temp: {temp}", font=font, fill=255)
    draw.text((x, top + 20), f"Mem: {MemUsage}", font=font, fill=255)
    draw.text((x, top + 30), f"Disk: {Disk}", font=font, fill=255)

    # Draw CPU graph
    max_val = max(values) if max(values) > 0 else 1
    for i, val in enumerate(values):
        y = int((val / max_val) * graph_height)
        draw.point((i, graph_y_offset + graph_height - y), fill=255)

    # Update display
    display.image(image)
    display.show()

    time.sleep(0.5)
