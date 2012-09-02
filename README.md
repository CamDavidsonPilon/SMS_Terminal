Turn your Android into a SMS-Based Terminal
===========================================

See [this intro] (http://camdp.com/blogs/turn-your-android-phone-sms-based-command-line) for a description of 
what can be accomplished.

TL;DR
------
Basically, send your Android device SMS messages containing commands and your device will run said commands. Useful if
your phone is not on you (it is charging, lost etc.) and you hate that feeling. Ex:
If I text (from my friend's phone) my Android 

    root -h
    
I receive

    -h #help <br/>
    -s #all scripts available
    -d [script] #doc for [script]
    -r [script] #run [script]
    -l #location
    -u [pass] #unread messages

which I can use to send more commands to my phone. 

Installation Guide
----------------

First, you need two apps: [SL4A](http://code.google.com/p/android-scripting/) and [Tasker](http://tasker.dinglisch.net/). Tasker is paid, yes, but if you have an Android you're gunna want Tasker. 

Install SL4A and the Python package.

In the script that initalizes your SMSTerminal object, smsReciever.py, specify a *root word* and a *password*. The root word, *root* in my 
example above, keeps just anyone from running commands. It can shared with friends as you wish. If things get unruley, just
change the root word.

The password is for more sensitive commands, like returning all unread msgs.


SMSTerminal.py contains some default commands like the ones above, and you can create your own. The main structure should look like:

    def _x(self, [optinal args], [optinal defaults] )
        try:
            """Do fun stuff here. If everything goes well, return MSG to text back."""
            return (MSG, True)
        except:
            """Oh uh, something went wrong. Let MSG be some error message."""
            return (MSG, False)

For example:

    def _r(self, script):
        #r: runs a script on the phone and returns the result. Usage:
        #-r <script>
        try:
            script = self._removeTrailingPy( script ) 
            execfile('/sdcard/sl4a/scripts/' + script + '.py' )
            return ("%s ran successfully."%script, True)
        except:
            return ("No script called %s exists in /sdcard/sl4a/scripts/"%script, False)
        
        
        

Finally, create a Tasker profile to run whenever a text is received. The task should be to run the script smsReceiver.py (which
should be in the same folder as SMSTerminal.py). 

That should be it!

Lastly
-----------------
email me at cam.davidson.pilon@gmail.com and visit me at [camdp.com](http://www.camdp.com) and follow me at [cmrn_dp](http://twitter/cmrn_dp)
            
        
