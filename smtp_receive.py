import asyncio
import subprocess
from aiosmtpd.controller import Controller

IMAP_USER = "demo"

class PymapDeliveryHandler:
    async def handle_DATA(self, server, session, envelope):
        try:
            subprocess.run(
                ["pymap-admin", "append", IMAP_USER],
                input=envelope.content,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Delivery failed: {e.stderr.decode(errors='replace')}")
            return '451 Requested action aborted: delivery failed'

        print(f"Delivered from {envelope.mail_from} to {envelope.rcpt_tos}")
        return '250 Message accepted for delivery'


def run_smtp():
    controller = Controller(PymapDeliveryHandler(), hostname='localhost', port=1025)
    controller.start()
    print("SMTP listening on localhost:1025")


if __name__ == '__main__':
    run_smtp()
    try:
        asyncio.run(asyncio.Event().wait())
    except KeyboardInterrupt:
        pass