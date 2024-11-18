import secrets
print("SAS_API_KEY=" + secrets.token_hex(32))
print("CALENDAR_API_KEY=" + secrets.token_hex(32))