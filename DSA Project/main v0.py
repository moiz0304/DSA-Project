from bardapi import Bard
from bardapi import BardCookies
from keys import cookie_dict
bard = BardCookies(cookie_dict=cookie_dict)

image = open('pic.jpg', 'rb').read() # (jpeg, png, webp) are supported.
bard_answer = bard.ask_about_image('Give a one line Image Description in English', image)
print(bard_answer['content'])
