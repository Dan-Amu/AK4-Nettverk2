import re
username_regex = re.compile(r"[^a-z]+g")
while True:

    print(username_regex.match(input("Test string:")))
