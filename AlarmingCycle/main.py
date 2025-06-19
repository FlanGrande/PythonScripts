import classes.config as config
import time
import os

def cyclic_alarm(on_duration, off_duration, cycles):
    cycling = True
    current_cycle = 0

    while cycling:
        current_cycle += 1

        print(f"Cycle {current_cycle}: ON for {on_duration} seconds.")
        os.system(f'pw-play {config.get_config_value("on_soundfx_path", "")}')  # Play sound to signal the start of the "on" state
        time.sleep(int(on_duration))
        
        print(f"Cycle {current_cycle}: OFF for {off_duration} seconds.")
        os.system(f'pw-play {config.get_config_value("off_soundfx_path", "")}')  # Play sound to signal the start of the "off" state
        time.sleep(int(off_duration))

        if current_cycle == int(cycles):
            break
    
    print("Alarm cycles complete!")
    os.system(f'pw-play {config.get_config_value("end_soundfx_path", "")}')  # Final sound to signal completion

if __name__ == "__main__":
    print("Cyclic Alarm Utility")
    on_duration = input("Enter the ON duration (seconds, default 20 minutes): ")
    off_duration = input("Enter the OFF duration (seconds, default 20 minutes): ")
    cycles = input("Enter the number of cycles (default -> forever): ")

    if on_duration.strip() == "":
        on_duration = 1200

    if off_duration == "":
        off_duration = 1200
    
    if cycles == "":
        cycles = 0
    
    print("Starting the cyclic alarm...")
    cyclic_alarm(on_duration, off_duration, cycles)
