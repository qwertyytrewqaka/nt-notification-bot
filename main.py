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
        titles = soup.select("#list-body > li > div.wr-subject > a")
        temp = soup.select("#list-body > li > div.wr-subject > a")

        constants.before_number = constants.latest_number
        constants.latest_number = posts[6].text
        latest_link = temp[6]['href']
        latest_time = time[3].text
        latest_downloads = downloads[6].text[1:]
        latest_title = titles[6].text.partition("  ")[2].rpartition(" ")[0]
        name = soup.select('#list-body > li > div.wr-name.hidden-xs > a > span')
        latest_member = name[6].text[1:]

        with open(os.path.join(constants.BASE_DIR, 'latest.txt'), 'r+') as f_read:
            before_link = f_read.readline()

        if before_link != latest_link:
            constants.history[1] = constants.history[0]
            constants.history[0] = latest_link
            with open(os.path.join(constants.BASE_DIR, 'latest.txt'), 'w+') as f_write:
                f_write.write(latest_link)
                f_write.close()

            if constants.history[1] != latest_link:
                print(constants.latest_number, "번째", "새 글이 올라옴", "|", "제목:", latest_title)

                if latest_downloads not in {'0 ', ' 0 '} or latest_title in {"권한이 없는 게시물입니다. "}:
                    constants.bot.sendMessage(constants.chat_id,
                                              text=" " + latest_time + " : " + "\n" + latest_member + " 님의 " + str(
                                                  constants.latest_number) +
                                                   "번째 새 글이 올라왔어요!" + '\n' + "다운로드 수" + " : " + latest_downloads)
                    print(constants.latest_number, "번째", "새 공유 글이 올라옴")


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
