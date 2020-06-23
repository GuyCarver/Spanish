from imaplib import IMAP4_SSL as imap
from bs4 import BeautifulSoup
import email
#wotd-quick-translation
#box-h1-blue

MY_ACCOUNT = 'guydcarver@gmail.com'
MY_PWD = 'svbvdepxccabpqlk'
SMTP_SERVER = "imap.gmail.com"
FROM_ACCOUNT = '"Juan at SpanishDict"'
WORD_FILE = 'words.txt'

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python, process the spanish words and save to a file.
#
# ------------------------------------------------
     
def findwords(  ):
  imapper = imap(SMTP_SERVER)
  imapper.login(MY_ACCOUNT, MY_PWD)
  v = imapper.select('inbox')
  # get all messages from SpanishDict.
  typ, msgnums = imapper.search(None, 'FROM', FROM_ACCOUNT)
  processed = 0

  if len(msgnums[0]):
    with open(WORD_FILE, 'a', encoding='utf-8') as f:
      for mail_id in msgnums[0].split():
        mail = imapper.fetch(mail_id, '(RFC822)')
        #mail = ('ok', [('(mail_id)', msg)])
        msg = email.message_from_bytes(mail[1][0][1])
        bdy = msg.get_payload(decode=True)
#       print(bdy)
        processed += 1
  
        soup = BeautifulSoup(bdy, 'html.parser')
#       all = soup.find_all('a')
  
        href = soup.find('a', class_='box-h1 blue')
        spanish = href[0].contents[0].strip()
  
        href = soup.find('a', class_='wotd-quick-translation')
        english = href[0].contents[0].strip()
        entry = spanish + ', ' + english + '\n'
        print(entry, end='')
        f.write(entry)
        imapper.store(mail_id, '+FLAGS', r'(\Deleted)')      

  imapper.close()
  imapper.logout()

if __name__ == '__main__':
  findwords()

