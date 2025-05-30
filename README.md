# **Instagram Login Tool - Code Explanation**

![License: MIT](https://img.shields.io/badge/License-MIT-red) [![Follow me](https://img.shields.io/github/followers/ebsa491?label=Follow%20me&style=social)](https://github.com/ebsa491)

## **Overview**
This project implements a secure and professional Instagram login tool using Python. The tool provides a robust solution for Instagram authentication with a focus on security and user experience.

## **Core Components**

### 1. **Main Script (`instagram_login.py`)**

The main script is structured around the `InstagramLoginTool` class, which handles all authentication and credential management functionality. Here's a breakdown of its key components:

#### **Class Initialization**

```python
def __init__(self):
    self.console = Console()
    self.client = Client()
    self.credentials_file = Path("credentials.enc")
    self.key_file = Path("key.key")
    self._load_or_create_key()
```
- Initializes a rich console for beautiful terminal output
- Creates an Instagram client instance
- Sets up paths for credential and key storage
- Loads or creates encryption key

#### **Security Features**

The tool implements several security measures:

1. **Credential Encryption**

```python
def _encrypt_credentials(self, username: str, password: str):
    credentials = {
        "username": username,
        "password": password,
        "timestamp": datetime.now().isoformat()
    }
    encrypted_data = self.cipher_suite.encrypt(json.dumps(credentials).encode())
```
- Uses Fernet symmetric encryption
- Stores credentials with timestamp
- Encrypts data before writing to disk

2. **Key Management**

```python
def _load_or_create_key(self):
    if self.key_file.exists():
        with open(self.key_file, "rb") as f:
            self.key = f.read()
    else:
        self.key = Fernet.generate_key()
```
- Generates a new encryption key if none exists
- Securely stores the key for future use

#### **Authentication Flow**
The login process is handled through the `login()` method, which:
- Attempts to use saved credentials
- Prompts for new credentials if none exist
- Handles two-factor authentication
- Provides visual feedback during the process
- Securely stores successful login credentials

#### **Account Information Display**

```python
def get_account_info(self):
    account = self.client.account_info()
    self.console.print(Panel(
        f"[bold]Account Information[/bold]\n"
        f"Username: {account.username}\n"
        # ... more account details
    ))
```
- Fetches and displays account information
- Uses rich formatting for better readability
- Handles errors gracefully

### 2. **Dependencies (`requirements.txt`)**

The project uses several key libraries:
- `instagrapi`: For Instagram API interaction
- `python-dotenv`: For environment variable management
- `rich`: For terminal UI enhancement
- `cryptography`: For secure credential encryption

## **Security Considerations**

1. **Credential Storage**
   - Credentials are never stored in plain text
   - Uses industry-standard encryption (Fernet)
   - Implements secure key management

2. **Password Handling**
   - Uses `getpass` for secure password input
   - Never displays passwords in logs or output
   - Implements proper error handling for failed attempts

3. **Session Management**
   - Handles Instagram sessions securely
   - Implements proper error handling for various scenarios
   - Supports two-factor authentication

## **User Interface**

The tool provides a professional user experience through:
- Progress indicators for long operations
- Color-coded status messages
- Formatted account information display
- Clear error messages and instructions

## **Error Handling**

The code implements comprehensive error handling for:
- Invalid credentials
- Two-factor authentication
- Network issues
- API limitations
- File system operations

## **Usage Example**

```python
tool = InstagramLoginTool()
if tool.login():
    tool.get_account_info()
```

This creates a new instance of the tool, attempts to log in, and displays account information if successful.

## **Best Practices Implemented**

1. **Code Organization**
   - Clear class structure
   - Well-documented methods
   - Type hints for better code understanding

2. **Security**
   - Secure credential storage
   - Proper encryption implementation
   - Safe password handling

3. **User Experience**
   - Clear feedback
   - Progress indicators
   - Formatted output

4. **Error Handling**
   - Comprehensive exception handling
   - User-friendly error messages
   - Graceful failure recovery

This tool demonstrates professional-grade Python development practices while maintaining security and user experience as top priorities.

## **License**

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more information.
