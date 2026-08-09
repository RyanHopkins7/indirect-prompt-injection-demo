1. Install requirements `pip install requirements.txt`
2. Run the imap server `./pymap_server.sh`
3. Create imap user `pymap-admin set-user demo`
4. Set the password to "demo"
5. Try sending a test email `python ./smtp_send.py -f demo@localhost -t test@localhost -s HELLO -b "This is a test."`