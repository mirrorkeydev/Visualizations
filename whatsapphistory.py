# This script takes a WhatsApp chat history and offers:
# - calc_freq_over_time() - creates a line graph of texting frequency over time
# - calc_num_words() - calculates number of total words sent by each party
# - calc_avg_text_len() - calculates average text length
# - [tbi] creates an average time plot of texts for each user
# - [tbi] determines the most used emoji for each party

import os, sys
from datetime import datetime
import plotly.express as px
import re
import pandas as pd

def main():
    f = open("whatsapp.txt", "r", encoding='utf-8')
    #calc_freq_over_time(f)
    melanie_words, noah_words = calc_num_words(f)
    print("Number of words sent: Melanie - " + str(melanie_words) + ". Noah - " + str(noah_words))
    f.close()
    f = open("whatsapp.txt", "r", encoding='utf-8')
    melanie_avg, noah_avg = calc_avg_text_len(f)
    print("Average num of words per text: Melanie - %.2f. Noah - %.2f" % (melanie_avg, noah_avg))

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
    fig.write_image("whatsappimages/frequencybyday.svg")

def calc_num_words(f):
    m_sumwords = 0
    n_sumwords = 0
    for text in f:
        text = text[text.find("-")+2:len(text)-1]
        if (len(text) > 0):
            if (text[0] == "M"):
                text = text[text.find(":")+1:len(text)-1]
                m_sumwords += len(text.split(" "))
            if (text[0] == "N"):
                text = text[text.find(":")+1:len(text)-1]
                n_sumwords += len(text.split(" "))
    return (m_sumwords, n_sumwords)

def calc_avg_text_len(f):
    m_sum_len = 0
    m_total_texts = 0
    n_sum_len = 0
    n_total_texts = 0

    for text in f:
        text = text[text.find("-")+2:len(text)-1]

        if (len(text) > 0):

            if (text[0] == "M"):
                m_total_texts += 1
                text = text[text.find(":")+1:len(text)-1]
                m_sum_len += len(text.split(" "))

            if (text[0] == "N"):
                n_total_texts += 1
                text = text[text.find(":")+1:len(text)-1]
                n_sum_len += len(text.split(" "))

    return ( m_sum_len/m_total_texts , n_sum_len/n_total_texts)

if __name__ == "__main__":
    main()