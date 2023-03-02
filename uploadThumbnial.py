from PIL import Image, ImageFont, ImageDraw
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload


API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def create_thumbnail(videoId, views):
  img = Image.new('RGB', (1280,720), (0,0,0))
  font = ImageFont.truetype('Rubik-Medium.ttf', 100)
  text = f'{views} views' 
  edit_image = ImageDraw.Draw(img)
  edit_image.text((15,15), text, (237, 230, 211), font = font)
  img.save(f'{videoId}.png')


def upload_thumbnail(credentials):

  youtube = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)
  channel = youtube.channels().list(mine = True, part='contentDetails').execute()
  channelId = channel['items'][0]['id']
  popular = youtube.search().list(part = 'snippet', channelId = channelId, maxResults = 5, order = 'viewCount').execute()
  for item in popular['items'] :
    if item['id']['kind'] == 'youtube#channel':
      continue
    videoId = item['id']['videoId']
    video = youtube.videos().list(id = videoId, part = 'statistics').execute()
    views = video['items'][0]['statistics']['viewCount']
    create_thumbnail(videoId, views)
    request = youtube.thumbnails().set(videoId = videoId, media_body = MediaFileUpload(f'{videoId}.png')).execute()
    print(views)