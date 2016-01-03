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
link = alinks[0]

token = 'token'

link.url = '/academic/utility/crselst.jsp?' + token
link.absolute_url = 'http://asc.iitb.ac.in/academic/utility/crselst.jsp?' + token
link.attrs = [('href', '/academic/utility/crselst.jsp?' + token)]

request = br.click_link(link)
response = br.follow_link(link)

reg_students = []
roll_names = {}

for idx, code in enumerate(course_codes):
    br.select_form(nr=0)
    br.form['crseCd'] = code
    req = br.submit()
    soup = BeautifulSoup(req.read())
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')[1:]
    reg_df = pd.DataFrame(columns=['Roll No', 'Credit/Audit'])
    s_index = 0
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) > 2:
            roll_names[cols[1]] = cols[2]
            reg_df.loc[s_index] = [cols[1], cols[3][0]]
            s_index += 1
    reg_students.append((code, reg_df))
    br.back()
    print idx

stalk_students = {roll: [] for roll in list(roll_names.keys())}

for code, reg in reg_students:
    for idx, row in reg.iterrows():
        stalk_students[row[0]].append(code)
