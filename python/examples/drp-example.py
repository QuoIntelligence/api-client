from quointelligence import QIClient

client = QIClient('<user name>', '<password>')
tickets = client.drp(since='60d')  # 60 days
#tickets = client.drp(since='1h')   # 1 hour
#tickets = client.drp(since='15m')  # 15 minutes

for t in tickets:
    print(client.ticket(t['id']))
    print('~~~~~~~')
