#you can play around with this, I just wrote it to make the examples self-containing.

import SMSTerminal
import android


ROOT = "rootword"
PASS = "password"

droid = android.Android()

sms_tmnl = SMSTerminal.SMSTerminal( ROOT, PASS )

try:
    recent_sms = droid.smsGetMessages(1).result[0]
except: 
    recent_sms = droid.smsGetMessages(0).result[0]
    
    
sms_tmnl.run( recent_sms) 



