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

    def _get_default_favorite_user_ids(self):
        return [(6, 0, [self.env.uid])]

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
    favorite_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='screen_favorite_user_rel',
        column1='twitter_screen_id',
        column2='user_id',
        default=_get_default_favorite_user_ids,
        string='Favorite Users'
    )
    is_favorite = fields.Boolean(
        compute='_compute_is_favorite',
        inverse='_inverse_is_favorite',
        string='Show Screen on Dashboard',
        help='Whether this screen should be displayed on the dashboard or not'
    )

    def _compute_is_favorite(self):
        for screen in self:
            screen.is_favorite = self.env.user in screen.favorite_user_ids

    def _inverse_is_favorite(self):
        sudo_screens = self.sudo()
        screens_to_favorite = sudo_screens.filtered(lambda screen: self.env.user not in screen.favorite_user_ids)
        screens_to_favorite.write({'favorite_user_ids': [(4, self.env.uid)]})
        (sudo_screens - screens_to_favorite).write({'favorite_user_ids': [(3, self.env.uid)]})
        return True

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
            'image': base64.encodebytes(image_data),
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

    @api.model
    def _get_tweets(self):
        api = self._get_api(tweet_mode='extended')
        timeline = api.GetUserTimeline(
            screen_name=self.screen,
            include_rts=False,
            count=3
        )
        tweets = [i.AsDict() for i in timeline]
        tweet_obj = self.env['twitter.tweet']
        tweet_attach_obj = self.env['twitter.attachment']
        self.twitter_tweets_ids.unlink()
        for t in tweets:
            try:
                keys = t.keys()
                id_str = t['id_str']
                date_creation = t['created_at']
                likes = t['favorite_count'] if 'favorite_count' in keys else None
                retweets = t['retweet_count'] if 'retweet_count' in keys else None
                content = t['full_text']
                new_tweet = tweet_obj.create({
                    'twitter_screen_id': self.id,
                    'twitter_id_str': id_str,
                    'date_creation': date_creation,
                    'author': self.screen,
                    'body': content,
                    'likes': likes,
                    'retweets': retweets
                })
                media = t['media'] if 'media' in keys else None
                new_tweet.twitter_attachment_ids.unlink()
                for med in media:
                    k = med.keys()
                    image_attach = med['media_url_https'] if 'media_url_https' in k else None
                    image_data = urllib.request.urlopen(image_attach).read()
                    tweet_attach_obj.create({
                        'twitter_tweet_id': new_tweet.id,
                        'image': base64.encodebytes(image_data)
                    })
            except:
                continue
