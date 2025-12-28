import time

def alarm_clock(alarm_time):
    print(f"Alarm set for {alarm_time}.")
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == alarm_time:
            print("Alarm! Time to wake up!")
            break
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    user_input = input("Enter the time for the alarm (HH:MM): ")
    alarm_clock(user_input)
