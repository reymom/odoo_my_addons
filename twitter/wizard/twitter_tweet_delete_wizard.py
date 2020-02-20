from odoo import models, fields, api


class TwitterTweetDeleteWizard(models.TransientModel):
    _name = 'twitter.tweet.delete.wizard'
    _description = 'Wizard: Delete a Tweet'

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
    twitter_tweet_ids = fields.Many2many(
        comodel_name='twitter.tweet',
        domain="[('twitter_screen_id', '=', twitter_screen_id)]"
    )

    def action_delete_tweets(self):
        api = self.env['twitter.screen']._get_api()
        for tweet in self.twitter_tweet_ids:
            api.DestroyStatus(status_id=tweet.twitter_id_str)
