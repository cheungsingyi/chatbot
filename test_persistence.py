#!/usr/bin/env python
"""
Test script to verify SQLite persistence is working correctly.
"""
import asyncio
import sqlite3
from utils.database import get_data_layer

async def test_data_layer():
    print("🧪 Testing SQLite-compatible data layer...")
    
    data_layer = get_data_layer()
    print(f"✅ Data layer created: {type(data_layer).__name__}")
    
    print("\n📊 Checking database contents...")
    conn = sqlite3.connect("./chatbot.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM threads")
    thread_count = cursor.fetchone()[0]
    print(f"   Threads in database: {thread_count}")
    
    cursor.execute("SELECT COUNT(*) FROM steps")
    step_count = cursor.fetchone()[0]
    print(f"   Steps in database: {step_count}")
    
    if thread_count > 0:
        cursor.execute("SELECT id, name, createdAt FROM threads ORDER BY createdAt DESC LIMIT 1")
        thread = cursor.fetchone()
        print(f"\n📝 Most recent thread:")
        print(f"   ID: {thread[0]}")
        print(f"   Name: {thread[1] or '(unnamed)'}")
        print(f"   Created: {thread[2]}")
        
        thread_id = thread[0]
        cursor.execute("SELECT COUNT(*) FROM steps WHERE threadId = ?", (thread_id,))
        thread_steps = cursor.fetchone()[0]
        print(f"   Steps in this thread: {thread_steps}")
    
    conn.close()
    
    print("\n✅ Data layer test completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Open http://localhost:8001 in your browser")
    print("   2. Start a new conversation or click an existing thread")
    print("   3. Send a message like 'My name is Jack'")
    print("   4. Ask 'What's my name?'")
    print("   5. Refresh the page")
    print("   6. Click the thread in the sidebar")
    print("   7. Ask 'Do you remember my name?'")
    print("   8. The assistant should remember your name!")

if __name__ == "__main__":
    asyncio.run(test_data_layer())
