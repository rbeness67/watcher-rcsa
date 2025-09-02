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

# URLs with individual match keywords
URLS = [
    {
        "name": "Racing Club de Strasbourg",
        "url": "https://billetterie.rcstrasbourgalsace.fr/fr/",
        "match_keywords": ["CRYSTAL PALACE", "OLYMPIQUE DE MARSEILLE","conference"],
    },
    # You can add more objects like this:
    {
         "name": "Olympique de Marseille",
         "url": "https://billetterie.om.fr/fr/",
         "match_keywords": ["Paris", "Ajax","Liverpool","Atalanta","Newcastle","Champions"],
    },
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


def check_match_and_reservation(driver, config):
    """Check one URL for matches with 'Réserver' available."""
    driver.get(config["url"])
    time.sleep(3)  # let page load

    found = False
    try:
        match_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-component="MatchCard"]')
        for card in match_cards:
            text = card.text.upper()  # normalize card text
            for keyword in config["match_keywords"]:
                if keyword.upper() in text:  # normalize keyword too
                    try:
                        # Look for "Réserver" button inside the card
                        reserver_btn = card.find_elements(By.XPATH, ".//a[contains(text(), 'Réserver')]")
                        if reserver_btn:
                            subject = f"🎟️ Tickets Available: {keyword} ({config['name']})"
                            message = (
                                f"Match containing '{keyword}' is available!\n\n"
                                f"📍 Section: {config['name']}\n"
                                f"🔗 URL: {config['url']}\n\n"
                                f"Card Text:\n{text}"
                            )
                            send_email_notification(subject, message)
                            found = True
                        else:
                            print(f"⛔ {keyword} found at {config['name']} but no 'Réserver' button.")
                    except Exception as e:
                        print(f"⚠️ Could not parse actions for card: {e}")
                        continue
    except Exception as e:
        print(f"Error checking {config['url']}: {e}")

    return found


    return found


def attempt_booking(driver):
    while True:
        for config in URLS:
            print(f"🔍 Checking {config['name']} → {config['url']}...")
            if check_match_and_reservation(driver, config):
                print(f"✅ Found tickets in {config['name']}")
        print("⏳ Sleeping 60s before next check...")
        time.sleep(60)


def main():
    subject = "🚀 Starting Match Watcher"
    message = "Now watching these URLs:\n" + "\n".join([f"{c['name']}: {c['url']}" for c in URLS])
    send_email_notification(subject, message)

    driver = start_driver()
    attempt_booking(driver)


if __name__ == "__main__":
    main()
