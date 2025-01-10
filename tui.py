def display_title():
    title = "Disneyland Review Analyser"
    print("-" * len(title))
    print(title)
    print("-" * len(title))

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

def handle_view_data(data):
    choice = view_data_submenu()
    if choice == 'A':
        park = input("Enter the park name to view reviews: ").strip()
        park_reviews = data[data['Branch'] == park]
        if not park_reviews.empty:
            print(park_reviews[['Review_ID', 'Rating', 'Reviewer_Location', 'Year_Month']])
        else:
            print("No reviews found for the specified park.")
    elif choice == 'B':
        park = input("Enter the park name: ").strip()
        location = input("Enter the reviewer location: ").strip()
        review_count = data[(data['Branch'] == park) & (data['Reviewer_Location'] == location)].shape[0]
        print(f"The park '{park}' has received {review_count} reviews from '{location}'.")
    elif choice == 'C':
        park = input("Enter the park name: ").strip()
        year = input("Enter the year (YYYY): ").strip()
        year_reviews = data[(data['Branch'] == park) & (data['Year_Month'].str.startswith(year))]
        if not year_reviews.empty:
            avg_rating = year_reviews['Rating'].mean()
            print(f"The average rating for '{park}' in {year} is {avg_rating:.2f}.")
        else:
            print(f"No reviews found for the park '{park}' in the year {year}.")
    elif choice == 'D':
        avg_scores = data.groupby(['Branch', 'Reviewer_Location'])['Rating'].mean().unstack()
        print(avg_scores)
    else:
        print("Invalid choice. Returning to main menu.")
