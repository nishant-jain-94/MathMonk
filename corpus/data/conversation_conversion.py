import json

with open('conversations.corpus.json') as corpus:
	conversations = json.load(corpus)['conversations']

with open('conversations.corpus.csv', 'w') as corpus:
	for conversation in conversations:
		[corpus.write(','.join(['"'+sentence+'"', '"'+conversation[index + 1]+'"' + "\n"])) for index, sentence in enumerate(conversation) if index != len(conversation)-1]
		

