import tweepy
import random
from keys import BEARER, ACC_KEY, ACC_SEC, API_KEY, API_SEC
from time import sleep

client = tweepy.Client(
    bearer_token=BEARER,
    consumer_key=API_KEY,
    consumer_secret=API_SEC,
    access_token=ACC_KEY,
    access_token_secret=ACC_SEC
)

# Object formatting:
# str = regular count noun
# list[str, str] = irregular count noun
# list[str] = mass noun
objects = (['goose', 'geese'], 'puddle', ['box', 'boxes'], 'pavement', 'turtle', 'towel',
           ['can of squirty cream', 'cans of squirty cream'], ['butter'], 'egg', 'necklace',
           ['plush octopus', 'plush octopuses'], 'window', 'lime', 'clay pot', 'whistle', 'book', ['torch', 'torches'],
           'mouse mat', 'magnet', 'purse', 'sticker book', ['cup of tea', 'cups of tea'], 'washing machine', 'candle',
           ['sheep'], 'keyboard', 'charging cable', 'marble', 'hamster', 'bottle',
           ['pair of safety goggles', 'pairs of safety goggles'], 'feather', 'apple', ['steak knife', 'steak knives'],
           ['butter knife', 'butter knives'], 'boat', ['fish'], 'teddy bear', ['paintbrush', 'paintbrushes'],
           'harmonica', 'desk', 'door', 'pillow', 'unicorn', 'button', 'belt', 'radio', 'locket', 'key', 'hat',
           'quartz crystal', 'bracelet', 'spoon', ['chalk'], 'spanner', ['perfume'], ['soup'], ['cheese'],
           ['tin of baked beans', 'tins of baked beans'])

# People
# noinspection SpellCheckingInspection
people = ('Theresa May', 'Boris Johnson', 'Priti Patel', 'Donald Trump', 'Joe Biden', 'Barack Obama', 'Keir Starmer',
          'Jnake the Wise', 'Nigel Farage', 'David Walliams', 'Jeremy Corbyn', 'Albert Einstein', 'Emma Watson',
          'Daniel Radcliffe', 'Archimedes', 'Pythagoras', 'Jesus Christ', 'Abraham Lincoln', 'Richard Ayoade',
          'Daniel Craig', 'Benedict Cumberbatch', 'Tom Holland', 'Stephen Fry', 'Hugh Laurie', 'David Tennant',
          'Simon Pegg', 'Sir David Attenborough', 'Jeremy Clarkson', 'Simon Cowell', 'Jonathan Ross', 'Gordon Ramsay',
          'Margaret Thatcher', 'Anne Hegarty', 'Bradley Walsh', 'James May', 'Richard Hammond', 'Matt LeBlanc',
          'Jennifer Aniston', 'Peter Kay', 'Greg Davies', 'Alex Horne', 'Frank Skinner', 'Dave Gorman')

# Templates
templates = ('Fry the whole *OBJECT*.', '*PERSON* is a *OBJECT*.', '*PERSON* may or may not be themselves.',
             'The *OBJECTS* are lying to you.', 'Don\'t you want to see how *PERSON* will ruin it?',
             'What about *OBJECTS*?', 'Spare a thought for *PERSON*\'s *OBJECT*.',
             'What if *PERSON* is actually *PERSON*?', '*PERSON* is planning to eat a *OBJECT*.',
             'Is your *OBJECT* really worth it?', 'Is the *OBJECT* is crucial to your success?',
             'Does *PERSON* really need their *OBJECT*?',
             'Look in the mirror. Say "*PERSON*" over and over. Do you see them?',
             'Look in the mirror. Say "*OBJECT*" over and over. Does it come to you?',
             'Think about the best present you ever received. Are you thinking about that *OBJECT*? You should.',
             'Contemplate *OBJECTS* until they make sense.', 'Acquire *OBJECTS*. Imagine *PERSON*. Feel bliss.',
             'Apologise to your *OBJECTS*.', '*PERSON* has done so much for you. Think about them today.',
             'The best advice you\'ll receive involves *OBJECTS*.',
             'Your *OBJECT* is perfect, no matter what *PERSON* says.', '*PERSON*? *PERSON*? *PERSON*?',
             'When did that *OBJECT* first make sense to you?', 'Everything you know about *OBJECTS* is wrong.',
             'You\'ve never thought about *OBJECTS*?', '*PERSON* doesn\'t believe in you. Show them they\'re wrong.',
             'Rethink your whole position on *PERSON*.', 'Rethink your whole position on *OBJECTS*.')


def generate_wisdom():
    base = random.choice(templates).split('*')
    for index, segment in enumerate(base):
        if segment == 'OBJECT':
            replace = random.choice(objects)
            if isinstance(replace, list):
                replace = replace[0]
        elif segment == 'OBJECTS':
            replace = random.choice(objects)
            if isinstance(replace, str):
                replace = f'{replace}s'
            else:
                replace = replace[0] if len(replace) == 1 else replace[1]
        elif segment == 'PERSON':
            replace = random.choice(people)
        else:
            continue
        base[index] = replace
    return ''.join(base)


def get_last_id():
    with open('last_id.txt', 'r') as f:
        val = int(f.read().strip())
    return val


def set_last_id(val):
    with open('last_id.txt', 'w') as f:
        f.write(str(val))


def main():
    last_id = get_last_id()
    mentions = client.get_users_mentions(id='1430831783675826177', since_id=last_id)
    print(mentions)
    if mentions.data is None:
        return
    for mention in reversed(mentions.data):
        last_id = mention.id
        tweet = client.get_tweet(id=last_id, expansions='author_id')
        user = tweet.includes['users']
        client.create_tweet(text=f'Hi @{user[0].username}! Your Personal Wisdom today is:'
                                 f'\n\n"{generate_wisdom()}"\n\nHave a nice day!', in_reply_to_tweet_id=last_id)
    set_last_id(last_id)


if __name__ == '__main__':
    main()
