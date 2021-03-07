import os
import time
import spotipy
import spotipy.util as util
from spotipy import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import discord
from discord.ext import commands
from discord.utils import get
import pandas as pd
import numpy as np
from matplotlib import style
import matplotlib.pyplot as plt
from itertools import cycle

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = os.path.join(bot.sp_cache,f'.cache-{bot.sp_username}')
        self.colors = cycle(bot.plt_colors)
        token = util.prompt_for_user_token(
                                username=bot.sp_username,
                                scope=bot.sp_scope,
                                client_id=bot.sp_client_id,
                                client_secret=bot.sp_client_secret,
                                redirect_uri=bot.sp_redirect_uri,
                                cache_path=self.cache)

        self.sp = spotipy.Spotify(auth=token)
    
    @commands.command()
    async def playlist_stats(self, ctx, playlist_name='Big World'):
        playlist_id = await self.sp_search(playlist_name)
        tracks = await self.get_playlist_tracks(playlist_id)
        feats = await self.get_audio_features(tracks)
        df = await self.build_dataframe(feats)
        await self.display_playlist_means(df,playlist_name)
        img_path = os.path.join(self.bot.image,'spotify_{}.png'.format(playlist_name.replace(' ','_')))
        plt.savefig(img_path)
        await ctx.channel.send(file=discord.File(img_path))
        os.remove(img_path)
        plt.clf()

    async def sp_search(self,name,search_type='playlist'):
        types = search_type+'s'
        results = self.sp.search(name,type=search_type)
        for item in results[types]['items']:
            if name == item['name']:
                return item['id']
        return None

    async def get_playlist_tracks(self,playlist_id):
        tracks = self.sp.playlist_tracks(playlist_id)['items']

        if len(tracks) > 0:
            for i in range(len(tracks)):
                temp = {
                    'id':tracks[i]['track']['id'],
                    'title':tracks[i]['track']['name'],
                    'added_by':tracks[i]['added_by']['id'],
                    'artist':tracks[i]['track']['artists'][0]['name'],
                    'uri':tracks[i]['track']['uri'],
                }
                if temp['added_by'] == '':
                    temp['added_by'] = 'Spotify'
                else:
                    user_info = self.sp.user(temp['added_by'])
                    temp['added_by'] = user_info['display_name']
                
                tracks[i] = temp
            return tracks
        
        return None

    async def get_audio_features(self,tracks):
        track_ids = [track['id'] for track in tracks]
        tracks_features = self.sp.audio_features(track_ids)
        results = list(map(lambda dict1, dict2: {**dict1, **dict2}, tracks, tracks_features))

        return results

    async def build_dataframe(self,features):
        feats_df = pd.DataFrame(features)
        feats_df = feats_df.drop('key',axis=1)
        feats_df = feats_df.drop('mode',axis=1)
        feats_df = feats_df.drop('duration_ms',axis=1)
        feats_df = feats_df.drop('tempo',axis=1)
        feats_df = feats_df.drop('time_signature',axis=1)
        feats_df = feats_df.drop('loudness',axis=1)
        return feats_df

    async def calc_means(self,df):
        means = df.mean(axis=0)
        return means

    async def display_playlist_means(self,playlist_df,playlist_name):
        fig=plt.figure(figsize = (8,8))
        ax = fig.add_subplot(polar=True)
        num_features = 7
        angles = np.linspace(0,2*np.pi,num_features,endpoint=False)
        angles = np.concatenate((angles,[angles[0]])) 
            
        #iterate through the added_by column and generate feat_means from that
        for name in playlist_df.added_by.unique():
            temp_df = playlist_df[playlist_df.added_by == name]
            user_means = await self.calc_means(temp_df)
            stats = user_means.tolist()
            stats = np.concatenate((stats,[stats[0]]))
            color = next(self.colors)

            ax.plot(angles, stats, 'o-', linewidth=2, label =name, color=color)
            ax.fill(angles, stats, alpha=0.25, facecolor=color)

        labels = list(user_means.index)[:]
        labels.append(labels[0])
        ax.set_thetagrids(angles * 180/np.pi, labels , fontsize = 13)
        ax.set_rlabel_position(250)
        plt.yticks([0.2 , 0.4 , 0.6 , 0.8], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
        plt.ylim(0,1)
        ax.set_title('{} Audio Features'.format(playlist_name),{'fontsize':18,'fontweight':30})
        ax.grid(True)

        plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
        plt.tight_layout()

def setup(bot):
    bot.add_cog(Spotify(bot))