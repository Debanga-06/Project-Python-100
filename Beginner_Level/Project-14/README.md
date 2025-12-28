# Countdown Timer 

A console-based countdown timer with live display, multiple time input formats, and customizable completion messages.

## Features

- **Multiple Input Formats**: Seconds, MM:SS, HH:MM:SS
- **Live Countdown Display**: Real-time updates
- **Custom Messages**: Personalized completion alerts
- **Audio Alert**: Beep notification when complete
- **Keyboard Interrupt**: Cancel with Ctrl+C
- **Input Validation**: Prevents invalid times

## Requirements

- Python 3.x

## Usage

```bash
python countdown_timer.py
```

## Examples

### Simple Seconds
```
Enter countdown time: 90
⏱️  Starting 01:30 countdown...
⏳ Time Remaining: 00:45
```

### Minutes and Seconds
```
Enter countdown time: 5:30
⏱️  Starting 05:30 countdown...
```

### Hours, Minutes, Seconds
```
Enter countdown time: 1:30:00
⏱️  Starting 01:30:00 countdown...
```

## Input Formats

| Format | Example | Description |
|--------|---------|-------------|
| Seconds | `90` | 90 seconds |
| MM:SS | `5:30` | 5 minutes 30 seconds |
| HH:MM:SS | `1:30:00` | 1 hour 30 minutes |

## Use Cases

- **Productivity**: Pomodoro technique (25-minute work sessions)
- **Cooking**: Recipe timing
- **Exercise**: Workout intervals
- **Study**: Timed study sessions
- **Presentations**: Speaking time limits
- **Meetings**: Time management

## Common Timings

- **Pomodoro**: 25:00 (25 minutes)
- **Short Break**: 5:00
- **Long Break**: 15:00
- **Boil Egg**: 3:00 (soft) or 7:00 (hard)
- **Steep Tea**: 3:00 to 5:00

## License

Free to use and modify.