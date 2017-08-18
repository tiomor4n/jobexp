#https://github.com/burnash/gspread
def GetGsht():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    from django.conf import settings as djangoSettings
    from .models import oper_para

    fileroute = djangoSettings.STATIC_ROOT  + '\\'
    #fileroute = 'D:\google service account key' + '\\'
    scope = ['https://spreadsheets.google.com/feeds']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(fileroute + 'auth.json', scope)
    gc = gspread.authorize(credentials)
    sht1 = gc.open_by_key(oper_para.objects.get(name='shtkey').content)
    

    return sht1

def GetJobDesc():
    sht1 = GetGsht()
    sht11 = sht1.get_worksheet(0)
    acnt=0
    for x in sht11.col_values(1):
        if x!= '':
            acnt = acnt +1
        else:
            break
    
    
    strdesc = ''
    jobid = ''
    jobname = ''
    joblocation = ''
    jobdesc = ''
    joburl = ''
    
    for i in range(2,acnt+1):
    	jobid = sht11.cell(i,2).value
    	jobname = sht11.cell(i,3).value
    	joblocation = sht11.cell(i,4).value
    	jobdesc = sht11.cell(i,5).value
    	joburl = sht11.cell(i,6).value
    	strdesc = strdesc + u'工作ID:{} \n 工作名稱:{} \n 工作地點:{} \n 工作敘述:{} \n 連結:{} \n'.format(jobid,jobname,joblocation,jobdesc,joburl)

    return strdesc

def WriteCustData(Jobid,CustName,CustTel,CustGender):
    from datetime import datetime as dt
    nowstr = dt.now().strftime('%Y/%m/%d %H:%M:%S')
    sht1 = GetGsht()
    sht12 = sht1.get_worksheet(1)
    #acnt = len(sht12.col_values(1))-1000
    sht12.append_row([nowstr,Jobid,CustName,CustTel,CustGender])
    return 'ok'