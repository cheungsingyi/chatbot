# init_db.py

```python
import asyncio
import aiosqlite

async def init_database():
    async with aiosqlite.connect("chatbot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                "id" TEXT PRIMARY KEY,
                "identifier" TEXT UNIQUE NOT NULL,
                "metadata" TEXT,
                "createdAt" TEXT
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS threads (
                "id" TEXT PRIMARY KEY,
                "createdAt" TEXT,
                "name" TEXT,
                "userId" TEXT,
                "userIdentifier" TEXT,
                "tags" TEXT,
                "metadata" TEXT,
                FOREIGN KEY("userId") REFERENCES users("id")
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS steps (
                "id" TEXT PRIMARY KEY,
                "name" TEXT,
                "type" TEXT,
                "threadId" TEXT NOT NULL,
                "parentId" TEXT,
                "streaming" INTEGER,
                "waitForAnswer" INTEGER,
                "isError" INTEGER,
                "metadata" TEXT,
                "tags" TEXT,
                "input" TEXT,
                "output" TEXT,
                "createdAt" TEXT,
                "start" TEXT,
                "end" TEXT,
                "generation" TEXT,
                "showInput" TEXT,
                "language" TEXT,
                "indent" INTEGER,
                "defaultOpen" INTEGER,
                FOREIGN KEY("threadId") REFERENCES threads("id") ON DELETE CASCADE,
                FOREIGN KEY("parentId") REFERENCES steps("id") ON DELETE CASCADE
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS elements (
                "id" TEXT PRIMARY KEY,
                "threadId" TEXT,
                "type" TEXT,
                "url" TEXT,
                "chainlitKey" TEXT,
                "objectKey" TEXT,
                "name" TEXT NOT NULL,
                "display" TEXT,
                "size" TEXT,
                "language" TEXT,
                "page" TEXT,
                "forId" TEXT,
                "mime" TEXT,
                "props" TEXT,
                FOREIGN KEY("threadId") REFERENCES threads("id") ON DELETE CASCADE
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS feedbacks (
                "id" TEXT PRIMARY KEY,
                "forId" TEXT NOT NULL,
                "value" INTEGER NOT NULL,
                "comment" TEXT,
                FOREIGN KEY("forId") REFERENCES steps("id") ON DELETE CASCADE
            )
        """)
        
        await db.commit()
        print("✅ Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_database())
```
