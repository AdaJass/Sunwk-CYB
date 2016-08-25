import aiohttp
import asyncio
import config
import processData as pd
from pyquery import PyQuery as pq
import sys
import writeExcel

async def fetchData(callback = pd.processData, params=None):
    #set request url and parameters here or you can pass from outside. 
    
    #use s.** request a webside will keep-alive the connection automaticaly,
    #so you can set multi request here without close the connection 
    #while in the same domain.
    #i.e. 
    #await s.get('***/page1')
    #await s.get('***/page2')
    ############################################            
    conn = aiohttp.TCPConnector(limit=config.REQ_AMOUNTS)    
    s = aiohttp.ClientSession(headers = config.HEADERS, connector=conn)        
    r=await s.get('http://www.cyzone.cn/event/list-764-0-1-0-0-0/')
    r=await r.text(encoding='utf-8')
    d=pq(r)
    lastpage=d('div#pages a').eq(-2).text()
    try:
        lastpage=int(lastpage)
    except Exception:
        print('lastpage parse error, process will terminal.')
        exit(-1)
    # print(lastpage)
    data = await callback(lastpage, s)
    writeExcel.writedb(data)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()    
    #coroutine in tasks will run 
    tasks = [fetchData(pd.processData)]    
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close() 
