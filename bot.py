import groupy
from groupy import Bot
import time
import hashlib
import configparser
from libbot import *
import random

config = configparser.ConfigParser()
config.read('config.ini')

ADMIN_NAME_HASH = config['DEFAULT']['AdminNameHash'] #MD5 hash of the bot admin's name, they have the power to !kill
TBA_APP_ID = config['DEFAULT']['TBAAppID']
TBA_AUTH_KEY = config['DEFAULT']['TBAAuthKey']
GROUP_NAME = config['DEFAULT']['GroupName']
S_WORDS = ["stuff","spit","skit","ship","shirt","sport","short","script"] #TODO: put these into a CSV
MF_WORDS =["Monday-Friday","monkey-fightin","megaphonin","mighty flippin","Marty flyin","meadow frolickin","metal forgin"]

bot = Bot.list().first
groups = groupy.Group.list()
for i in groups:
    if i.name == GROUP_NAME:
        group=i
oldMsg = ""

while True:
    try:
        latestMsg = group.messages().newest
    except:
        latestMsg = " "
    if latestMsg != oldMsg:
        #print(latestMsg)
        if latestMsg.text == "Hi bot!":
            bot.post("Hi, "+latestMsg.name)
        else:
            if latestMsg.text:
                cmdname = latestMsg.text.split(" ")[0]
            else:
                cmdname = " "
            if cmdname == "!amlookup":
                productNo = latestMsg.text.split(" ")[1]
                part = andymark_item(productNo)
                if part:
                    #print(part)
                    bot.post("The item you looked up is a "+part[1]+". It costs "+part[2]+".")
                else:
                    bot.post("Item not found.")
            elif cmdname == "!nextmeeting":
                if int(time.strftime("%W")) <= 12:
                    if int(time.strftime("%W")) == 1:
                        bot.post("Kickoff is Saturday! G E T H Y P E")
                        bot.post("Also be sure to download the encrypted manual from https://firstfrc.blob.core.windows.net/frc2017/Manual/2017FRCGameSeasonManual.pdf")
                    elif int(time.strftime("%w")) == 0:
                        bot.post("The next meeting is held Monday at 6:30 PM!")
                    elif int(time.strftime("%w")) <= 5:
                        bot.post("The next meeting will be held TODAY and every weekday at 6:30 PM!")
                    elif int(time.strftime("%w")) == 6:
                        bot.post("The next meeting will be held TODAY and every Saturday at 10:00 AM!")
                else:
                    if int(time.strftime("%w")) <= 1:
                        bot.post("The next meeting will be on Monday at 6:30 PM!")
                    else:
                        bot.post("The next meeting will be on Saturday at 12 PM!")
                #TODO: combine this with a google calendar for cases such as the FTC events and build season
            elif cmdname == "!zesty": #DO NOT DOCUMENT THIS COMMAND EVER
                bot.post("ayy lmao")
            elif cmdname == "!about" or cmdname == "!?" or cmdname == "!help":
                bot.post("For more information, visit https://github.com/bobbysq/GroupMeBot")
            elif cmdname == "!tba":
                teamNo = latestMsg.text.split(" ")[1]
                teamName = tbaGetName(teamNo, TBA_APP_ID, TBA_AUTH_KEY)
                if teamNo == "8":
                    bot.post("TBA Link to team #8, The 8th team, Team \"The Ocho\" 8: https://thebluealliance.com/team/8")
                    bot.post("Wait, when did they change their name?")
                elif teamName:
                    bot.post("TBA Link to team "+teamNo+", "+teamName+": https://thebluealliance.com/team/"+teamNo)
                else:
                    bot.post("TBA Link to team: https://thebluealliance.com/team/"+teamNo)
            elif cmdname == "!kill":
                m = hashlib.md5(latestMsg.name.encode("utf-8","ignore")).hexdigest()
                print(m)
                if m == ADMIN_NAME_HASH:
                    bot.post("Shutting down")
                    exit()
                else:
                    bot.post("You're not an admin.")
            elif cmdname == "!manual" or cmdname == "!rtfm" or cmdname == "!thegame":
                bot.post("Manual is here: http://www.firstinspires.org/resource-library/frc/competition-manual-qa-system")
            elif cmdname == "!vexlookup": #
                productNo = latestMsg.text.split(" ")[1]
                part = vex_item(productNo)
                if part:
                    #print(part)
                    bot.post("The item you looked up is a "+part[1].split(" - ")[0]+". It costs "+part[2]+".")
                else:
                    bot.post("Item not found.")
            elif cmdname == "!rollout":
                bot.post("Optimus Remind is now officially rolling out! Check https://github.com/bobbysq/GroupMeBot/blob/master/README.md for a command list!")
            elif cmdname == "!tsimfd":
                sWord = random.choice(S_WORDS)
                mfWord = random.choice(MF_WORDS)
                bot.post("This "+sWord+" is "+mfWord+" dope. That's it.")
            elif cmdname == "!quote":
                quote = cdQuote()
                bot.post(quote)
            elif cmdname == "!robit":
                quote = movieQuote()
                bot.post(quote)
            elif "upvotes" in latestMsg.text.lower():
                bot.post("Don't worry, they'll upvote anything.")
            elif "cowtown" in latestMsg.text.lower():
                bot.post("CowTwon*")
            elif "prius patrol" in latestMsg.text.lower():
                bot.post(random.choice["https://www.youtube.com/watch?v=r_WCfcJfh2A","https://www.youtube.com/watch?v=BQmBh-8QC6w","https://www.youtube.com/watch?v=uNNGLdTVlDY","https://www.youtube.com/watch?v=RksFDe6nkaY","https://www.youtube.com/watch?v=PElH5Kidupk"])
        oldMsg = latestMsg
    time.sleep(2)
