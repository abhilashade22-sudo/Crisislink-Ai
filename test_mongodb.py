
from app.mongo import init_mongodb

try:
    db = init_mongodb()

    db.connection_test.insert_one({
        "message": "CrisisLink AI MongoDB connection successful!"
    })

    print("Test document inserted successfully!")

except Exception as e:
    print("MongoDB connection failed:", e)
