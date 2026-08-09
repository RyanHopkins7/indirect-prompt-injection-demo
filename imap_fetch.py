import imaplib
import email

imap = imaplib.IMAP4("localhost", 1143)
imap.login("demo", "demo")
imap.select("INBOX")

_, data = imap.search(None, "ALL")

for msg_id in data[0].split():
    _, msg_data = imap.fetch(msg_id, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    print(f"From: {msg['From']} | Subject: {msg['Subject']}")
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                print(part.get_payload(decode=True).decode(errors="replace"))
    else:
        print(msg.get_payload(decode=True).decode(errors="replace"))
    print()

imap.logout()