import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import pyodbc
import traceback

class ExcelFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("Student_Performance_Combined.xlsx"):
            print("Excel file updated. Processing new data...")
            ingest_students_and_performance()
        elif event.src_path.endswith("Trainer_MethodEffectiveness_Combined.xlsx"):
            print("Trainer Excel file updated. Processing new data...")
            ingest_data_from_excel()
        elif event.src_path.endswith("Subject_Attendance_Combined.xlsx"):
            print("Attendance Excel file updated. Processing new attendance and subject data...")
            ingest_subjects_and_attendance()
        elif event.src_path.endswith("Material_Assessment_Combined.xlsx"):
            print("Excel file updated. Processing new test data...")
            ingest_material_and_assessments()
        else:
            print(".........")            

def ingest_students_and_performance():
    try:
        # Database connection setup
        conn = pyodbc.connect(
            "Driver={MySQL ODBC 9.1 ANSI Driver};"
            "Server=localhost;"
            "Database=TrainingProgramDB;"
            "USER=rushi;"
            "Password=Tellmehow123@"
        )
        cursor = conn.cursor()

        # Read the Excel file
        df = pd.read_excel("./../data/Student_Performance_Combined.xlsx")

        # Process students data
        students_columns = df[['Student_ID', 'Name', 'Gender', 'Grade', 'Date_Of_Joining',
                               'Mail_ID', 'Parent_Phone_No', 'Active_Status']].drop_duplicates()

        # Fetch existing student IDs from the database
        cursor.execute("SELECT Student_ID FROM students")
        existing_student_ids = {row[0] for row in cursor.fetchall()}

        # Filter new students data
        new_students_data = students_columns[~students_columns['Student_ID'].isin(existing_student_ids)]

        # Insert new students data into the students table
        insert_students_query = """
        INSERT INTO students (Student_ID, Name, Gender, Grade, Date_Of_Joining,
                              Mail_ID, Parent_Phone_No, Active_Status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        for index, row in new_students_data.iterrows():
            cursor.execute(insert_students_query,
                           row['Student_ID'],
                           row['Name'],
                           row['Gender'],
                           row['Grade'],
                           row['Date_Of_Joining'],
                           row['Mail_ID'],
                           row['Parent_Phone_No'],
                           row['Active_Status'])

        print(f"{len(new_students_data)} new rows inserted into the students table.")

        # Process student performance data
        performance_columns = df[['Performance_ID', 'Student_ID', 'Week_Number',
                                   'Engagement_Score', 'Task_Status', 
                                   'Custom_Performance_Index', 'Feedback']].drop_duplicates()

        # Fetch existing performance IDs from the student_performance table
        cursor.execute("SELECT Performance_ID FROM student_performance")
        existing_performance_ids = {row[0] for row in cursor.fetchall()}

        # Filter new student performance data
        new_performance_data = performance_columns[~performance_columns['Performance_ID'].isin(existing_performance_ids)]

        # Insert new student performance data into the student_performance table
        insert_performance_query = """
        INSERT INTO student_performance (Performance_ID, Student_ID, Week_Number, 
                                         Engagement_Score, Task_Status, 
                                         Custom_Performance_Index, Feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        for index, row in new_performance_data.iterrows():
            cursor.execute(insert_performance_query,
                           row['Performance_ID'],
                           row['Student_ID'],
                           row['Week_Number'],
                           row['Engagement_Score'],
                           row['Task_Status'],
                           row['Custom_Performance_Index'],
                           row['Feedback'])

        print(f"{len(new_performance_data)} new rows inserted into the student_performance table.")

        # Commit changes
        conn.commit()

    except Exception as e:
        print(f"Error ingesting data: {e}")
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def ingest_data_from_excel():
    try:
        # Database connection setup
        conn = pyodbc.connect(
            "Driver={MySQL ODBC 9.1 ANSI Driver};"
            "Server=localhost;"
            "Database=TrainingProgramDB;"
            "USER=rushi;"
            "Password=Tellmehow123@"
        )
        cursor = conn.cursor()

        # Read the Excel file containing trainers and method effectiveness data
        df = pd.read_excel("./../data/Trainer_MethodEffectiveness_Combined.xlsx")  # Adjust the path as needed

        # Process trainers data
        # Select required columns for trainers table
        trainers_columns = df[['Trainer_ID', 'Name', 'Expertise', 'Class_Grade', 'Specialization']]

        # Fetch existing Trainer_IDs from the database
        cursor.execute("SELECT Trainer_ID FROM trainers")
        existing_trainer_ids = {row[0] for row in cursor.fetchall()}

        # Filter new trainers data
        new_trainers_data = trainers_columns[~trainers_columns['Trainer_ID'].isin(existing_trainer_ids)]

        # Insert new trainers data into the trainers table
        if not new_trainers_data.empty:
            insert_trainers_query = """
            INSERT INTO trainers (Trainer_ID, Name, Expertise, Class_Grade, Specialization)
            VALUES (?, ?, ?, ?, ?)
            """
            for index, row in new_trainers_data.iterrows():
                cursor.execute(insert_trainers_query, 
                               row['Trainer_ID'], 
                               row['Name'], 
                               row['Expertise'], 
                               row['Class_Grade'], 
                               row['Specialization'])
            print(f"{len(new_trainers_data)} new trainers inserted into the trainers table.")
        else:
            print("No new trainers to insert.")

        # Process method effectiveness data
        # Select required columns for method_effectiveness table
        method_effectiveness_columns = df[['Method_Effectiveness_ID', 'Trainer_ID', 'Engagement_Score', 
                                            'Course_Completion_Percentage', 'Student_Feedback_Rating', 
                                            'Date_Feedback_Provided', 'Method_Description']]

        # Fetch existing Method_Effectiveness_IDs from the database
        cursor.execute("SELECT Method_Effectiveness_ID FROM method_effectiveness")
        existing_method_effectiveness_ids = {row[0] for row in cursor.fetchall()}

        # Filter new method effectiveness data
        new_method_effectiveness_data = method_effectiveness_columns[~method_effectiveness_columns['Method_Effectiveness_ID'].isin(existing_method_effectiveness_ids)]

        # Insert new method effectiveness data into the method_effectiveness table
        if not new_method_effectiveness_data.empty:
            insert_method_effectiveness_query = """
            INSERT INTO method_effectiveness (Method_Effectiveness_ID, Trainer_ID, Engagement_Score, 
                                               Course_Completion_Percentage, Student_Feedback_Rating, 
                                               Date_Feedback_Provided, Method_Description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            for index, row in new_method_effectiveness_data.iterrows():
                cursor.execute(insert_method_effectiveness_query, 
                               row['Method_Effectiveness_ID'], 
                               row['Trainer_ID'], 
                               row['Engagement_Score'], 
                               row['Course_Completion_Percentage'], 
                               row['Student_Feedback_Rating'], 
                               row['Date_Feedback_Provided'], 
                               row['Method_Description'])
            print(f"{len(new_method_effectiveness_data)} new method effectiveness records inserted into the method_effectiveness table.")
        else:
            print("No new method effectiveness records to insert.")

        # Commit the changes
        conn.commit()
        
    except Exception as e:
        print(f"Error ingesting data from Excel: {e}")
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def ingest_subjects_and_attendance():
    try:
        # Database connection setup
        conn = pyodbc.connect(
            "Driver={MySQL ODBC 9.1 ANSI Driver};"
            "Server=localhost;"
            "Database=TrainingProgramDB;"
            "USER=rushi;"
            "Password=Tellmehow123@"
        )
        cursor = conn.cursor()

        # Read the Excel file
        df = pd.read_excel("./../data/Subject_Attendance_Combined.xlsx")

        # Process subjects data
        subjects_columns = df[['Subject_ID', 'Subject_Name', 'Subject_Description']].drop_duplicates()
        cursor.execute("SELECT Subject_ID FROM subjects")
        existing_subject_ids = {row[0] for row in cursor.fetchall()}
        new_subjects_data = subjects_columns[~subjects_columns['Subject_ID'].isin(existing_subject_ids)]
        
        insert_subjects_query = """
        INSERT INTO subjects (Subject_ID, Subject_Name, Subject_Description)
        VALUES (?, ?, ?)
        """
        for index, row in new_subjects_data.iterrows():
            cursor.execute(insert_subjects_query, 
                           row['Subject_ID'], 
                           row['Subject_Name'], 
                           row['Subject_Description'])
        print(f"{len(new_subjects_data)} new rows inserted into the subjects table.")

        # Process attendance data
        attendance_columns = df[['Attendance_ID', 'Subject_ID', 'Student_ID', 'Trainer_ID', 
                                  'Date', 'Attendance_Status', 'Engagement_Impact']]
        cursor.execute("SELECT Attendance_ID FROM attendance")
        existing_attendance_ids = {row[0] for row in cursor.fetchall()}
        new_attendance_data = attendance_columns[~attendance_columns['Attendance_ID'].isin(existing_attendance_ids)]

        insert_attendance_query = """
        INSERT INTO attendance (Attendance_ID, Subject_ID, Student_ID, Trainer_ID, Date, 
                                Attendance_Status, Engagement_Impact)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        for index, row in new_attendance_data.iterrows():
            try:
                cursor.execute(insert_attendance_query, 
                               row['Attendance_ID'], 
                               row['Subject_ID'], 
                               row['Student_ID'], 
                               row['Trainer_ID'], 
                               row['Date'], 
                               row['Attendance_Status'], 
                               row['Engagement_Impact'])
            except Exception as e:
                print(f"Error inserting attendance record for Attendance_ID {row['Attendance_ID']}: {e}")
                print(f"Trainer_ID: {row['Trainer_ID']} does not exist in the trainers table.")
        
        print(f"{len(new_attendance_data)} new rows inserted into the attendance table.")
        conn.commit()
        
    except Exception as e:
        print(f"Error ingesting data from Excel: {e}")
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def ingest_material_and_assessments():
    try:
        # Database connection setup
        conn = pyodbc.connect(
            "Driver={MySQL ODBC 9.1 ANSI Driver};"
            "Server=localhost;"
            "Database=TrainingProgramDB;"
            "USER=rushi;"
            "Password=Tellmehow123@"
        )
        cursor = conn.cursor()

        # Read the Excel file
        df = pd.read_excel("./../data/Material_Assessment_Combined.xlsx")

        # Process material usage data
        # Select required columns for material_usage table
        material_usage_columns = df[['Material_ID', 'Student_ID', 'Material_Type', 
                                     'Usage_Percentage', 'Effectiveness_Score', 'Feedback_x']].drop_duplicates()
        
        # Fetch existing IDs from the material_usage table
        cursor.execute("SELECT Material_ID, Student_ID FROM material_usage")
        existing_material_ids = {(row[0], row[1]) for row in cursor.fetchall()}

        # Filter new material usage data
        new_material_usage_data = material_usage_columns[
            ~material_usage_columns.set_index(['Material_ID', 'Student_ID']).index.isin(existing_material_ids)
        ]

        # Insert new material usage data into the material_usage table
        insert_material_usage_query = """
        INSERT INTO material_usage (Material_ID, Student_ID, Material_Type, Usage_Percentage, 
                                    Effectiveness_Score, Feedback_m)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        for index, row in new_material_usage_data.iterrows():
            cursor.execute(insert_material_usage_query, 
                           row['Material_ID'], 
                           row['Student_ID'], 
                           row['Material_Type'], 
                           row['Usage_Percentage'], 
                           row['Effectiveness_Score'], 
                           row['Feedback_x'])

        print(f"{len(new_material_usage_data)} new rows inserted into the material_usage table.")

        # Process assessments data
        # Select required columns for assessments table
        assessments_columns = df[['Student_ID', 'Assessment_ID', 'Type', 'Score', 'Feedback_y']].drop_duplicates()
        
        # Fetch existing IDs from the assessments table
        cursor.execute("SELECT Assessment_ID FROM assessments")
        existing_assessment_ids = {row[0] for row in cursor.fetchall()}

        # Filter new assessments data
        new_assessments_data = assessments_columns[~assessments_columns['Assessment_ID'].isin(existing_assessment_ids)]

        # Insert new assessments data into the assessments table
        insert_assessments_query = """
        INSERT INTO assessments (Student_ID, Assessment_ID, Type, Score, Feedback_a)
        VALUES (?, ?, ?, ?, ?)
        """
        for index, row in new_assessments_data.iterrows():
            cursor.execute(insert_assessments_query, 
                           row['Student_ID'], 
                           row['Assessment_ID'], 
                           row['Type'], 
                           row['Score'], 
                           row['Feedback_y'])

        print(f"{len(new_assessments_data)} new rows inserted into the assessments table.")

        # Commit the changes
        conn.commit()
        
    except Exception as e:
        print(f"Error ingesting data from Excel: {e}")
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




if __name__ == "__main__":
    path = "C:\D\TASK_PROJECT\data"
    print("Watcher Started...")
    event_handler = ExcelFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(6)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
