import pickle
import hashlib

f = open('./users','r')
users = pickle.load(f)
f.close()

print('Current user list:')
print(users)

print('Enter your name:')
name = raw_input()

coffee = 0
while True:
    print('What is your favorite coffee? (1-3)')
    coffee = input()
    if (1<=coffee and coffee<=3):
        break
    print('Invalid option. Please try again')

print('Swipe your card')
raw_card = raw_input()
hash = hashlib.sha256(raw_card.encode())
card = hash.hexdigest()

user = None
for u in users:
    if u['card'] == card:
        user = u
        print('User already in the system!')
        quit()

newUser = {'card':card,'name':name,'coffee':coffee,'admin':False}

users.append(newUser)

f = open("./users","w")
pickle.dump(users,f)
f.close() 