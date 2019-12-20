# This script takes a WhatsApp chat history:
# - calc_freq_over_time(f) - creates a line graph of texting frequency over time
# - [tbi] calculates number of total words sent by each party
# - [tbi] calculates average text length
# - [tbi] creates an average time plot of texts for each user
# - [tbi] determines the most used emoji for each party

import os, sys
from datetime import datetime
import plotly.express as px
import re
import pandas as pd

def main():
    f = open("whatsapp.txt", "r", encoding='utf-8')
    calc_freq_over_time(f)
    
# Helper function that gets a list of datetime objects representing each text message 
def get_texts_per_day(f):
    texts_per_day = {} # format: {(date, m or n) : [date, num texts, m or n]}, ... 

    # for each text in our chat history
    for text in f:
        
        # grab the date-time string
        dtstr = text[0: text.find("-")-1]

        # if it matches the expected format (m/d/y, t:tt AM/PM)
        if (re.match("\d{1,2}\/\d{1,2}\/\d{2}, \d{1,2}:\d{2} [AP]M", dtstr)):
            
            # parse it into a datetime object
            date_time_obj = datetime.strptime(dtstr, "%m/%d/%y, %I:%M %p")
            day = date_time_obj.date()

            # sort the text by whether it was sent from M or N
            if (text[text.find("-")+2:text.find("-")+3] == "M"):
                if (day, "M") in texts_per_day:
                    texts_per_day[(day, "M")][1] += 1
                else:
                    texts_per_day[(day, "M")] = [day, 1 , "Melanie"]

            elif (text[text.find("-")+2:text.find("-")+3] == "N"):
                if (day, "N") in texts_per_day:
                    texts_per_day[(day, "N")][1] += 1
                else:
                    texts_per_day[(day, "N")] = [day, 1 , "Noah"]

    df = pd.DataFrame.from_dict(texts_per_day, orient='index', columns = ['Date', 'Number of Texts', 'Person'])
    return df

def calc_freq_over_time(f):
    df = get_texts_per_day(f)
    fig = px.line(df, x="Date", y="Number of Texts", title='Frequency of Text Messages', color='Person')
    fig.show()
    fig.write_image("whatsappimages/frequencybyday.svg")

if __name__ == "__main__":
    main()