from odoo import models, fields, api


class TwitterTweet(models.Model):
    _name = 'twitter.tweet'
    _description = 'Twitter Tweet'

    twitter_screen_id = fields.Many2one(
        comodel_name='twitter.screen',
        required=True
    )
    date_creation = fields.Char()
    author = fields.Char()
    body = fields.Text()
    likes = fields.Integer()
    retweets = fields.Integer()
