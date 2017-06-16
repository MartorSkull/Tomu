
class BotConfiguration:
    config={}
    def __init__(self):
        self.config={
            'main': {
                'token': "", #this is the Discord Token to connect
                'botmodule': "botcom" #this is the module that the bot will search commands for in each app
            },
            'bot':{
                'prefixes': ["!"] #command prefixes
            },
            'strings':{
                'description': "Tomu - The bot with its own webpage" #bots description
            },
            'server': {
                'announces': "announcements", #the name of the anouncements channel
                'output': "logs", #the name of the channel where the bot will send its logs
                'bot-role': "Tomu", #the name of the role that the bot will use
                'admin-role': "admin", #the name for the admin role
                'bot-color': 0x11806A, #the color for the bot role
                'admin-color': 0xE74C3C #the color for the admin role
            },
        }