# Online Crime Reporting System - Setup Instructions

## Prerequisites
- Python 3.x installed
- Web browser (Chrome, Firefox, etc.)

## Project Structure
```text
/backend
  /migrations, /models, /routes, /uploads, app.py, run.py, requirements.txt
/frontend
  /css, /js, index.html, login.html, register.html, report.html, track.html, admin.html
```

## Step-by-Step Setup

1. **Install Dependencies:**
   Open your terminal in the `backend` folder and run:
   ```cmd
   pip install -r requirements.txt
   ```

2. **Run the Backend Server:**
   While still in the `backend` folder, run:
   ```cmd
   python run.py
   ```
   The server will start at `http://127.0.0.1:5000`. Keep this terminal open.

3. **Open the Frontend:**
   - Locate the `frontend` folder in your file explorer.
   - Simply double-click `index.html` to open the app in your browser.

4. **Using the App:**
   - **Report a Crime**: Click "File a Report" (with or without login).
   - **Evidence**: You can upload images/videos during submission.
   - **Tracking**: Use the provided Tracking ID on the "Track Status" page.
   - **Admin Panel**: 
     - Create an account first.
     - You'll need to manually set the `role` to `'admin'` in the `crime_system.db` (using a tool like SQLite Browser) OR I can pre-configure an admin user below.

## Default Admin Credentials
For your seminar demo, you can use these pre-configured credentials:
- **Username**: `admin`
- **Password**: `admin123`

---

## Technical Presentation Points
- **Architecture**: REST API using Flask (Backend) with Vanilla JS (Frontend).
- **Security**: JWT for session management, Bcrypt for password protection.
- **Storage**: SQLite for relational data, local filesystem for evidence files.
- **UI**: Modern Glassmorphism design using CSS variables and backdrop-filters.
