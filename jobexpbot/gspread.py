#https://github.com/burnash/gspread
def GetJobDesc():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    from django.conf import settings as djangoSettings

    fileroute = '.' + djangoSettings.STATIC_URL
    #fileroute = 'D:\google service account key' + '\\'
    scope = ['https://spreadsheets.google.com/feeds']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(fileroute + 'auth.json', scope)
    gc = gspread.authorize(credentials)
    sht1 = gc.open_by_key('1bCAYb2AlqEMcDezraXYU3QepIvKXh9EOJxkfOfs2Yps')
    sht11 = sht1.get_worksheet(0)
    acnt = len(sht11.col_values(1))-1000
    #sht11.insert_row(['2017/8/6','W','K','W','D','1'],acnt + 1)
    
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
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    from django.conf import settings as djangoSettings
    scope = ['https://spreadsheets.google.com/feeds']
    fileroute = '.' + djangoSettings.STATIC_URL
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(fileroute + 'auth.json', scope)
    gc = gspread.authorize(credentials)
    sht1 = gc.open_by_key('1bCAYb2AlqEMcDezraXYU3QepIvKXh9EOJxkfOfs2Yps')
    sht12 = sht1.get_worksheet(1)
    #acnt = len(sht12.col_values(1))-1000
    sht12.append_row(['2017/8/8',Jobid,CustName,CustTel,CustGender])
    return 'ok'