import time
import logging
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "tickrcsa@gmail.com"
SENDER_PASSWORD = "mryk fdwy wntl knxo"  # App password if Gmail with 2FA
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
    time.sleep(5)

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    return driver

def open_main_page(driver):
    url = "https://billetterie.rcstrasbourgalsace.fr/fr/catalogue"  # Catalogue page with matches
    driver.get(url)

def check_match_and_reservation(driver):
    try:
        # Find all MatchCards
        match_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-component="MatchCard"]')
        for card in match_cards:
            if "LE HAVRE" in card.text.upper():
                try:
                    reserver_btn = card.find_element(By.XPATH, ".//a[contains(text(), 'Réserver')]")
                    if reserver_btn:
                        subject = "🎟️ RCSA - LE HAVRE Tickets Available!"
                        message = "The match RCSA vs LE HAVRE has a 'Réserver' button! Go check now!"
                        send_email_notification(subject, message)
                        return True
                except:
                    continue
        return False
    except Exception as e:
        print(f"Error checking match card: {e}")
        return False

def attempt_booking(driver):
    while True:
        if check_match_and_reservation(driver):
            print("✅ Match found and mail sent. Stopping check.")
            break
        else:
            print("⏳ Not available yet, retrying in 60s...")
        time.sleep(60)
        driver.refresh()

def main():
    subject = "🚀 Starting Match Watcher"
    message = "Now watching RCSA catalogue for LE HAVRE tickets..."
    send_email_notification(subject, message)

    driver = start_driver()
    open_main_page(driver)
    attempt_booking(driver)

if __name__ == "__main__":
    main()

