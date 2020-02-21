import base64
from io import BytesIO
from PIL import Image

from odoo import models, fields, api
from odoo.exceptions import UserError


class TwitterPersonalScreenWizard(models.TransientModel):
    _name = 'twitter.personal.screen.wizard'
    _description = 'Wizard: Update my Profile'

    @api.model
    def _get_user_authenticated(self):
        screen_obj = self.env['twitter.screen']
        api = screen_obj._get_api()
        screen = api.VerifyCredentials().AsDict()['screen_name']
        auth_user = screen_obj.search([('screen', '=', screen)])
        if auth_user:
            return auth_user
        else:
            raise UserError('Screen associated to the API keys is not present in the records.')

    twitter_screen_id = fields.Many2one(
        comodel_name='twitter.screen',
        required=True,
        default=_get_user_authenticated,
        readonly=True
    )
    author = fields.Text(
        related='twitter_screen_id.name'
    )
    description = fields.Text(
        related='twitter_screen_id.description'
    )
    image = fields.Binary(
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
    new_name = fields.Text()
    new_description = fields.Text()
    new_image = fields.Binary()

    def update_profile(self):
        screen_obj = self.env['twitter.screen']
        api = screen_obj._get_api()
        name = self.new_name or None
        description = self.new_description or None
        if self.new_image:
            im = Image.open(BytesIO(base64.b64decode(self.new_image)))
            im.save('img.png')
            image='img.png'
        else:
            image = None

        api.UpdateProfile(name=name, description=description)
        api.UpdateImage(image=image)
        self.twitter_screen_id.count_screen_stats()
        return api
