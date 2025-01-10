
import pandas as pd
import matplotlib.pyplot as plt
import json

class DataExporter:
    def __init__(self, data):
        self.data = data

    def aggregate_data(self):
        result = self.data.groupby('Branch').agg(
            number_of_reviews=('Review_ID', 'count'),
            number_of_positive_reviews=('Rating', lambda x: (x >= 4).sum()),
            average_review_score=('Rating', 'mean'),
            number_of_countries=('Reviewer_Location', 'nunique')
        ).reset_index()
        return result

    def export_to_txt(self, filename):
        aggregate = self.aggregate_data()
        with open(filename, 'w') as f:
            for _, row in aggregate.iterrows():
                f.write(f"Park: {row['Branch']}, Reviews: {row['number_of_reviews']}, Positive Reviews: {row['number_of_positive_reviews']}, Average Score: {row['average_review_score']:.2f}, Countries: {row['number_of_countries']}\n")

    def export_to_csv(self, filename):
        aggregate = self.aggregate_data()
        aggregate.to_csv(filename, index=False)

    def export_to_json(self, filename):
        aggregate = self.aggregate_data()
        aggregate.to_json(filename, orient='records')

def display_title():
    title = "Disneyland Review Analyser"
    print("-" * len(title))
    print(title)
    print("-" * len(title))

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully. The dataset contains {len(data)} rows.")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def main_menu():
    print("\nPlease enter the letter which corresponds with your desired menu choice:")
    print("[A] View Data")
    print("[B] Visualise Data")
    print("[C] Export Data")
    print("[X] Exit")
    return input("\nYour choice: ").strip().upper()

def view_data_submenu():
    print("\nPlease enter one of the following options:")
    print("[A] View Reviews by Park")
    print("[B] Number of Reviews by Park and Reviewer Location")
    print("[C] Average Rating for a Park by Year")
    print("[D] Average Score per Park by Reviewer Location")
    return input("\nYour choice: ").strip().upper()

def visualise_data_submenu():
    print("\nPlease enter one of the following options:")
    print("[A] Pie Chart: Reviews per Park")
    print("[B] Top 10 Locations by Average Rating for a Park")
    print("[C] Monthly Average Rating for a Park")
    return input("\nYour choice: ").strip().upper()

def handle_view_data(data):
    choice = view_data_submenu()
    if choice == 'A':
        if 'Branch' in data.columns and 'Review_ID' in data.columns:
            park = input("Enter the park name to view reviews: ").strip()
            park_reviews = data[data['Branch'] == park]
            if not park_reviews.empty:
                print(park_reviews[['Review_ID', 'Rating', 'Reviewer_Location', 'Year_Month']])
            else:
                print("No reviews found for the specified park.")
        else:
            print("Required columns ('Branch', 'Review_ID') are missing from the dataset.")
    elif choice == 'B':
        if 'Branch' in data.columns and 'Reviewer_Location' in data.columns and 'Review_ID' in data.columns:
            park = input("Enter the park name: ").strip()
            location = input("Enter the reviewer location: ").strip()
            review_count = data[(data['Branch'] == park) & (data['Reviewer_Location'] == location)].shape[0]
            print(f"The park '{park}' has received {review_count} reviews from '{location}'.")
        else:
            print("Required columns ('Branch', 'Reviewer_Location', 'Review_ID') are missing.")
    elif choice == 'C':
        if 'Year_Month' in data.columns and 'Branch' in data.columns and 'Rating' in data.columns:
            park = input("Enter the park name: ").strip()
            year = input("Enter the year (YYYY): ").strip()
            year_reviews = data[(data['Branch'] == park) & (data['Year_Month'].str.startswith(year))]
            if not year_reviews.empty:
                avg_rating = year_reviews['Rating'].mean()
                print(f"The average rating for '{park}' in {year} is {avg_rating:.2f}.")
            else:
                print(f"No reviews found for the park '{park}' in the year {year}.")
        else:
            print("Required columns ('Year_Month', 'Branch', 'Rating') are missing.")
    elif choice == 'D':
        if 'Branch' in data.columns and 'Reviewer_Location' in data.columns and 'Rating' in data.columns:
            avg_scores = data.groupby(['Branch', 'Reviewer_Location'])['Rating'].mean().unstack()
            print(avg_scores)
        else:
            print("Required columns ('Branch', 'Reviewer_Location', 'Rating') are missing.")
    else:
        print("Invalid choice. Returning to main menu.")

def handle_visualise_data(data):
    choice = visualise_data_submenu()
    if choice == 'A':
        if 'Branch' in data.columns:
            counts = data['Branch'].value_counts()
            counts.plot(kind='pie', autopct='%1.1f%%', title='Reviews per Park')
            plt.ylabel('')
            plt.show()
        else:
            print("Column 'Branch' is missing.")
    elif choice == 'B':
        if 'Branch' in data.columns and 'Reviewer_Location' in data.columns and 'Rating' in data.columns:
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
        else:
            print("Required columns ('Branch', 'Reviewer_Location', 'Rating') are missing.")
    elif choice == 'C':
        if 'Branch' in data.columns and 'Year_Month' in data.columns and 'Rating' in data.columns:
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
        else:
            print("Required columns ('Branch', 'Year_Month', 'Rating') are missing.")
    else:
        print("Invalid choice. Returning to main menu.")

def handle_export_data(data):
    exporter = DataExporter(data)
    print("\nPlease select the export format:")
    print("[1] TXT")
    print("[2] CSV")
    print("[3] JSON")
    choice = input("\nYour choice: ").strip()
    if choice == '1':
        exporter.export_to_txt('exported_data.txt')
        print("Data exported to 'exported_data.txt'.")
    elif choice == '2':
        exporter.export_to_csv('exported_data.csv')
        print("Data exported to 'exported_data.csv'.")
    elif choice == '3':
        exporter.export_to_json('exported_data.json')
        print("Data exported to 'exported_data.json'.")
    else:
        print("Invalid choice. Returning to main menu.")

def main():
    display_title()
    file_path = r'C:\Users\MHaroon\OneDrive - Cedar Financial\Desktop\python test\project_template (1)\disneyland_reviews.csv'

    data = load_data(file_path)

    if data is None:
        return

    while True:
        choice = main_menu()
        if choice == 'A':
            handle_view_data(data)
        elif choice == 'B':
            handle_visualise_data(data)
        elif choice == 'C':
            handle_export_data(data)
        elif choice == 'X':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
