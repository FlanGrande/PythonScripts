import requests
from bs4 import BeautifulSoup

# Step 1: Set the base URL of the website
base_url = 'https://downloads.khinsider.com'

# Step 2: Access the album page (or the first link in the process)
album_url = f'{base_url}/game-soundtracks/album/the-urbz-sims-in-the-city-gamerip'
response = requests.get(album_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Find all download links on the album page
track_links = soup.select('.playlistDownloadSong a')

# Step 4: Loop through the track links and visit each page
for link in track_links:
    track_page_url = base_url + link['href']
    track_response = requests.get(track_page_url)
    track_soup = BeautifulSoup(track_response.content, 'html.parser')

    # Step 5: Find the actual MP3 download link
    download_link = track_soup.select("#pageContent > p:nth-child(9) > a")[0]["href"]

    # Step 6: Download the file
    mp3_response = requests.get(download_link)
    file_name = download_link.split('/')[-1]  # Extract the file name from the URL
    with open(file_name, 'wb') as file:
        file.write(mp3_response.content)
    print(f"Downloaded {file_name}")
