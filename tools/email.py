import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from config.config_loader import load_config
from utils.logger import setup_logger
from bs4 import BeautifulSoup

logger = setup_logger()
config = load_config()

EMAIL_ADDRESS = config["email"]["address"]
EMAIL_PASSWORD = config["email"]["app_password"]
IMAP_SERVER = config["email"]["imap_server"]
SMTP_SERVER = config["email"]["smtp_server"]
SMTP_PORT = config["email"]["smtp_port"]


# ================= CLEAN HTML =================
def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # remove script/style/link tags
    for tag in soup(["script", "style", "a"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # remove empty lines
    lines = [line.strip() for line in text.splitlines()]
    clean_lines = [line for line in lines if line]

    return "\n".join(clean_lines)


# ================= READ EMAIL =================
def read_recent_emails(limit=5, summarize=False, llm=None):
    try:
        logger.info(f"Reading {limit} emails | summarize={summarize}")

        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        mail_ids = data[0].split()

        if not mail_ids:
            return "Inbox is empty."

        latest_ids = mail_ids[-int(limit):][::-1]
        emails_output = []

        for index, mail_id in enumerate(latest_ids):
            result, msg_data = mail.fetch(mail_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = msg.get("subject", "No Subject")
            sender = msg.get("from", "Unknown Sender")

            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()

                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                        except:
                            pass

                    elif content_type == "text/html" and not body:
                        try:
                            html = part.get_payload(decode=True).decode(errors="ignore")
                            body = clean_html(html)
                        except:
                            pass
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors="ignore")

            body = body.strip()

            # ---------- SUMMARIZE MODE ----------
            if summarize and llm:
                summary_text = llm(
                    f"Summarize this email clearly and concisely:\n\n{body[:6000]}"
                )

                emails_output.append(
                    f"\nFrom: {sender}\nSubject: {subject}\nSummary:\n{summary_text}\n"
                )
            else:
                if index == 0:
                    emails_output.append(
                        f"\nFrom: {sender}\nSubject: {subject}\nBody:\n{body}\n"
                    )
                else:
                    emails_output.append(
                        f"\nFrom: {sender}\nSubject: {subject}\n"
                    )

        mail.logout()
        logger.info("Email fetch successful")

        return "\n".join(emails_output)

    except Exception as e:
        logger.error("Email read failed", exc_info=True)
        return f"Error reading emails: {e}"


# ================= SEND EMAIL =================
def send_email(to="", subject="", body=""):
    try:
        logger.info(f"Sending email to {to}")

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        logger.info("Email sent successfully")

        return f"Email sent to {to}"

    except Exception as e:
        logger.error("Email send failed", exc_info=True)
        return f"Error sending email: {e}"