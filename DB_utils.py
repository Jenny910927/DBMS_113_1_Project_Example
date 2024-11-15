import sys
import psycopg2


DB_NAME = "STUDY_GROUP"
DB_USER = "DBTA"
DB_HOST = "127.0.0.1"
DB_PORT = 5432

cur = None
db = None

def db_connect():
    exit_code = 0
    # db = None
    try:
        global db
        db = psycopg2.connect(database=DB_NAME, user=DB_USER, password='1234', 
                              host=DB_HOST, port=DB_PORT)
        # exit_code = main(db)
        print("Successfully connect to DBMS.")
        global cur
        cur = db.cursor()
        return db
        
    except psycopg2.Error as err:
        print("DB error: ", err)
        exit_code = 1
    except Exception as err:
        print("Internal Error: ", err)
        raise err
    # finally:
    #     if db is not None:
    #         db.close()
    sys.exit(exit_code)
    

def fetch_data(cur, cmd):
    if cmd == "test":
        cur.execute('select * from test;')

        for tup in cur.fetchall():
            print(f'fetch: {tup}')



# ============================= System function =============================
def db_register_user(userid, username, pwd, email):
    # TODO
    pass

def fetch_user(userid): 
    # TODO: fetch user info

    return "Jenny", "1234", "jenny@gmail.com", "User"

    # TODO: check user is User or Admin
    pass

# ============================= function for User =============================
def create_study_group(cur, content, user_max, course_id, user_id, 
                       event_date, event_period_start, event_duration, classroom_id):

    cmd =   """
            Insert Into STUDY_EVENT (Content, Status, User_max, Course_id, User_id)
            Values (%s, 'Ongoing', %s, %s, %s);
            Set @newID = last_insert_id();
            Insert Into STUDY_EVENT_PERIOD (Event_date, Event_period, Classroom_id, Event_id)
            Values (%s, %s, %s, @newID);
            """
    
    for hour in range(event_duration):
        cur.execute(cmd, [content, user_max, course_id, user_id, 
                          event_date, event_period_start + hour, classroom_id])
    
def list_available_study_group(cur):
    cmd =   """
            Select se.*
            From STUDY_EVENT As se
            Left Join PARTICIPATION As p On se.Event_id = p.Event_id
            Where se.Status = 'Ongoing'
            Group By se.Event_id
            Having Count(p.User_id) < (
                Select User_max
                From STUDY_EVENT AS se2
                Where se.Event_id = se2.Event_id
            );
            """
    cur.execute(cmd)
    
    # TODO: return or send fetch result 
    pass


def leave_study_group(cur, event_id, user_id):
    cmd =   """
            Delete From PARTICIPATION
            Where Event_id = %s And User_id = %s;
            """
    cur.execute(cmd, [event_id, user_id])
    
def list_history(cur, user_id):
    cmd =   """
            Select se.*
            From PARTICIPATION As p
            Join STUDY_EVENT As se On p.Event_id = se.Event_id
            Where p.User_id = %s;
            """
    cur.execute(cmd, [user_id])

    # TODO: return or send fetch result 
    pass


def find_course(cur, instructor_name, course_name):
    cmd =   """
            Select *
            From COURSE
            Where Instructor_name Like '%%s%'
            Or Course_name Like '%%s';
            """
    cur.execute(cmd, [instructor_name, course_name])

    # TODO: return or send fetch result 
    pass


def find_reserved_room_on_date(cur, event_date):
    cmd =   """
            Select c.Room_name, sep.Event_period
            From STUDY_EVENT_PERIOD As sep
            Join Classroom As c On sep.Classroom_id = c.Classroom_id
            Where sep.Event_date = '%s;
            """
    
    cur.execute(cmd, [event_date])
    # TODO: return or send fetch result 
    pass



# ============================= function for Admin =============================
def append_classroom(cur, building_name, capacity_size, floor_number, room_name):
    cmd =   """
            Insert Into CLASSROOM(%s, %s, %s, %s)
            Values ('共同', 120, 3, '312');
            """
    cur.execute(cmd, [building_name, capacity_size, floor_number, room_name])

def remove_classroom(cur, classroom_id):
    cmd =   """
            Delete From CLASSROOM
            Where Classroom_id = %s;
            """
    cur.execute(cmd, [classroom_id])

def update_classroom(cur, classroom_id, capacity_size):
    cmd =   """
            Update CLASSROOM
            Set Capacity_size = %s
            Where Classroom_id = %s;
            """
    cur.execute(cmd, [classroom_id, capacity_size])

def list_classroom(cur, building_name):
    cmd =   """
            Select *
            From CLASSROOM
            Where Building_name = %s;
            """
    cur.execute(cmd, [building_name])

def list_user_info(cur, user_id):
    cmd =   """
            Select *
            From USER
            Where User_id = %s;
            """
    cur.execute(cmd, [user_id])

def list_course_info(cur, course_name):
    cmd =   """
            Select se.*
            From STUDY_EVENT As se
            Join COURSE As c On se.Course_id = c.Course_id
            Where c.Course_name = %s;
            """
    cur.execute(cmd, [course_name])


