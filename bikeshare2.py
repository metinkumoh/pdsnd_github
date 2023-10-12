import time
import pandas as pd
import numpy as np

# Dictionary mapping city names to CSV file names
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


''' The next part of the script will prompt the user which city, month, and day they would like to explore. 
To do this, a function was created to act as a data filter based on the users input. 
This is followed by a function to load the selected data. '''
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. Be sure to make the input .lower()
    Utilize while True: loops
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!') 
    
    
    #get user input for city (chicago, new york city, washington).
    city_options = ['chicago', 'new york city', 'washington']
    city_input = input("Select City: Chicago, New York City,Washington: ").lower()

    while city_input not in city_options:
        print("Sorry, I didn't catch that. Try again.")
        city_input = input("Select City: Chicago, New York City,Washington: ").lower()

    # Get user input for month (all, january, february, ... , june)
    month_options = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month_input = input("Select month: All, January, February, March, April, May, or June: ").lower()

    while month_input not in month_options:
        print("Sorry, I didn't catch that. Try again.")
        month_input = input("Select month: All, January, February, March, April, May, or June: ").lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day_options = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_input = input("Select Day: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: ").lower()

    while day_input not in day_options:
        print("Sorry, I didn't catch that. Try again.")
        day_input = input("Select Day: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: ").lower()
    
    print('-'*40)
    return city_input, month_input, day_input

   
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Optimized the filtering process for better efficiency
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df

def time_stats(df):
    
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    busy_month = df['month'].mode()[0]
    print("The busiest month: ", busy_month)
    
    print("The busiest day:", df['day_of_week'].mode()[0])
    
    print("The busiest starting hour:", df['hour'].mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station is: ', most_common_start_station)

    #display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station is: ', most_common_end_station)

    combination_of_start_end_station=df.groupby(['Start Station','End Station'])
    most_frequent_combined_station = combination_of_start_end_station.size().sort_values(ascending=False).head(1)
    print('Most common trip from start to end is: ', most_frequent_combined_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Compute trip duration
    # Trip duration is in seconds
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is: ', total_travel_time)

    # display mean travel time
    # Trip duration is in seconds
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
# Compute user info
def user_info(df, city):
    """
    Displays information on bikeshare users.
    Refactored user information display for better readability.
    """

    print('\nCalculating User info...:')
    start_time = time.time()

    # Display user type counts
    print('Counts of each user type:')
    print(df['User Type'].value_counts())

    if 'Gender' in df:
        # Display gender counts
        print('Counts of each gender:')
        print(df['Gender'].value_counts())

    if 'Birth Year' in df:
        # Display birth year information
        print('Earliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth:', int(df['Birth Year'].mode()[0]))
       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
def show_row_data(df):

    """
    Displays raw data if the users wishes to see it.
    """
    x = 0
    while True:
        raw_data = input("Would you like to see the raw data? Enter yes or no.\n").lower()
        
        if raw_data == "yes":
            print(df.iloc[x: x + 5])
            x += 5
        elif raw_data == "no":
            break
        else:
            print("Sorry! You entered Wrong Input, Kindly try Again!")
            
# This function ties all the codes together.
def main():
 
    while True:
        city,month,day = get_filters()      
        df = load_data(city,month,day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_info(df,city)
        show_row_data(df)
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break
        
if __name__ == "__main__":
	main()