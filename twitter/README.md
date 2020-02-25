Twitter Connector
-----------------

The App connects with Twitter, allowing you to manage your account and display your favourite Tweets.

![Alt text](static/images/MyTwitterMenu.png?raw=true "Menu")

This has been done in order to practice and get used to Odoo's programming tools, not to imitate the premium 
app built by Odoo called Social Marketing, which certainly has a kinder design and more functionality. 
Nevertheless it is very complete and integrates many features, so it would be useful for example for a tutorial. 
For building it, I have used the library
[python-twitter](https://github.com/bear/python-twitter), which helped me not to overload the code
writing all the methods from raw and it is itself pretty good. So thank you and congratulations 
[jeremylow](https://github.com/jeremylow) for this library.

# Functionality

In the Configuration you put your Twitter Consumer and Access tokens and secrets. Moreover, you can
select there how many of the last Tweets of the profiles you have registered do you want to save and visualize.
By default this number is set to 5.

When you change your Keys, the app automatically search the associated account, raising an error if it is
not valid. Furthermore, it creates the first record, which is your Profile information, filling the profile image, description,
number of followers and followed accounts, etc.

Screens and Tweets
------------------

Your Profile form can be found either directly clicking in the menu **My Twitter/My Twitter** as well as in 
**Screens/Screens** by selecting your record.

![Alt text](static/images/Screens.png?raw=true "Screens-Screens")

![Alt text](static/images/MyTwitterAccount.png?raw=true "Screens-Screens")

You can register other Screens as well, just introducing the @name. The stats of them are taken as well automatically at 
creation, but you can update them later by pressing the button **Count Stats** in the form of the records.

For all records you can as well execute the action Synchronize Last Tweets to take the 
last number of tweets specified in the configuration.

This action will be executed automatically by a chron every # days (by default every day, you just change it in the chron form)
in the screens you have selected the field **Update With the Chron**.

Your Twitter Account
--------------------

You can easily update your profile image, name and description through the wizard found in the menu **My Twitter**:

![Alt text](static/images/MyTwitterUpdate.png?raw=true "Screens-Screens")

With the other two wizards, you can publish a post, or deleting the ones you want:

![Alt text](static/images/MyTwitterPost.png?raw=true "Screens-Screens")

![Alt text](static/images/MyTwitterDelete.png?raw=true "Screens-Screens")

Main Kanban View
----------------

When you access to the form, you find the Tweets organized by Profiles like that:

![Alt text](static/images/Control.png?raw=true "Screens-Screens")

I have looked into many details like the reconstruction of the links and hashtags inside the tweets
so to access there directly from the kanban. The relative date is also computed in the code, trying to imitate
the Twitter views.