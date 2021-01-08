import requests
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from config import credentials

url = 'https://www.amazon.com/dp/0674007077/?coliid=I2FTYLALQEVLZF&colid=25GELF5WT36MN&psc=1&ref_=lv_ov_lig_dp_it'

headers={
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

def check_price():
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id='productTitle').get_text()
    price = soup.find(id='newBuyBoxPrice').get_text()
    converted_price = float(price[1:])

    if converted_price <= 25.00:
        send_email(title, converted_price)

    print(title.strip(),
          converted_price)

def send_email(title, converted_price):
    server = smtplib.SMTP(credentials['SMTP_config'], int(credentials['SMTP_port']))
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(credentials['sender_email'], credentials['sender_password'])

    sender_email=credentials['sender_email']
    receiver_email = credentials['recipient_email']

    _subject = f"♦♦♦PRICE ALERT♦♦♦ {title}"
    subject = " ".join(_subject.split())


    message = MIMEMultipart()
    message["Subject"] = subject

    message["From"] = sender_email
    message["To"] = receiver_email




    html = f"The product you've been tracking, <i><b><a href='https://www.amazon.com/dp/0674007077/?coliid=I2FTYLALQEVLZF&colid=25GELF5WT36MN&psc=1&ref_=lv_ov_lig_dp_it'>{title}</b></i></a>, has dropped to <b>${converted_price}</b> "


    part1 = MIMEText(html,"html")


    message.attach(part1)

    server.sendmail(sender_email,
                    receiver_email,
        message.as_string()

    )

    print('HEY, EMAIL HAS BEEN SENT!')

    server.quit()

while(True):

    check_price()
    time.sleep(43200)
