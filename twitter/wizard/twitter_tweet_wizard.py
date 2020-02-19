import base64
from io import BytesIO
from PIL import Image

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TwitterTweetWizard(models.TransientModel):
    _name = 'twitter.tweet.wizard'
    _description = 'Wizard: Post a Tweet'

    @api.model
    def _get_user_authenticated(self):
        screen_obj = self.env['twitter.screen']
        api = screen_obj._get_api()
        screen = api.VerifyCredentials().AsDict()['screen_name']
        auth_user = screen_obj.search([('screen', '=', screen)])
        if auth_user:
            return auth_user
        else:
            auth_user = screen_obj.create({
                'screen': screen,
            })
            auth_user.count_screen_stats()
            return auth_user

    twitter_screen_id = fields.Many2one(
        comodel_name='twitter.screen',
        required=True,
        default=_get_user_authenticated,
        readonly=True
    )
    author = fields.Text(
        related='twitter_screen_id.name'
    )
    description_author = fields.Text(
        string='Description',
        related='twitter_screen_id.description'
    )
    image_author = fields.Binary(
        related='twitter_screen_id.image'
    )
    count_following = fields.Integer(
        string='Following',
        related='twitter_screen_id.count_following'
    )
    count_followers = fields.Integer(
        string='Followers',
        related='twitter_screen_id.count_followers'
    )
    body = fields.Text()
    media_image = fields.Binary()

    @api.constrains('body')
    def check_body_maximum_length(self):
        for rec in self:
            if len(rec.body) >= 280:
                raise ValidationError(_('Twitter accepts a maximum of 280 characters!'))

    def post_tweet(self):
        if self.media_image:
            im = Image.open(BytesIO(base64.b64decode(self.media_image)))
            im.save('img.png', 'PNG')
            media = open('img.png', 'rb')
        else:
            media = None
        return self.env['twitter.screen']._get_api().PostUpdate(status=self.body, media=media)
