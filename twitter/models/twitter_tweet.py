from datetime import datetime
import re

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class TwitterTweet(models.Model):
    _name = 'twitter.tweet'
    _description = 'Twitter Tweet'

    twitter_screen_id = fields.Many2one(
        comodel_name='twitter.screen',
        required=True,
        ondelete='cascade'
    )
    display_name = fields.Char(
        compute='_compute_display_name'
    )
    twitter_id_str = fields.Char()
    date_creation = fields.Datetime()
    relative_time_creation = fields.Char(
        string="Time Ago",
    )
    author = fields.Char()
    body = fields.Text()
    body_html = fields.Html(
        compute='_compute_body_html',
        store=True
    )
    likes = fields.Integer()
    twitter_attachment_ids = fields.One2many(
        comodel_name='twitter.attachment',
        inverse_name='twitter_tweet_id',
    )
    retweets = fields.Integer()
    favorite_user_ids = fields.Many2many(
        comodel_name='res.users',
        related='twitter_screen_id.favorite_user_ids'
    )

    _sql_constraints = [
        ('twitter_id', 'unique( twitter_id_str )', 'Id must be unique.')
    ]

    @api.depends('twitter_id_str')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = 'Tweet nº ' + rec.twitter_id_str

    @api.model
    def create(self, vals):
        if vals.get('date_creation'):
            date_creation = datetime.strptime(vals.get('date_creation'), DEFAULT_SERVER_DATETIME_FORMAT)
            lapse_time =  datetime.now() - date_creation
            if lapse_time.days < 1:
                if lapse_time.seconds < 60*60:
                    lapse = str(int(lapse_time.seconds/(60))) + 'min'
                else:
                    lapse = str(int(lapse_time.seconds/(60*60))) + 'h'
            else:
                if date_creation.year == datetime.now().year:
                    lapse = str(date_creation.strftime('%d %b.'))
                else:
                    lapse = str(date_creation.strftime('%d %b %Y'))
            vals['relative_time_creation'] = lapse
        return super(TwitterTweet, self).create(vals)

    @api.depends('body')
    def _compute_body_html(self):
        """
        Manages links:
        - Takes the body of a tweet and makes hashtags visible as a link
        - Moreover, it search for the link of the tweet as well as other possible links.
        """
        for rec in self:
            body_html = rec.body
            # Links
            pattern = '(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
            links = re.findall(pattern, body_html)
            for link in links:
                link_html = '<a target="_blank" href="' + link + '">' + link + '</a>'
                body_html = re.sub(link, link_html, body_html)
            # Hashtags
            hashtags = re.findall(r'#(\w+)', body_html)
            for hashtag in hashtags:
                link_hashtag = 'https://twitter.com/hashtag/{}?src=hashtag_click'.format(hashtag)
                link_html = '<a target="_blank" href="' + link_hashtag + '">#' + hashtag + '</a> '
                body_html = re.sub('#' + hashtag + ' ', link_html, body_html)
            users =  re.findall(r'@(\w+)', body_html)
            for user in users:
                link_user = 'https://twitter.com/{}'.format(user)
                link_html = '<a target="_blank" href="' + link_user + '">@' + user + '</a> '
                body_html = re.sub('@' + user + ' ', link_html, body_html)
            rec.body_html = body_html
