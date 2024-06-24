from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
import tqdm
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


header = Headers(
    browser='chrome',
    os="win",
    headers=True
)
headers = header.generate()
# print(headers)
# url = input("Enter URL anime:\n")
#
# request = requests.get(url, headers=headers)
# soup = BeautifulSoup(request.text, "html.parser")
#
# seasons = soup.find_all("div", class_="the_invis")
# AmountSeason = 0
# for season in seasons:
#     AmountSeason += 1
#
# print(f"Amount Season: {AmountSeason}")
def season(url):
    """
    Подсчёт количества сезонов
    :param url: url для парсинга
    :return: количество сезонов
    """
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    amount_season = 0
    seasons = soup.find_all("div", class_="the_invis")
    for _ in seasons:
        amount_season += 1
    return amount_season


def get_season_episodes(url, season_choose):
    """
    Получение ссылок серии из сезона
    :param url:передача ссылки на сезон
    :param season_choose:выбор сезона
    :return:список ссылками на серии
    """
    if season_choose != 0:
        url += f"season-{season_choose}"
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    episodes = soup.find_all("a", class_="short-btn green video the_hildi")
    href_list = []
    for href in episodes:
        href_list.append(f"https://jut.su{href.get('href')}")
    if not href_list:
        episodes = soup.find_all("a", class_="short-btn black video the_hildi")
        for href in episodes:
            href_list.append(f"https://jut.su{href.get('href')}")
    return href_list


def download_video(url, episode_number, path, season_choose):
    try:
        print("start downloading video")
        response = requests.get(url=url, headers=headers)
        with open(f"{path}\\video{1 if season_choose == 0 else season_choose}-{episode_number}.mp4", 'wb') as file:
            file.write(response.content)
            print("Video downloaded successfully")
        return True
    except Exception as e:
        return f"Oops!\n{e}"


def get_video_episode(path, episodes_links, season_choose, quality):
    episode_number = 1
    for episode in episodes_links:
        request = requests.get(episode, headers=headers)
        soup = BeautifulSoup(request.text, "html.parser")
        link = soup.find("source", label=f"{quality}").get('src')
        if download_video(link, episode_number, path, season_choose):
            print(f"Downloading video!\t{episode_number}")
            episode_number += 1
    return True



def main():
    url = input("Enter URL anime:\n")
    path = str(input("Enter path to save video\n"))
    quality = input("choose video quality:\n360p\t480p\t720p\t1080p\n")
    amount_season = season(url)
    season_choose = 0
    if amount_season != 0:
        season_choose = input("Choose a season\t")
    episodes_links = get_season_episodes(url, season_choose)
    if get_video_episode(path, episodes_links, season_choose, quality):
        print("FINISH!!!")
    # print(episodes_link)
    # print(AmountSeason)


if __name__ == "__main__":
    while True:
        start = input("Start download season? y/n\t")
        if start == "y":
            main()
        else:
            print("bye!")
            exit(0)
