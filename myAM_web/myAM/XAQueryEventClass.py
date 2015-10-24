class XAQueryEvents:
    queryState = 0
    querySuccess = 0
    def OnReceiveData(self, szTrCode):
        print("XAQueryEvents: ReceiveData")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, messageCode, message):
        print("XAQueryEvents: ReceiveMessage")
        print("XAQueryEvents: message: ",message)
        print("XAQueryEvents: messageCode",str(messageCode))
        XAQueryEvents.querySuccess = int(messageCode)
