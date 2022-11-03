token = '' # Your account's token
backup_dms = False # False/True
dm_backup_whitelist = [] # IDs/Group Chats of users you want to backup DMs with. (Leave blank to backup all friends.)

#

import requests, time, datetime, itertools

colors_pool = itertools.cycle(['27m', '33m', '69m', '74m', '74m', '73m', '73m', '73m', '78m', '114m', '114m', '113m', '113m', '155m', '155m', '155m', '155m', '155m', '155m', '191m', '191m', '185m', '185m', '185m', '185m', '185m', '185m', '221m', '221m', '221m', '221m', '221m', '215m', '215m', '215m', '209m', '209m', '209m', '203m', '203m', '203m', '204m', '204m', '204m', '198m', '198m', '129m', '129m', '135m', '99m', '99m', '99m', '99m', '63m', '63m', '63m', '63m', '69m', '69m', '69m'])

def cout(input):
    print('[\x1b[38;5;%s%s\x1b[0m] %s' % (next(colors_pool), datetime.datetime.now().strftime('%H:%M:%S'), input))

class Main:
    def __init__(self):
        self.token = token
        self.session = self.create_session()
        self.path = '' # For VSC users that use folders (Ex: Folder/)
        self.dm_backup_whitelist = dm_backup_whitelist

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
        open('%srelationships.txt' % self.path, 'w+', encoding = 'UTF-8').close()
        with open('%srelationships.txt' % self.path, 'a+', encoding = 'UTF-8') as file:
            file.write('Date: %s\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
        for user in self.session.get('https://discord.com/api/v9/users/@me/relationships').json():
            username = user['user']['username']
            discriminator = user['user']['discriminator']
            tag = '%s#%s' % (username, discriminator)
            response = self.session.get('https://discord.com/api/v9/users/@me/notes/%s' % user['id'])
            if response:
                note = response.json()['note']
                cout('Saved note for: %s' % tag)
            elif response.status_code == 429:
                retry_after = response.json()['retry_after']
                cout('Rate limited, sleeping for: %s' % int(retry_after) + 1)
                time.sleep(retry_after + 1)
                response = self.session.get('https://discord.com/api/v9/users/@me/notes/%s' % user['id'])
                if response:
                    note = response.json()['note']
                    cout('Saved note for: %s' % tag)
                else:
                    note = 'None'
            else:
                note = 'None'
            with open('%srelationships.txt' % self.path, 'a+', encoding = 'UTF-8') as file:
                file.write('%s | Note: %s | %s\n' % (tag, note.replace('\n', '\\n'), user['id']))
                cout('Saved friend: %s' % tag)

    def backup_group_chats(self):
        open('%sguilds.txt' % self.path, 'w+', encoding = 'UTF-8').close()
        with open('%sguilds.txt' % self.path, 'a+', encoding = 'UTF-8') as file:
            file.write('Date: %s\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
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
                    cout('Created invite for group chat: %s | %s' % (recipients, invite))
                    time.sleep(1)
                    with open('%sguilds.txt' % self.path, 'a+', encoding = 'UTF-8') as file:
                        file.write('Group chat: %s | %s | %s\n' % (recipients, channel['id'], invite))
                else:
                    retry_after = response.json()['retry_after']
                    cout('Rate limmited, sleeping for: %s' % int(retry_after) + 1)
                    time.sleep(retry_after + 1)
                    invite = response.json()['code']
                    recipients = []
                    for user in channel['recipients']:
                        recipients.append(user['username'])
                    recipients = ', '.join(recipients)
                    cout('Created invite for group chat: %s | %s' % (recipients, invite))
                    time.sleep(1)
                    with open('%sguilds.txt' % self.path, 'a+', encoding = 'UTF-8') as file:
                        file.write('Group chat: %s | %s | %s\n' % (recipients, channel['id'], invite))

    def backup_guilds(self):
        allowed_channel_types = [0, 2, 3, 5, 13]
        for guild in self.session.get('https://discord.com/api/v9/users/@me/guilds').json():
            if 'VANITY_URL' in guild['features']:
                invite = self.session.get('https://discord.com/api/v9/guilds/%s' % guild['id']).json()['vanity_url_code']
                cout('Created invite for: %s | %s' % (guild['name'], invite))
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
                            cout('Created invite for: %s | %s.' % (guild['name'], invite))
                            time.sleep(1)
                            break
                        elif response.status_code == 429:
                            cout('Rate limited, sleeping for: %s seconds.' % int(response.json()['retry_after']) + 1)
                            time.sleep(response.json()['retry_after'] + 1)
                            response = self.session.post('https://discord.com/api/v9/channels/%s/invites' % channel['id'], json = json)
                            if response.status_code == 200:
                                invite = response.json()['code']
                                cout('Created invite for: %s | %s.' % (guild['name'], invite))
                                time.sleep(1)
                                break
                            else:
                                invite = 'None'
                                cout('Couldn\'t create invite for: %s.' % guild['name'])
                                time.sleep(1)
                        else:
                            invite = 'None'
                            cout('Couldn\'t create invite for: %s.' % guild['name'])
                            time.sleep(1)
            with open('%sguilds.txt' % self.path, 'a+', encoding = 'UTF-8') as file:
                file.write('%s | %s | %s\n' % (guild['name'], guild['id'], invite))

    def get_channel(self, id):
        json = {
            'recipients': [id]
        }
        return self.session.post('https://discord.com/api/v9/users/@me/channels', json = json).json()['id']

    def backup_dms(self):
        if self.dm_backup_whitelist:
            ids = self.dm_backup_whitelist
        else:
            ids = []
            for user in self.session.get('https://discord.com/api/v9/users/@me/relationships').json():
                if user['type'] == 1 or user['type'] == 4:
                    ids.append(int(user['id']))
        for id in ids:
            time.sleep(1)
            try:
                channel_id = self.get_channel(id)
                response = self.session.get('https://discord.com/api/v9/users/%s' % id).json()
                tag = '%s#%s' % (response['username'], response['discriminator'])
            except:
                channel_id = id
                tag = 'Group Chat'
            cout('Started DM/GC backup with: %s (ID: %s)' % (tag, id))
            pins_list = []
            attachments_list = []
            messages_list = []
            messages = self.session.get('https://discord.com/api/v9/channels/%s/messages?limit=100' % channel_id)
            while len(messages.json()) > 0:
                for message in messages.json():
                    date = datetime.datetime.fromisoformat(message['timestamp']).strftime('%Y-%m-%d | %H:%M %p')
                    if message['attachments']:
                        _attachments_list = []
                        for attachment in message['attachments']:
                            attachments_list.append('Attachment name: %s | Attachment URL: %s' % (attachment['filename'], attachment['url']))
                            _attachments_list.append('Attachment name: %s | Attachment URL: %s' % (attachment['filename'], attachment['url']))
                        content = '(%s) %s#%s: %s | Attachment(s): %s' % (date, message['author']['username'], message['author']['discriminator'], message['content'], ', '.join(_attachments_list))
                    else:
                        content = '(%s) %s#%s: %s' % (date, message['author']['username'], message['author']['discriminator'], message['content'])
                    messages_list.append(content)
                    if message['pinned']:
                        pins_list.append(content)
                messages = self.session.get('https://discord.com/api/v9/channels/%s/messages?before=%s&limit=100' % (channel_id, messages.json()[-1]['id']))
            with open('%sDMs/%s.txt' % (self.path, id), 'w+', encoding = 'UTF-8') as file:
                file.write('Date: %s\n' % datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S %p %Z'))
                file.write('DMs with: %s (ID: %s)\n\n' % (tag, id))
                file.write('Statistics: All: %s, Pinned: %s, Attachments: %s\n\n' % (len(messages_list), len(pins_list), len(attachments_list)))
                file.write('--- PINNED MESSAGE(S) --- (Total: %s)\n\n' % len(pins_list))
                for message in pins_list:
                    file.write('%s\n' % message)
                file.write('\n--- ATTACHMENT(S) --- (Total: %s)\n\n' % len(attachments_list))
                for message in attachments_list:
                    file.write('%s\n' % message)
                file.write('\n--- ALL MESSAGE(S) --- (Total: %s)\n\n' % len(messages_list))
                for message in messages_list:
                    file.write('%s\n' % message)
            cout('Backed up %s message(s), %s pin(s), %s attachment(s) with: %s (ID: %s)' % (len(messages_list), len(pins_list), len(attachments_list), tag, id))

    def run(self):
        self.backup_relationships()
        if backup_dms:
            self.backup_dms()
        self.backup_group_chats()
        self.backup_guilds()

if __name__ == '__main__':
    Main().run()
