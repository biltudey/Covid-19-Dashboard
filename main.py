import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
from PIL import Image
from datetime import date

def run():
    img = Image.open('image.jpeg')
    img = img.resize((500,250))
    st.image(img)
    st.title('Covid 19 report for any Country')
    link = '[© Devolop By Biltu Dey](https://www.linkedin.com/in/biltudey/)'
    st.sidebar.markdown(link,unsafe_allow_html=True)

run()
st.write("""
------------
This dashboard provides daily updates of the 7-day-incidence (number of cases per 100,000 inhabitants), the rolling 7-day-average number of new cases and the raw number of new reported Covid-19 cases. You may select the state to view and compare.
The data are the latest official figures provided by the Indian government, sourced from [ourworldindata]('https://covid.ourworldindata.org/data/').
If you are viewing this on a mobile device, tap **>** in the top left corner to select district and timescale.
""")
st.write("---")

def get_data():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    full = pd.read_csv(url)
    full['date'] = pd.to_datetime(full['date'])
    start_date = '2021-11-08'
    end_date = date.isoformat(date.today())
    mask = (full['date'] > start_date) & (full['date'] <= end_date)
    df = full.loc[mask]
    
    return df
    
df = get_data()

country = list(df['location'].value_counts().index)

selected_country = st.sidebar.selectbox(
    'Select District(s):',
    country,  # setting Lichtenberg as the default district as it's the one I'm most interested in seeing
)
no_of_day = st.sidebar.slider('Number of Day',0,365,30)

st.sidebar.write('---')
st.sidebar.write('Chart Presentation Settings:')
nocyber = st.sidebar.checkbox('Light Style')

df = df[df['location']==selected_country]
df = df.iloc[:-1]
# st.dataframe(df)
new_reported_cases = df[['date','new_cases']]

# rolling
data_to_plot = df['date']

seven_day_average = df.rolling(window=7)['new_cases'].mean()
new_col_name = ('7 Day Average')
historic_cases = df
historic_cases[new_col_name] = seven_day_average
data_to_plot = pd.concat([data_to_plot, historic_cases[new_col_name]], axis = 1)

# Creating a 7 day rolling sum of cases
new_reported_cases['Seven Day Sum'] = new_reported_cases['new_cases'].rolling(7).sum()


# Creating a DataFrame containing only the 7-day-incidence data
incidence = new_reported_cases['date']
incidence = pd.concat([incidence, new_reported_cases['Seven Day Sum']], axis = 1)
incidence.fillna(0,inplace=True)
# st.dataframe(incidence)

if nocyber == False:
    plt.style.use('cyberpunk')
else:
    plt.style.use('ggplot')
st.write('## 7 Days incidence')
incidence_data = incidence.iloc[-no_of_day:,:]
# st.dataframe(incidence_data)

fig, ax = plt.subplots()

plt.plot(incidence_data['date'],incidence_data['Seven Day Sum'])

ax.legend([selected_country]) # pass a list 
plt.xticks(rotation=45,
    horizontalalignment='right',
    fontweight='normal',
    fontsize='small',
    color= '1')
plt.yticks(color = '1')
plt.ylim((0))
plt.title('Seven Day Incidence - Last ' + str(no_of_day) + ' Days', color = '1')
if nocyber == False:
    mplcyberpunk.add_glow_effects()
else:
    # fig.patch.set_facecolor('gray')
    legend = plt.legend(selected_country)
    plt.setp(legend.get_texts(), color='k')
st.pyplot(fig)

st.write('---')


# Plotting the 7 day average

#CYBERPUNK

st.write('## New reported cases - Rolling 7 Day Average')
st.write('This chart shows a [rolling 7-day-average](https://en.wikipedia.org/wiki/Moving_average) of newly reported cases for the selected country.')
st.write('This smoothes out the spikes somewhat and makes it easier to identify the real trend in cases.')

data = data_to_plot.iloc[-no_of_day:,:]
# st.dataframe(data)
# Defining the figure 
fig, ax = plt.subplots()

# for i in selected_country: # looping to plot each district
plt.plot(data['date'], data['7 Day Average'])

ax.legend([selected_country])
plt.xticks(rotation=45,
    horizontalalignment='right',
    fontweight='light',
    fontsize='small',
    color= '1')
plt.yticks(color = '1')
plt.title('Rolling 7-day-average - Last ' + str(no_of_day) + ' Days', color = '1')

if nocyber == False:
    mplcyberpunk.add_glow_effects()
else:
    legend = plt.legend(selected_country)
    plt.setp(legend.get_texts(), color='k')

# Displaying the plot and the last 3 days' values
st.pyplot(fig)
# st.table(data_to_plot.iloc[-10:,:])

st.write('---')

st.write('## Newly Reported Cases')
st.write('This chart shows the raw number of new reported cases in the selected district(s).')
st.write("This will show larger variance and generally be 'noisier' than the 7-day-average chart.")
st.write('Notice that the numbers tend to dip to near zero on weekends and spike on Mondays. This is an artifact of the data collection process and not a real trend - new cases are generally not recorded / reported over weekends.')

new_cases = new_reported_cases.iloc[-no_of_day:,:]

# Defining the figure 
fig, ax = plt.subplots()

# for i in selected_country:
plt.plot(new_cases['date'], new_cases['new_cases'])

ax.legend([selected_country])
plt.xticks(rotation=45, 
    horizontalalignment='right',
    fontweight='light',
    fontsize='small',
    color= '1')
plt.yticks(color = '1')
plt.title('New Reported Cases - Last ' + str(no_of_day) + ' Days', color='1')

# Removing the mplcyberpunk glow effects if checkbox selected
if nocyber == False:
    mplcyberpunk.add_glow_effects()
else:
    legend = plt.legend(selected_country)
    plt.setp(legend.get_texts(), color='k')

# Displaying the plot and the last 3 days' values
st.pyplot(fig)
number_to_limit_table = len(selected_country) + 1 # This is just a hack to display the figures I want
# st.table(new_reported_cases.iloc[-3:,:number_to_limit_table])

st.write('---')


# st.dataframe(df)


## For death 
st.write('## New Reported Deaths Cases  ')

death = df[['date','new_deaths']]
death = death.iloc[-no_of_day:,:]
fig, ax = plt.subplots()

# for i in selected_country:
plt.plot(death['date'], death['new_deaths'])

ax.legend([selected_country])
plt.xticks(rotation=45, 
    horizontalalignment='right',
    fontweight='light',
    fontsize='small',
    color= '1')
plt.yticks(color = '1')
plt.title('New Reported Deaths Cases - Last ' + str(no_of_day) + ' Days', color='1')

# Removing the mplcyberpunk glow effects if checkbox selected
if nocyber == False:
    mplcyberpunk.add_glow_effects()
else:
    legend = plt.legend(selected_country)
    plt.setp(legend.get_texts(), color='k')

# Displaying the plot and the last 3 days' values
st.pyplot(fig)



st.write('''
    Dashboard created by [Biltu Dey](https://linkedin.com/in/biltudey), with [Streamlit](https://www.streamlit.io).
    See the code on [GitHub](https://github.com/biltudey/Covid-19-Dashboard).
    Disclaimer: I have made every effort to ensure the accuracy and reliability of the information on this dashboard. However, the information is provided "as is" without warranty of any kind.
''')
