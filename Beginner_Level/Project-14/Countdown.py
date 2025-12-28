"""
Countdown Timer 
Console-based countdown timer with formatted time display.
"""

import time
import sys


def format_time(seconds):
    """
    Format seconds into HH:MM:SS format.
    
    Args:
        seconds (int): Total seconds
    
    Returns:
        str: Formatted time string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def parse_time_input(time_str):
    """
    Parse time input in various formats.
    Supports: seconds, MM:SS, HH:MM:SS
    
    Args:
        time_str (str): Time input string
    
    Returns:
        int: Total seconds
    """
    time_str = time_str.strip()
    
    if ':' in time_str:
        parts = time_str.split(':')
        if len(parts) == 2:  # MM:SS
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
    else:
        # Just seconds
        return int(time_str)


def countdown(seconds, message="Time's Up!"):
    """
    Perform countdown with live display.
    
    Args:
        seconds (int): Total countdown seconds
        message (str): Message to display when complete
    """
    print(f"\n⏱️  Starting {format_time(seconds)} countdown...\n")
    
    try:
        for remaining in range(seconds, 0, -1):
            # Clear line and display countdown
            sys.stdout.write(f"\r⏳ Time Remaining: {format_time(remaining)}   ")
            sys.stdout.flush()
            time.sleep(1)
        
        # Countdown complete
        sys.stdout.write(f"\r✓ {message}                    \n")
        
        # Sound alert (platform independent)
        print("\a" * 3)  # Beep three times
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Countdown cancelled by user.")
        return False
    
    return True


def main():
    """Main program execution."""
    print("=" * 60)
    print("                 COUNTDOWN TIMER")
    print("=" * 60)
    print("\nEnter time in one of these formats:")
    print("  • Seconds: 90")
    print("  • Minutes:Seconds: 1:30")
    print("  • Hours:Minutes:Seconds: 0:1:30")
    
    while True:
        print("\n" + "-" * 60)
        
        try:
            time_input = input("\nEnter countdown time (or 'q' to quit): ").strip()
            
            if time_input.lower() == 'q':
                print("\nGoodbye!")
                break
            
            # Parse time input
            total_seconds = parse_time_input(time_input)
            
            if total_seconds <= 0:
                print("❌ Please enter a positive time value.")
                continue
            
            if total_seconds > 86400:  # 24 hours
                print("⚠️  Warning: Countdown is longer than 24 hours.")
                confirm = input("Continue? (y/n): ")
                if confirm.lower() != 'y':
                    continue
            
            # Optional custom message
            custom_msg = input("Custom completion message (optional): ").strip()
            if not custom_msg:
                custom_msg = "Time's Up!"
            
            # Start countdown
            success = countdown(total_seconds, custom_msg)
            
            if success:
                again = input("\nStart another countdown? (Y/n): ")
                if again.lower() == 'n':
                    print("\nThank you for using Countdown Timer!")
                    break
        
        except ValueError:
            print("❌ Invalid time format. Please try again.")
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()