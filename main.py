token = ''

#

import requests, time

class Main:
    def __init__(self):
        self.token = token
        self.session = self.create_session()
        self.path = '' # For VSC users that use folders (Ex: Folder/)

    def get_cookie(self):
        cookie = str(requests.get('https://discord.com/app').cookies)
        return cookie.split('dcfduid=')[1].split(' ')[0], cookie.split('sdcfduid=')[1].split(' ')[0], cookie.split('cfruid=')[1].split(' ')[0]

    def create_session(self):
        session = requests.Session()
        session.headers.update({
            'accept': '*/*',
            'accept-encoding': 'application/json',
            'accept-language': 'en-US,en;q=0.8',
            'authorization': self.token,
            'cookie': '__dcfduid=%s; __sdcfduid=%s; __cfruid=%s' % self.get_cookie(),
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

    def backup_relationships(self):
        for user in self.session.get('https://discord.com/api/v9/users/@me/relationships').json():
            with open('%srelationships.txt' % self.path, 'a', encoding = 'UTF-8') as file:
                username = user['user']['username']
                discriminator = user['user']['discriminator']
                file.write('%s#%s | %s\n' % (username, discriminator, user['id']))
                print('Saved friend: %s#%s' % (username, discriminator))

    def backup_group_chats(self):
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
                        recipients.append(user['username'])
                    recipients = ', '.join(recipients)
                    print('Created invite for group chat: %s | %s' % (recipients, invite))
                    time.sleep(1)
                    with open('%sguilds.txt' % self.path, 'a', encoding = 'UTF-8') as file:
                        file.write('Group chat: %s | %s | %s\n' % (recipients, channel['id'], invite))

    def backup_guilds(self):
        allowed_channel_types = [0, 2, 3, 5, 13]
        for guild in self.session.get('https://discord.com/api/v9/users/@me/guilds').json():
            if 'VANITY_URL' in guild['features']:
                response = self.session.get('https://discord.com/api/v9/guilds/%s' % guild['id'])
                invite = response.json()['vanity_url_code']
                print('Created invite for: %s | %s' % (guild['name'], invite))
                time.sleep(1)
            else:
                for channel in self.session.get('https://discord.com/api/v9/guilds/%s/channels' % guild['id']).json():
                    if channel['type'] in allowed_channel_types:
                        json = {
                            'max_age': 0,
                            'max_uses': 0,
                            'temporary': False
                        }
                        response = self.session.post('https://discord.com/api/v9/channels/%s/invites' % channel['id'], json = json)
                        if response.status_code == 200:
                            invite = response.json()['code']
                            print('Created invite for: %s | %s.' % (guild['name'], invite))
                            time.sleep(1)
                            break
                        elif response.status_code == 429:
                            print('Rate limited, sleeping for: %s seconds.' % response.json()['retry_after'])
                            time.sleep(response.json()['retry_after'])
                            response = self.session.post('https://discord.com/api/v9/channels/%s/invites' % channel['id'], json = json)
                            if response.status_code == 200:
                                invite = response.json()['code']
                                print('Created invite for: %s | %s.' % (guild['name'], invite))
                                time.sleep(1)
                                break
                            else:
                                invite = 'None'
                                print('Couldn\'t create invite for: %s.' % guild['name'])
                                time.sleep(1)
                        else:
                            invite = 'None'
                            print('Couldn\'t create invite for: %s.' % guild['name'])
                            time.sleep(1)
            with open('%sguilds.txt' % self.path, 'a', encoding = 'UTF-8') as file:
                file.write('%s | %s | %s\n' % (guild['name'], guild['id'], invite))

    def run(self):
        self.backup_relationships()
        self.backup_group_chats()
        self.backup_guilds()

if __name__ == '__main__':
    Main().run()
