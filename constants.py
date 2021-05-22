import telegram
import os

token = '1797942385:AAEcs9PhA0P0gBbbpGALQAq1v-NPNXs-S3E'
chat_id = "-1001493236873"
bot = telegram.Bot(token=token)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
history = ["", "", "", "", "", ""]
server_state = 0