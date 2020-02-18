from odoo import models, fields


class TwitterAttachment(models.Model):
    _name = 'twitter.attachment'
    _description = 'Twitter Attachment'

    twitter_tweet_id = fields.Many2one(
        comodel_name='twitter.tweet',
        required=True
    )
    image = fields.Binary()
