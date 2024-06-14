from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

Base.metadata.create_all(engine)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = session.query(Task).all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks])

@app.route('/task', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data.get('description'))
    session.add(new_task)
    session.commit()
    return jsonify({'message': 'Task added successfully'})

@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = session.query(Task).get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task.title = data['title']
    task.description = data.get('description')
    session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    session.delete(task)
    session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
