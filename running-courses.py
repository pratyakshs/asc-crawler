import mechanize
br = mechanize.Browser()
br.set_handle_robots(False)   
br.set_handle_refresh(False)  
    
response = br.open('http://asc.iitb.ac.in/acadmenu/WebPages/Login.jsp')
br.select_form('loginForm')
br.form['UserName'] = 'pratyaksh'
br.form['UserPassword'] = 'password'
req = br.submit()
atxt = req.read()

alinks = [link for link in br.links()]
link = alinks[-1]

request = br.click_link(link)
response = br.follow_link(link)
atxt = response.read()

alinks = [link for link in br.links()]
link = alinks[7]

token = 'token'
link.url = '/academic/utility/allDept.jsp?' + token
link.absolute_url = 'http://asc.iitb.ac.in/academic/utility/allDept.jsp?' + token
link.attrs[2] = ('href', '/academic/utility/allDept.jsp?' + token)

request = br.click_link(link)
response = br.follow_link(link)

alinks = [link for link in br.links()][1:]

import pandas as pd
from bs4 import BeautifulSoup

all_courses = pd.DataFrame(columns=['Department', 'Course Code', 'Course Name', 'Instructor', 'Venue', 'Slot'])

c_index = 0

for link in alinks:
    dept = link.text
    request = br.click_link(link)
    response = br.follow_link(link)
    atxt = response.read()
    soup = BeautifulSoup(atxt)
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) > 1 and cols[1] == 'timetable':
            pre = [dept] + cols[2:6] 
            if len(cols[6]) > 0:
                slot = cols[6].split()[0]
            else:
                slot = ''
            all_courses.loc[c_index] = pre + [slot]
            c_index += 1
    br.back()

course_codes = list(set(all_courses['Course Code']))
