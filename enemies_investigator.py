import pandas as pd
import time
# from json import dumps
from selenium import webdriver 
from time import sleep 
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

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
    

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})

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


to_search=input('Enter key word to search:')
to_search=to_search.replace('   ', '  ')
to_search=to_search.replace('  ', ' ')
to_search=to_search.replace(' ', '%20')


group_name=input('Enter Group name:')

driver.get('https://www.facebook.com/groups/' + group_name + '/search/?query=' + to_search + '&epa=FILTERS') 

scroll(15)
gotop()
print ("ended")         


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

tablatotal=pd.DataFrame(columns=['post_link', 'post_date', 'post_author', 'post_content', 'dates', 'author_comment', 'comment'])

totaltabs=len(driver.window_handles)

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
    # else:
    #     tabla=pd.DataFrame([tablename, postdate, creator, post ])
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

tablatotal.to_csv("tablatotal.csv"  ,index=False , encoding="utf-8")
