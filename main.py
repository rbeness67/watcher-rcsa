import time
import logging
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "tickrcsa@gmail.com"
SENDER_PASSWORD = "mryk fdwy wntl knxo"  # App-specific password
TO_EMAIL = "tickrcsa@gmail.com"

def send_email_notification(subject, message):
    """Send an email using SMTP."""
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("📧 Email sent!")
    except Exception as e:
        print(f"Error sending email: {e}")
    time.sleep(30)

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    return driver

def open_ticket_page(driver):
    url = "https://billetterie.rcstrasbourgalsace.fr/fr/acheter/billet-unite-tout-public-racing-crystal-palace-2025-bth8bc0pomoz/list"
    driver.get(url)

def is_tickets_available(driver):
    sections = ["OUEST KOP",]

    for section in sections:
        try:
            button = driver.find_element(By.XPATH, f"//button[.//b[contains(text(), '{section}')]]")
            button.click()
            subject = "🎫 Billets disponibles UNITE Crystal Palace!"
            message = f"Tickets trouvés pour CP dans la section {section} !"
            send_email_notification(subject, message)
            return False
        except:
            continue

def attempt_booking(driver):
    while True:
        is_tickets_available(driver)
        time.sleep(15)
        driver.refresh()



def main():
    subject = "LANCEMENT UNITE RCSA CRYSTAL PALACE !"
    message = f"Début du watch des tickets de Crystal Palace !"
    send_email_notification(subject, message)
    driver = start_driver()
    open_ticket_page(driver)
    attempt_booking(driver)

if __name__ == "__main__":
    main()