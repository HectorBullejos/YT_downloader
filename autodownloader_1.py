import os
from datetime import datetime, timedelta
from pytube import YouTube
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery

def get_previous_month_folder():
    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Calculate the previous month
    previous_month = current_month - 1
    if previous_month == 0:
        previous_month = 12
        current_year -= 1

    # Create folder name
    folder_name = f"Madrid{current_year}{previous_month:02d}"

    return folder_name

def get_previous_month_url_count(folder_path, link_list, prev_folder_name):
    # Define the path for the first downloaded text file
    first_downloaded_file = os.path.join(prev_folder_name, "first_downloaded.txt")
    print("first downloaded file", first_downloaded_file)
    # Variable to store the URL from the previous month
    previous_month_url = None

    # Variable to count the number of songs before the previous month's URL
    url_count = 0

    # Check if the first_downloaded.txt file exists
    if os.path.exists(first_downloaded_file):
        # Read the URL from the file
        with open(first_downloaded_file, "r") as f:
            previous_month_url = f.read().strip()
            print(previous_month_url)

        # Count the number of songs before the previous month's URL
        for link in link_list:
            if link == previous_month_url:
                break
            url_count += 1

    return url_count

# Create Madrid folder for the current month
def create_madrid_folder():
    # Get current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Create folder name
    folder_name = f"Madrid{current_year}{current_month:02d}"

    # Create directory if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
        return folder_name
    else:
        print(f"Folder '{folder_name}' already exists.")
        return None

# Get current month's folder
created_folder = create_madrid_folder()

# If current month's folder is created, proceed with downloading
if created_folder:
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = 'Your_Developer_Key'

    url = 'https://www.youtube.com/playlist?list=FLG8bKGKexijTiGcvNvMSyJQ'

    # Extract playlist id from URL
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]

    print(f'get all playlist items links from {playlist_id}')
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyCtd_reWN_KGZ1UG_9t3ksydxBaMrnurRU")

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=20
    )
    response = request.execute()

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    print(f"total: {len(playlist_items)}")

    link_list = [f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
                 for t in playlist_items]

    cwd = os.getcwd()
    folder_name = created_folder
    print(folder_name)
    folder_path = os.path.join(cwd, folder_name)

    # Get the number of songs to download based on the previous month's URL
    prev_folder_name = get_previous_month_folder()
    print("prev_folder_name", prev_folder_name)
    number_of_songs_to_download = get_previous_month_url_count(folder_path, link_list, prev_folder_name)
    print(number_of_songs_to_download)

    count = 0

    # Define the path for the first downloaded text file
    first_downloaded_file = os.path.join(folder_path, "first_downloaded.txt")

    # Variable to track if the first URL has been downloaded
    first_url_downloaded = False

    for j in range(number_of_songs_to_download):
        print(link_list[j], count)
        count = count + 1
        i = link_list[j]

        yt = YouTube(str(i))

        # Extract only audio
        video = yt.streams.filter(only_audio=True).first()
        try:
            # Check for destination to save file
            destination = str(folder_path)

            # Download the file
            out_file = video.download(output_path=destination)

            # Save the file
            base, ext = os.path.splitext(out_file)
            new_file = base + '.wav'
            os.rename(out_file, new_file)

            # If the first URL has not been downloaded yet, store it in the text file
            if not first_url_downloaded:
                with open(first_downloaded_file, "w") as f:
                    f.write(i)
                first_url_downloaded = True

            # Result of success
            print(yt.title + " has been successfully downloaded.")
        except Exception as e:
            print("############################### Error: ", e, "\nin song:", j)
else:
    print("Error creating folder for the current month.")
