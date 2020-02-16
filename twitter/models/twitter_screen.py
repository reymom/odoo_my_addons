import base64
import logging
import urllib.request

import twitter
from twitter import TwitterError
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class TwitterScreen(models.Model):
    _name = 'twitter.screen'
    _description = 'Twitter Screen'

    screen = fields.Text(
        help='Twitter Screen Search'
    )
    name = fields.Text(
        help='Name on Twitter'
    )
    description = fields.Text(
        help='Official Account Description'
    )
    image = fields.Binary()
    twitter_tweets_ids = fields.One2many(
        comodel_name='twitter.tweet',
        inverse_name='twitter_screen_id',
    )
    count_screen_tweets = fields.Integer(
        string='Total Tweets',
        store=True,
    )
    count_following = fields.Integer(
        string='Following',
        store=True
    )
    count_followers = fields.Integer(
        string='Followers',
        store=True
    )
    active = fields.Boolean(
        default=True
    )

    def count_screen_stats(self):
        api = self._get_api()
        screen_stats = api.GetUser(
            screen_name=self.screen,
        ).AsDict()
        keys = screen_stats.keys()
        name = screen_stats['name']
        description = screen_stats['description'] if 'description' in keys else None
        image_url = screen_stats['profile_image_url'] if 'profile_image_url' in keys else None
        image_data = urllib.request.urlopen(image_url).read()
        count_screen_tweets = screen_stats['listed_count'] if 'listed_count' in keys else None
        count_following = screen_stats['friends_count'] if 'friends_count' in keys else None
        count_followers = screen_stats['followers_count'] if 'followers_count' in keys else None
        self.update({
            'name': name,
            'description': description,
            'image': base64.encodestring(image_data),
            'count_screen_tweets': count_screen_tweets,
            'count_following': count_following,
            'count_followers': count_followers
        })

    def _get_api(self, tweet_mode=None):
        try:
            params = self.env['ir.config_parameter'].sudo()
            twitter_consumer_key = params.get_param('media_connector.twitter_consumer_key')
            twitter_consumer_secret = params.get_param('media_connector.twitter_consumer_secret')
            twitter_access_token_key = params.get_param('media_connector.twitter_access_token_key')
            twitter_access_token_secret = params.get_param('media_connector.twitter_access_token_secret')
            api = twitter.Api(
                twitter_consumer_key, twitter_consumer_secret, twitter_access_token_key, twitter_access_token_secret,
                tweet_mode=tweet_mode
            )
            api.VerifyCredentials()
            return api
        except:
            return TwitterError

    def action_get_tweets(self):
        for rec in self:
            rec._get_tweets()

    def _get_tweets(self):
        api = self._get_api(tweet_mode='extended')
        timeline = api.GetUserTimeline(
            screen_name=self.screen,
            include_rts=False,
            count=10
        )
        tweets = [i.AsDict() for i in timeline]
        tweet_obj = self.env['twitter.tweet']
        twitter_end = 'https://t.co/'
        self.twitter_tweets_ids.unlink()
        for t in tweets:
            print(t)
            try:
                id_str = t['id_str']
                date_creation = t['created_at']
                likes = t['favorite_count']
                retweets = t['retweet_count']
                content = t['full_text'].split(twitter_end)
                tweet_obj.create({
                    'twitter_screen_id': self.id,
                    'twitter_id_str': id_str,
                    'date_creation': date_creation,
                    'author': self.screen,
                    'body': content[0],
                    'link': twitter_end + content[1],
                    'likes': likes,
                    'retweets': retweets
                })
            except:
                continue
