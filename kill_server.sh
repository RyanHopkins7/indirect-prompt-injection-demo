RUNNING_PYMAP_PID="$(lsof -t -i:1143)"
RUNNING_SMTP_PID="$(lsof -t -i:1025)"

if [ -n "$RUNNING_PYMAP_PID" ]; then
    kill $RUNNING_PYMAP_PID
    echo "Killed pymap server on PID $RUNNING_PYMAP_PID"
fi

if [ -n "$RUNNING_SMTP_PID" ]; then
    kill $RUNNING_SMTP_PID
    echo "Killed smtp server on PID $RUNNING_PYMAP_PID"
fi
