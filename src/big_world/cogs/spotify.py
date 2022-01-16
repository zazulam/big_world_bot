import os
import re
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
        # self.token = util.prompt_for_user_token(
        #                         username=bot.sp_username,
        #                         scope=bot.sp_scope,
        #                         client_id=bot.sp_client_id,
        #                         client_secret=bot.sp_client_secret,
        #                         redirect_uri=bot.sp_redirect_uri,
        #                         cache_path=self.cache)
        self.cred_manager = SpotifyOAuth(
                                scope=bot.sp_scope,
                                client_id=bot.sp_client_id,
                                client_secret=bot.sp_client_secret,
                                redirect_uri=bot.sp_redirect_uri,
                                cache_path=self.cache)
        self.sp = spotipy.Spotify(oauth_manager=self.cred_manager,auth_manager=self.cred_manager)
        
    async def verify_token(self):
        token_info = self.cred_manager.get_cached_token()
        if self.cred_manager.is_token_expired(token_info):
            self.token = self.cred_manager.refresh_access_token(token_info['refresh_token'])
            self.sp = spotipy.Spotify(auth=self.token,auth_manager=self.cred_manager)

    @commands.command()
    async def playlist_stats(self, ctx, *args):
        await self.verify_token()
        if args:
            playlist_name = ' '.join(args)
        else:
            playlist_name = 'Big World'
        playlist_id = await self.sp_search(None,'playlist',playlist_name)
        tracks = await self.get_playlist_tracks(playlist_id)
        feats = await self.get_audio_features(tracks)
        df = await self.build_dataframe(feats)
        await self.display_playlist_means(df,playlist_name,show_users=True)
        img_path = os.path.join(self.bot.image,'spotify_{}.png'.format(playlist_name.replace(' ','_')))
        plt.savefig(img_path)
        await ctx.channel.send(file=discord.File(img_path))
        os.remove(img_path)
        plt.clf()

    @commands.command()
    async def sp_search(self, ctx: commands.Context, search_type, *args):
        await self.verify_token()
        types = search_type+'s'
        
        # Internal use from other commands
        if not ctx:
            results = self.sp.search(args[0],type=search_type)
            terms = args[0].lower()
            for item in results[types]['items']:
                if terms == re.sub('[^A-Za-z0-9 ]+','',item['name'].lower()):
                    print('found playlist',terms)
                    return item['id']
            return None
        # Actual command code
        else:
            search_terms = ' '.join(args).lower()
            search_terms = re.sub('[^A-Za-z0-9 ]+','',search_terms)
            results = self.sp.search(search_terms,type=search_type)
            for item in results[types]['items']:
                if search_terms == re.sub('[^A-Za-z0-9 ]+','',item['name'].lower()):
                    print('Match found: {} || {}'.format(search_terms,item['name']))
                    result = item['id']
                    break
            if result:
                # Check for type as Artist/Track/Playlist return info based on that
                if search_type.lower() == 'playlist':
                    #follow the same as playlist_stats
                    tracks = await self.get_playlist_tracks(result)
                elif search_type.lower() == 'track':

                    tracks = [item]
                elif search_type.lower() == 'artist':
                    # call self without ctx to get "This Is" playlist of artist
                    playlist_name = 'This Is {}'.format(item['name'])
                    search_terms = playlist_name
                    playlist_id = await self.sp_search(None,'playlist',search_terms)
                    print(playlist_id)
                    tracks = await self.get_playlist_tracks(playlist_id)
                else:
                    await ctx.channel.send("idk if Spotify has {}".format(types))
                    return
                
                feats = await self.get_audio_features(tracks)
                df = await self.build_dataframe(feats)
                await self.display_playlist_means(df,search_terms,show_users=False)
                img_path = os.path.join(self.bot.image,'spotify_{}.png'.format(search_terms.replace(' ','_')))
                plt.savefig(img_path)

                await ctx.channel.send(item['external_urls']['spotify'],file=discord.File(img_path))
                os.remove(img_path)
                plt.clf()
            else:
                await ctx.channel.send("Can't find whatever you're looking for")

    async def get_playlist_tracks(self,playlist_id):
        tracks = self.sp.playlist_tracks(playlist_id)['items']
        tracks_data = []
        if len(tracks) > 0:
            for i in range(len(tracks)):
                if tracks[i]['track'] is None:
                    continue
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
                
                tracks_data.append(temp)
            return tracks_data
        
        return None

    async def get_audio_features(self,tracks):
        track_ids = [track['id'] for track in tracks]
        tracks_features = self.sp.audio_features(track_ids)
        for i in range(len(tracks)):
            if 'added_by' not in tracks[i]:
                temp = {
                    'id':tracks[i]['id'],
                    'title':tracks[i]['name'],
                    'added_by':tracks[i]['artists'][0]['name'],
                    'artist':tracks[i]['artists'][0]['name'],
                    'uri':tracks[i]['uri'],
                }
                tracks[i] = temp
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

    async def display_playlist_means(self,playlist_df,playlist_name,show_users):
        fig=plt.figure(figsize = (8,8))
        ax = fig.add_subplot(polar=True)
        num_features = 7
        angles = np.linspace(0,2*np.pi,num_features,endpoint=False)
        angles = np.concatenate((angles,[angles[0]])) 
            
       
        if show_users:
             #iterate through the added_by column and generate feat_means from that
            for name in playlist_df.added_by.unique():
                temp_df = playlist_df[playlist_df.added_by == name]
                user_means = await self.calc_means(temp_df)
                stats = user_means.tolist()
                stats = np.concatenate((stats,[stats[0]]))
                color = next(self.colors)

                ax.plot(angles, stats, 'o-', linewidth=2, label=name, color=color)
                ax.fill(angles, stats, alpha=0.25, facecolor=color)
        else:
            user_means = await self.calc_means(playlist_df)
            stats = user_means.tolist()
            stats = stats = np.concatenate((stats,[stats[0]]))
            color = next(self.colors)

            ax.plot(angles, stats, 'o-', linewidth=2, label=playlist_name, color=color)
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