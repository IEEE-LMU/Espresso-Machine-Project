import pickle
import hashlib

f = open('./users','r')
users = pickle.load(f)
f.close()

print(users)


print('Swipe card of user to remove')
raw_card = raw_input()
hash = hashlib.sha256(raw_card.encode())
card = hash.hexdigest()

user = None
for u in users:
    if u['card'] == card:
        user = u
        break

if user == None:
    print('Unknown User!')
    quit()

print ('Are you sure you want to remove user ' + user['name'] + '? (y/n)')
decision = raw_input()
if decision == 'y':
    users.remove(user)
    print('User removed!')
else:
    print('Not removed')

f = open("./users","w")
pickle.dump(users,f)
f.close() 
