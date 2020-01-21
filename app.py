
# Dependencies
import imaplib
import email
import urllib.request

from bs4 import BeautifulSoup as bs

from credentials import details
import pandas as pd
from flask import Flask, Response
app = Flask(__name__)



@app.route('/')
def email_Scrape():
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        # imaplib module implements connection based on IMAPv4 protocol
        mail.login(details[0],details[1])
        # print(mail.login(details[0],details[1]))
        print(details)
        mail.list() # Lists all labels in GMail
        mail.select('inbox')# Connected to inbox.
        result, data = mail.uid('search', 'From "easyguru@gmail.com" Subject "Fwd: Fly Morning News"', "ALL")
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
        l=[]
        for tick in soup.select('a[href*="/news.php?symbol"]') :
            titles = tick.parent.parent.parent.select('a[href^="https://thefly.com/permalinks/entry.php"] span')
            if(tick.text.find(",")==-1 and len(titles)>0):
                dict1 ={}
                dict1["Tick"]=tick.text 
                dict1["News"]=titles[0].text
                l.append(dict1)
        flydf =pd.DataFrame(l)
        print(flydf.head(5))
        group_ticker=flydf.groupby("Tick").count()
        group_ticker=group_ticker.reset_index()
        group_ticker.head()
        sort_ticker=group_ticker.sort_values("News",ascending=False)
        sort_ticker.head()
        merged_df=pd.merge(flydf,sort_ticker,on=["Tick"])
        merged_df.head()
        final_tickerdf=merged_df.rename(columns={"News_x": "TickerNews", "News_y": "Count"})
        final_tickerdf
        final_tickerdf=final_tickerdf.sort_values(["Count","Tick"],ascending=False)
        final_tickerdf.head()
        print("nnnn")
        return Response(

                        final_tickerdf.to_csv(index=False),

                            mimetype="text/csv",

                            headers={"Content-disposition":

                                    "attachment; filename=flydata.csv"})
if __name__ == '__main__':

    app.run(debug=True)
