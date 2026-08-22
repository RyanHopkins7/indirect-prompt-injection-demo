import imaplib
import email

def imap_fetch():
    imap = imaplib.IMAP4("localhost", 1143)
    imap.login("demo", "demo")
    imap.select("INBOX")

    _, data = imap.search(None, "ALL")
    messages = ""

    for msg_id in data[0].split():
        _, msg_data = imap.fetch(msg_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        if msg["To"] == "demo":
            messages += f"From: {msg['From']}\nSubject: {msg['Subject']}"
            messages += "\nBody: \n"
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        messages += part.get_payload(decode=True).decode(errors="replace")
            else:
                messages += msg.get_payload(decode=True).decode(errors="replace")

    imap.logout()

    if messages == "":
        messages = "The maibox for demo@localhost is empty."

    return messages

if __name__ == "__main__":
    print(imap_fetch())
