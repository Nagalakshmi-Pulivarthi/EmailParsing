
# coding: utf-8

# In[18]:

import imaplib
import email
# Dependencies
import urllib.request
# from lxml import html
from os import getcwd
from os.path import join
from bs4 import BeautifulSoup as bs
import io
import os
#from credentials import details

mail = imaplib.IMAP4_SSL('imap.gmail.com')
# imaplib module implements connection based on IMAPv4 protocol
senderEmail =os.environ['SenderEmail']
senderPassword =os.environ['SenderPassword']
receiverEmail=os.environ['ReceiverEmail']
fromMail=os.environ['FromMail']
mail.login(senderEmail,senderPassword)

# In[19]:

mail.list() # Lists all labels in GMail
mail.select('inbox') # Connected to inbox.


# In[20]:

result,data=mail.uid('search', "From "+fromMail  + ' Subject "Fly Morning News"', "ALL")
i = len(data[0].split())
latest_email_uid = data[0].split()[i-1] 
result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = email_data[0][1]
raw_email_string = raw_email.decode('utf-8')
email_message = email.message_from_string(raw_email_string)
for part in email_message.walk():
    if part.get_content_type() == "text/html": # ignore attachments/html
            body = part.get_payload(decode=True)
            text=body.decode("utf-8")
soup = bs(text, 'html.parser')


# In[21]:

import pandas as pd
l=[]
for tick in soup.select('a[href*="/news.php?symbol"]') :
        titles = tick.parent.parent.parent.select('a[href^="https://thefly.com/permalinks/entry.php"] span')
        if(tick.text.find(",")==-1 and len(titles)>0):
            dict1 ={}
            dict1["Tick"]=tick.text 
            dict1["News"]=titles[0].text
            l.append(dict1)
flydf =pd.DataFrame(l)
flydf


# In[22]:

group_ticker=flydf.groupby("Tick").count()
group_ticker=group_ticker.reset_index()
group_ticker.head()


# In[23]:

sort_ticker=group_ticker.sort_values("News",ascending=False)
sort_ticker.head()


# In[24]:

merged_df=pd.merge(flydf,sort_ticker,on=["Tick"])
merged_df.head()


# In[25]:

final_tickerdf=merged_df.rename(columns={"News_x": "TickerNews", "News_y": "Count"})
final_tickerdf
final_tickerdf=final_tickerdf.sort_values(["Count","Tick"],ascending=False)
final_tickerdf.head()
final_tickerdf.to_csv("today_flymorningnews.csv",index=False)


# In[26]:

final_tickerdf.head()


# In[27]:

targetraised_df=final_tickerdf[final_tickerdf["TickerNews"].str.contains("target raised")]
targetraised_df
targetraised_df.to_csv("tagetraised.csv",index=False)
targetlowered_df=final_tickerdf[final_tickerdf["TickerNews"].str.contains("target lowered")]
targetlowered_df.to_csv("tagetlowered.csv",index=False)
targetupgraded_df=final_tickerdf[final_tickerdf["TickerNews"].str.contains("upgraded")]
targetupgraded_df.to_csv("tagetupgraded.csv",index=False)
targetdowngraded_df=final_tickerdf[final_tickerdf["TickerNews"].str.contains("downgraded")]
targetdowngraded_df.to_csv("tagetdowngraded.csv",index=False)


# In[28]:

targetupgraded_df.head()


# In[29]:

b=final_tickerdf[final_tickerdf["Count"] >= 3 ]
final_ticker_more_3_df=b.sort_values(["Count","Tick"],ascending=False)
final_ticker_more_3_df.head()
final_ticker_more_3_df.to_csv("3_or_more_ticks.csv",index=False)


# In[30]:

final_ticker_more_3_df.head()


# In[31]:

c=final_ticker_more_3_df["Tick"].unique()
ticksdf=pd.DataFrame(c) 
ticksdf
# ticksdf.to_csv("allticks.csv",index=False)


# In[32]:

targetraised_df_ticker=final_ticker_more_3_df[final_ticker_more_3_df["TickerNews"].str.contains("target raised")]
targetraised_df_ticker_3more=targetraised_df_ticker[targetraised_df_ticker["Count"] >= 3]
targetraised_df_ticker_3more
a=targetraised_df_ticker_3more["Tick"].unique()

df4=pd.DataFrame(a)
df4.to_csv("tagetraised_3ormore.txt",index=False)
# a.to_csv("tagetraised_3ormore.txt",index=False)
df4


# In[33]:

targetraised_df_ticker=final_tickerdf[final_tickerdf["TickerNews"].str.contains("upgraded")]
targetraised_df_ticker_3more=targetraised_df_ticker[targetraised_df_ticker["Count"] >= 3]
c=targetraised_df_ticker_3more["Tick"].unique()
df5=pd.DataFrame(c)
df5.to_csv("tagetupgraded_3ormore.txt",index=False)


# In[34]:

df5


# In[ ]:


import smtplib
from email.message import EmailMessage
import  csv
import os

# In[ ]:

contacts=[receiverEmail]
msg=EmailMessage()
msg['Subject']="Fly Morning News"
msg['From']=senderEmail
msg['To']=','.join(contacts)
msg.set_content("Please find the files attached. Review and get back to me if any questions. -Naga")
files=["tagetraised_3ormore.txt","tagetupgraded_3ormore.txt","today_flymorningnews.csv"]
for file in files:
    with open(file,"rb") as f:
        filedata=f.read()
        filename=f.name       
    msg.add_attachment(filedata,maintype="text/csv",subtype="octet-stream",filename=filename)
with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
    smtp.login(senderEmail,senderPassword)
    smtp.send_message(msg)

    
