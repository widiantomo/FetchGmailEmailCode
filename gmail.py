import email, getpass, imaplib, os
from email import policy
import re

detach_dir = '.' # directory where to save attachments (default: current)
user = "wewe@gmail.com"
pwd = getpass.getpass("Enter your password: ")

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
m.select("inbox") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes

resp, items = m.search(None, 'TEXT \"apple.com\"') # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id
n = 0

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1] # getting the mail content
    mail = email.message_from_bytes(email_body, policy=policy.default) # parsing the mail content to get a mail object

    #Check if any attachments at all
    if mail.get_content_maintype() != 'multipart':
        continue

    #print("["+mail["From"]+"] :" + mail["Subject"])

    # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
    for part in mail.walk():
        # multipart are just containers, so we skip them
        if part.get_content_maintype() == 'text':
            linex = part.get_payload()
            continue

        # is this part an attachment ?
        if part.get('Content-Disposition') is None:
            continue

        #filename = part.get_filename()
        
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', linex)
        #linex = part.get_payload()
        #match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', linex)
        #filename = mail["From"] + "_hw1answer"
        if match is not None:
            print(match.group(0))
            #n = n + 1
            #print(n)
        else:
        # no need for else: really if it doesn't contain anything useful
            pass
        #att_path = os.path.join(detach_dir, filename)

        #Check if its already there
        #if not os.path.isfile(att_path) :
            # finally write the stuff
            # fp = open(att_path, 'wb')
            # fp.write(part.get_payload(decode=True))
            # fp.close()
