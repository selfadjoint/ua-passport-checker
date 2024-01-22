import requests as req
import re
import os
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Constants
REG_URL = 'https://pasport.org.ua/solutions/checker'
CHECK_URL = 'https://dmsu.gov.ua/services/docstate.html'

session = req.Session()


def check_last_update(url):
    """
    Checks the last database update timestamp
    """
    try:
        check_page = req.get(url)
        soup = BeautifulSoup(check_page.content, 'html.parser')
        timestamp_tag = soup.find('p', style="color:#02A411")

        if timestamp_tag:
            timestamp_text = timestamp_tag.get_text().strip()
            timestamp = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', timestamp_text)
            if timestamp:
                return datetime.strptime(timestamp.group(), '%Y-%m-%d %H:%M:%S').replace(
                    tzinfo=pytz.timezone('Europe/Kiev'))

        raise ValueError("Timestamp not found in HTML")
    except Exception as e:
        logging.error(f"Error in check_last_update: {e}")
        raise


def check_passport(series, number):
    """
    Checks the passport status
    """
    headers = {
        'Host': 'pasport.org.ua',
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    body = {
        'doc_service': 2,
        'doc_age': 0,
        'doc_2_select': 1,
        'doc_2_series': series,
        'doc_2_number6': number
    }
    try:
        response = session.post(REG_URL, data=body, headers=headers)
        response.raise_for_status()
        status = response.json()['0']['statusDate'] + ': ' + re.sub(r'<[^>]+>', '', response.json()['send_status_msg'])
        return status
    except req.exceptions.RequestException as e:
        logging.error(f"Failed to check passport: {e}")
        return False


def send_message(token, chat_id, message):
    """
    Sends status to Telegram
    """
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': chat_id, 'text': message}
        response = req.post(url, data=data)
        return response.json()
    except Exception as e:
        logging.error(f"Error in send_message: {e}")


def lambda_handler(event=None, context=None):
    """
    Lambda function handler
    """
    try:
        logging.info("Lambda function started")
        now = datetime.now(pytz.timezone('Europe/Kiev'))
        last_update = check_last_update(CHECK_URL)

        if now <= last_update + timedelta(minutes=15) or 'test' in event:
            series = os.environ['PASSPORT_SERIES']
            number = os.environ['PASSPORT_NUMBER']
            status = check_passport(series, number)
            if status:
                token = os.environ['TELEGRAM_TOKEN']
                chat_id = os.environ['TELEGRAM_CHAT_ID']
                message = f"Останнє оновлення бази даних: {last_update.strftime('%d.%m.%Y %H:%M:%S')}\n\n{status}"
                send_message(token, chat_id, message)

                logging.info("Status checked and message sent")
                return {'statusCode': 200, 'body': message}
            else:
                logging.info("Status check failed")
        else:
            logging.info("No updates within the last 15 minutes")

        return {'statusCode': 200, 'body': 'No updates'}
    except Exception as e:
        logging.error(f"Error in lambda_handler: {e}")
        return {'statusCode': 500, 'body': 'Error occurred'}


if __name__ == '__main__':
    lambda_handler()
