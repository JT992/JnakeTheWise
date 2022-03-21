import tweepy
import random
from keys import BEARER, ACC_KEY, ACC_SEC, API_KEY, API_SEC, ACCOUNT_ID
from time import sleep
from datetime import datetime, timezone

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
           ['tin of baked beans', 'tins of baked beans'], 'lemon')

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


# Sections of General Wisdom greetings
gw_first = ('Hi everyone!', 'Hello everyone!', 'Hi all!', 'Hello all!', 'Good afternoon, students!',
            'Good day, students!', 'Good afternoon, wise ones!', 'Good day, wise ones!', 'Good afternoon, Twitter!',
            'Good day, Twitter!')
gw_second = ('Ready for today\'s General Wisdom?', 'It\'s time for today\'s General Wisdom.',
             'Get ready for today\'s General Wisdom.', 'Time for today\'s General Wisdom.',
             'Prepare for today\'s General Wisdom!', 'Behold today\'s General Wisdom.')
gw_third = ('Here goes:', 'Behold:', 'Heed it:', 'And it says:', 'It is:', 'I decree:', 'Bask in its glory:',
            'Prepare yourselves, it\'s a big one:')
gw_final = ('I know, right?', 'Powerful stuff.', 'Enjoy.', 'Good luck!', 'Have a nice day!', 'Have a wonderful day!',
            'I will see you tomorrow, students.', 'Let that sink in.')


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


def generate_general():
    return f'{random.choice(gw_first)} {random.choice(gw_second)} {random.choice(gw_third)}' \
           f'\n\n"{generate_wisdom()}"\n\n{random.choice(gw_final)}'


def get_last_id():
    with open('last_id.txt', 'r') as f:
        val = int(f.read().strip())
    return val


def set_last_id(val):
    with open('last_id.txt', 'w') as f:
        f.write(str(val))


def post_general():
    pass  # add in next commit


def main():
    last_id = get_last_id()
    mentions = client.get_users_mentions(
        id=ACCOUNT_ID,
        since_id=last_id,
    )
    print(mentions)
    now = datetime.now(timezone.utc)
    if now.hour == 5 and now.minute == 0:
        post_general()
    if mentions.data is None:
        return
    for mention in reversed(mentions.data):
        last_id = mention.id
        tweet = client.get_tweet(id=last_id, expansions='author_id')
        user = tweet.includes['users']
        client.create_tweet(text=f'Hi @{user[0].username}! Your Personal Wisdom is:'
                                 f'\n\n"{generate_wisdom()}"\n\nHave a nice day!', in_reply_to_tweet_id=last_id)
    set_last_id(last_id)


if __name__ == '__main__':
    while True:
        main()
        sleep(60)  # don't want to go over the tweet cap!
