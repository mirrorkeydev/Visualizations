# [Data Visualizations](https://mirrorkeydev.github.io/Visualizations/)

### ["Are You The One?" Simulation + Analysis (2020)](https://mirrorkeydev.github.io/Visualizations/areyoutheone/areyoutheone.html)
A simulation of the first season of the dating reality TV show "Are You The One". Simulates all possible permutations of contestant pairings and provides probabilities for pairings as the season progresses.
- Data Source: [AYTO Season 1](https://www.netflix.com/title/81228406)
- Data Processing Script: [areyoutheone.ipynb](https://github.com/mirrorkeydev/Visualizations/blob/master/areyoutheone/areyoutheone.ipynb). A Python Jupyter Notebook thats run the simulations and provides context and explanations for each step.
- Formatting: [custom.css](https://gist.github.com/mirrorkeydev/5c9a996f8926fd8c6c7836825e71c6eb.org). A `custom.css` Jupyter style that mimics the Palenight VSCode theme.

### [A Year of WhatsApp Conversation (2019)](https://mirrorkeydev.github.io/Visualizations/public/whatsapp.html)
An infographic analysis of around a year's worth of conversations over WhatsApp with one person. For each person, the infographic shows weekly texting frequency over the entire time period, total number of texts sent each hour of the day, total words sent, the most common first text of the day, average words per text, the most used emoji, and the first person to text each day.
- Data Source: [Exported WhatsApp Chat](https://faq.whatsapp.com/en/android/23756533/)
- Data Processing Script: [whatsapphistory.py](https://github.com/mirrorkeydev/Visualizations/blob/master/whatsapp/whatsapphistory.py). Uses Python and Plotly in order to generate the line and radial plots shown. Outputs the rest of the statistics on the command line.
- Formatting: [Inkscape](inkscape.org). The final infographic was created manually.

### [Six Years of Netflix Binging History (2019)](https://mirrorkeydev.github.io/Visualizations/public/netflix.html)
An interactive bar chart that documents the shows I have binged (a significant number of episodes watched) on Netflix for the past six years. Unfortunately, Netflix's viewing activity only saves the most recent watch-through of an episode, else The Office would have appeared every year.
- Data Source: [Netflix Viewing Activity](https://www.netflix.com/viewingactivity)
- Data Processing Script: [netflixhistory.py](https://github.com/mirrorkeydev/Visualizations/blob/master/netflix/netflixhistory.py). Uses Python and Pygal to generate the interactive bar chart.
