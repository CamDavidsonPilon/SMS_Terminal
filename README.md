Turn your Android into a SMS-Based Terminal
===========================================

See [this intro] (http://camdp.com/blogs/turn-your-android-phone-sms-based-command-line) for a description of 
what can be accomplished.

TL;DR
------
Basically, send you Android device SMS messages containing commands and your device will run said commands. Useful if
your phone is not on you and you hate that feeling. Ex:
If I text (from my friends phone) my phone 

    root -h
    
I receive

    -h #help <br/>
    -s #all scripts available
    -d [script] #doc for [script]
    -r [script] #run [script]
    -l #location
    -u [pass] #unread messages

which I can use to send more commands to my phone. 

How Does it Work?
----------------

First, you need two apps: [SL4A](http://code.google.com/p/android-scripting/) and [Tasker](http://tasker.dinglisch.net/). Tasker is paid, yes, but if you have an Android you're gunna want Tasker. 

Install SL4A and the Python package.

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
        
        
        
Easy. Thirdly, edit smsReceiver.py to include a *root word* and *password*. The root word is the word that your phone will
recognize is meant for it, eg: "root" in my examples above. Password is used for more sensitive commands like retrieving location
or unread messages. 

Finally, create a Tasker profile to run whenever a text is received. The task should be to run the script smsReceiver.py (which
should be in the same folder as SMSTerminal.py). 

That should be it!

Lastly
-----------------
email me at cam.davidson.pilon@gmail.com and visit me at [camdp.com](http://www.camdp.com) and follow me at [cmrn_dp](http://twitter/cmrn_dp)
            
        