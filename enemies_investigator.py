# all the code works in python 3
# With this code you can only gather information from people who share a group with you,
# It is not hacking!!!!! and it is legal, at least in my country.


# Fist of all run these lines to update pip and download moduls and chromedriver
# pip install --upgrade pip
pip install selenium
pip install webdriver-manager
pip install wget
import wget
from zipfile import ZipFile
print('Beginning file download with wget module')
url = 'https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_win32.zip'
wget.download(url, 'chromedriver_win32.zip')

with ZipFile('chromedriver_win32.zip', 'r') as zipObj:
# Extract all the contents of zip file in current directory
zipObj.extractall()

# Second step: import all the packages you will need
import pandas as pd
import time
# from json import dumps
from selenium import webdriver 
from time import sleep 
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

#Some functions we will use
def scroll(x):
    scrolls = x
    while True:
        scrolls -= 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(2)
        if scrolls < 0:
            break
    
def gotop():
    driver.execute_script("window.scrollTo(0, 0);")
    

#     Let start with disable all thing can bother us from crhome
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})


# Let login Facebook
usr=input('Enter Email Id:')  
pwd=input('Enter Password:')  

driver = webdriver.Chrome(chrome_options=option) 
# driver = webdriver.Chrome(options) 
driver.get('https://www.facebook.com/') 
print ("Opened facebook") 
sleep(1) 
  
username_box = driver.find_element_by_id('email') 
username_box.send_keys(usr) 
print ("Email Id entered") 
sleep(1)
password_box = driver.find_element_by_id('pass') 
password_box.send_keys(pwd) 
print ("Password entered") 

login_box = driver.find_element_by_id('loginbutton') 
login_box.click() 
sleep(2) 

# Let search all the posts and comments

# Very importan!!!! 
# every class name can change in the time, that means that maybe you'll need to find the new classes in the future.
# this is not a problem if you are family with html, css and javascript 

to_search=input('Enter key word to search:')
to_search=to_search.replace('   ', '  ')
to_search=to_search.replace('  ', ' ')
to_search=to_search.replace(' ', '%20')

group_name=input('Enter Group name:')

driver.get('https://www.facebook.com/groups/' + group_name + '/search/?query=' + to_search + '&epa=FILTERS') 

scroll(15)
gotop()
print ("ended") 

#Now we have one tab with all the posts and some posts that have comments that includes our keyword

#let open every post and extend every text that Facebook compress 
URL = driver.find_elements_by_class_name("_3084")
U=[]

for u in range(len(URL)):
    U.append(URL[u].get_attribute('href'))
    print (U[u])
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[(u + 1)])
    driver.get(U[u])
    sleep(1)
    scroll(5)
    sleep(1)
    gotop()

    commentsopen = driver.find_elements_by_class_name('_4sxc') 
    for com in range(len(commentsopen)):
        try:
            commentsopen[com].click()
        except:
            pass
       
    sleep(1)
    gotop()
    vermas=driver.find_elements_by_class_name('_5v47')
    for ver in range(len(vermas)):
        try:
            vermas[ver].click()
            element.scroll(0, -70);

        except:
            pass

    driver.switch_to.window(driver.window_handles[0])

#After that have opened and extend every comment let create a big database 
tablatotal=pd.DataFrame(columns=['post_link', 'post_date', 'post_author', 'post_content', 'dates', 'author_comment', 'comment'])
totaltabs=len(driver.window_handles)

#this loop picks up the data from every tab (post) and merge into one big table
for tab in range(1, totaltabs):
    driver.switch_to.window(driver.window_handles[tab])
    comentario=driver.find_elements_by_class_name('_72vr') #_4a6n
    dichos=[]
    if not comentario:
        dichos='no_comments'
    else:
        for com in range(len(comentario)):
            dichos.append(comentario[com].text)

    posteador=driver.find_elements_by_class_name('_6qw4') 
    nombres=[]
    if not posteador:
        nombres='no_comments_author'
    else:
        for com in range(len(posteador)):
            nombres.append(posteador[com].text)

    fechas=driver.find_elements_by_css_selector('abbr.livetimestamp') 
    taarij=[]
    if not fechas:
        dates='no_comments_date'
    else:
        for com in range(len(fechas)):
            taarij.append(fechas[com].get_attribute('data-tooltip-content'))
        dates = [] 
        for val in taarij: 
            if val != None : 
                dates.append(val)
        if not dates:
            dates='no_comments_date'


    # postrashi=driver.find_element_by_css_selector('div.post_message') 
    postrashi=driver.find_element_by_class_name('userContent ') #post_message data-testid="post_message"
    post=postrashi.text
    # post

    creator=driver.find_element_by_class_name('_7tae') 
    creator=creator.text
    # creator

    postfecha=driver.find_element_by_class_name('_5ptz') # _42ft # _4sxc
    postdate=postfecha.text
    # postdate

    tablename=U[0]

    tabla=pd.DataFrame([tablename, postdate, creator, post ]).T
    tabla.rename( columns={ 0: 'post_link' , 1:'post_date', 2: 'post_author' , 3: 'post_content'  }, inplace=True)
    # tabla

    if type(nombres) !=str:
        posts=pd.DataFrame(list(zip(dates, nombres ,dichos)))
    else:
        posts=pd.DataFrame([[dates,nombres,dichos]])

    posts.rename( columns={ 0: 'dates' , 1: 'author_comment' , 2: 'comment'}, inplace=True)
    # posts

    final=posts.join(tabla)
    final
    if type(nombres) !=str:
        final['post_link'].fillna(tablename , inplace = True)
        final['post_date'].fillna(postdate , inplace = True)
        final['post_author'].fillna(creator , inplace = True)
        final['post_content'].fillna(post , inplace = True)

    finaltable=final[list(tabla.columns.values)  + list( posts.columns.values)]
    tablatotal=tablatotal.append(finaltable , sort=False)

tablatotal.reset_index(drop=True, inplace=True)
tablatotal.tail()

#finally we have our data and now we save him as CSV file
tablatotal.to_csv("tablatotal.csv"  ,index=False , encoding="utf-8")
