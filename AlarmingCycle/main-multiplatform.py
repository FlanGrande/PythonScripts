import os
import time
import platform

import classes.config as config

def play_sound(sound_path):
    """
    A small helper function to play sound in a platform-dependent way.
    For Windows, uses 'start' (which will open the default media player).
    For other OSes, uses 'pw-play'.
    """
    # If no sound file is specified, return
    if not sound_path:
        return

    system_name = platform.system()

    if system_name == "Windows":
        # /B option prevents creating a new window
        # The extra "" right after /B is a quirk to avoid confusion between
        # title parameter and file path in the start command
        os.system(f'start /B "" "{sound_path}"')
    else:
        # For Linux (and possibly macOS if you have pw-play installed), do:
        os.system(f'pw-play "{sound_path}"')

def cyclic_alarm(on_duration, off_duration, cycles):
    cycling = True
    current_cycle = 0

    while cycling:
        current_cycle += 1

        print(f"Cycle {current_cycle}: ON for {on_duration} seconds.")
        play_sound(config.get_config_value("on_soundfx_path", ""))  # Start of "on" state
        time.sleep(int(on_duration))

        print(f"Cycle {current_cycle}: OFF for {off_duration} seconds.")
        play_sound(config.get_config_value("off_soundfx_path", ""))  # Start of "off" state
        time.sleep(int(off_duration))

        if current_cycle == int(cycles):
            break

    print("Alarm cycles complete!")
    play_sound(config.get_config_value("end_soundfx_path", ""))  # Final sound to signal completion

if __name__ == "__main__":
    print("Cyclic Alarm Utility")
    on_duration = input("Enter the ON duration (seconds, default 20 minutes): ")
    off_duration = input("Enter the OFF duration (seconds, default 20 minutes): ")
    cycles = input("Enter the number of cycles (default -> forever): ")

    if on_duration.strip() == "":
        on_duration = 1200

    if off_duration.strip() == "":
        off_duration = 1200

    if cycles.strip() == "":
        cycles = 0

    print("Starting the cyclic alarm...")
    cyclic_alarm(on_duration, off_duration, cycles)
