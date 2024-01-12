import os
import googleapiclient.discovery
from pytube import YouTube
import os
from urllib.parse import parse_qs, urlparse



api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = 'DeveloperKey'

playlist_url = input("copy your url play list: ")
print(playlist_url)

if not playlist_url:
    url = 'https://www.youtube.com/playlist?list=FLG8bKGKexijTiGcvNvMSyJQ'
    # url = 'https://www.youtube.com/playlist?list=PLWwaplyqkgeGubIV6S-lJLcOh-nMMdceO'
    print("hector bullejos")
else:
    url = playlist_url



#extract playlist id from url

query = parse_qs(urlparse(url).query, keep_blank_values=True)
playlist_id = query["list"][0]

print(f'get all playlist items links from {playlist_id}')
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyCtd_reWN_KGZ1UG_9t3ksydxBaMrnurRU")

request = youtube.playlistItems().list(
    part = "snippet",
    playlistId = playlist_id,
    maxResults = 20

)
response = request.execute()

playlist_items = []
while request is not None:
    response = request.execute()
    playlist_items += response["items"]
    request = youtube.playlistItems().list_next(request, response)

print(f"total: {len(playlist_items)}")
# print([f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
#     for t in playlist_items
# ])
link_list = [f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
    for t in playlist_items
]




cwd = os.getcwd()
folder_name = input("Name your folder: ")
print(folder_name)
folder_path = os.path.join(cwd, folder_name)
os.mkdir(folder_path)
number_of_songs = input("number of songs: ")
print(number_of_songs)

count = 0
for j in range(int(number_of_songs)):
    print(link_list[j], count)
    count = count + 1
    i = link_list[j]

    yt = YouTube(str(i))

        # extract only audio
    video = yt.streams.filter(only_audio=True).first()
    try:

        # check for destination to save file
        # print("Enter the destination (leave blank for current directory)")
        destination = str(folder_path)

        # download the file
        out_file = video.download(output_path=destination)

        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.wav'
        os.rename(out_file, new_file)

        # result of success
        print(yt.title + " has been successfully downloaded.")
    except Exception as e:
        print("############################### Error: ", e , "\nin song:", j)
