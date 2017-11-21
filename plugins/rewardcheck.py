import requests
from threading import Thread
import time
from disco.bot import Plugin
import arrow
import dateparser



class RewardCheckPlugin(Plugin):
    """checks periodically to see if conditions have been met to give out clan engrams using the destiny 2 api. also can be checked manually by users :)""" #this smiley face was written at the start of the night

    API_KEY = 'PUT_THE_KEY_HERE'#bungie API key (message me and ill send mine to you)

    HEADER = {"X-API-KEY": API_KEY}
    baseURL = "https://www.bungie.net/platform/"

    killThreads = False
    
    
    #rewardsEnum = {'crucible': '964120289', 'nightfall': '3789021730', 'raid': '2043403989', 'trials': '2112637710'} #maybe reverse this so the ids are linked to the string rather than vice/versa

    rewardsEnum = {'964120289': 'Crucible', '3789021730': 'Nightfall', '2043403989': 'Leviathan Raid', '2112637710': 'Trials of the Nine'} #just linking stuff
    completedEnum = {'Crucible': False, 'Nightfall': False, 'Leviathan Raid': False, 'Trials of the Nine': False} #contains whether we've completed it yet


    currentTime = arrow.utcnow()#set the timer
    nextCheck = currentTime.shift(seconds=+10)#timestep every 10 seconds
    goalTime = currentTime.shift(seconds=+30)#goal time is 30 seconds (we check the engram status every 30 seconds)

    @Plugin.listen('Ready')
    def on_ready(self, event):
        request = requests.get(self.baseURL + "/GroupV2/Name/OpieOP/1", headers=self.HEADER)#get the clanID from bungie API
        #opieOP clan id: 2819396

        clanInfo = request.json()

        self.clanID = clanInfo['Response']['detail']['groupId'] #parse it and store it
        print("clanID obtained: {}".format(self.clanID))

        self.startTimer(event) #start the timers

    @Plugin.listen('PresenceUpdate')#doesnt work
    def on_presence_update(self, event):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!presence update!!!!!!!!!!!!!!!!!!!!!!")
        print(event.client.channels)

    
    def force_presence_update(self):#doesnt work
        self.client.update_presence(Status[1], None, False, 0.01)


    def startTimer(self, event):
        timer_next = Thread(target=self.checkTimer, args=(event,)) #copied smt's code
        timer_next.start()

    def checkTimer(self, event):
        while True:
            #self.force_presence_update()
            if self.killThreads:
                break
            if self.nextCheck < arrow.utcnow():#if we're past the time we're supposed to check

                print("timestep")
                self.nextCheck = self.nextCheck.shift(seconds=+10) #push the next check back 1 min
                if self.nextCheck >= self.goalTime:#this isnt completely right but its good enough for testing. should check to see if anything changed since the last time we checked
                    print("checking engrams")
                    self.goalTime = self.goalTime.shift(minutes=+1)
                    self.checkEngrams(event)
                    break

    @Plugin.command('check', group='engrams')
    def checkEngrams(self, event):
        request = requests.get(self.baseURL + "/Destiny2/Clan/" + self.clanID + "/WeeklyRewardState/", headers=self.HEADER)#get a json element with info on our engrams

        milestoneInfo = request.json()

        self.rewardsList = milestoneInfo['Response']['rewards'][0]['entries']

        for count in range(len(self.rewardsList)):
            if self.rewardsList[count]['earned'] == True:
                self.completedEnum[self.rewardsEnum[str(self.rewardsList[count]['rewardEntryHash'])]] = True #simplify this lmao
        
        
        self.displayEngrams(event)

    def displayEngrams(self, event):#should be where we display it in a nice format but i cant send messages. should only display if something has changed since last time.
        #self.force_presence_update()
        print("displaying engrams")
        print(str(self.completedEnum))


        currentTime = arrow.utcnow()
        self.nextCheck = currentTime.shift(seconds=+10)
        self.goalTime = currentTime.shift(seconds=+30)
        timer_next = Thread(target=self.checkTimer, args=(event,))
        timer_next.start()





#with open("rewards.txt", mode="w") as rewards:
	#rewards.write(str(milestoneInfo['Response']['rewards'][0]))

     #self.channels = event.user.client.state.channels

        #print(self.channels)
        
        #embed_message = message.MessageEmbed.set_thumbnail("//images//luminous_engram.png")

        #event.msg.content("test")

        #msg = Message()
        #msg.content = "test"
        #self.channels[350079791237562375].send_message(msg)

        #ignore this it doesnt work
        
        #embed_msg.embeds.set_author(name="Engram Status", icon_url="https://www.bungie.net/common/destiny2_content/icons/a54ede4713181762bfcce25063a1d642.png")
        #embed_msg.embeds.set_thumbnail(url="https://www.bungie.net/common/destiny2_content/icons/a54ede4713181762bfcce25063a1d642.png")
        #embed_msg.embeds.add_field(name="Nightfall", value="DONE!", inline=True)
        #embed_msg.embeds.add_field(name="Crucible", value="DONE!", inline=True)
        #embed_msg.embeds.add_field(name="Raid", value="DONE!", inline=True)
        #embed_msg.embeds.add_field(name="Trials of the Nine", value="DONE!", inline=True)

        #self.send_message(self.channels[0], "test")