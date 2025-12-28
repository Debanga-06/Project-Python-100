# Password Generator 

A Python program that creates strong, random passwords with customizable options for letters, numbers, and symbols.

## Features

- **Customizable Length**: Generate passwords from 8 to 32 characters
- **Character Type Options**: 
  - Letters (uppercase A-Z and lowercase a-z)
  - Numbers (0-9)
  - Symbols (!@#$%^&*()_+-=[]{}|;:,.<>?)
- **Smart Generation**: Ensures at least one character from each selected type
- **Strength Indicator**: Visual feedback on password security level
- **Multiple Generations**: Create unlimited passwords in one session
- **Secure Randomization**: Uses Python's random module for unpredictability
- **Character Shuffling**: Prevents predictable patterns

## Requirements

- Python 3.x

## How to Run

1. Save the program as `password.py`
2. Open your terminal or command prompt
3. Navigate to the directory containing the file
4. Run the program:

```bash
python password_generator.py
```

## Usage Example

```
==================================================
         PASSWORD GENERATOR
==================================================

--------------------------------------------------
Password length (8-32, default 12): 16
Include letters? (Y/n): y
Include numbers? (Y/n): y
Include symbols? (Y/n): y

==================================================
Your generated password:
  K#9mL$xR2pQw@7Tz
==================================================
Strength: 🟢 STRONG

Generate another? (Y/n): n

Goodbye!
```

## Password Strength Ratings

The program evaluates password strength based on:

### 🟢 STRONG
- 12+ characters in length
- Includes letters, numbers, AND symbols
- Maximum security for sensitive accounts

### 🟡 MODERATE
- Good character variety but shorter length
- OR missing one character type
- Suitable for less critical accounts

### 🔴 WEAK
- Short length (less than 12 characters)
- Limited character variety (only 1-2 types)
- Not recommended for important accounts

## Character Sets

### Letters (52 characters)
- **Uppercase**: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
- **Lowercase**: a b c d e f g h i j k l m n o p q r s t u v w x y z

### Numbers (10 characters)
- **Digits**: 0 1 2 3 4 5 6 7 8 9

### Symbols (32 characters)
- **Special characters**: ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~

## Security Best Practices

### Password Guidelines
1. **Length Matters**: Use at least 12 characters (16+ is better)
2. **Complexity**: Mix uppercase, lowercase, numbers, and symbols
3. **Uniqueness**: Never reuse passwords across different accounts
4. **Avoid Patterns**: Don't use keyboard patterns (qwerty, 12345)
5. **No Personal Info**: Avoid names, birthdays, or dictionary words

### Password Management
- **Use a Password Manager**: Store passwords securely (LastPass, 1Password, Bitwarden)
- **Enable 2FA**: Add two-factor authentication when available
- **Regular Updates**: Change passwords periodically for sensitive accounts
- **Check for Breaches**: Use services like "Have I Been Pwned" to check compromised passwords

### When to Use Strong Passwords
- Email accounts (primary security gateway)
- Banking and financial accounts
- Social media accounts
- Work/corporate accounts
- Cloud storage services
- Any account with personal or sensitive data

## How It Works

### Algorithm Steps
1. **Initialize**: Create empty character pool
2. **Add Character Sets**: Based on user selections
3. **Guarantee Coverage**: Add at least one character from each selected type
4. **Fill Remaining**: Randomly select characters to reach desired length
5. **Shuffle**: Randomize character order to avoid predictable patterns
6. **Return**: Display generated password

### Code Example
```python
# Simplified logic
characters = ""
if use_letters: characters += string.ascii_letters
if use_numbers: characters += string.digits
if use_symbols: characters += string.punctuation

password = [random.choice(each_type)]  # Guarantee one of each
password += [random.choice(characters) for _ in range(length - len(password))]
random.shuffle(password)
```

## Code Structure

### Functions
- `generate_password(length, use_letters, use_numbers, use_symbols)`
  - Main password generation logic
  - Returns generated password string
  
- `main()`
  - User interface and input handling
  - Displays results and strength rating
  - Manages program flow

### Modules Used
- `random` - Secure random character selection
- `string` - Pre-defined character sets (ascii_letters, digits, punctuation)

## Sample Passwords

### Strong Passwords (16 characters, all types)
- `aK9#mP$xR2qW@7Tz`
- `J!5nL*8vB&3cX%1D`
- `pQ@4rY#9tU$6wE*2`

### Moderate Passwords (12 characters, letters + numbers)
- `aB3cD5eF7gH9`
- `mN2oP4qR6sT8`

### Weak Passwords (8 characters, letters only)
- `aBcDeFgH`
- `xYzAbCdE`

## Common Password Mistakes to Avoid

❌ **DON'T**
- Use personal information (name, birthday)
- Use dictionary words
- Use keyboard patterns (qwerty, asdfgh)
- Use sequential numbers (123456, abcdef)
- Reuse passwords across sites
- Share passwords with others
- Write passwords on paper or sticky notes

✅ **DO**
- Use this generator for random passwords
- Store in a secure password manager
- Use unique passwords for each account
- Enable two-factor authentication
- Update passwords regularly
- Use long passwords (16+ characters)

## Testing Password Strength

After generating a password, you can test it on these sites:
- **How Secure Is My Password**: howsecureismypassword.net
- **Password Meter**: passwordmeter.com
- **Kaspersky Password Checker**: password.kaspersky.com

## Use Cases

- Creating new account passwords
- Resetting compromised passwords
- Generating temporary passwords
- Creating Wi-Fi passwords
- Secure API keys or tokens
- Educational demonstrations on password security

## Customization Ideas

- Add option to exclude similar characters (0/O, 1/l/I)
- Generate multiple passwords at once
- Save passwords to encrypted file
- Add passphrase generation option
- Include password strength estimation
- Add clipboard copy functionality
- Export passwords to CSV

## Technical Notes

- Uses `random.randint()` and `random.choice()` for selection
- Shuffles final password to avoid pattern at start
- Input validation prevents invalid lengths
- Guarantees character type requirements are met

## License

Free to use and modify for any purpose.