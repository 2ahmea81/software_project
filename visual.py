import matplotlib.pyplot as plt
import pandas as pd

def visualise_data_submenu():
    print("\nPlease enter one of the following options:")
    print("[A] Pie Chart: Reviews per Park")
    print("[B] Top 10 Locations by Average Rating for a Park")
    print("[C] Monthly Average Rating for a Park")
    return input("\nYour choice: ").strip().upper()

def handle_visualise_data(data):
    choice = visualise_data_submenu()
    if choice == 'A':
        counts = data['Branch'].value_counts()
        counts.plot(kind='pie', autopct='%1.1f%%', title='Reviews per Park')
        plt.ylabel('')
        plt.show()
    elif choice == 'B':
        park = input("Enter the park name: ").strip()
        park_data = data[data['Branch'] == park]
        if not park_data.empty:
            top_locations = park_data.groupby('Reviewer_Location')['Rating'].mean().sort_values(ascending=False).head(10)
            top_locations.plot(kind='bar', title=f'Top 10 Locations by Average Rating for {park}')
            plt.xlabel('Reviewer Location')
            plt.ylabel('Average Rating')
            plt.show()
        else:
            print(f"No data found for the park '{park}'.")
    elif choice == 'C':
        park = input("Enter the park name: ").strip()
        park_data = data[data['Branch'] == park]
        if not park_data.empty:
            park_data['Month'] = pd.to_datetime(park_data['Year_Month']).dt.month_name()
            monthly_avg = park_data.groupby('Month')['Rating'].mean()
            ordered_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            monthly_avg = monthly_avg.reindex(ordered_months)
            monthly_avg.plot(kind='bar', title=f'Monthly Average Rating for {park}')
            plt.xlabel('Month')
            plt.ylabel('Average Rating')
            plt.show()
        else:
            print(f"No data found for the park '{park}'.")
