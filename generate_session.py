"""
Ye script tumhare ASSISTANT account (jo voice chat me join karega) ka
SESSION_STRING generate karta hai. Ye kisi bot account ka nahi, tumhare
apne (ya kisi dusre) normal Telegram account ka session hota hai.

Run karo:  python3 generate_session.py

Warning: SESSION_STRING kabhi kisi ke saath share mat karo - ye tumhare
Telegram account ka full access deta hai.
"""

from pyrogram import Client

API_ID = int(input("Apna API_ID daalo: "))
API_HASH = input("Apna API_HASH daalo: ")

with Client("assistant_session", api_id=API_ID, api_hash=API_HASH) as app:
    print("\nYe raha tumhara SESSION_STRING (.env me SESSION_STRING= ke aage paste karo):\n")
    print(app.export_session_string())
