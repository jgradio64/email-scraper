test = [b'Citi Custom Cash\xc2\xae Card', 'utf-8', b'<citicards@info15.citi.com>', None]
# test = [b"\xe2\x80\xa2 Don't forget \xe2\x80\x92 Please read: Benjamin, we kindly encourage you to view this credit limit information...", 'utf-8']

# test[0] = test[0].decode('utf-8')
# test[2] = test[2].decode('utf-8')

# Decode any byte strings.
for x in range(len(test)):
    if isinstance(test[x], bytes):
        test[x] = test[x].decode('utf-8')
    elif isinstance(x, str):
        pass

test.remove("utf-8")
test.remove(None)
# test = filter(None, test)
# print(test.index("@"))
res = [i.find('@') for i in test]
email_address_index = None
for x in range(len(res)):
    if(res[x] > 0):
        email_address_index = x
    
# get just the email address from the list
print(test[x])