import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

class ExcelFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified_time = 0
        self.processing_files = set()  # Track files currently being processed

    def on_modified(self, event):
        # Check if the modified file is an Excel file and not a temporary file
        if event.src_path.endswith('.xlsx') and event.src_path not in self.processing_files and not event.src_path.split('/')[-1].startswith('~$'):
            current_time = time.time()
            # Check if enough time has passed since the last modification
            if current_time - self.last_modified_time > 2:  # 2 seconds debounce time
                self.last_modified_time = current_time
                print(f"Detected change in: {event.src_path}")
                # Clean data for the modified file
                self.clean_data(event.src_path)

    def clean_data(self, file_path):
        self.processing_files.add(file_path)  # Mark file as being processed
        cleaned_data = None  # Initialize cleaned_data to None
        
        # Determine which cleaning function to call based on the file name
        if "Student_Performance_Combined" in file_path:
            cleaned_data = clean_student_performance_data(file_path)
        elif "Trainer_MethodEffectiveness_Combined" in file_path:
            cleaned_data = clean_trainer_data(file_path)
        elif "Subject_Attendance_Combined" in file_path:
            cleaned_data = clean_subject_attendance_data(file_path)
        elif "Material_Assessment_Combined" in file_path:
            cleaned_data = clean_material_assessment_data(file_path)

        # Check if cleaned_data was assigned a value
        if cleaned_data is not None:
            time.sleep(3)
            # Save cleaned data back to the same file
            cleaned_data.to_excel(file_path, index=False)  # Overwrite the existing file
            print(f"Cleaned data saved for: {file_path}")
        else:
            print(f"No cleaning function was called for: {file_path}")

        self.processing_files.remove(file_path)  # Mark file as no longer being processed

def clean_student_performance_data(file_path):
    df = pd.read_excel(file_path)
    df = df.drop_duplicates()
    df['Name'] = df['Name'].fillna('Unknown')
    df['Mail_ID'] = df['Mail_ID'].fillna('No Email')
    df['Parent_Phone_No'] = df['Parent_Phone_No'].fillna('Not Provided')
    df['Date_Of_Joining'] = pd.to_datetime(df['Date_Of_Joining'], errors='coerce')
    return df

def clean_trainer_data(file_path):
    df = pd.read_excel(file_path)
    df = df.drop_duplicates()
    df['Name'] = df['Name'].fillna('Unknown')
    df['Expertise'] = df['Expertise'].fillna('General')
    return df

def clean_subject_attendance_data(file_path):
    df = pd.read_excel(file_path)
    df = df.drop_duplicates()
    df['Subject_Name'] = df['Subject_Name'].fillna('Unknown')
    df['Attendance_Status'] = df['Attendance_Status'].fillna('Absent')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

def clean_material_assessment_data(file_path):
    df = pd.read_excel(file_path)
    df = df.drop_duplicates()
    df['Material_Type'] = df['Material_Type'].fillna('Unknown')
    return df

def main():
    path = "./../data"  # Directory to monitor for Excel file changes
    print("Watcher Started...")
    event_handler = ExcelFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
