import logging

import twitter
from twitter import TwitterError
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class TwitterScreen(models.Model):
    _name = 'twitter.screen'
    _description = 'Twitter Screen'

    name = fields.Text(
        help='Twitter Screen Search'
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
        last_tweet = api.GetUserTimeline(
            screen_name=self.name,
            count=1
        )[0].AsDict()
        count_screen_tweets = last_tweet['user']['listed_count']
        count_following = last_tweet['user']['friends_count']
        count_followers = last_tweet['user']['followers_count']
        description = last_tweet['user']['description']
        image_url = last_tweet['user']['profile_image_url']
        self.update({
            'count_screen_tweets': count_screen_tweets,
            'count_following': count_following,
            'count_followers': count_followers,
            'description': description,
            # 'image': base64 encoding from url
        })

    def _get_api(self):
        try:
            params = self.env['ir.config_parameter'].sudo()
            twitter_consumer_key = params.get_param('media_connector.twitter_consumer_key')
            twitter_consumer_secret = params.get_param('media_connector.twitter_consumer_secret')
            twitter_access_token_key = params.get_param('media_connector.twitter_access_token_key')
            twitter_access_token_secret = params.get_param('media_connector.twitter_access_token_secret')
            api = twitter.Api(
                twitter_consumer_key, twitter_consumer_secret, twitter_access_token_key, twitter_access_token_secret
            )
            api.VerifyCredentials()
            return api
        except:
            return TwitterError

    def action_get_tweets(self):
        for rec in self:
            rec._get_tweets()

    def _get_tweets(self):
        api = self._get_api()
        timeline = api.GetUserTimeline(
            screen_name=self.name,
            count=10
        )
        tweets = [i.AsDict() for i in timeline]
        tweet_obj = self.env['twitter.tweet']
        for t in tweets:
            if 'retweeted_status' in t.keys():
                date_creation = t['created_at']
                likes = t['retweeted_status']['favorite_count']
                retweets = t['retweet_count']
                body = t['text']
                tweet_obj.create({
                    'twitter_screen_id': self.id,
                    'date_creation': date_creation,
                    'author': self.name,
                    'body': body,
                    'likes': likes,
                    'retweets': retweets
                })
