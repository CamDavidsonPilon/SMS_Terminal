
import SMSTerminal
import android


ROOT = "root"
PASS = "sl4a"

droid = android.Android()

sms_tmnl = SMSTerminal.SMSTerminal( ROOT, PASS )


try:
    recent_sms = droid.smsGetMessages(1).result[0]
except: 
    recent_sms = droid.smsGetMessages(0).result[0]
    
    
sms_tmnl.run( recent_sms) 



