import random
chapters_amount = 8  #change it to 6 if doing short test
chapters = range(1,chapters_amount + 1)
for i in xrange(chapters_amount):
    temp = random.choice(chapters)
    chapters.remove(temp)
    print temp
raw_input("And that's all. Good luck!")
