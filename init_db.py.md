# init_db.py

## Purpose
Database initialization script that creates the required SQLite schema for Chainlit persistence.

## Schema Design

### Tables Created
1. **users** - User identities and metadata
2. **threads** - Conversation threads with tags and metadata
3. **steps** - Individual messages and actions within threads
4. **elements** - Attachments, files, and rich content
5. **feedbacks** - User feedback (thumbs up/down) on messages

### Key Relationships
- `threads.userId` → `users.id` (one-to-many)
- `steps.threadId` → `threads.id` (cascade delete)
- `steps.parentId` → `steps.id` (cascade delete, for nested steps)
- `elements.threadId` → `threads.id` (cascade delete)
- `feedbacks.forId` → `steps.id` (cascade delete)

## Usage

Run this script once to initialize a new database:

```bash
python init_db.py
```

**Output**: Creates `chatbot.db` with all required tables.

## Notes
- Safe to run multiple times (uses `IF NOT EXISTS`)
- Foreign key constraints enable cascade deletes for data integrity
- Uses `aiosqlite` for async database operations
- Compatible with `SQLiteFriendlyDataLayer` implementation
