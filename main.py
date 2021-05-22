import requests
from bs4 import BeautifulSoup
import os
import constants

def nt_notify():
    with requests.get("https://newtoki95.com/toki_bl",  headers=constants.headers) as req:
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        number = soup.select("#list-body > li > div.wr-num.hidden-xs")[6].text
        time = soup.select("#list-body > li > div.wr-date.hidden-xs > span")[3].text
        downloads = soup.select("#list-body > li > div.wr-down.hidden-xs")[6].text[1:].rstrip()
        title = soup.select("#list-body > li > div.wr-subject > a")[6].text.partition("  ")[2].rpartition(" ")[0]
        member = soup.select("#list-body > li > div.wr-name.hidden-xs > a > span")[6].text[1:].lstrip()
        category = soup.select("#list-body > li > div.wr-subject > a > span.tack-icon")[6].text
        link = soup.select("#list-body > li > div.wr-subject > a")[6]['href']

        print("첫번째:", number, time, downloads, title, member, category, link)

        with open(os.path.join(constants.BASE_DIR, 'latest.txt'), 'r+') as f_read:
            before_number = f_read.readline()
            if before_number != number:
                with open(os.path.join(constants.BASE_DIR, "latest.txt"), "w+") as f_write:
                    f_write.write(number)
                    f_write.close()

                if before_number <= number:
                    print(number, "번째", "새 글이 올라옴", "|", "제목:", title)

                    if category == "공유":
                        constants.bot.sendMessage(constants.chat_id,
                                                  text="분류: 공유" + "\n" + time + ": " + "\n" + member + "님의 " + str(number) +
                                                       "번째 새 글이 올라왔어요!" + '\n' + "다운로드 수" + ": " + downloads)
                        print(number, "번째", "새 공유탭 글이 올라옴")

            if 50 > int(downloads) > 0 and link not in constants.history and category != "공유":
                constants.history.insert(0, link)
                constants.history.pop()
                print(constants.history)
                constants.bot.sendMessage(constants.chat_id,
                                          text="첫번째 글:" + "\n" + "분류: " + category + " " + time + ": " + "\n" + member + "님의 "
                                               + str(number) + "번째 새 글이 올라왔어요!" + '\n' + "다운로드 수" + ": " + downloads
                                               + "\n" + "제목: " + title)

                print(number, "번째", "새 공유탭에 없는 공유글이 올라옴(1번째글)", "분류: ", category)

            number = soup.select("#list-body > li > div.wr-num.hidden-xs")[7].text
            time = soup.select("#list-body > li > div.wr-date.hidden-xs > span")[4].text
            downloads = soup.select("#list-body > li > div.wr-down.hidden-xs")[7].text[1:].rstrip()
            title = \
                soup.select("#list-body > li > div.wr-subject > a")[7].text.partition("  ")[2].rpartition(" ")[0]
            member = soup.select("#list-body > li > div.wr-name.hidden-xs > a > span")[7].text[1:].lstrip()
            category = soup.select("#list-body > li > div.wr-subject > a > span.tack-icon")[7].text
            link = soup.select("#list-body > li > div.wr-subject > a")[7]['href']
            print("두번째:", number, time, downloads, title, member, category, link)

            if 50 > int(downloads) > 0 and link not in constants.history and category != "공유" and not (time[-2] == '분' and int(time[:-2]) > 10):
                constants.history.insert(0, link)
                constants.history.pop()
                print(constants.history)
                constants.bot.sendMessage(constants.chat_id,
                                          text="첫번째 글:" + "\n" + "분류: " + category + " " + time + ": " + "\n" + member + "님의 "
                                               + str(number) + "번째 새 글이 올라왔어요!" + '\n' + "다운로드 수" + ": " + downloads
                                               + "\n" + "제목: " + title)

                print(number, "번째", "새 공유탭에 없는 공유글이 올라옴(2번째글)", "분류: ", category)
                

def main():
    try:
        nt_notify()

    except requests.exceptions.ChunkedEncodingError:
        print("에러가 발생했습니다. (ChunkedEncodingError) 다시 연결하는 중...")

    except IndexError:
        if constants.server_state == 0:
            constants.bot.sendMessage(constants.chat_id,
                                          text="서버 오류/문제 생김")
        constants.server_state = 1
        print("에러가 발생했습니다. (ConnectionError) 다시 연결하는 중...")

    else:
        if constants.server_state == 1:
                    constants.bot.sendMessage(constants.chat_id, text="서버 오류/문제 해결됨")
        constants.server_state = 0