#-*- coding:utf-8 -*-
import json
import glob
from bs4 import BeautifulSoup
import urllib,urllib2
import cookielib

def get_all_user_list():
    base_directory_path = '/var/www/scsc_2016_summer/boj_study/data/users/'
    user_paths  = glob.glob(base_directory_path+'*')
    user_list   = []
    for user_path in user_paths:
        user_list.append(user_path.split('/')[-1])
    return user_list

def download_source(url,values,headers,cookie_jar):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36'
    user_agent_headers = { 'User-Agent' : user_agent }
    headers = dict(user_agent_headers.items() + headers.items())
    data = urllib.urlencode(values)
    if cookie_jar == None:
        cookie_jar = cookielib.LWPCookieJar()
    cookie = urllib2.HTTPCookieProcessor(cookie_jar)

    opener = urllib2.build_opener(cookie) 

    req = urllib2.Request(url, data, headers)
    res = opener.open(req)

    html_doc = res.read()
    res.close()
    return (html_doc,cookie_jar)

def update():
    url = 'http://www.acmicpc.net/signin'
    values = {
            'login_user_id' : 'javava',
            'login_password' : 'tkdrmsld123',
            'auto_login' : 'on',
            'next' : 'problem/1016',
            }
    headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Connection' : 'keep-alive',
            }
    (source,cookie_jar) =  download_source(url,values,headers,None)
    user_ids = get_all_user_list()
    for user_id in user_ids:
        url = 'https://www.acmicpc.net/user/'+user_id
        (source,cookie_jar) = download_source(url,values,headers,cookie_jar)

        soup = BeautifulSoup(source)
        problem_info = soup.find(id='problem_info')

        panel_bodys = problem_info.findAll('div','panel-body')
        solved_problem_numbers = panel_bodys[0].findAll('span','problem_number')
        solved_problem_titles  = panel_bodys[0].findAll('span','problem_title')
        solved_problem_ids = []
        for solved_problem_number in solved_problem_numbers:
            problem_id = solved_problem_number.a.string.strip()
            solved_problem_ids.append(problem_id)

        failed_problem_numbers = panel_bodys[1].findAll('span','problem_number')
        failed_problem_titles  = panel_bodys[1].findAll('span','problem_title')
        failed_problem_ids = []
        for failed_problem_number in failed_problem_numbers:
            problem_id = failed_problem_number.a.string.strip()
            failed_problem_ids.append(problem_id)
        ans = {
                'solved': solved_problem_ids,
                'failed': failed_problem_ids
                }
        
        with open('/var/www/scsc_2016_summer/boj_study/data/status/'+user_id+'.json','w') as fp:
            fp.write(json.dumps(ans))

if __name__ == '__main__':
    update()
