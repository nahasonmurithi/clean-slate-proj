#!/usr/bin/env python3

from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Cleaner, CleaningTask, Client, ClientTask

fake = Faker()

experience_levels = ["Junior", "Intermediate", "Senior"]
cleaning_tasks = [
    {
        "task_description": "Dish washing",
        "Price": 150
    },
    {
        "task_description": "Laundry",
        "Price": 200
    },
    {
        "task_description": "Carpet Cleaning",
        "Price": 95
    },
    {
        "task_description": "Car wash",
        "Price": 400
    },
    {
        "task_description": "Spring Cleaning",
        "Price": 190
    },
    {
        "task_description": "House Cleaning",
        "Price": 500
    },
    {
        "task_description": "Dryer vent cleaning",
        "Price": 99
    },
    {
        "task_description": "Décor clean",
        "Price": 367
    },
    {
        "task_description": "Upholstery cleaning tasks",
        "Price": 298
    },
    {
        "task_description": "Mini Clean",
        "Price": 115
    }
]

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///clean_slate.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    #empty previous data
    session.query(Cleaner).delete()
    session.query(CleaningTask).delete()
    session.query(Client).delete()
    session.query(ClientTask).delete()



    for i in range(5):
        cleaner = Cleaner(
            full_name = fake.unique.name(),
            contact_number = fake.phone_number(),
            experience_level= random.choice(experience_levels)
        )
        session.add(cleaner)
        session.commit()



    for service in cleaning_tasks:
        cleaning_task = CleaningTask(
            task_description = service["task_description"],
            price=service["Price"],
            cleaner_id = random.randint(1, 5)
        )
        session.add(cleaning_task)
        session.commit()

    for i in range(20):
        client = Client(
            client_name = fake.unique.name(),
            email = fake.email(),
            password = fake.password(length = 12),
            contact_number = fake.phone_number()
        )
        session.add(client)
        session.commit()

    task_ids = [task.task_id for task in session.query(CleaningTask)]
    client_ids = [client.client_id for client in session.query(Client)]

    for i in range(10):
        client_task = ClientTask(
            client_id = random.choice(client_ids),
            task_id = random.choice(task_ids)
        )
        session.add(client_task)
        session.commit()
    session.close()

