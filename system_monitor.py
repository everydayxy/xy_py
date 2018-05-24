import psutil

class obj1:
    def __init__(self,service_name):
        self.servicename = service_name
    def check_service(self):
        pids = psutil.pids()
        #print(pids)
        for pid in pids:
            check_name = psutil.Process(pid).name()
            #print(check_name)
            if self.servicename == check_name:
                return True
        return False

ob2 = obj1("python.exe")

print (ob2.check_service())