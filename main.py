import requests
from bs4 import BeautifulSoup
import os
import constants


def nt_notify():
    with requests.get("https://newtoki95.com/toki_bl") as req:
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.select('#list-body > li > div.wr-num.hidden-xs')
        time = soup.select("#list-body > li > div.wr-date.hidden-xs > span")
        downloads = soup.select("#list-body > li > div.wr-down.hidden-xs")
        title = soup.select("#list-body > li > div.wr-subject > a")
        latest_time = time[3].text
        latest_downloads = downloads[6].text[1:].replace(" ", "")
        latest_number = posts[6].text
        latest_title = title[6].text.partition("  ")[2].rpartition(" ")[0]
        name = soup.select('#list-body > li > div.wr-name.hidden-xs > a > span')
        latest_member = name[6].text[1:]

        with open(os.path.join(constants.BASE_DIR, 'latest.txt'), 'r+') as f_read:
            before_number = f_read.readline()

        if before_number != latest_number:
            with open(os.path.join(constants.BASE_DIR, 'latest.txt'), 'w+') as f_write:
                f_write.write(latest_number)
                f_write.close()

            if before_number < latest_number:
                constants.message_sent = False
                if constants.before_title != latest_title:
                    print(latest_number, "번째", "새 글이 올라옴", "|", "제목:", latest_title)
                else:
                    constants.bot.sendMessage(constants.chat_id, text="상추를 흔드는 글에 누가 답댓을 달아줬네요.")
                    print("요청 답글")

        if latest_downloads != "0" or latest_title in {"권한이 없는 게시물입니다. "}:
            if not constants.message_sent:
                constants.bot.sendMessage(constants.chat_id,
                                          text=" " + latest_time + " : " + "\n" + latest_member + " 님의 " + str(
                                              latest_number) +
                                               "번째 새 글이 올라왔어요!" + '\n' + "다운로드 수" + " : " + latest_downloads)
                constants.message_sent = True
                print(latest_number, "번째", "새 공유 글이 올라옴")


def main():
    try:
        nt_notify()

    except requests.exceptions.ChunkedEncodingError:
        print("에러가 발생했습니다. (ChunkedEncodingError) 다시 연결하는 중...")

    except requests.exceptions.ConnectionError:
        constants.connection_error_count += 1
        print("에러가 발생했습니다. (ConnectionError) 다시 연결하는 중...")
        if constants.connection_error_count >= 5:
            constants.connection_error_count = 0
            input("인터넷 연결을 확인해 주세요.(Press Any Key to Continue)")
            constants.bot.sendMessage(constants.chat_id, text="인터넷 연결이 끊어진 후 다시 연결되었습니다.")
