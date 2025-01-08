# Data Management System for Training Program

## Project Overview

This Data Management System was designed to support a 4-month training program focused on digital literacy, AI, and robotics for students in grades 6–12. The system is built to manage key aspects such as **attendance**, **performance**, **material usage**, and **teaching methodologies**, providing stakeholders with real-time insights.

Using **Python**, **PostgreSQL**, and **Power BI**, I created a streamlined workflow that automates data processing, storage, and visualization. This project is scalable and automated, providing easy access to interactive dashboards for efficient monitoring and decision-making.

---

## Key Contributions

### 1. **Automated Data Processing**
I developed Python scripts to automate the following tasks:
- **File Monitoring**: Using the Watchdog library for real-time updates.
- **Data Cleaning**: Removed duplicates, standardized missing values, and resolved inconsistencies.
- **Formatting**: Converted datetime formats and ensured consistency across datasets.

### 2. **Database Design from Scratch**
A well-thought-out relational database schema was created to handle all aspects of the program. The key tables include:
- **Students**: Contains student details like name, grade, and contact information.
- **Trainers**: Tracks trainers' expertise and assigned grades.
- **Subjects**: Stores the topics covered in training sessions.
- **Attendance**: Daily attendance records linked to students and trainers.
- **Performance**: Weekly feedback, scores, and KPIs.
- **Material Usage**: Logs resource utilization by students and trainers.
- **Method Effectiveness**: Includes engagement scores, completion rates, and student feedback.

Here is a preview of the **Database Design**:

![Database Design](img/database_design.png)

### 3. **Interactive Power BI Dashboards**
The dashboards are designed to present data visually, including:
- Attendance trends and engagement metrics.
- Performance evaluations of both trainers and students.
- Insights into material usage.
- Effectiveness of teaching methods.

Here is a preview of the **Power BI Dashboard**:

![Power BI Dashboard](img/dashboard.png)

These dashboards are hosted online, enabling stakeholders to access real-time insights for easy collaboration.

---

## Tools and Workflow

### Programming:
- **Python**: Utilized libraries such as Watchdog for file monitoring, Pandas for automation, and data analysis.
  
### Database:
- **PostgreSQL**: Designed and implemented a relational database, with optimized queries to handle large datasets.

### Visualization:
- **Power BI**: Created interactive dashboards to visualize attendance, performance, and material usage.

### Hosting:
- **Netlify**: Hosted the Power BI dashboards for real-time access by stakeholders.

### Workflow:
- Collected data from Excel sheets (dummy data generated via ChatGPT).
- Automated data ingestion, validation, and cleaning using Python.
- Designed and deployed a PostgreSQL database to store and manage data.
- Connected Power BI dashboards to the SQL database for real-time analysis.
- Hosted the dashboards online for easy access by stakeholders.

---

## Project Impact

### 1. **Efficiency**:
By automating key processes, I reduced manual data handling and streamlined workflows, saving valuable time for stakeholders.

### 2. **Insightful Analysis**:
The system enabled the monitoring of key metrics such as performance, attendance, and material usage, leading to better decision-making and improved training outcomes.

### 3. **Scalability**:
The system was built to accommodate larger datasets and more complex workflows, ensuring that it can handle future expansions and new programs.

---

## What's Next?

The next steps for improving the project include:
- **Predictive Analytics**: Integrating machine learning models to provide forecasts for performance and engagement.
- **Enhanced Dashboards**: Adding more interactivity and optimizing the dashboards for faster loading times.
- **System Expansion**: Adapting the system to handle additional programs and datasets.

---

## Contact

Feel free to reach out for any questions or suggestions. I’d love to hear from you!

**Name**: Rushi Birewar  
**Email**: birewarrushi0@gmail.com  

Explore this project, share your feedback, and let me know how I can make it even better!

