### Telegram bot for Serpstat API
Telegram bot for quick and convenient use of Serpstat tools.
This bot speeds up and simplifies interaction with certain tools of Serpstat. 
At this stage, it is implemented to obtain the number of keywords and traffic for one site depending
on search engine and region 

##### The following functions are implemented:
1) User registration in telegram bot
2) Adding and changing your api key for Serpstat
3) Adding and changing the region for which data is requested

#####To run your local bot copy:
1) Add the **.env** file to the project root template of the file you can see at the **example.env**
2) Add your **TELEGRAM_API_KEY** to the **.env** file, **TELEGRAM_API_KEY** can be found in **@botfather**
3) Add POSTGRES_DB_ADDRESS, POSTGRES_DB_PORT, POSTGRES_DB_NAME, POSTGRES_DB_LOGIN, POSTGRES_DB_PASSWORD values
to .env file. This data will be used for database creation via docker-compose, if you will use another database location
fill your database location and user data
4) If you are using docker-compose, run docker-compose in project directory
5) Run python3 dbhelper.py to create tables
6) Run bot.py file

#####To deploy production copies to heroku:
1) Add the **.env** file to the project root template of the file you can see at the **example.env**.
2) Add your **TELEGRAM_API_KEY** to the .env file, **TELEGRAM_API_KEY** can be found in **@botfather**.
3) Add your **HEROKU_APP_URL** to the **.env** file, **HEROKU_APP_URL** can be found in the heroku account.
4) Run code in heroku repository(it will run automatically because of **Procfile**).
5) Create database in heroku by running command `heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application`
6) Run `heroku run python dbhelper.py --app serpstat-bot` to create tables

After a successful start, **you need to go to the root of your application** (the URL indicated in HEROKU_APP_URL) 
if everything is successful, the message _“Your app is working”_ should be displayed.
Bot is running successfully.

#####Using the bot:
To use the bot, you need to register **/register** in bot and add your serpstat api key **/add_key**, 
and add the region **/set_region** to get data. Then you can send plain domain name in a message and receive the result.

####Commands:
**/start** - Returns a list of bot commands.

**/register** - Registration in the bot.

**/add_key** - Setting a **Serpstat key** after you run the command you need to insert your **API KEY** from the Serpstat,
 plain text, without quotes and additional characters (spaces, line breaks).
 To update the key you need to re-run the command.

**/get_limits** - shows how many limits are left for **API KEY**.

**/region_codes** - list of popular regions and search engines codes.

**/show_regions** - shows the regions are currently installed.

**/change_regions** - change regions. After calling the command, an input field appears, 
 the region codes must be entered as specified in **/region_codes** command response, 
 if you're input several regions they must be separated by commas without any quotes and spaces. 
 To replace the regions, you need to call the command again.
To obtain domain statistics, you need to enter plain domain in the **_domain.com_** format,
 all data will be returned in response. 
