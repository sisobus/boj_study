#!/usr/bin/python
#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, session
import json
import glob
from operator import itemgetter
import os
import datetime
import random
from bs4 import BeautifulSoup
import urllib,urllib2
import cookielib
import sys
from datetime import timedelta

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

def get_all_date_list():
    base_directory_path = '/var/www/scsc_2016_summer/boj_study/data/problems/'
    date_paths  = glob.glob(base_directory_path+'*')
    date_list   = []
    for date_path in date_paths:
        date_list.append(date_path.split('/')[-1])
    date_list.sort(reverse=True)
    return date_list

def get_problem_list_with_date(cur_date):
    base_directory_path = '/var/www/scsc_2016_summer/boj_study/data/problems/'
    date_file_path = base_directory_path + cur_date
    l = []
    with open(date_file_path,'r') as fp:
        l = fp.read().strip().split()
    return l

def get_all_user_list():
    base_directory_path = '/var/www/scsc_2016_summer/boj_study/data/users/'
    user_paths  = glob.glob(base_directory_path+'*')
    user_list   = []
    for user_path in user_paths:
        user_list.append(user_path.split('/')[-1])
    return user_list

def get_pdf_list(cur_date):
    base_directory_path = '/var/www/scsc_2016_summer/boj_study/static/pdf/'
    date_file_path = base_directory_path + cur_date + '/'
    pdf_file_path = glob.glob(date_file_path+'*')
    pdf_list = []
    for path in pdf_file_path:
        d = {
            'filename': path.split('/')[-1],
            'path': '/static/pdf/'+cur_date+'/'+path.split('/')[-1]
                }
        pdf_list.append(d)
    return pdf_list

def convert_problems(user_id,problems):
    # is solve : 1
    # none : 0
    # fail : -1
    if os.path.exists('/var/www/scsc_2016_summer/boj_study/data/status/'+user_id+'.json'):
        with open('/var/www/scsc_2016_summer/boj_study/data/status/'+user_id+'.json','r') as fp:
            status = json.loads(fp.read())
    else:
        status = {}
    
    solved = []
    failed = []
    if 'solved' in status:
        solved = status['solved']
    if 'failed' in status:
        failed = status['failed']
    ret = []
    for problem in problems:
        mask = 0
        if problem in solved:
            mask = 1
        elif problem in failed:
            mask = -1
        d = {
            'problem_id': problem,
            'status': mask
                }
        ret.append(d)
    return ret

def get_accept_rate(problems):
    number_of_accept    = 0.0
    for problem in problems:
        if problem['status'] == 1:
            number_of_accept += 1
    return (number_of_accept/float(len(problems)))*100

def get_all_username(user_list):
    ret = {}
    base_directory_path = '/var/www/scsc_2016_summer/boj_study/data/users/'
    for user_item in user_list:
        with open(base_directory_path+user_item,'r') as fp:
            cur_username = fp.read().strip()
        ret[user_item] = cur_username
    return ret

@app.route('/',methods=['GET'])
def home():
    user_list = get_all_user_list()
    username_dict = get_all_username(user_list)
    date_list = get_all_date_list()
    posts = []
    number_of_total_problem = 0
    for date_item in date_list:
        problem_list = get_problem_list_with_date(date_item)
        number_of_total_problem += len(problem_list)
        users = []
        for user_item in user_list:
            cur_problems = convert_problems(user_item,problem_list)
            accept_rate  = round(get_accept_rate(cur_problems),2)
            d = {
                    'user_id': user_item,
                    'problems': cur_problems,
                    'accept_rate': accept_rate
                    }
            users.append(d)
        users = sorted(users, key=lambda k: k['accept_rate'], reverse=True)
        d = {
                'users': users,
                'date': date_item,
                'pdfs': get_pdf_list(date_item)
                }
        posts.append(d)

    ret = {
            'posts': posts,
            'number_of_total_problem': number_of_total_problem
            }
    html_code = render_template('home.html',ret=ret,username_dict=username_dict)
    return html_code

@app.route('/admin/<password>')
def admin(password):
    with open('/var/www/skny/skny/password/password','r') as fp:
        cur_password = fp.read().strip()
    if password == cur_password:
        session['logged_in'] = True
        return redirect('/')
    else :
        return redirect('/')

@app.route('/adminout')
def adminout():
    session.pop('logged_in',None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='1.226.82.204',debug=True)
