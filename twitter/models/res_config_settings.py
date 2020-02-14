from odoo import fields, models


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

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_consumer_key', self.twitter_consumer_key)
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_consumer_secret', self.twitter_consumer_secret)
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_access_token_key', self.twitter_access_token_key)
        self.env['ir.config_parameter'].sudo().set_param('media_connector.twitter_access_token_secret', self.twitter_access_token_secret)
