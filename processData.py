import asyncio
from pyquery import PyQuery as pq
import config

data=[]

async def processData(lastpage, session):
    '''
    data is from the http response in main module.
    '''
    global data

    urls =['http://www.cyzone.cn/event/list-764-0-', '-0-0-0/']
    page=1
    while page<=lastpage:        
        coroutines = [session.get(urls[0]+str(page+i)+urls[1]) for i in range(5)]
        for coroutine in asyncio.as_completed(coroutines):
            r = await coroutine
            r = await r.text(encoding='utf-8')            
            d=pq(r)
            blog={}
            for item in d('tr.table-plate3').items():
                blog['name']=item('span.tp2_tit a').text()
                blog['fullname']=item('span.tp2_com').text()
                blog['money']=item('td').eq(2).text()
                blog['turns']=item('td').eq(3).text()
                blog['field']=item('td').eq(5).text()
                blog['date'] =item('td').eq(6).text()
                blog['investors']=[it('a').text() for it in item('td.tp3').items()]

            data.append(blog)   
                     
        page+=len(coroutines)

    print(data)
    return data


            

