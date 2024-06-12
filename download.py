# import requests
# import os
# from urllib.parse import urlparse

# def download_image(url, save_dir):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             parsed_url = urlparse(url)
#             filename = os.path.basename(parsed_url.path)
#             filepath = os.path.join(save_dir, filename)
#             with open(filepath, 'wb') as f:
#                 f.write(response.content)
#             print("Image downloaded successfully to:", filepath)
#         else:
#             print("Failed to download image:", response.status_code)
#     except Exception as e:
#         print("Error occurred while downloading image:", str(e))

# # Example usage:
# url = "https://private-user-images.githubusercontent.com/81317364/330426025-d73f36c8-2867-4802-97dd-ceca5173e103.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTgxOTAyMTYsIm5iZiI6MTcxODE4OTkxNiwicGF0aCI6Ii84MTMxNzM2NC8zMzA0MjYwMjUtZDczZjM2YzgtMjg2Ny00ODAyLTk3ZGQtY2VjYTUxNzNlMTAzLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjEyVDEwNTgzNlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWE3ZjUxMDk4ZTU5OTQwNDlmM2RjYzBmMjNjYjlkNTAzZmY3ZWFlZGI2YzQ3MjhjN2JmNDI5NGRjMzFiY2VkMzEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.56g3hx2DkHn_1VTgYE5iL0QPfD2wiiZ5ufviSzUY5zk"
# save_directory = "images"

# if not os.path.exists(save_directory):
#     os.makedirs(save_directory)

# download_image(url, save_directory)

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

def download_image(url, save_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            filepath = os.path.join(save_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print("Image downloaded successfully to:", filepath)
        else:
            print("Failed to download image:", response.status_code)
    except Exception as e:
        print("Error occurred while downloading image:", str(e))

def download_images_from_github_issue(issue_url, save_dir):
    try:
        response = requests.get(issue_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            image_tags = soup.find_all('img')
            for img in image_tags:
                img_url = img.get('src')
                if img_url:
                    download_image(img_url, save_dir)
        else:
            print("Failed to fetch issue page:", response.status_code)
    except Exception as e:
        print("Error occurred while downloading images:", str(e))

# Example usage:
issue_url = "https://github.com/emqx/emqx/issues/13045"
save_directory = "images_from_issue"

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

download_images_from_github_issue(issue_url, save_directory)

