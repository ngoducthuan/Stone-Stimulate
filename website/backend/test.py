from  werkzeug.security import generate_password_hash

text = "abcd"
hash1 = generate_password_hash(text)
print(hash1)
if text == hash1:
    print("OKe")