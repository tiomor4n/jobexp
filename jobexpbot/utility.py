import os
import json
from django.conf import settings as djangoSettings


#fileroute = djangoSettings.STATIC_ROOT  + '\\'
#prefilename = 'bot\linemsg_'
fileroute = '.' + djangoSettings.STATIC_URL
prefilename = 'bot/linemsg_'

def ReadFromStaticBOT(mid):
    import json
    import sys
    sys.setdefaultencoding='utf8'

    filename = prefilename + mid
    filepath = fileroute + filename
    with open(filepath) as json_data:
        d = json.load(json_data)
    return json.dumps(d)

def WriteToStaticBOT(msgstr='',way=''):
    from datetime import datetime
    import calendar
    #import sys
    #sys.setdefaultencoding='utf8'
    msgjson = json.loads(msgstr)

    mid = mid = msgjson['events'][0]['source']['userId']
    mtext = msgjson['events'][0]['message']['text']
   
    filename = prefilename + mid
    filepath = fileroute + filename
    tstamp = calendar.timegm(datetime.now().timetuple())
    #確認檔案是否存在
    if os.path.isfile(filepath):
        #print u'有檔案'.encode('utf-8')
        print (u'有檔案')
        with open(filepath) as msgkeep:
            jdata = json.load(msgkeep)
            stepcnt = jdata['nowstep']
            
        jdata['timestamp'] = tstamp
        talk = jdata['step' + str(stepcnt)]
        if way == 'ask':
            
            stepcnt = stepcnt + 1
            jdata['step' + str(stepcnt)] = {}
            jdata['step' + str(stepcnt)]['ask'] = mtext
            #print 'ask:' + mtext.encode('utf-8')
        else:    #reply
            talk['reply'] = mtext
            #print 'reply:' + mtext.encode('utf-8')
                
        jdata['nowstep'] = stepcnt
                
        with open(filepath, 'w+') as msgwrite:
            #msgwrite.write(json.dumps(jdata,encoding="UTF-8", ensure_ascii=False).encode('utf-8'))
            msgwrite.write(json.dumps(jdata))
            msgwrite.close()
            
    else:
        #print u'沒檔案'.encode('utf-8')
        print (u'沒檔案')
        step = 0
        msgkeep = {}
        msgkeep['timestamp'] = tstamp
        msgkeep['nowstep'] = step
        msgkeep['step' + str(step)] = {}
        msgkeep['step' + str(step)]['ask'] = mtext
        #print 'ask:' + mtext.encode('utf-8')
        
        file = open(filepath , 'w+')
        file.write(json.dumps(msgkeep))
        file.close()

def CheckStep(mid=''):
    purporse = ''
    step = 0
    last_ask = ''
    timestamp = 0
    last_reply=''

    filename = prefilename + mid
    print (filename)
    #filepath = './' + djangoSettings.STATIC_URL + '/bot/' + filename
    filepath = fileroute +  filename
    print (filepath)
    
    #先確認檔案是否存在
    if os.path.exists(filepath):
        with open(filepath) as json_data:
            data= json.load(json_data)
            step = data['nowstep']
            purporse = data['step0']['ask']
            if step == 0:
                last_ask = data['step' + str(step)]['ask']
                #last_reply = data['step' + str(step)]['reply']
            else:
                last_ask = data['step' + str(step - 1)]['ask']
                last_reply = data['step' + str(step - 1)]['reply']
            timestamp = data['timestamp']
    
    return purporse,step,last_ask,last_reply,timestamp

def CheckDialog(mid):
    filepath = fileroute + prefilename + mid
    if os.path.isfile(filepath):
        return True
        

def RemoveDialog(mid):
    filepath = fileroute + prefilename + mid
    os.remove(filepath)
    print ('initial jobapply')


def WriteCustProfile(mid):
    from .gspread import WriteCustData
    filename = prefilename + mid
    filepath = fileroute +  filename
    Jobid = ''
    CustName = ''
    CustTel = ''
    CustGender = ''
    if CheckDialog(mid):
        with open(filepath) as json_data:
            data= json.load(json_data)
            Jobid = data['step1']['ask']
            CustName = data['step2']['ask']
            CustTel = data['step3']['ask']
            CustGender = data['step4']['ask']
            WriteCustData(Jobid,CustName,CustTel,CustGender)
            return 'ok'
    else:
        return 'no file'