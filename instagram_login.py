#!/usr/bin/env python3

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from getpass import getpass
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    BadCredentials,
    TwoFactorRequired,
    ClientError
)
from dotenv import load_dotenv
from cryptography.fernet import Fernet

class InstagramLoginTool:
    def __init__(self):
        self.console = Console()
        self.client = Client()
        self.credentials_file = Path("credentials.enc")
        self.key_file = Path("key.key")
        self._load_or_create_key()

    def _load_or_create_key(self) -> None:
        """Load or create encryption key for credentials"""
        if self.key_file.exists():
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.key)
        self.cipher_suite = Fernet(self.key)

    def _encrypt_credentials(self, username: str, password: str) -> None:
        """Encrypt and save credentials"""
        credentials = {
            "username": username,
            "password": password,
            "timestamp": datetime.now().isoformat()
        }
        encrypted_data = self.cipher_suite.encrypt(json.dumps(credentials).encode())
        with open(self.credentials_file, "wb") as f:
            f.write(encrypted_data)

    def _decrypt_credentials(self) -> Optional[Dict[str, Any]]:
        """Decrypt and load credentials"""
        if not self.credentials_file.exists():
            return None
        try:
            with open(self.credentials_file, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            self.console.print(f"[red]Error loading credentials: {str(e)}[/red]")
            return None

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> bool:
        """Handle Instagram login process"""
        try:
            # Try to load saved credentials if not provided
            if not username or not password:
                saved_creds = self._decrypt_credentials()
                if saved_creds:
                    username = saved_creds["username"]
                    password = saved_creds["password"]

            if not username or not password:
                self.console.print("[yellow]No saved credentials found. Please enter your credentials:[/yellow]")
                username = input("Username: ")
                password = getpass("Password: ")

            with Progress() as progress:
                task = progress.add_task("[cyan]Logging in...", total=100)
                
                # Attempt login
                self.client.login(username, password)
                
                progress.update(task, completed=100)
                self.console.print("[green]Successfully logged in![/green]")
                
                # Save credentials if login successful
                self._encrypt_credentials(username, password)
                return True

        except TwoFactorRequired:
            self.console.print("[yellow]Two-factor authentication required.[/yellow]")
            code = input("Enter 2FA code: ")
            try:
                self.client.login(username, password, verification_code=code)
                self.console.print("[green]Successfully logged in with 2FA![/green]")
                self._encrypt_credentials(username, password)
                return True
            except Exception as e:
                self.console.print(f"[red]2FA login failed: {str(e)}[/red]")
                return False

        except BadCredentials:
            self.console.print("[red]Invalid username or password.[/red]")
            return False

        except ClientError as e:
            self.console.print(f"[red]Instagram client error: {str(e)}[/red]")
            return False

        except Exception as e:
            self.console.print(f"[red]Unexpected error: {str(e)}[/red]")
            return False

    def get_account_info(self) -> None:
        """Display account information"""
        try:
            account = self.client.account_info()
            self.console.print(Panel(
                f"[bold]Account Information[/bold]\n"
                f"Username: {account.username}\n"
                f"Full Name: {account.full_name}\n"
                f"Followers: {account.follower_count}\n"
                f"Following: {account.following_count}\n"
                f"Media Count: {account.media_count}\n"
                f"Private Account: {'Yes' if account.is_private else 'No'}",
                title="Instagram Account Details",
                border_style="green"
            ))
        except Exception as e:
            self.console.print(f"[red]Error fetching account info: {str(e)}[/red]")

def main():
    tool = InstagramLoginTool()
    
    # Display welcome message
    tool.console.print(Panel(
        "[bold blue]Instagram Login Tool[/bold blue]\n"
        "A professional tool for Instagram authentication",
        border_style="blue"
    ))

    # Attempt login
    if tool.login():
        tool.get_account_info()
    else:
        tool.console.print("[red]Login failed. Please try again.[/red]")

if __name__ == "__main__":
    main()