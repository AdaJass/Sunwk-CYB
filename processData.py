import asyncio
from pyquery import PyQuery as pq
import config
from datetime import datetime as dt, timedelta as td


async def processData(lastpage, session):
    '''
    data is from the http response in main module.
    '''
    data=[]

    urls =['http://www.cyzone.cn/event/list-764-0-', '-0-0-0/']
    page=1
    blog=['' for i in range(20)]
    while page<=lastpage:        
        coroutines = [session.get(urls[0]+str(page+i)+urls[1]) for i in range(5)]
        for coroutine in asyncio.as_completed(coroutines):
            r = await coroutine
            r = await r.text(encoding='utf-8')            
            d=pq(r)            
            for item in d('tr.table-plate3').items():
                for i in range(20):
                    blog[i]=''
                # print(blog)
                blog[1]=item('span.tp2_tit a').text()  #name
                # print(item('span.tp2_tit a').text())
                blog[3]=item('span.tp2_com').text()    #full name
                blog[5]=item('td').eq(2).text()   #fields
                blog[4]=item('td').eq(3).text()   #turns
                blog[2]=item('td').eq(5).text()   #money
                tim = item('td').eq(6).text()
                try:
                    time = dt.strptime(tim,'%Y-%m-%d') 
                except Exception:
                    continue
                blog[0] = time           #time

                tem=item('td.tp3').text().strip()

                for n,it in enumerate(tem.split(' ')):
                    blog[6+n]=it

                data.append(blog.copy())
                     
        page+=len(coroutines)
        
    # print(data)
    data.sort(reverse=True)
    for i,v in enumerate(data):
        time = v[0]
        if type(time)==type(''):
            continue 
        time=dt.strftime(time,'%Y.%m.%d')
        data[i][0]=time

        

    return data


            

