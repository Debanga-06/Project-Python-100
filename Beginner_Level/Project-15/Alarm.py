"""
Alarm Clock 
Basic console alarm clock with time scheduling.
"""

import time
from datetime import datetime, timedelta


def parse_alarm_time(time_str):
    """
    Parse alarm time in HH:MM format (24-hour).
    
    Args:
        time_str (str): Time string
    
    Returns:
        datetime: Alarm datetime object
    """
    time_str = time_str.strip()
    
    try:
        # Parse time
        alarm_time = datetime.strptime(time_str, "%H:%M")
        
        # Get current time
        now = datetime.now()
        
        # Set alarm for today
        alarm = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)
        
        # If alarm time has passed, set for tomorrow
        if alarm <= now:
            alarm += timedelta(days=1)
        
        return alarm
    
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM (24-hour format).")


def wait_for_alarm(alarm_time, message="ALARM!"):
    """
    Wait until alarm time and trigger alert.
    
    Args:
        alarm_time (datetime): Target alarm time
        message (str): Alarm message
    
    Returns:
        bool: True if alarm triggered, False if cancelled
    """
    now = datetime.now()
    wait_seconds = (alarm_time - now).total_seconds()
    
    print(f"\n⏰ Alarm set for: {alarm_time.strftime('%I:%M %p')}")
    print(f"   ({alarm_time.strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"   Time until alarm: {format_duration(wait_seconds)}")
    print("\nPress Ctrl+C to cancel alarm\n")
    
    try:
        while True:
            now = datetime.now()
            remaining = (alarm_time - now).total_seconds()
            
            if remaining <= 0:
                # Trigger alarm
                trigger_alarm(message)
                return True
            
            # Update display every second
            print(f"\r⏱️  Time until alarm: {format_duration(remaining)}   ", end='', flush=True)
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Alarm cancelled by user.")
        return False


def format_duration(seconds):
    """Format seconds into readable duration."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def trigger_alarm(message):
    """Trigger alarm with visual and audio alerts."""
    print("\n\n" + "=" * 60)
    print(f"⏰ {message}")
    print("=" * 60)
    
    # Beep multiple times
    for _ in range(5):
        print("\a", end='', flush=True)
        time.sleep(0.5)
    
    # Display large alarm message
    alarm_art = """
    
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║          🔔  ALARM!  ALARM!  ALARM!  🔔          ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
    
    """
    print(alarm_art)
    
    # Keep beeping
    input("Press Enter to stop alarm...")


def main():
    """Main program execution."""
    print("=" * 60)
    print("                   ALARM CLOCK")
    print("=" * 60)
    print("\nSet an alarm using 24-hour format (HH:MM)")
    print("Example: 14:30 for 2:30 PM")
    
    while True:
        print("\n" + "-" * 60)
        
        try:
            time_input = input("\nEnter alarm time (HH:MM) or 'q' to quit: ").strip()
            
            if time_input.lower() == 'q':
                print("\nGoodbye!")
                break
            
            # Parse alarm time
            alarm_time = parse_alarm_time(time_input)
            
            # Optional custom message
            custom_msg = input("Alarm message (optional): ").strip()
            if not custom_msg:
                custom_msg = "ALARM!"
            
            # Wait for alarm
            triggered = wait_for_alarm(alarm_time, custom_msg)
            
            if triggered:
                again = input("\nSet another alarm? (Y/n): ")
                if again.lower() == 'n':
                    print("\nThank you for using Alarm Clock!")
                    break
        
        except ValueError as e:
            print(f"❌ Error: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()