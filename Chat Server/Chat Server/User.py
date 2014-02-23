import default_client_port from GlobalVars

class User:
    isInvisible = False;
    isAdmin = False;
    
    messagesInTimeout=0;
    timeSinceActive=0;

    port = default_client_port
    
    def __init__(self, alias):
        self.alias = alias;

    def toggleAdmin():
        self.isAdmin = not self.isAdmin;
        return "Admin status: " + str(isAdmin);

    def toggleInvisible():
        self.isInvisible = not self.isInvisible;
        return "Invisibility: " + str(self.isInvisible);

