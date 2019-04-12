import pickle
import hashlib

f = open('./users','r')
users = pickle.load(f)
f.close()

print(users)

while True:
    print('Swipe card')
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
        continue
    
    print(user['name'])
    print('Your favorite coffee is: ' + str(user['coffee']))