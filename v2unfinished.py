# if u guys wanna use the code for anything
import requests, json, time, binascii, os, random, pathlib, datetime, base64, sys
import tls_client # pip install tls-client   </>   Required for relationship restoring, otherwise it gets captcha and doesn't friend anybody.

class Main():
    def __init__(self):
        self.token = ''
        self.session = self.createSession()
        self.dirPath = str(pathlib.Path(__file__).resolve().parent).replace('\\', '/')

    def getCfBm(self):
        response = requests.get('https://discord.com/register').text
        payload = {
            'm': response.split(',m:\'')[1].split('\',s:')[0],
            'results': [
                str(binascii.b2a_hex(os.urandom(16)).decode('UTF-8')),
                str(binascii.b2a_hex(os.urandom(16)).decode('UTF-8'))
            ],
            'timing': random.randint(40, 180),
            'fp': {
                'id': 3,
                'e': {
                    'r': [
                        1920,
                        1080
                    ],
                    'ar': [
                        1054,
                        1920
                    ],
                    'pr': 1,
                    'cd': 24,
                    'wb': False,
                    'wp': False,
                    'wn': False,
                    'ch': True,
                    'ws': False,
                    'wd': False
                }
            }
        }
        return requests.post('https://discord.com/cdn-cgi/bm/cv/result?req_id=%s' % response.split('r:\'')[1].split('\',s')[0], json = payload).cookies.get('__cf_bm')

    def createSession(self, tls = False):
        cookie = requests.get('https://discord.com/app').cookies
        if tls:
            session = tls_client.Session(client_identifier = 'chrome_105')
            session.headers.update({'content-type': 'application/json'})
        else:
            session = requests.Session()
        session.headers.update({
            'accept': '*/*',
            'accept-encoding': 'application/json',
            'accept-language': 'en-US,en;q=0.8',
            'authorization': self.token,
            'cookie': '__cfruid=%s; __dcfduid=%s; __sdcfduid=%s; locale=en-US; __cf_bm=%s' % (cookie['__cfruid'], cookie['__dcfduid'], cookie['__sdcfduid'], self.getCfBm()),
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-super-properties': 'eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTEuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjExMS4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE4NDM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=='
        })
        return session

    def getRequest(self, url):
        while True:
            response = self.session.get(url)
            if response.status_code == 429:
                time.sleep(response.json()['retry_after'])
            else:
                return response

    def postRequest(self, url, json):
        while True:
            response = self.session.post(url, json = json)
            if response.status_code == 429:
                time.sleep(response.json()['retry_after'])
            else:
                return response

    def patchRequest(self, url, json):
        while True:
            response = self.session.patch(url, json = json)
            if response.status_code == 429:
                time.sleep(response.json()['retry_after'])
            else:
                return response

    def putRequest(self, url, json, session = None):
        while True:
            if session:
                response = session.put(url, json = json)
            else:
                response = self.session.put(url, json = json)
            if response.status_code == 429:
                time.sleep(response.json()['retry_after'])
            else:
                return response

    def readJson(self, key):
        with open('%ssettings.json' % self.path, 'r', encoding = 'UTF-8') as file:
            return json.load(file)[key]

    def writeJson(self, key, value):
        with open('%ssettings.json' % self.path, 'r', encoding = 'UTF-8') as file:
            data = json.load(file)
        data[key] = value
        with open('%ssettings.json' % self.path, 'w', encoding = 'UTF-8') as file:
            json.dump(data, file, indent = 4)

    def backupProfile(self):
        print('Backing up profile', end = '\r')
        user = self.profile['user']
        userId = user['id']
        username = user['username']
        discriminator = user['discriminator']
        avatar = user['avatar']
        banner = user['banner']
        bio = user['bio']
        connectedAccounts = self.profile['connected_accounts']
        try:
            themeColors = self.profile['user_profile']['theme_colors']
        except:
            themeColors = None
        email = self.me['email']
        phone = self.me['phone']
        try:
            note = self.getRequest('https://discord.com/api/v9/users/@me/notes/%s' % userId).json()['note']
        except:
            note = None
        with open('%sMe/info.txt' % self.path, 'w', encoding = 'UTF-8') as file:
            file.write('Date: %s\n\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
            if connectedAccounts:
                file.write('Connections:\n\n')
                for connection in connectedAccounts:
                    file.write('Type: %s\nName: %s\n\n' % (connection['type'], connection['name']))
            file.write('Other info:\n\n')
            file.write('User ID: %s\nUsername: %s\nDiscriminator: %s\nBio: %s\nNote: %s\nEmail: %s\nPhone: %s' % (userId, username, discriminator, bio, note, email, phone))
        payload = {}
        if themeColors:
            payload['theme'] = themeColors
        if note:
            payload['note'] = note
        if bio:
            payload['bio'] = bio
        self.writeJson('profile', payload)
        if avatar:
            for file in os.listdir('%sMe/' % self.path):
                if 'avatar' in file:
                    os.remove('%sMe/%s' % (self.path, file))
            response = self.getRequest('https://cdn.discordapp.com/avatars/%s/%s.gif?size=4096' % (userId, avatar))
            if response.headers.get('content-type') == 'image/gif':
                with open('%sMe/avatar.gif' % self.path, 'wb') as file:
                    file.write(response.content)
            else:
                with open('%sMe/avatar.png' % self.path, 'wb') as file:
                    file.write(self.getRequest('https://cdn.discordapp.com/avatars/%s/%s.png?size=4096' % (userId, avatar)).content)
        if banner:
            for file in os.listdir('%sMe/' % self.path):
                if 'banner' in file:
                    os.remove('%sMe/%s' % (self.path, file))
            response = self.getRequest('https://cdn.discordapp.com/banners/%s/%s.gif?size=4096' % (userId, banner))
            if response.headers.get('content-type') == 'image/gif':
                with open('%sMe/banner.gif' % self.path, 'wb') as file:
                    file.write(response.content)
            else:
                with open('%sMe/banner.png' % self.path, 'wb') as file:
                    file.write(self.getRequest('https://cdn.discordapp.com/banners/%s/%s.png?size=4096' % (userId, banner)).content)
        print('Backed up profile              ')

    def restoreProfile(self):
        print('Restoring profile', end = '\r')
        json = self.readJson('profile')
        if 'note' in json:
            self.putRequest('https://discord.com/api/v9/users/@me/notes/%s' % self.me['id'], {'note': json['note']})
        if 'bio' in json and 'theme' in json:
            self.patchRequest('https://discord.com/api/v9/users/@me/profile', {'bio': json['bio'], 'theme_colors': json['theme']})
        elif 'bio' in json:
            self.patchRequest('https://discord.com/api/v9/users/@me/profile', {'bio': json['bio']})
        elif 'theme' in json:
            self.patchRequest('https://discord.com/api/v9/users/@me/profile', {'theme_colors': json['theme']})
        payload = {}
        if os.path.exists('%sMe/avatar.png' % self.path):
            with open('%sMe/avatar.png' % self.path, 'rb') as file:
                payload['avatar'] = 'data:image/png;base64,%s' % base64.b64encode(file.read()).decode('UTF-8')
        elif os.path.exists('%sMe/avatar.gif' % self.path):
            if self.me['premium_type']:
                with open('%sMe/avatar.gif' % self.path, 'rb') as file:
                    payload['avatar'] = 'data:image/gif;base64,%s' % base64.b64encode(file.read()).decode('UTF-8')
        if self.me['premium_type'] == 2:
            if os.path.exists('%sMe/banner.png' % self.path):
                with open('%sMe/banner.png' % self.path, 'rb') as file:
                    payload['banner'] = 'data:image/png;base64,%s' % base64.b64encode(file.read()).decode('UTF-8')
            elif os.path.exists('%sMe/banner.gif' % self.path):
                with open('%sMe/banner.gif' % self.path, 'rb') as file:
                    payload['banner'] = 'data:image/gif;base64,%s' % base64.b64encode(file.read()).decode('UTF-8')
        self.patchRequest('https://discord.com/api/v9/users/@me', payload)
        print('Restored profile              ')

    def backupSettings(self):
        print('Backing up settings', end = '\r')
        self.writeJson('settings', self.getRequest('https://discord.com/api/v9/users/@me/settings').json())
        self.writeJson('settings-proto-1', self.getRequest('https://discord.com/api/v9/users/@me/settings-proto/1').json())
        self.writeJson('settings-proto-2', self.getRequest('https://discord.com/api/v9/users/@me/settings-proto/2').json())
        self.writeJson('settings-proto-3', self.getRequest('https://discord.com/api/v9/users/@me/settings-proto/3').json())
        print('Backed up settings              ')

    def restoreSettings(self):
        print('Restoring settings', end = '\r')
        self.patchRequest('https://discord.com/api/v9/users/@me/settings', self.readJson('settings'))
        self.patchRequest('https://discord.com/api/v9/users/@me/settings-proto/1', self.readJson('settings-proto-1'))
        self.patchRequest('https://discord.com/api/v9/users/@me/settings-proto/2', self.readJson('settings-proto-2'))
        self.patchRequest('https://discord.com/api/v9/users/@me/settings-proto/3', self.readJson('settings-proto-3'))
        print('Restored settings              ')

    def setHypesquad(self):
        print('[1] - House of Bravery (Purple)')
        print('[2] - House of Brilliance (Red)')
        print('[3] - House of Balance (Green)')
        option = int(input('House > '))
        self.postRequest('https://discord.com/api/v9/hypesquad/online', {'house_id': option})
        print('Set HypeSquad')

    def setGuildNotifications(self):
        print('Setting guild notifications to mentions only')
        guilds = self.getRequest('https://discord.com/api/v9/users/@me/guilds').json()
        for counter, guild in zip(range(len(guilds), 0, -1), reversed(guilds)):
            print('Guilds left: %s                            ' % counter, end = '\r')
            self.patchRequest('https://discord.com/api/v9/users/@me/guilds/%s/settings' % guild['id'], {'message_notifications': 1})
        print('Set all guild notifications to mentions only              ')

    def backupRelationships(self):
        print('Backing up relationships')
        relationships = []
        response = self.getRequest('https://discord.com/api/v9/users/@me/relationships').json()
        def formatRelationship(user, type):
            tag = '%s#%s' % (user['user']['username'], user['user']['discriminator'])
            userId = user['id']
            response = self.getRequest('https://discord.com/api/v9/users/@me/notes/%s' % userId)
            payload = {}
            if response:
                payload['note'] = response.json()['note']
            if user['nickname']:
                payload['nickname'] = user['nickname']
            payload['userId'] = userId
            payload['userTag'] = tag
            payload['type'] = type
            return payload
        for counter, user in zip(range(len(response), 0, -1), reversed(response)):
            print('Users left: %s                            ' % counter, end = '\r')
            if user['type'] == 1:
                relationships.append(formatRelationship(user, 'friend'))
            elif user['type'] == 2:
                relationships.append(formatRelationship(user, 'blocked'))
            elif user['type'] == 4:
                relationships.append(formatRelationship(user, 'outgoing'))
        with open('%srelationships.txt' % self.path, 'w', encoding = 'UTF-8') as file:
            file.write('Date: %s\n\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
            friends = []
            outgoing = []
            blocked = []
            for i in relationships:
                if i['type'] == 'friend':
                    friends.append(i)
                elif i['type'] == 'outgoing':
                    outgoing.append(i)
                elif i['type'] == 'blocked':
                    blocked.append(i)
            file.write('All: %s Friends: %s Outgoing: %s Blocked: %s\n\n' % (len(friends) + len(outgoing) + len(blocked), len(friends), len(outgoing), len(blocked)))
            def writeFile(file, list):
                for i in list:
                    string = 'Tag: %s\nUser ID: %s\n' % (i['userTag'], i['userId'])
                    if 'note' in i:
                        string += 'Note: %s\n' % i['note']
                    if 'nickname' in i:
                        string += 'Nickname: %s\n' % i['nickname']
                    file.write('%s\n' % string)
            file.write('Friends (%s):\n\n\n' % len(friends))
            writeFile(file, friends)
            file.write('\nOutgoing (%s):\n\n\n' % len(outgoing))
            writeFile(file, outgoing)
            file.write('\nBlocked (%s):\n\n\n' % len(blocked))
            writeFile(file, blocked)
        for i in relationships:
            del i['userTag']
        self.writeJson('relationships', relationships)
        print('Backed up relationships                            ')
# Restore friends, notes and nicknames options
    def restoreRelationships(self):
        print('Restoring relationships', end = '\r')
        current = []
        for i in self.getRequest('https://discord.com/api/v9/users/@me/relationships').json():
            if i['type'] in [1, 2, 4]:
                current.append(str(i['id']))
        relationships = self.readJson('relationships')
        keep = []
        for item in relationships:
            if item['userId'] not in current:
                keep.append(item)
        session = self.createSession(True)
        for counter, i in zip(range(len(keep), 0, -1), reversed(keep)):
            print('Users left: %s                      ' % counter, end = '\r')
            if i['type'] in ['friend', 'outgoing']:
                self.putRequest('https://discord.com/api/v9/users/@me/relationships/%s' % i['userId'], {}, session)
            elif i['type'] == 'blocked':
                self.putRequest('https://discord.com/api/v9/users/@me/relationships/%s' % i['userId'], {'type': 2})
        print('Restored relationships              ')
        print('Restoring notes and nicknames', end = '\r')
        notesNicknames = []
        for item in relationships:
            if 'note' in item or 'nickname' in item:
                notesNicknames.append(item)
        for counter, i in zip(range(len(notesNicknames), 0, -1), reversed(notesNicknames)):
            print('Notes and nicknames left: %s                      ' % counter, end = '\r')
            if 'note' in i:
                self.putRequest('https://discord.com/api/v9/users/@me/notes/%s' % i['userId'], {'note': i['note']})
            if 'nickname' in i:
                self.patchRequest('https://discord.com/api/v9/users/@me/relationships/%s' % i['userId'], {'nickname': i['nickname']})
        print('Restored notes and nicknames              ')

    def backupGuilds(self):
        print('Backing up guilds')
        oldGuilds = self.readJson('guilds')
        guilds = self.getRequest('https://discord.com/api/v9/users/@me/guilds').json()
        guildsList = []
        for counter, guild in zip(range(len(guilds), 0, -1), reversed(guilds)):
            print('Guilds left: %s                      ' % counter, end = '\r')
            guildId = guild['id']
            if 'VANITY_URL' in guild['features']:
                invite = self.getRequest('https://discord.com/api/v9/guilds/%s' % guildId).json()['vanity_url_code']
            else:
                invite = None
            if not invite:
                for channel in self.getRequest('https://discord.com/api/v9/guilds/%s/channels' % guildId).json():
                    if channel['type'] in [0, 2, 5, 13, 15]:
                        payload = {
                            'flags': 0,
                            'max_age': 0,
                            'max_uses': 0,
                            'target_type': None,
                            'temporary': False
                        }
                        response = self.postRequest('https://discord.com/api/v9/channels/%s/invites' % channel['id'], payload)
                        if response.status_code == 200:
                            invite = response.json()['code']
                            break
            payload = {
                'guildName': guild['name'],
                'guildId': guildId
            }
            if invite:
                payload['invite'] = invite
            else:
                for i in oldGuilds:
                    if guildId in i and i['invite']:
                        payload['invite'] = i['invite']
                        break
            guildsList.append(payload)
        with open('%sguilds.txt' % self.path, 'w', encoding = 'UTF-8') as file:
            file.write('Date: %s\n\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
            file.write('All guilds: %s\n\n' % len(guildsList))
            for i in guildsList:
                if 'invite' in i:
                    file.write('Name: %s\nID: %s\nInvite: %s\n\n' % (i['guildName'], i['guildId'], i['invite']))
                else:
                    file.write('Name: %s\nID: %s\n\n' % (i['guildName'], i['guildId']))
        self.writeJson('guilds', guildsList)
        print('Backed up guilds       ')

    def restoreGuilds(self):
        print('Restoring guilds\n')
        skip = []
        while True:
            guilds = [guild['id'] for guild in self.getRequest('https://discord.com/api/v9/users/@me/guilds').json()]
            oldGuilds = self.readJson('guilds')
            keep = []
            for item in oldGuilds:
                if 'invite' in item:
                    if item['guildId'] not in guilds and item not in skip:
                        keep.append(item)
            if keep:
                print('Guilds left: %s' % len(keep))
                print('Join (%s) - discord.gg/ %s\n' % (keep[0]['guildName'], keep[0]['invite']))
                option = input('Y - proceed | E - exit | S - skip\n\nOption > ')
                if option.lower() == 'y':
                    continue
                elif option.lower() == 'e':
                    break
                elif option.lower() == 's':
                    skip.append(keep[0])
            else:
                print('Finished restoring guilds.')
                break

    def backupGroupChats(self):
        print('Backing up group chats')
        groupsList = []
        channels = self.getRequest('https://discord.com/api/v9/users/@me/channels').json()
        for counter, channel in zip(range(len(channels), 0, -1), reversed(channels)):
            print('Group chats left: %s                      ' % counter, end = '\r')
            if channel['type'] == 3:
                payload = {
                    'max_age': 86400
                }
                response = self.postRequest('https://discord.com/api/v9/channels/%s/invites' % channel['id'], json = payload)
                if response.status_code == 200:
                    invite = response.json()['code']
                    recipients = []
                    for user in channel['recipients']:
                        recipients.append('%s#%s' % (user['username'], user['discriminator']))
                    recipients = ', '.join(recipients)
                    payload = {
                        'recipients': recipients,
                        'channelId': channel['id'],
                        'invite': invite
                    }
                    if channel['name']:
                        payload['name'] = channel['name']
                    groupsList.append(payload)
        with open('%sgroups.txt' % self.path, 'w', encoding = 'UTF-8') as file:
            file.write('Date: %s\n\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
            file.write('All groups: %s\n\n' % len(groupsList))
            for i in groupsList:
                if 'name' in i:
                    file.write('Name: %s\nRecipients: %s\nChannel ID: %s\nInvite: %s\n\n' % (i['name'], i['recipients'], i['channelId'], i['invite'])) # expiery date 24h here
                else:
                    file.write('Recipients: %s\nChannel ID: %s\nInvite: %s\n\n' % (i['recipients'], i['channelId'], i['invite']))
        self.writeJson('groups', groupsList)
        print('Backed up group chats                               ')

    def restoreGroupChats(self):
        print('Restoring groups\n')
        skip = []
        while True:
            groups = [channel['id'] for channel in self.getRequest('https://discord.com/api/v9/users/@me/channels').json() if channel['type'] == 3]
            oldGroups = self.readJson('groups')
            keep = []
            for item in oldGroups:
                if item['channelId'] not in groups and item not in skip:
                    keep.append(item)
            if keep:
                print('Groups left: %s' % len(keep))
                if 'name' in keep[0]:
                    print('Join (%s) - discord.gg/ %s\n' % (keep[0]['name'], keep[0]['invite']))
                else:
                    print('Join (Recipients: %s)\ndiscord.gg/ %s\n' % (keep[0]['recipients'], keep[0]['invite']))
                option = input('Y - proceed | E - exit | S - skip\n\nOption > ')
                if option.lower() == 'y':
                    continue
                elif option.lower() == 'e':
                    break
                elif option.lower() == 's':
                    skip.append(keep[0])
                print()
            else:
                print('Finished restoring groups.')
                break

    def backupDms(self):
        pass

    def backupEverything(self):
        pass

    def restoreEverything(self):
        pass

    def run(self):
        if sys.platform == 'win32':
            cmd = 'cls'
        else:
            cmd = 'clear'
        os.system(cmd)
        print('Checking for files')
        self.me = self.getRequest('https://discord.com/api/v9/users/@me').json()
        self.profile = self.getRequest('https://discord.com/api/v9/users/%s/profile' % self.me['id']).json()
        self.path = '%s/Data/%s-%s/' % (self.dirPath, self.profile['user']['username'][:5].lower(), self.me['id'])
        if not os.path.exists('%s/Data/' % self.dirPath):
            os.makedirs('%s/Data/' % self.dirPath)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            os.makedirs('%sMe/' % self.path)
            payload = {
                'settings': {},
                'settings-proto-1': {},
                'settings-proto-2': {},
                'settings-proto-3': {},
                'profile': {},
                'relationships': [],
                'guilds': [],
                'groups': []
            }
            with open('%ssettings.json' % self.path, 'w') as file:
                json.dump(payload, file, indent = 4)
        os.system(cmd)
        while True:#fix gc counter and auto check for updated friends guilds /expired gc inv links for all tokens?
            print('Loading', end = '\r')
            self.me = self.getRequest('https://discord.com/api/v9/users/@me').json()
            self.profile = self.getRequest('https://discord.com/api/v9/users/%s/profile' % self.me['id']).json()
            print('Loading.', end = '\r')
            currentGuilds = [guild['id'] for guild in self.getRequest('https://discord.com/api/v9/users/@me/guilds').json()]
            restoreGuilds = len([item for item in self.readJson('guilds') if 'invite' in item and item['guildId'] not in currentGuilds])
            print('Loading..', end = '\r')
            currentFriends = [friend['id'] for friend in self.getRequest('https://discord.com/api/v9/users/@me/relationships').json()]
            restoreFriends = sum(1 for item in self.readJson('relationships') if item['userId'] not in currentFriends)
            print('Loading...', end = '\r')
            currentGroups = [channel['id'] for channel in self.getRequest('https://discord.com/api/v9/users/@me/channels').json() if channel['type'] == 3]
            restoreGroups = sum(1 for item in self.readJson('groups') if item['channelId'] not in currentGroups)
            settingsCount = sum(1 for key in ['settings', 'settings-proto-1', 'settings-proto-2', 'settings-proto-3'] if self.readJson(key))
            os.system(cmd)
            menuItems = [
                ['', ' Logged in as %s#%s. <33' % (self.me['username'], self.me['discriminator']), ''],
                [],
                ['         Backup', '         Restore', '        Misc'],
                [],
                ['[1] - Backup relationships (x%s)' % len(currentFriends), '[7] - Restore relationships (x%s)' % restoreFriends, '[12] - Set HypeSquad'],
                ['[2] - Backup guilds (x%s)' % len(currentGuilds), '[8] - Restore guilds (x%s)' % restoreGuilds, '[13] - Set all guild notifications to mentions only (x%s)' % len(currentGuilds)],
                ['[3] - Backup groups (x%s)' % len(currentGroups), '[9] - Restore groups (x%s)' % restoreGroups],
                ['[4] - Backup profile', '[10] - Restore profile', '[14] - Backup everything (x%s)' % (len(currentFriends) + len(currentGuilds) + len(currentGroups) + 4)],
                ['[5] - Backup settings (x4)', '[11] - Restore settings (x%s)' % settingsCount, '[15] - Restore everything (x%s)' % (restoreFriends + restoreGuilds + restoreGroups + settingsCount)],
                ['[6] - Backup DMs', '', '\033[31mE - Exit\033[0m']
            ]
            print('\n'.join([' '.join([f'{item:<{37}}' for item in row]) for row in menuItems]))
            print()
            option = input('Option >> ')
            if option.lower() == 'e':
                break
            try:
                optionsList = [self.backupRelationships, self.backupGuilds, self.backupGroupChats, self.backupProfile, self.backupSettings, self.backupDms, self.restoreRelationships, self.restoreGuilds, self.restoreGroupChats, self.restoreProfile, self.restoreSettings, self.setHypesquad, self.setGuildNotifications, self.backupEverything, self.restoreEverything]
                optionsList[int(option) - 1]()
            except:
                continue

if __name__ == '__main__':
    Main().run()
