# Read all joystick events to console
#!/usr/bin/env python3
import struct
import sys

DEVICE = "/dev/input/js0"

EVENT_FORMAT = "IhBB"   # uint32 time, int16 value, uint8 type, uint8 number
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

JS_EVENT_BUTTON = 0x01
JS_EVENT_AXIS   = 0x02
JS_EVENT_INIT   = 0x80

def main():
    print(f"Opening joystick device: {DEVICE}")

    try:
        js = open(DEVICE, "rb")
    except FileNotFoundError:
        print("Error: Joystick not found!")
        sys.exit(1)

    print("Joystick opened successfully.\n")
    print("Reading events...\n")

    while True:
        event = js.read(EVENT_SIZE)
        if not event:
            continue

        time_ms, value, event_type, number = struct.unpack(EVENT_FORMAT, event)

        # Ignore initialization events
        if event_type & JS_EVENT_INIT:
            continue

        # Axis movement
        if event_type & JS_EVENT_AXIS:
            print(f"[AXIS]   Axis {number} = {value}")

        # Button press/release
        elif event_type & JS_EVENT_BUTTON:
            state = "PRESSED" if value else "RELEASED"
            print(f"[BUTTON] Button {number} {state}")

if __name__ == "__main__":
    main()
