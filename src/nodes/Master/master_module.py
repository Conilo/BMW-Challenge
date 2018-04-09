import rospy
import bmw_wrap as bw
import time as tm

# System's states definitions
IDLE = 0
MAPPING = 1
ESCAPING = 2

# Task names descriptions
task_desc = {
    IDLE: 'Waitting...',
    MAPPING: 'Mapping...',
    ESCAPING: 'Escaping...'
    }

# Classes definitions
class Task:
    """
    This class keeps the task's desc. info.
    """
    name = None
    ID = None

    def __init__(self, task_id):
        self.name = task_desc[task_id]
        self.ID = task_id

class Master():
    """
    This class contains all the master's node
    methods and attrivutes.
    """

    """
    The distance value read from the 
    ultrasonic sensor.
    """
    distance = None
    
    """
    The distance value read from the 
    ultrasonic sensor.
    """
    voltage = None
    
    """
    The distance value read from the 
    ultrasonic sensor.
    """
    left_sensor_value =  None
    
    """
    Right light sensor value read.
    """
    right_sensor_value = None
    
    """
    Left light sensor value read.
    """
    left_sensor_string = None
    
    """
    Right light sensor string read.
    """
    right_sensor_string = None

    """
    Left light sensor string read.
    """
    mapping_flag = None
    
    """
    Flag that indicates when the mapping
    process is done.
    """
    mapping_done = None

    """
    List that contains the path to be 
    followed.
    """
    path = None
    
    """
    List that contains the tasks to 
    to be executed by the system.
    """
    tasks_pile = None

    def __init__(self):
        self.tasks_pile = []
        self.add_task(Task(IDLE))
        self.mapping_flag = False
        self.mapping_done = False
        self.path = []

    def add_task(self, task):
        """
        This function adds a new task to the
        pile.
        """
        self.tasks_pile.append(task)

    def remove_task(self, task_index):
        """
        This function removes the last task
        on the pile.
        """
        if len(self.tasks_pile)> 1:
            self.tasks_pile.pop(task_index)

    def get_current_task(self):
        """
        This function gets the task that is
        currently being executed.
        """
        return self.tasks_pile[-1]

    def task_assigner(self):
        """
        This function checks the system's status
        and adds tasks depending.
        """
        current_task = self.get_current_task()

        # First checks if mapping flag is up
        if (self.mapping_flag == True and 
           current_task.ID == IDLE):

            # Adds mapping routine to tasks pile
            self.add_task(Task(MAPPING))
                
        # Then cheks is mapping is done
        elif (self.mapping_done == True and 
             current_task.ID == IDLE):
            
            # Adds escaping routine
            self.add_task(Task(ESCAPING))
                
        # Iddle mode    
        else:
            pass

    def task_solver(self):
        """
        This function executes the current task, 
        which is the task on the pile's top.
        """
        # Get current task
        current_task = self.get_current_task()

        # Depending on the current task, execute diferent commands.
        if current_task.ID == IDLE:
            
            # Make led 1 blink, indicating idle state.
            bw.board.Set_Led(1,1)
            tm.sleep(0.4)
            bw.board.Set_Led(1,0)
            tm.sleep(0.4)
            print('idle')

        elif current_task.ID == MAPPING:
            
            # Make led 2 blink, idicating mapping state.
            bw.board.Set_Led(2,1)
            
            # Call line following routine
            self.line_following(
                self.left_sensor_string,
                self.right_sensor_string)
            
            bw.board.Set_Led(2,0)
            
        elif current_task.ID == ESCAPPING:
            
            # Make led 3 blink, idicating escaping state.
            bw.board.Set_Led(3,1)
            
            # Call line following routine
            self.line_following(
                self.left_sensor_string,
                self.right_sensor_string)
            
            bw.board.Set_Led(2,0)
            

    def run(self):
        """
        This function executes the task solver and
        assigner.
        """

        self.task_assigner()
        self.task_solver()

    def line_following(self,
                       left_sensor,
                       right_sensor):
        """
        This function takes care of the line following 
        and turns execution.
        """

        # Same color read case
        if left_sensor ==  right_sensor:

            color =  left_sensor

            # Line centered case
            if color == 'white':
                
                bw.set_motors_speeds(-100,100)

            # Intsersection case
            elif color == 'black':

                # Execute path instruction
                if len(self.path)>0:
                    execute_move(self.path[0])
                    
                # Path empty, finished trajectory
                else:
                    self.mapping_done = False

        else:

            # Car loaded to left side
            if left_sensor == 'white' :

                # Move to left
                bw.set_motors_speeds(-100,65)

            # Car loaded to right side
            elif right_sensor ==  'white':

                # Move to left
                bw.set_motors_speeds(-65,100)
