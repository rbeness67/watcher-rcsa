import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ===========================
# CONFIGURATION
# ===========================

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "tickrcsa@gmail.com"
SENDER_PASSWORD = "mryk fdwy wntl knxo"  # App-specific password
TO_EMAIL = "tickrcsa@gmail.com"


# List of (name, url) to check
URLS = [
    ("RCSA", "https://billetterie.rcstrasbourgalsace.fr/fr/"),
    ("OM", "https://billetterie.om.fr/fr"),
]

# List of match keywords to monitor (uppercase)
MATCH_KEYWORDS = [
    "LE HAVRE",
    "PARIS",
    "MONACO",
]

# ===========================
# FUNCTIONS
# ===========================

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


def check_match_and_reservation(driver, name, url):
    """Check one URL for matches."""
    driver.get(url)
    time.sleep(3)  # let page load

    found = False
    try:
        match_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-component="MatchCard"]')
        for card in match_cards:
            text = card.text.upper()
            for keyword in MATCH_KEYWORDS:
                if keyword in text:
                    try:
                        reserver_btn = card.find_element(By.XPATH, ".//a[contains(text(), 'Réserver')]")
                        if reserver_btn:
                            subject = f"🎟️ Tickets Available: {keyword} ({name})"
                            message = (
                                f"Match containing '{keyword}' is available!\n\n"
                                f"📍 Section: {name}\n"
                                f"🔗 URL: {url}\n\n"
                                f"Card Text:\n{text}"
                            )
                            send_email_notification(subject, message)
                            found = True
                    except:
                        continue
    except Exception as e:
        print(f"Error checking {url}: {e}")

    return found


def attempt_booking(driver):
    while True:
        for name, url in URLS:
            print(f"🔍 Checking {name} → {url}...")
            if check_match_and_reservation(driver, name, url):
                print(f"✅ Found tickets in {name} ({url})")
        print("⏳ Sleeping 60s before next check...")
        time.sleep(60)


def main():
    subject = "🚀 Starting Match Watcher"
    message = "Now watching these URLs:\n" + "\n".join([f"{name}: {url}" for name, url in URLS])
    send_email_notification(subject, message)

    driver = start_driver()
    attempt_booking(driver)


if __name__ == "__main__":
    main()
