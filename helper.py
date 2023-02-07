from pushbullet import  Pushbullet
pb = Pushbullet("o.HUC1HDJBKNeUKcSDNnrJnJMMOIjhveP2")
def send(company,number):
    pb.push_note(company, number)