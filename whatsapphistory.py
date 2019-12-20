# This script takes a WhatsApp chat history and offers:
# - calc_freq_over_time() - creates a line graph of texting frequency over time
# - calc_num_words() - calculates number of total words sent by each party
# - calc_avg_text_len() - calculates average text length
# - [tbi] creates an average time plot of texts for each user
# - most_used_emoji() determines the most used emoji for each party

import os, sys
import datetime
import plotly.express as px
import re
import pandas as pd
import emoji
import operator

### GLOBAL SETTINGS ###
# name of whatsapp chat history txt file to open:
file_name = "whatsapp.txt"

def main():
    #calc_freq_over_time(f)

    calc_avg_texts_per_hour()

    melanie_words, noah_words = calc_num_words()
    print("Number of words sent: Melanie - %d. Noah - %d" % (melanie_words, noah_words))

    melanie_avg, noah_avg = calc_avg_text_len()
    print("Average num of words per text: Melanie - %.2f. Noah - %.2f" % (melanie_avg, noah_avg))

    emoji, num_times_used = most_used_emoji()
    print("Most used emoji: %c, which was used %d times" % (emoji, num_times_used))

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
            date_time_obj = datetime.datetime.strptime(dtstr, "%m/%d/%y, %I:%M %p")
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

# Outputs an line chart (.svg) displaying the frequency of texts per day over the entire time period
def calc_freq_over_time():
    f = open(file_name, "r", encoding='utf-8')
    df = get_texts_per_day(f)
    f.close()
    fig = px.line(df, x="Date", y="Number of Texts", title='Frequency of Text Messages', color='Person')
    fig.write_image("whatsappimages/frequencybyday.svg")

# Calculates the number of words each party sent over the entire time period
def calc_num_words():
    f = open(file_name, "r", encoding='utf-8')

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

    f.close()
    return (m_sumwords, n_sumwords)

# Calculates the average text length for each party
def calc_avg_text_len():
    f = open(file_name, "r", encoding='utf-8')

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
    f.close()
    return ( m_sum_len/m_total_texts , n_sum_len/n_total_texts)

# This function taken from: https://gist.github.com/jezdez/0185e35704dbdf3c880f
def is_emoji(s):
    return s in emoji.UNICODE_EMOJI

# Calculate what the most used emoji between both party's combined texts is
def most_used_emoji():
    f = open(file_name, "r", encoding='utf-8')

    emojis = {}

    # including this string speeds up execution time as it disqualifies letters early on in the process from being emojis
    # the order of characters is determined by letter frequency in word averages (http://letterfrequency.org/)
    common_chars = " aetaoinsrhldcumfpgwybvkxjqzAETAOINSRHLDCUMFPGWYBVKXJQZ1234567890,<.>/?;:\'\"[{]}-_=+\|]\\`~!@#$%^&*()"
    for text in f:
        for char in text:
            if char not in common_chars and is_emoji(char):
                if char in emojis:
                    emojis[char] += 1 
                else:
                    emojis[char] = 1
    f.close()
    # this grabs the most used emoji from the dictionary of emojis
    return(max(emojis.keys(), key=(lambda k: emojis[k])), emojis[max(emojis, key=emojis.get)])

# Creates a radar chart showing the total texts for each hour of the day
def calc_avg_texts_per_hour():
    f = open(file_name, "r", encoding='utf-8')

    # create a new dictionary with the format: times = {0:0, 1:0, 2:0, ... }
    # where the key is the number of hours in 24 hour time and the value is the number of occurences
    times = {n:0 for n in range(24)}
    m_times = {n:0 for n in range(24)}
    n_times = {n:0 for n in range(24)}

    # for each text in our chat history
    for text in f:
        
        # grab the date-time string
        dtstr = text[0: text.find("-")-1]

        # if it matches the expected format (m/d/y, t:tt AM/PM)
        if (re.match("\d{1,2}\/\d{1,2}\/\d{2}, \d{1,2}:\d{2} [AP]M", dtstr)):
            
            # parse it into a datetime object
            time = datetime.datetime.strptime(dtstr, "%m/%d/%y, %I:%M %p").time().hour

            # add to our overall total
            times[time] += 1

            # add to our subtotals for each party
            text = text[text.find("-")+2:len(text)-1]
            if (len(text) > 0):
                if (text[0] == "M"): m_times[time] += 1
                elif (text[0] == "N"): n_times[time] += 1

    # restructure data for the mixed_df (showing both parties on the radar chart)
    data = {'r' : [], 'theta' : [], 'person' : []}

    for time in m_times:
        data['r'].append(m_times[time])
        data['theta'].append(str(time)+":00")
        data['person'].append("M")
    for time in n_times:
        data['r'].append(n_times[time])
        data['theta'].append(str(time)+":00")
        data['person'].append("N")

    total_df = pd.DataFrame(dict(r=[times[x] for x in times], theta=[str(x)+":00" for x in range(24)]))
    mixed_df = pd.DataFrame.from_dict(data)

    # swap out mixed_df for total_df to see the combined texts radar chart
    fig = px.line_polar(mixed_df, r='r', theta='theta', color='person', line_close=True)
    fig.write_image("whatsappimages/hourlytextsboth.svg")
    f.close()


if __name__ == "__main__":
    main()