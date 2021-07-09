# To-Do list can improve your work and personal life. You can use it to reduce
# the stress in your life and get more done in less time. It also helps you become
# more reliable for other people and save time for the best things in life. So let's
# implement it!

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return self.task


class Todolist:
    def __init__(self, session):
        self.active = True
        self.session = session
        self.menu = {'1': {'title': "Today's tasks",
                           'action': self.day},
                     '2': {'title': "Week's tasks",
                           'action': self.week},
                     '3': {'title': "All tasks",
                           'action': self.all},
                     '4': {'title': "Missed tasks",
                           'action': self.missed},
                     '5': {'title': "Add task",
                           'action': self.add},
                     '6': {'title': "Delete task",
                           'action': self.delete},
                     '0': {'title': "Exit",
                           'action': self.exit}
                     }

    def print_menu(self):
        for key, value in self.menu.items():
            print(f'{key}) {value["title"]}')

    @staticmethod
    def print_tasks(tasks, header, nothing_msg='Nothing to do!', show_deadline=False):
        print(header, end=':\n')
        if tasks:
            for idx, row in enumerate(tasks):
                print(f'{idx + 1}. {row.task}',
                      f'. {row.deadline.strftime("%#d %b")}' if show_deadline else '',
                      sep='')
        else:
            print(nothing_msg)
        print()

    def _all_tasks(self):
        return self.session.query(Task).order_by(Task.deadline).all()

    def day(self, _date=None):
        if _date is None:
            _date = datetime.today()
            weekday = 'Today'
        else:
            weekday = _date.strftime('%A')
        tasks = self.session.query(Task).filter(Task.deadline == _date.date()).all()
        self.print_tasks(tasks, f'{weekday} {_date.strftime("%#d %b")}')

    def week(self):
        print()
        for day in range(7):
            self.day(_date=datetime.today() + timedelta(day))

    def all(self):
        self.print_tasks(self._all_tasks(), 'All tasks', show_deadline=True)

    def missed(self):
        tasks = self.session.query(Task).filter(Task.deadline < datetime.today().date()).all()
        self.print_tasks(tasks, 'Missed tasks', nothing_msg='Nothing is missed!', show_deadline=True)

    def add(self):
        task_desc = input('Enter task\n')
        task_date = input('Enter deadline\n')
        if not task_date:
            task_date = datetime.today()
        else:
            task_date = datetime.strptime(task_date, '%Y-%m-%d')

        new_task = Task(task=task_desc, deadline=task_date.date())
        self.session.add(new_task)
        self.session.commit()
        print('The task has been added!\n')

    def delete(self):
        tasks = self._all_tasks()
        self.print_tasks(tasks, 'Choose the number of the task you want to delete:',
                         nothing_msg='Nothing to delete', show_deadline=True)
        self.session.delete(tasks[int(input()) - 1])
        self.session.commit()
        print('The task has been deleted!\n')

    def start(self):
        while self.active:
            self.print_menu()
            self.menu[input()]['action']()
        else:
            print('\nBye')

    def exit(self):
        self.active = False


if __name__ == '__main__':
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    todo = Todolist(Session())
    todo.start()
