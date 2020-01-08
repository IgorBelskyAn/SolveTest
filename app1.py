import flask, hashlib, dictionary 
from flask import Flask
import bs4, requests
from bs4 import BeautifulSoup as BS
app = Flask(__name__)
@app.route("/",methods=['POST','GET'])
def main_func():
 if flask.request.method == 'POST':
  link = flask.request.form['link']
  page = requests.get(str(link))
  b = BS(page.text,'html.parser')
  content = b.find_all(class_='q')
  newtext = content
  global_answers = []*len(content)
  for i in range (len(content)):
     if content[i].find_all('td',{'class':'check'})!=[]:
        answers = []
        true_answers = ''
        m1=i
        pager = content[i].find_all('td',{'class':'check'})
        for i in range(len(content[i].find_all('td',{'class':'check'}))):
           ans = pager[i].find('input')['value']
           answers.append(ans)
        for i in range(len(answers)):
           if answers[i] == '1':
              true_answers+=''+str(i+1)
              newtext[m1].find_all('td',{'class':'check'})[i].find('input')['checked']=''
        global_answers.append(true_answers)
     elif content[i].find_all('td',{'class':'radio'})!=[]:
        pager = content[i].find_all('td',{'class':'radio'})
        k = 0
        m = i
        for i in range(len(pager)):
           if pager[i].find('input')['value']=='1':
             k = i+1
             newtext[m].find_all('td',{'class':'radio'})[i].find('input')['checked']=''
        global_answers.append(str(k))
     elif content[i].find_all('td',{'class':'text'})!=[]:
        val =content[i].find_all('td',{'class':'text'})[0].find('input')['value']
        h = val
        for i in range(-10000,10001):
           if str(hashlib.md5(str(i).encode('utf-8')).hexdigest())==val:
             val=str(i)
             break
        if str(val) in dictionary.d:
           val=dictionary.d[str(val)]
        if val==h:
            val='-'
        global_answers.append(val)
     else: 
          global_answers.append(' ')
  result=''
  for i in range(len(global_answers)):
     result +=str(i+1)+'. '+global_answers[i]+' '+flask.Markup('<br>')
     print (str(i+1)+' .'+global_answers[i]+' '+'<br>')
  print (result)
  newtext = str(newtext).replace(']','').replace('[','').replace(',','')
  if result!=None:
       return flask.render_template('indexx.html',result=flask.Markup(newtext),res=result,title=b.find_all('title')[0].next,val=link,align='left')
 return flask.render_template('indexx.html',result=flask.Markup('Здесь будут ответы'),align='center')

  
if __name__ == "__main__":
    app.run()
