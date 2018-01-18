import random

def is_divided(num, div):
    answer = int(raw_input("Is it divided by {}?".format(div)))
    if num % div == 0 :
        real_answer = 1
    else:
        real_answer = 0
    if answer == real_answer:
        print "well done!!!!!!!!!!!!!!"
    else:
        print "You are wrong :("
    

while True:
    num = random.choice(range(1000))
    print "\r\n1 for yes and 0 for no "
    print num
    for i in range(2,10):
        is_divided(num, i)
