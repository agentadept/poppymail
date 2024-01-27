# POP3 Email Access Script by Agent Adept http://micro.rodeo
import poplib
import email
from email.header import decode_header

# Replace these with your details
username = 'your_email@example.com'
password = 'your_password'
pop3_server = 'pop3_server_domain'
port = 995  # usually 995 for POP3 over SSL

# Function to get the body of the email
def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition and content_type == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

# Connect to the server
server = poplib.POP3_SSL(pop3_server, port)

# Authenticate
server.user(username)
server.pass_(password)

# Get message count
num_messages = len(server.list()[1])

print(f"You have {num_messages} email(s).")

# Fetch and parse emails
for i in range(num_messages):
    _, raw_message, _ = server.retr(i + 1)
    raw_message_string = b'\n'.join(raw_message).decode('utf-8')
    email_message = email.message_from_string(raw_message_string)

    # Decode the email subject
    subject = decode_header(email_message['Subject'])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()

    print(f"Email {i+1}:")
    print(f"From: {email_message['From']}")
    print(f"Subject: {subject}")

    # Fetching the email body
    body = get_body(email_message)
    print("Body:", body)
    print("\n---\n")

# Quit the server
server.quit()
