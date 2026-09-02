import argparse
import imaplib
import email

def imap_fetch(email_addr="demo@localhost", host="localhost", port=1143):
    imap = imaplib.IMAP4(host, port)
    imap.login("demo", "demo")
    imap.select("INBOX")

    _, data = imap.search(None, "ALL")
    messages = ""

    for msg_id in data[0].split():
        _, msg_data = imap.fetch(msg_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        if msg["To"] == email_addr:
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
        messages = f"The maibox for {email_addr} is empty."

    return messages

def parse_args():
    parser = argparse.ArgumentParser(description="Get emails from local IMAP server.")
    parser.add_argument("-a", "--address", default="demo@localhost", help="Email inbox address")
    parser.add_argument("--host", default="localhost", help="IMAP host (default: localhost)")
    parser.add_argument("--port", type=int, default=1143, help="IMAP port (default: 1143)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    emails = imap_fetch(email_addr=args.address, host=args.host, port=args.port)
    print(emails)
