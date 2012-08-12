'''
Created on 2012-08-11

@author: Cameron
'''
from time import sleep

import android



class SMSTerminal(object):


    def __init__(self, root_word, password):
        """
        root_word: a word that your phone will recognize that the incoming text is for itself. ex: "root" or "$"
        password: a password for more sensitive commands, like returning all unread msgs.
        """
        self.root_word = root_word
        self.msg = ""
        self.droid = android.Android()
        self._password = password #used for more sensitive commands
        self.verbose = True # the command -q will turn this off and return no texts.
        self.SMS = None
    

    
    
    def run(self, SMS):
        """this is the main function that is called on each text recived."""
        self.SMS = SMS
        body = SMS['body']
        if( self._isCommand( body ) ):
        
            commandList = self._getCommandList(body)
            self._iterateCommandList( commandList  )
            if (self.msg and self.verbose):
                self._sendSMS(self.msg, SMS['address'] )
        else:
            return
            

    
    def _h(self):
        """
-h #help
-s #all scripts
-d <script> #doc for script
-r <script> #run script
-v #verbose
-u <pass> #unread msgs
-m <pass> #return unread
-l #location"""
        return (self._h.__doc__, True)
        
    def _s(self):
        """
s: returns all scripts available to run. Usage: -s
        """
        return ("""say_time.py, findMe.py, take_picture.py """, True)
        
    def _d(self, script):
        """
d: returns the documentation of a script. Usage:
-d <script name>
See -s for all available scripts.
        """
        script = self._removeTrailingPy(script)
        try:
            #This will catch import errors, that is the script does not exist.
            exec( 'from ' + script + ' import DOC' )
        except ImportError,e:
            return  ("No script named %s.py available."%script, False)
        try:
            #This will catch if the variable DOC doesn't exist.
            return (DOC, True)
        except NameError, e:
            return  ("No documentation present for script %s available."%script, False)
    
    
    def _r(self, script):
        """
r: runs a script on the phone and returns the result. Usage:
-r <script>
        """
        try:
            script = self._removeTrailingPy( script ) 
            execfile('/sdcard/sl4a/scripts/' + script + '.py' )
            return ("%s ran successfully."%script, True)
        except:
            return ("No script called %s exists in /sdcard/sl4a/scripts/"%script, False)
    
    def _q(self):
        """
q: return no texts to address. Quiet mode. Usage: -q
        """
        self.verbose = False;
        return ("", True)
        
    

    
    def _l(self):
        """l: return the current location, in long, lad coords of the device. Usage: -l
        """
        (longt, lat) = self._getLocation()
        return ( "Long: %f, Lat: %f."%(longt,lat), True)
        
        
    def _u(self, password):
        """
u: return all unread SMS messages. Password required. Usage: 
-u <password>
        """
        if not self._checkPassword(password):
            return ("Wrong password for -m", False)
        else:
             unreadMsgs = self.droid.smsGetMessages(1).result
             no_unreadTexts = len(unreadMsgs)
             #no_missedCalls = len( get missed calls )
             d = self._tally_msgs( unreadMsgs )
             body = "You have %d new sms messages from: \n "%(no_unreadTexts)
             body += str(d)
             return (body, True)
        
        
    def _m(self, password):
        """
m: return all unread messages. Requires password. Usage:
-m <password>
        """
        if not self._checkPassword(password):
            return ("Wrong password for -u", False)
        else:
            unreadMsgs = self.droid.smsGetMessages(1).result
            body = ""
            for msg in unreadMsgs:
                body += "%s, %s, %s \n\n"%( msg['name'], msg['address'], msg['body'] )
            if body=="":
                return ("No unread messages.", True)
            else:
                return (body, True)

            
   #Utility functions

    
    def _sendSMS(self, msg, address):
        for text in self._split_sms_response( msg):
            self.droid.smsSend( address, text )
            
    
        def _getCommandList(self, commandString):
        """creates a list of commands/arguments from the body of the text"""
        return commandString.strip().split(" ")[1:] #ignore the root_word.
        
    def _isCommand(self, body):
        """Returns True if the message is for the terminal."""
        iscommand = False
        if( body.lower().startswith(self.root_word ) ):
            iscommand=True
        return iscommand
        
    def _iterateCommandList( self, commandList ):
        if not commandList[0].startswith("-"):
            #user must supply a command initially.
            self.msg = self._h() #help command.
       
        i=1
        commandList.append("END")
        nextCommand = commandList[0][1]
        arguments = []
        while i<len(commandList):
            command = commandList[i]
            if command.startswith("-") or command == "END":
                try:
                    temp_msg, ok = getattr( self, "_"+nextCommand)(*arguments) #this should run __x(*args). Note the use of *
                    if ok:
                        self.msg += temp_msg.strip() + "\n"
                    else:
                        self.msg = temp_msg
                        return
                    nextCommand = command[1]
                except TypeError:
                    #if the got the arugments wrong, send them back the documentation for that command
                   try:
                        self.msg = getattr( self, "_"+nextCommand).__doc__
                        return 
                   except:
                        #there is no _<nextCommand>
                        self.msg = self._h()
                arguments = []
            else:
                arguments.append( command )
            
            i+=1

    
    def _split_sms_response(self, body ):
       """This function splits a message into a list of 145 character pieces"""
       texts = []
       max_len = 145
       pos = 0 
       while 1:
           if pos+max_len < len(body):
              texts.append( body[pos:pos+max_len] )
              pos += max_len
           else:
              texts.append( body[pos:] )
              return texts
        
        
    def _removeTrailingPy(self, script):
            pos = script.split(".py")
            return pos[0]
    
    
    def _getLocation(self):
        self.droid.startLocating()
        sleep(20)
        location = self.droid.readLocation().result
        self.droid.stopLocating()

        if 'gps' in location:
            location = location['gps']
        elif 'network' in location:
            location = location['network']
           
        lat = location['latitude']
        longt = location['longitude']
        return [(lat, longt), True]
        
    
    def _tally_msgs(self, unreadMsgs ):
        d = {}
        for msg in unreadMsgs:
            try:
                name = msg['sender']
            except KeyError:
                name = msg['address']
            if name not in d.keys():
                d[name] = 1
            else:
                d[name] += 1
        return d
        
    
    
    
       
    def _checkPassword(self, password):
        if self._password == password:
            return True
        else:
            return False
            

        

        