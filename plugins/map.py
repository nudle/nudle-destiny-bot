from disco.bot import Plugin

class MapPlugin(Plugin):
    """Disco plugin holding all of the commands related to Destiny 2 maps"""

    @Plugin.command('underbelly', group='map')
    def command_ub(self, event):
        """Posts a map of the raid underbelly"""
        event.msg.reply('https://i.imgur.com/RbTbtjt.png')

    @Plugin.command('underbelly3d', group='map')
    def command_ub3d(self, event):
        """Posts a 3d map of the raid underbelly"""
        event.msg.reply('https://i.imgur.com/UVt3gMR.jpg')

    @Plugin.command('doggos', group='map')
    def command_dog(self, event):
        """Posts a map of the dog room"""
        event.msg.reply('https://i.imgur.com/oCEK6EK.png')
