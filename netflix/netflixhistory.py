import pygal
import xlrd
import datetime
import random
from pygal.style import Style

##############################################
# dissect the excel data into separate shows #
##############################################

wb = xlrd.open_workbook(r'C:\Users\Melanie\Downloads\NetflixHistory.xlsx')
sheet = wb.sheet_by_index(0)

shows = {}

# grab all shows and dates watched from the excel spreadsheet
for i in range(1, sheet.nrows):
    show_name = str(sheet.cell_value(i,0)).partition(":")[0]
    date_watched = xlrd.xldate_as_datetime(sheet.cell_value(i,1), wb.datemode)

    if show_name in shows:
        shows[show_name].append(date_watched)
    else:
        shows[show_name] = [date_watched]

# do a second pass, removing shows/movies where less than 30 episodes were watched
to_delete = []
for show, dates in shows.items():
    if len(dates) < 45:
        to_delete.append(show)

# python 3 doesn't allow deleting from a dictionary while iterating through it,
# so we had to store the keys to delete first
for key in to_delete:
    del shows[key]

############################################
# calculate the what goes into each bucket #
############################################

num_buckets = 6

# the goal is to have show_name : [count, count, ... , count],
# where the list has as many items as num_buckets

start_date = datetime.datetime(2013, 11, 27, 0, 0)
end_date = datetime.datetime(2019, 11, 3, 0, 0)

diff = (end_date - start_date) / num_buckets

# create our date buckets
date_buckets = []
for i in range(num_buckets):
    date_buckets.append(start_date + diff*i)
date_buckets.append(end_date)

sorted_shows = {}

# sort dates into buckets
for show, dates in shows.items():
    for date in dates:
        for i in range(0, len(date_buckets)-1):
            if date >= date_buckets[i] and date < date_buckets[i+1]:
                if show in sorted_shows:
                    sorted_shows[show][i] += 1
                else:
                    sorted_shows[show] = [0]*num_buckets

# do a third pass, removing shows/movies from buckets where less than 5
# episodes were watched per bucket
to_delete = []
for show, times_watched in sorted_shows.items():
    for i in range(len(times_watched)):
        if times_watched[i] != 0 and times_watched[i] < 5:
            sorted_shows[show][i] = 0

# smol unit test
for show, dates in sorted_shows.items():
    assert(len(dates) == num_buckets)
    for date in dates:
        assert(date == 0 or date >= 5)

###########################
# create the actual chart #
###########################
c_style = Style(
    background = 'black',
    plot_background = 'transparent',
    foreground = 'white',
    foreground_strong = 'white',
    foreground_subtle='white',
    opacity = '1',
    colors = ['#ff867d', '#ffb57d', '#ffda7d', '#fff97d', '#daff7d', '#8aff7d', '#7dfff0', '#7dcfff', '#7d99ff', '#937dff', '#b87dff', '#e17dff', '#ff7df4', '#f5f5f5','#b8b8b8', '#8a8a8a', '#5c5c5c']
)
c = pygal.StackedBar(style = c_style)
c.title = 'My Netflix Viewing History (Num. of Episodes)'
c.x_labels = map(str, range(2014, 2020))


for show, dates in sorted_shows.items():
    c.add(show, dates)

c.render_to_file('chart' + str(random.randint(1, 1000)) + '.svg')
