# test_persistence.py

## Purpose
Verification script that tests SQLite persistence functionality and provides diagnostic information about the database state.

## What It Tests

### 1. Data Layer Creation
- Verifies `get_data_layer()` returns a `SQLiteFriendlyDataLayer` instance
- Confirms the custom data layer is properly configured

### 2. Database Statistics
- Counts total threads in the database
- Counts total steps (messages) in the database
- Shows most recent thread with ID, name, and creation timestamp
- Displays step count for the most recent thread

### 3. Connection Test
- Opens a direct SQLite connection to `chatbot.db`
- Executes queries against the persistence tables
- Validates schema is accessible

## Usage

Run this script to check persistence status:

```bash
python test_persistence.py
```

**Expected output**:
```
🧪 Testing SQLite-compatible data layer...
✅ Data layer created: SQLiteFriendlyDataLayer

📊 Checking database contents...
   Threads in database: 3
   Steps in database: 12

📝 Most recent thread:
   ID: abc123...
   Name: (unnamed)
   Created: 2025-10-03T14:23:45.678Z
   Steps in this thread: 4

✅ Data layer test completed successfully!
```

## Manual Testing Steps (Provided by Script)
1. Open http://localhost:8001 in browser
2. Start new conversation or click existing thread
3. Send message like "My name is Jack"
4. Ask "What's my name?"
5. Refresh the page
6. Click the thread in sidebar
7. Ask "Do you remember my name?"
8. Assistant should remember your name

## Troubleshooting

**No threads found**: Database is empty, start a conversation first.

**Database locked error**: Another process (app.py) is accessing the database.

**Import errors**: Run from project root with virtual environment activated.
