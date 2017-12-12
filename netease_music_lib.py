# coding=utf-8
import json,sys
import urllib
import urllib.parse
import urllib.request
import NEMbox.api
import requests

class NeteaseMusic(object):
    def __init__(self):
        self.ne = NEMbox.api.NetEase()

    def get_song_info_by_name(self, name, artist=''):
        song = self.search_song_by_name(name, artist)
        if not song:
            return None, None, None, None
        song_url, quality = NEMbox.api.geturl_new_api(song)
        song_id = song['id']
        song_name = song['name']
        song_artist = song['artists'][0]['name']
        return song_id, song_name, song_artist, song_url

    def get_song_info_by_id(self, song_id):
        info = self.ne.songs_detail_new_api([song_id])
        print(info)

    def search_song_by_name(self, name, artist):

        params ={
            's': name,
            'type': 1,
            'offset': 0,
            'sub': 'false',
            'limit': 20
        }
        search =requests.post('http://music.163.com/api/search/get',data=params)
        resp = search.content
        resp_js = json.loads(resp.decode('utf-8'))
        #print(resp_js)
        if resp_js['code'] == 200 and resp_js['result']['songCount'] > 0:
            result = resp_js['result']
            if artist == '':
                song = result['songs'][0]
            else:
                for song in result['songs']:
                    if song['artists'][0][name] == artist:
                        break
                else:
                    song = result['songs'][0]
            # return song['id'], song['name'], song['artists'][0][name]
            return song
        else:
            return None


if __name__ == '__main__':
    app = NeteaseMusic()
    print(app.get_song_info_by_name(" ".join(sys.argv[1:])))
    #print(app.get_song_info_by_id(725692))
