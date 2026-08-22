import argparse
import smtplib
from email.message import EmailMessage


def send_email(sender, recipient, subject, body, host="localhost", port=1025):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(host, port) as smtp:
        smtp.send_message(msg)

    return f"Successfully sent email from {sender} to {recipient}"

def parse_args():
    parser = argparse.ArgumentParser(description="Send an email via a local SMTP server.")
    parser.add_argument("-f", "--from", dest="sender", required=True, help="Sender address")
    parser.add_argument("-t", "--to", dest="recipient", required=True, help="Recipient address")
    parser.add_argument("-s", "--subject", required=True, help="Email subject")
    parser.add_argument("-b", "--body", required=True, help="Email body text")
    parser.add_argument("--host", default="localhost", help="SMTP host (default: localhost)")
    parser.add_argument("--port", type=int, default=1025, help="SMTP port (default: 1025)")
    return parser.parse_args()


def main():
    args = parse_args()
    send_email(
        sender=args.sender,
        recipient=args.recipient,
        subject=args.subject,
        body=args.body,
        host=args.host,
        port=args.port,
    )
    print(f"Sent: {args.sender} -> {args.recipient} [{args.subject}]")


if __name__ == "__main__":
    main()