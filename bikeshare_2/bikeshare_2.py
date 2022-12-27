import time
import pandas as pd
import numpy as np
import calendar #importing this module to get names of months and days correctly
months = calendar.month_name[1:7]
days = calendar.day_name[:]

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
y_n_list = ['y','yes','n','no']#to use it in functions

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = CITY_DATA.keys()
    city = input('Please,Choose the city that you want to know its data between [chicago or new york city or washington] ').strip().lower()
    while city not in cities :
       print('you entered invalid input city, please check the spelling of available cities from the prompt message ')
       city = input('Please,Choose the city that you want to know its data between [chicago or new york city or washington] ').strip().lower()

    # get user input for month (all, january, february, ... , june)
    month_quest = str()

    while month_quest not in y_n_list :
       month_quest = input('would you like to filter the data by month ? y or n :').strip().lower()
    if (month_quest ==  'y') or (month_quest =='yes') :
        month = input('please enter the month with the same format (january,february,march,april,may,june)  :').strip().title()
        while month not in months:
           print('you entered invalid input character ,you have to enter one of the first 6 months,please check the spelling from the prompt message ')
           month = input('please enter the month with the same format (january,february,march,april,may,june)  :').strip().title()
    else :
       month = 'all' #that means we will get the data for all months without filter
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_quest = str()
    while day_quest not in y_n_list :
       day_quest = input('would you like to filter the data by day ? y or n :').strip().lower()
    if (day_quest ==  'y') or (day_quest =='yes') :
        day = input('please enter the day with the same format (monday, tuesday,wednesday,thursday,friday,saturday,sunday)  :').strip().title()
        while day not in days:
           print('you entered invalid input day name, please check the spelling from the prompt message ')
           day = input('please enter the day with the same format (monday, tuesday,wednesday,thursday,friday,saturday,sunday)  :').strip().title()
    else :
       day = 'all'#that means we will get the data for all days without filter


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        month = months.index(month)+1
        df = df[df['month']==month]
    if day !='all':
            df = df[df['day of week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('the most common month that people travel in it is :  ',df['month'].mode()[0])

    # display the most common day of week
    print('the most common day that people travel in it is :  ',df['day of week'].mode()[0])


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('the most common hour that people travel in it is :  ',df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('the most common station that people travel from it is :  ',df['Start Station'].mode()[0])
    print('and it was repeated :  ',df['Start Station'].value_counts()[df['Start Station'].mode()[0]],' times')

    # display most commonly used end station
    print('the most common station that people travel to it is :  ',df['End Station'].mode()[0])
    print('and it was repeated :  ',df['End Station'].value_counts()[df['End Station'].mode()[0]],' times')


    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station'])
    print('the most frequent combination between start and end trip is :  ',combination.size().idxmax())
    print('and it was repeated :  ',combination.size()[combination.size().idxmax()],' times')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time for this period of time is :',df['Trip Duration'].sum() ,' seconds')

    # display mean travel time
    print('The average travel time for this period of time is :',df['Trip Duration'].mean(),' seconds' )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user types are : ',df['User Type'].value_counts())

    # Display counts of gender
    if city != 'washington' :
         print('counts of gender are : ',df['Gender'].value_counts())
    # Display earliest, most recent, and most common year of birth
         print('the earliest birth year is : ',df['Birth Year'].min())
         print('the most recent birth year is : ',df['Birth Year'].max())
         print('the most common birth year is : ',df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_city_data(df):
    ask = input('\nWould you like to see the raw data? Enter yes or no.\n')
    i,j = 0,5
    while ask.lower() =='yes' :
        print(df[i:j])
        ask = input('\nWould you like to see more raw data? Enter yes or no.\n')
        i+=5
        j+=5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_city_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
