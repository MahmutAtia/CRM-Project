from pushbullet import  Pushbullet
with open("%data%/key.txt","r") as f:
    key = f.readlines()[0]
pb = Pushbullet(key)
def send(company,number):
    pb.push_note(company, number)

