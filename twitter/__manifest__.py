{
    "name": "Twitter",
    "summary": "Connects with Twitter",
    "version": "12.0.1.0.0",
    "category": "",
    "website": "",
    "author": "",
    "license": "AGPL-3",
    "depends": [
    ],
    "description": """
Twitter
===============
This module connects, organizes and display content of your social network accounts like Twitter
        """,

    "data": [
        'security/twitter_security.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/twitter_tweet_views.xml',
        'views/twitter_screen_views.xml',
        'views/twitter_menu.xml',
        'wizard/twitter_tweet_wizard.xml',
        'wizard/twitter_personal_screen_wizard.xml',
        'wizard/twitter_tweet_delete_wizard.xml',
        'data/ir_cron_data.xml'
    ],
}
