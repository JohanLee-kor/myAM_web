class XASessionEvents:
    logInState =0
    
    def OnLogin(self, code, msg):
        print("OnLogin method is called")
        print(str(code))
        print(str(msg))
        if str(code) == '0000':
            XASessionEvents.logInState = 1
            
    def OnLogout(self):
        # XASessionEvents.logInState=0
        print("OnLogout method is called")

    def OnDisconnectServer(self):
        print("OnDisconnect method is called")
