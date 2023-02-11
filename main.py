# USAGE:

'''
token.json:
Set `token` to your account's token.

config.json:
To backup group chat history put the group chat's ID in `dmBackupWhitelist`.
Leave `dmBackupWhitelist` blank to backup all DMs with your friends. (Excluding group chats.)
If you set `backupFullJson` to `true`, it will backup full message JSON. (Don't touch this if you didn't understand.)
'''









#
print()

import requests, time, datetime, itertools, pathlib, json, sys

def cout2(info, input):
    print('[\x1b[38;5;45m%s\x1b[0m] %s \x1b[38;5;45m>>\x1b[0m \033[1m%s\x1b[0m' % (datetime.datetime.now().strftime('%H:%M:%S'), info, input))

def cout(input):
    print('[\x1b[38;5;45m%s\x1b[0m] \x1b[38;5;45m>>\x1b[0m %s' % (datetime.datetime.now().strftime('%H:%M:%S'), input))

# RGB LOGGING
'''
colorsPool = itertools.cycle([27, 33, 69, 74, 74, 73, 73, 73, 78, 114, 114, 113, 113, 155, 155, 155, 155, 155, 155, 191, 191, 185, 185, 185, 185, 185, 185, 221, 221, 221, 221, 221, 215, 215, 215, 209, 209, 209, 203, 203, 203, 204, 204, 204, 198, 198, 129, 129, 135, 99, 99, 99, 99, 63, 63, 63, 63, 69, 69, 69])
def cout(input):
    print('[\x1b[38;5;%sm%s\x1b[0m] %s' % (next(colorsPool), datetime.datetime.now().strftime('%H:%M:%S'), input))
'''

path = '%s/' % str(pathlib.Path(__file__).resolve().parent).replace('\\', '/')
config = json.load(open('%s/config.json' % path))
backupFullJson = config['backupFullJson']

class Main:
    def __init__(self):
        self.token = json.load(open('%s/Data/token.json' % path))['token']
        self.session = self.createSession()
        self.path = path
        self.dmBackupWhitelist = config['dmBackupWhitelist']

    def getCookie(self):
        cookie = str(requests.get('https://discord.com/app').cookies)
        return cookie.split('dcfduid=')[1].split(' ')[0], cookie.split('sdcfduid=')[1].split(' ')[0], cookie.split('cfruid=')[1].split(' ')[0]

    def createSession(self):
        session = requests.Session()
        session.headers.update({
            'accept': '*/*',
            'accept-encoding': 'application/json',
            'accept-language': 'en-US,en;q=0.8',
            'authorization': self.token,
            'cookie': '__dcfduid=%s; __sdcfduid=%s; __cfruid=%s' % self.getCookie(),
            'referer': 'https://discord.com/channels/@me',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-super-properties': 'eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMDYuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjEwNi4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE1MTYzOCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
        })
        return session

    def backupRelationships(self):
        usersList = []
        for user in self.session.get('https://discord.com/api/v9/users/@me/relationships').json():
            tag = '%s#%s' % (user['user']['username'], user['user']['discriminator'])
            response = self.session.get('https://discord.com/api/v9/users/@me/notes/%s' % user['id'])
            if response:
                note = response.json()['note']
                cout2('Saved note for', tag)
            elif response.status_code == 429:
                retryAfter = response.json()['retry_after']
                cout2('Rate limited, sleeping for', '%ss' % (retryAfter + 1))
                time.sleep(retryAfter + 1)
                response = self.session.get('https://discord.com/api/v9/users/@me/notes/%s' % user['id'])
                if response:
                    note = response.json()['note']
                    cout2('Saved note for', tag)
                else:
                    note = 'None'
            else:
                note = 'None'
            usersList.append('%s | Note: %s | %s' % (tag, note.replace('\n', '\\n'), user['id']))
            cout2('Saved friend', tag)
        userCount = len(usersList)
        with open('%s/Data/relationships.txt' % self.path, 'w+', encoding = 'UTF-8') as file:
            file.write('Date: %s\n\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
            file.write('Total friends: %s\n\n' % userCount)
            for capture in usersList:
                file.write('%s\n\n' % capture)
        cout('Backuped %s friend(s).\n' % userCount)

    def backupGroupChats(self):
        groupsList = []
        for channel in self.session.get('https://discord.com/api/v9/users/@me/channels').json():
            if channel['type'] == 3:
                json = {
                    'max_age': 86400
                }
                response = self.session.post('https://discord.com/api/v9/channels/%s/invites' % channel['id'], json = json)
                if response.status_code == 200:
                    invite = response.json()['code']
                    recipients = []
                    for user in channel['recipients']:
                        recipients.append('%s#%s' % (user['username'], user['discriminator']))
                    recipients = ', '.join(recipients)
                    groupsList.append('Group chat: %s | %s | %s' % (recipients, channel['id'], invite))
                    cout2('Created invite for group chat', '%s | %s' % (recipients, invite))
                    time.sleep(1)
                else:
                    retryAfter = response.json()['retry_after']
                    cout2('Rate limmited, Sleeping for', '%ss' % (retryAfter + 1))
                    time.sleep(retryAfter + 1)
                    invite = response.json()['code']
                    recipients = []
                    for user in channel['recipients']:
                        recipients.append('%s#%s' % (user['username'], user['discriminator']))
                    recipients = ', '.join(recipients)
                    groupsList.append('Group chat: %s | %s | %s' % (recipients, channel['id'], invite))
                    cout2('Created invite for group chat', '%s | %s' % (recipients, invite))
                    time.sleep(1)
        groupCount = len(groupsList)
        with open('%s/Data/groups.txt' % self.path, 'w+', encoding = 'UTF-8') as file:
            file.write('Date: %s\n\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
            file.write('Total group chats: %s\n\n' % groupCount)
            for capture in groupsList:
                file.write('%s\n\n' % capture)
        print()
        cout('Backuped %s group chat(s).\n' % groupCount)

    def backupGuilds(self):
        guildsList = []
        for guild in self.session.get('https://discord.com/api/v9/users/@me/guilds').json():
            if 'VANITY_URL' in guild['features']:
                invite = self.session.get('https://discord.com/api/v9/guilds/%s' % guild['id']).json()['vanity_url_code']
                cout2('Created invite for', '%s | %s' % (guild['name'], invite))
                time.sleep(1)
            else:
                for channel in self.session.get('https://discord.com/api/v9/guilds/%s/channels' % guild['id']).json():
                    if channel['type'] in [0, 2, 3, 5, 13]:
                        json = {
                            'max_age': 0,
                            'max_uses': 0,
                            'temporary': False
                        }
                        response = self.session.post('https://discord.com/api/v9/channels/%s/invites' % channel['id'], json = json)
                        if response.status_code == 200:
                            invite = response.json()['code']
                            cout2('Created invite for', '%s | %s' % (guild['name'], invite))
                            time.sleep(1)
                            break
                        elif response.status_code == 429:
                            cout2('Rate limited, sleeping for', '%ss' % (response.json()['retry_after'] + 1))
                            time.sleep(response.json()['retry_after'] + 1)
                            response = self.session.post('https://discord.com/api/v9/channels/%s/invites' % channel['id'], json = json)
                            if response.status_code == 200:
                                invite = response.json()['code']
                                cout2('Created invite for', '%s | %s' % (guild['name'], invite))
                                time.sleep(1)
                                break
                            else:
                                invite = 'None'
                                cout2('Couldn\'t create invite for', guild['name'])
                                time.sleep(1)
                        else:
                            invite = 'None'
                            cout2('Couldn\'t create invite for', guild['name'])
                            time.sleep(1)
            guildsList.append('%s | %s | %s' % (guild['name'], guild['id'], invite))
        guildCount = len(guildsList)
        with open('%s/Data/guilds.txt' % self.path, 'w+', encoding = 'UTF-8') as file:
            file.write('Date: %s\n\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
            file.write('Total guilds: %s\n\n' % guildCount)
            for capture in guildsList:
                file.write('%s\n\n' % capture)
        cout('Backuped %s guild(s).\n' % guildCount)

    def getChannel(self, userId):
        json = {
            'recipients': [userId]
        }
        return self.session.post('https://discord.com/api/v9/users/@me/channels', json = json).json()['id']

    def backupDms(self):
        if self.dmBackupWhitelist:
            ids = self.dmBackupWhitelist
        else:
            ids = []
            for user in self.session.get('https://discord.com/api/v9/users/@me/relationships').json():
                if user['type'] == 1 or user['type'] == 4:
                    ids.append(int(user['id']))
        for id in ids:
            time.sleep(1)
            try:
                channelId = self.getChannel(id)
                response = self.session.get('https://discord.com/api/v9/users/%s' % id).json()
                tag = '%s#%s' % (response['username'], response['discriminator'])
                backupType = 'DM'
            except:
                channelId = id
                tag = 'Group Chat'
                backupType = 'GC'
            cout('Started %s backup with: %s (ID: %s)' % (backupType, tag, id))
            pinsList = []
            attachmentsList = []
            messagesList = []
            fullCaptures = []
            messages = self.session.get('https://discord.com/api/v9/channels/%s/messages?limit=100' % channelId)
            try:
                msgAmount = self.session.get('https://discord.com/api/v9/channels/%s/messages/search?channel_id=%s' % (channelId, channelId)).json()['total_results']
            except:
                try:
                    time.sleep(1)
                    msgAmount = self.session.get('https://discord.com/api/v9/channels/%s/messages/search?channel_id=%s' % (channelId, channelId)).json()['total_results']
                except:
                    msgAmount = 'Error'
            while len(messages.json()) > 0:
                sys.stdout.write('\r[\x1b[38;5;45m%s\x1b[0m] Scraped \x1b[38;5;45m>>\x1b[0m %s/%s messages' % (datetime.datetime.now().strftime('%H:%M:%S'), len(messagesList), msgAmount))
                sys.stdout.flush()
                for message in messages.json():
                    if backupFullJson:
                        fullCaptures.append(message)
                    date = datetime.datetime.fromisoformat(message['timestamp']).strftime('%Y-%m-%d | %H:%M %p')
                    if message['attachments']:
                        temp = []
                        for attachment in message['attachments']:
                            temp.append('Attachment name: %s | Attachment URL: %s' % (attachment['filename'], attachment['url']))
                            attachmentsList.append('Attachment name: %s | Attachment URL: %s' % (attachment['filename'], attachment['url']))
                        content = '(%s) %s#%s: %s | Attachment(s): %s' % (date, message['author']['username'], message['author']['discriminator'], message['content'], ', '.join(temp))
                    else:
                        content = '(%s) %s#%s: %s' % (date, message['author']['username'], message['author']['discriminator'], message['content'])
                    messagesList.append(content)
                    if message['pinned']:
                        pinsList.append(content)
                messages = self.session.get('https://discord.com/api/v9/channels/%s/messages?before=%s&limit=100' % (channelId, messages.json()[-1]['id']))
            sys.stdout.write('\r[\x1b[38;5;45m%s\x1b[0m] Scraped \x1b[38;5;45m>>\x1b[0m %s/%s messages' % (datetime.datetime.now().strftime('%H:%M:%S'), len(messagesList), msgAmount))
            sys.stdout.flush()
            print()
            print()
            with open('%s/Data/DMs/%s.txt' % (self.path, id), 'w+', encoding = 'UTF-8') as file:
                file.write('Date: %s\n\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
                file.write('DMs with: %s (ID: %s)\n\n' % (tag, id))
                file.write('Statistics: All: %s, Pinned: %s, Attachment(s): %s\n\n' % (len(messagesList), len(pinsList), len(attachmentsList)))
                file.write('--- PINNED MESSAGE(S) --- (Total: %s)\n\n' % len(pinsList))
                for message in pinsList:
                    file.write('%s\n' % message)
                file.write('\n--- ATTACHMENT(S) --- (Total: %s)\n\n' % len(attachmentsList))
                for message in attachmentsList:
                    file.write('%s\n' % message)
                file.write('\n--- ALL MESSAGE(S) --- (Total: %s)\n\n' % len(messagesList))
                for message in messagesList:
                    file.write('%s\n' % message)
            if backupFullJson:
                with open('%s/Data/DMs/c%s.txt' % (self.path, id), 'w+', encoding = 'UTF-8') as file:
                    for capture in fullCaptures:
                        file.write('%s\n' % capture)
            cout('Backuped %s message(s), %s pin(s), %s attachment(s) with: %s (ID: %s)\n' % (len(messagesList), len(pinsList), len(attachmentsList), tag, id))
        cout('Backuped %s DM(s).' % len(ids))

    def run(self):
        js = self.session.get('https://discord.com/api/v9/users/@me').json()
        cout2('Logged in as', '%s#%s' % (js['username'], js['discriminator']))
        print()
        if config['backupFriends']:
            self.backupRelationships()
        if config['backupGroupChats']:
            self.backupGroupChats()
        if config['backupGuilds']:
            self.backupGuilds()
        if config['backupDms']:
            self.backupDms()
        print()
        cout('Finished token backup.')
        print()

if __name__ == '__main__':
    Main().run()
