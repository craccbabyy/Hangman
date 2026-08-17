import shutil 
import os 
from datetime import datetime

# Define paths
DB_FILE = 'highscores.db' 
BACKUP_DIR = 'db_backups'

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)

# Create timestamped filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
backup_filename = f"highscores_backup_{timestamp}.db" 
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# Copy database
try: 
    shutil.copy2(DB_FILE, backup_path) 
    print(f"Backup created successfully: {backup_path}")
except FileNotFoundError: 
    print("Error: Database file not found.")
except Exception as e:
    print(f"Error creating backup: {e}")

