import pandas as pd

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

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully. The dataset contains {len(data)} rows.")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

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
