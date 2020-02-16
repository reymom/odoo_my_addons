from odoo import models, fields, api


class TwitterTweet(models.Model):
    _name = 'twitter.tweet'
    _description = 'Twitter Tweet'

    twitter_screen_id = fields.Many2one(
        comodel_name='twitter.screen',
        required=True
    )
    display_name = fields.Char(
        compute='_compute_display_name'
    )
    twitter_id_str = fields.Char()
    date_creation = fields.Char()
    author = fields.Char()
    body = fields.Text()
    link = fields.Char()
    likes = fields.Integer()
    retweets = fields.Integer()

    @api.depends('twitter_id_str')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = 'Tweet ' + rec.twitter_id_str

    _sql_constraints = [
        ('twitter_id', 'unique( twitter_id_str )', 'Id must be unique.')
    ]
