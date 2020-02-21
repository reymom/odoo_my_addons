import twitter

from odoo import api, fields, models, _
from odoo.exceptions import AccessError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_twitter = fields.Boolean(
        help='Allows you to synchronize with Twitter'
    )
    twitter_consumer_key = fields.Char(
        help='Twitter API Consumer Key',
        config_parameter='media_connector.twitter_consumer_key'
    )
    twitter_consumer_secret = fields.Char(
        help='Twitter API Consumer Secret',
        config_parameter='media_connector.twitter_consumer_secret'
    )
    twitter_access_token_key = fields.Char(
        help='Twitter API Access Token Key',
        config_parameter='media_connector.twitter_access_token_key'
    )
    twitter_access_token_secret = fields.Char(
        help='Twitter API Access Token Secret',
        config_parameter='media_connector.twitter_access_token_secret'
    )
    twitter_number_last_tweets = fields.Integer(
        help='The number of Last Tweets to Synchronize',
        config_parameter='media_connector.twitter_number_last_tweets',
        default=5
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_consumer_key', self.twitter_consumer_key)
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_consumer_secret', self.twitter_consumer_secret)
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_access_token_key', self.twitter_access_token_key)
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_access_token_secret', self.twitter_access_token_secret)
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_number_last_tweets', self.twitter_number_last_tweets)

    @api.model
    def create(self, vals):
        TwitterConfig = super(ResConfigSettings, self).create(vals)
        if vals.get('twitter_consumer_key') and vals.get('twitter_consumer_secret') and vals.get('twitter_access_token_key') and vals.get('twitter_access_token_secret'):
            try:
                api = twitter.Api(
                    vals.get('twitter_consumer_key'), vals.get('twitter_consumer_secret'),
                    vals.get('twitter_access_token_key'), vals.get('twitter_access_token_secret')
                )
                screen_obj = self.env['twitter.screen']
                screen = api.VerifyCredentials().AsDict()['screen_name']
                if not screen_obj.search([('screen', '=', screen)]):
                    screen_obj.create({
                        'screen': screen,
                        'my_screen': True
                    })
            except:
                raise AccessError(_('Incorrect Keys.'))
        else:
            raise AccessError(_('You have to declare keys to retrieve information from Twitter.'))
        return TwitterConfig

    def write(self, vals):
        TwitterConfig = super(ResConfigSettings, self).write(vals)
        if vals.get('twitter_consumer_key') and vals.get('twitter_consumer_secret') \
                and vals.get('twitter_access_token_key') and vals.get('twitter_access_token_secret'):
            try:
                api = twitter.Api(
                    vals.get('twitter_consumer_key'), vals.get('twitter_consumer_secret'),
                    vals.get('twitter_access_token_key'), vals.get('twitter_access_token_secret')
                )
                screen_obj = self.env['twitter.screen']
                screen = api.VerifyCredentials().AsDict()['screen_name']
                if not screen_obj.search([('screen', '=', screen)]):
                    screen_obj.create({
                        'screen': screen,
                        'my_screen': True
                    })
            except:
                raise AccessError(_('Incorrect Keys.'))
        return TwitterConfig
