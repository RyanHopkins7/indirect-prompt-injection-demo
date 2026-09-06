# Run the demo
1. Install requirements `pip install requirements.txt`
2. Run the imap server `./start_server.sh`
3. Try sending a test email `python ./smtp_send.py -f demo@localhost -t test@localhost -s HELLO -b "This is a test."`
4. Run the email agent `python ./demo.py`