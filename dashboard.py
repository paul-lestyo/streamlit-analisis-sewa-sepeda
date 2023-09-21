import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')


def create_daily_rent_bike_df(df):
    daily_rent = df.resample(rule='D', on='dteday').cnt.sum().reset_index()
    daily_rent = daily_rent.reset_index()
    return daily_rent


def create_daily_holiday_df(df):
    daily_holiday = df.groupby("holiday").cnt.sum()
    daily_holiday = daily_holiday.reindex([0, 1], fill_value=0)
    return daily_holiday


def create_daily_season_df(df):
    daily_season = df.groupby("season").cnt.sum().reset_index()
    daily_season['season'] = daily_season['season'].replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"})
    return daily_season

def create_daily_day_df(df):
    df = df.groupby('weekday', observed=True).cnt.sum()
    df = df.reindex([0, 1, 2, 3, 4, 5, 6], fill_value=0)
    df = df.reset_index()
    df['weekday'] = df['weekday'].astype('category')
    day_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
    df['weekday'] = df['weekday'].map(day_mapping)
    return df

def create_daily_hour_df(df):
    df = df.groupby('hr', observed=True).cnt.sum()
    df = df.reindex(range(0, 24), fill_value=0)
    df = df.reset_index()
    df['hr'] = df['hr'].astype('category')
    return df


day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

min_date_day = day_df['dteday'].min()
max_date_day = day_df['dteday'].max()

with st.sidebar:
    start_date = ""
    end_date = ""
    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu', min_value=min_date_day,
            max_value=max_date_day,
            value=[min_date_day, max_date_day]
        )
    except ValueError as e:
        st.subheader("Memilih Tanggal....")

main_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]
main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & (hour_df["dteday"] <= str(end_date))]
daily_rent_bike_df = create_daily_rent_bike_df(main_df)
daily_holiday_df = create_daily_holiday_df(main_df)
daily_season_df = create_daily_season_df(main_df)
daily_day_df = create_daily_day_df(main_df)
daily_hour_df = create_daily_hour_df(main_hour_df)


st.header("Rent Bike Collection Dashboard :sparkles:")
st.subheader("Daily Rents")

col1, col2, col3 = st.columns(3)

with col1:
    total_rent = daily_rent_bike_df.cnt.sum()
    st.metric("Total Rent Bike", value=total_rent)

with col2:
    min_rent = daily_rent_bike_df.cnt.min()
    st.metric("Min Rent Bike", value=min_rent)

with col3:
    max_rent = daily_rent_bike_df.cnt.max()
    st.metric("Max Rent Bike", value=max_rent)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_bike_df["dteday"],
    daily_rent_bike_df["cnt"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.subheader("Relationship Between Environmental Factors and Bike Rental Count")

fig, ax = plt.subplots()
sns.heatmap(main_df[['season', 'weathersit',  'holiday', 'workingday', 'weekday', 'cnt']].corr(), ax=ax, annot=True)
st.write(fig)

col1, col2 = st.columns(2)
nonHoliday = daily_holiday_df[0] if daily_holiday_df[0] else 0
holiday = daily_holiday_df[1] if daily_holiday_df[1] else 0

with col1:
    st.metric("Non-Holiday", value=nonHoliday)

with col2:
    st.metric("Holiday", value=holiday)


st.subheader("Daily Rents by Season")
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    daily_season_df["season"],
    daily_season_df["cnt"],
    color="#90CAF9"
)

ax.ticklabel_format(style='plain', axis='y')

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Daily Rents by Day in Week")
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    daily_day_df["weekday"],
    daily_day_df["cnt"],
    color="#90CAF9"
)

ax.ticklabel_format(style='plain', axis='y')

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Daily Rents by Hour in a Day")
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    daily_hour_df["hr"],
    daily_hour_df["cnt"],
    color="#90CAF9"
)

ax.ticklabel_format(style='plain', axis='y')
plt.xticks(daily_hour_df["hr"])
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)