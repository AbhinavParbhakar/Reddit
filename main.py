from praw import Reddit
from praw.models import Submission,Comment
import json
import requests
import dotenv

env_vars = dotenv.dotenv_values('.env')

reddit = Reddit(client_id=env_vars['CLIENT_ID'],
                client_secret=env_vars['CLIENT_SECRET'],
                user_agent='myscript')

posts : list[Submission] = reddit.subreddit('Rateme').hot(limit=2)

posts = list(posts)
post = posts[1]

url = post.url + '.json'
requestResult = requests.get(url)
json_data = requestResult.json()


image_metadata = json_data[0]['data']['children'][0]['data']['media_metadata']
image_keys = list(image_metadata.keys())
image_links = []

for image_key in image_keys:
    print(image_key)
    link : str = image_metadata[image_key]['s']['u']
    link = link.replace('&amp;','&')
    image_links.append(link)


for i,link in enumerate(image_links):
    filename = f'Image {i+1}.jpg'
    result = requests.get(link,stream=True)
    
    with open(filename,'wb') as f:
        f.write(result.content)