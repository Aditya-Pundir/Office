import json

with open("C:\\Users\\adity\\Documents\\Code-Playground\\Freelance\\1_Letz-Compare-Scraping\\tango_site\\content.txt", "r") as f:
    content = f.readlines()
devices = json.loads(json.loads(content[0]))["devices"]
for device in devices:
    print(device)
