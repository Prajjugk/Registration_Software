class observer():
  def update(self,event,data):
    pass

class Emailnotifier(observer):
  def update(self,event,data):
    if event== "Registration":
      print(f" Email sent to {data['email']}: Welcome {data['username']}! You have registered successfully")
    elif event=="Login":
      print(f" Email sent to {data['email']}: You logged in successfully!")


class notifier():
  def __init__(self):
    self.observer=[]

  def attach(self,observer):
    self.observer.append(observer)
  
  def notify(self,event,data):
    for obs in self.observer:
      obs.update(event,data)



  
    