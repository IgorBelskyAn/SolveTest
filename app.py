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
  global_answers = []*len(content)
  for i in range (len(content)):
     if content[i].find_all('td',{'class':'check'})!=[]:
        answers = []
        true_answers = ''
        pager = content[i].find_all('td',{'class':'check'})
        for i in range(len(content[i].find_all('td',{'class':'check'}))):
           ans = pager[i].find('input')['value']
           answers.append(ans)
        for i in range(len(answers)):
           if answers[i] == '1':
              true_answers+=''+str(i+1)
        global_answers.append(true_answers)
     elif content[i].find_all('td',{'class':'radio'})!=[]:
        pager = content[i].find_all('td',{'class':'radio'})
        k = 0
        for i in range(len(pager)):
           if pager[i].find('input')['value']=='1':
             k = i+1
        global_answers.append(str(k))
     elif content[i].find_all('td',{'class':'text'})!=[]:
        continue
        
     else: 
          global_answers.append(' ')
  result=''
  for i in range(len(global_answers)):
     result +=str(i+1)+'. '+global_answers[i]+' '+flask.Markup('<br>')
     print (str(i+1)+' .'+global_answers[i]+' '+'<br>')
  print (result)
  if result!=None:
       return flask.render_template('index.html',result=result,val=link,align='left')
 return flask.render_template('index.html',result=flask.Markup('Здесь будут ответы'),align='center')

  
if __name__ == "__main__":
    app.run()
