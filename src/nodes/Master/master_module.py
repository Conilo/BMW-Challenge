import rospy
import bmw_wrap as bw
import time as tm

# Definitions
IDLE = 0
MAPPING = 1
ESCAPING = 2

# Task names descriptions
task_desc = {
    IDLE: 'Waitting...',
    MAPPING: 'Mapping...',
    ESCAPING: 'Escaping...'
    }

# Some function utils

class Task:
    name = None
    ID = None

    def __init__(self, task_id):
        self.name = task_desc[task_id]
        self.ID = task_id

class Master():

    distance = None
    voltage = None
    left_sensor_value =  None
    right_sensor_value = None
    left_sensor_string = None
    right_sensor_string = None

    mapping_flag = None
    mapping_done = None

    path = None
    tasks_pile = None

    def __init__(self):
        self.tasks_pile = []
        self.add_task(Task(IDLE))
        self.mapping_flag = False
        self.mapping_done = False
        self.path = []

    def add_task(self, task):
        self.tasks_pile.append(task)

    def remove_task(self, task_index):
        if len(self.tasks_pile)> 1:
            self.tasks_pile.pop(task_index)

    def get_current_task(self):
        return self.tasks_pile[-1]

    def task_assigner(self):

        current_task = self.get_current_task()

        # First checks if mapping flag is up
        if self.mapping_flag == True:

            # Adds mapping routine
            if current_task.ID == IDLE:
                self.add_task(Task(MAPPING))

        elif self.mapping_done == True:
            if current_task.ID == IDLE:
                self.add_task(Task(ESCAPING))

    def task_solver(self):

        current_task = self.get_current_task()

        if current_task.ID == IDLE:
            bw.board.Set_Led(1,1)
            tm.sleep(0.4)
            bw.board.Set_Led(1,0)
            tm.sleep(0.4)
            print('idle')

        elif current_task.ID == MAPPING:
            bw.board.Set_Led(2,1)
            tm.sleep(0.2)
            bw.board.Set_Led(2,0)
            tm.sleep(0.2)
            print('mapping')

    def run(self):

        self.task_assigner()
        self.task_solver()
