import telegram
import os

token = '1797942385:AAEcs9PhA0P0gBbbpGALQAq1v-NPNXs-S3E'
chat_id = "-1001493236873"
bot = telegram.Bot(token=token)
index_error_count = 0
connection_error_count = 0
before_number = os.environ.get("before_number")
before_title = ""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
message_sent = False

print("초기 설정 완료.")
bot.sendMessage(chat_id, text="초기 설정을 완료하였습니다.")