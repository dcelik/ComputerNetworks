import GlobalVars as g
import ServerFunctions as s
import AdminCommands as a

UserCommands = {"set_name": "setName", "disp_users": "users", "get_help": "help", "connect": "connect","disconnect": "disconnect", "admin": "admin"}

#------------User Accessible Commands/Command Parsing------------#
def parseCommandString(message, source_IP):
        """ Given a command message, calls the corresponding function and passes any arguments """
        #TODO: Move all user commands to a seperate class
        message = message.split()
        if message is not None:
                command = message[0];
        else: return;
        if len(message)>1:
                argument = message[1];
        else: argument=None;

        if command in a.AdminCommands:
            if g.Users[source_IP].admin:
                a.parseCommandString(command, argument, source_IP);
                return;
            else:
                s.sendMessage("You do not have access to this command.", source_IP);
                return;


        #Only allow logged in users to execute commands other than \connect
        if g.Users.get(source_IP) is not None and not command==Commands[connect]:
                s.requestConnect(source_IP);
                return;

        #Parse Commands
        if command == Commands['set_name']:
                if argument is not None:
                        setName(argument, source_IP);
                else:
                        s.sendMessage("Invalid input. Please enter a valid name in format \\setName [name]",source_IP);
        elif command == Commands['connect']:
                if argument is not None:
                        connect(argument, source_IP);
                else:
                        s.sendMessage("Invalid input. Please enter a valid name in format \\connect [name]",source_IP);
        elif command == Commands['admin']:
                if argument is not None:
                       admin(argument, source_IP);
                else:
                        s.sendMessage("Invalid password entry. Please enter a valid entry in format \\admin [password]",source_IP);
        elif command == Commands['disconnect']:
                disconnect(source_IP);
        elif command == Commands['disp_users']:
                dispUsers(source_IP);
        elif command == Commands['get_help']:
                sendHelp(source_IP);
        else:
                s.sendMessage("Invalid command.", source_IP);
                

def admin(pw, source_IP):
        """ Toggle admin status on user """
        #TODO: add password hashing
        if pw==g.admin_pw:
                s.sendMessage(g.Users[source_IP].toggleAdmin(), source_IP);
        else:
                s.sendMessage("Invalid admin login.",source_IP);

def invisible(source_IP):
        """ Toggle invisible status on user """
        #TODO: make invisibility actually have an effect
        s.sendMessage(g.Users[source_IP].toggleInvisible(),source_IP);

                
def connect(name, source_IP):
        """ Creates a new user session """
        if Users.get(source_IP) is not None:
                renewConnection(source_IP);
        elif source_IP in g.BannedIPs:
            sendMessage("You are currently banned from the server.",source_IP);
        elif not name in g.IPs.keys():
            g.Users[source_IP] = User(name);
            g.IPs[name] = source_IP;
            s.serverWelcome(source_IP);
        else:
                s.sendMessage("Name already taken.",source_IP);

def disconnect(source_IP):
        """ Delete a user session """
        del g.IPs[g.Users(source_IP).alias];
        del g.Users[source_IP];
        s.sendMessage("Successfully logged out.", source_IP);
        
def setName(name, source_IP):
        """ Resets a client's alias """
        if not name in g.IPs.keys();
                del g.IPs[g.Users(source_IP).alias];
                g.Users(source_IP).alias = name;
                g.IPs[name] = source_IP;
        else:
                s.sendMessage("Name already taken.", source_IP);

def dispUsers(dest_IP):
        """ Sends a list of all logged in user aliases """
        #TODO: Implement invisibility
        message = "Users currently in chat: \n"
        for user in g.IPs.keys():
                message += user + "\n"
        s.sendMessage(message, dest_IP);
                
def sendHelp(dest_IP):
        #TODO: Add descriptions of functions
        """ Sends a message to the destination IP listing (and ideally explaining) functions available to them """
        for command in UserCommands.values():
                command_string += "//" + command + ", "
        help_message = "Available Commands: " + command_string[:-2];
        s.sendMessage(help_message, dest_IP);

        admin_command_string = "Available Admin Commands:"
        if g.Users[dest_IP].admin:
            for command in a.AdminCommands.values():
                admin_command_string += command + ", ";
        s.sendMessage(admin_command_string, dest_IP);

        
def renewConnection(dest_IP):
        """ Not Yet Implemented """
        #TODO: Implement
