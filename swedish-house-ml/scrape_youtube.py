"""
Connecting to YouTube API and pulling back videos by keyword
and
Reference: https://github.com/youtube/api-samples/blob/master/python/search.py
TODO: Convert to class?
"""


import os
import jmespath
import time
from itertools import count
import config as cfg

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def youtube_search(options):
  youtube = build(cfg.YOUTUBE_API_SERVICE_NAME, cfg.YOUTUBE_API_VERSION,
    developerKey=cfg.YOUTUBE_API_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part='id,snippet',
    maxResults=options.max_results
  ).execute()

  videos = []


  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s (%s)' % (search_result['snippet']['title'],
                                 search_result['id']['videoId']))
    else:
        pass

  print('Videos:\n', '\n'.join(videos), '\n')


def pull_video_thumbnail():
    '''
    Youtube cover image URL: https://img.youtube.com/vi/<insert-youtube-video-id-here>/0.jpg
    Pull this with requests locally for now
    Eventually, put it in an S3 bucket
    :return:
    '''
    pass

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='querystring', default='Kygo')
  parser.add_argument('--max-results', help='Max results', default=25)
  args = parser.parse_args()

  try:
    youtube_search(args)
  except(HttpError):
    print('An HTTP error %d occurred:\n%s') % (e.resp.status, e.content)

