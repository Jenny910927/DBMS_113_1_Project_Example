import sys
import psycopg2
from tabulate import tabulate
from threading import Lock

DB_NAME = "I'M_IN"
DB_USER = "dbta"
DB_HOST = "127.0.0.1"
DB_PORT = 5432

cur = None
db = None
create_event_lock = Lock()

def db_connect():
    exit_code = 0
    try:
        global db
        db = psycopg2.connect(database=DB_NAME, user=DB_USER, password='1234', 
                              host=DB_HOST, port=DB_PORT)
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
    
def print_table(cur):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    return tabulate(rows, headers=columns, tablefmt="github")

# ============================= System function =============================
def db_register_user(username, pwd, email):
    cmd =   """
            insert into "USER" (User_name, Password, Email) values (%s, %s, %s)
            RETURNING User_id;
            """
    cur.execute(cmd, [username, pwd, email])
    userid = cur.fetchone()[0]

    cmd =   """
            insert into "USER_ROLE" (User_id, Role) VALUES (%s, 'User');
            """
    cur.execute(cmd, [userid])
    db.commit()


    return userid

def fetch_user(userid): 
    cmd =   """
            select * 
            from "USER" u
            join "USER_ROLE" r on u.User_id = r.User_id
            where u.User_id = %s;
            """
    cur.execute(cmd, [userid])

    rows = cur.fetchall()
    if not rows:
        return None, None, None, None, None
    else:
        isUser = False
        isAdmin = False
        for row in rows:
            userid, username, pwd, email, userid, role = row
            
            if role == 'User':
                isUser = True
            elif role == 'Admin':
                isAdmin = True

    return username, pwd, email, isUser, isAdmin

def username_exist(username):
    
    cmd =   """
            select count(*) from "USER"
            where User_name = %s;
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [username])


    count = cur.fetchone()[0]
    return count > 0
    
def userid_exist(userid):
    cmd =   """
            select count(*) 
            from "USER"
            where User_id = %s;
            """
    cur.execute(cmd, [userid])
    count = cur.fetchone()[0]
    return count > 0



# ============================= function for User =============================
def update_user_info(userid, item, new_value):
    cmd =  f"""
            update "USER"
            set {item} = %s
            where User_id = %s;
            """
    print(f'Update User Info | {userid}: {item}->{new_value}')
    cur.execute(cmd, [new_value, userid])
    print(f'After update')
    db.commit()
    return

def isReserved(event_date, event_period_start, event_duration, classroom_id):
    query = f"""
            Select
            Case
                When Exists
                (
                    Select *
                    From "STUDY_EVENT_PERIOD" As sep
                    Where sep.Classroom_id = %s
                    And sep.Event_date = %s
                    And sep.Event_period >= %s
                    And sep.Event_period <= %s
                )
                Then 1
                Else 0
            End
            """

    # print(cur.mogrify(query, [classroom_id, event_date, event_period_start, int(event_period_start)+int(event_duration)]))
    cur.execute(query, [classroom_id, event_date, event_period_start, int(event_period_start)+int(event_duration)])
    return cur.fetchone()[0] > 0

def create_study_group(content, user_max, course_id, user_id, 
                       event_date, event_period_start, event_duration, classroom_id):
    
    create_event_lock.acquire()

    if isReserved(event_date, event_period_start, event_duration, classroom_id):
        return -1
    
    print("Is Available!!!")

    query = "select Create_Study_Group(%s, %s, %s, %s, %s, %s, %s, %s);"
    # print(cur.mogrify(query, [content, user_max, course_id, user_id, 
    #                    event_date, event_period_start, event_duration, classroom_id]))
    cur.execute(query, [content, user_max, course_id, user_id, 
                       event_date, event_period_start, event_duration, classroom_id])

    event_id = cur.fetchone()[0]
    db.commit()

    create_event_lock.release()

    return event_id


def list_available_study_group() -> str:
    query = """
            Select se.*
            From "STUDY_EVENT" As se
            Left Join "PARTICIPATION" As p On se.Event_id = p.Event_id
            Where se.Status = 'Ongoing'
            Group By se.Event_id
            Having Count(p.User_id) < (
                Select User_max
                From "STUDY_EVENT" AS se2
                Where se.Event_id = se2.Event_id
            );
            """
    
    cur.execute(query)

    return print_table(cur)

def join_study_group(user_id, event_id, join_time):
    query = """
            Insert Into "PARTICIPATION" (User_id, Event_id, Join_Time)
            Values (%s, %s, %s);
            """
    cur.execute(query, [user_id, event_id, join_time])
    db.commit()
    return
    
def isInEvent(user_id, event_id):
    query = """
            Select count(*)
            From "PARTICIPATION"
            Where Event_id = %s And User_id = %s;
            """
    cur.execute(query, [event_id, user_id])
    return cur.fetchone()[0] > 0


def leave_study_group(user_id, event_id):
    query = """
            Delete From "PARTICIPATION"
            Where Event_id = %s And User_id = %s;
            """
    cur.execute(query, [event_id, user_id])
    db.commit()
    
def list_history(user_id):
    query = """
            Select *
            From "PARTICIPATION" As p
            Join "STUDY_EVENT" As se On p.Event_id = se.Event_id
            Where p.User_id = %s;
            """
    cur.execute(query, [user_id])

    return print_table(cur)


def find_course(instructor_name, course_name):
    
    query = f"""
            Select *
            From "COURSE"
            Where 
            """
    count = 0
    if instructor_name != "None":
        count += 1
        query += f"Instructor_name Like '%{instructor_name}%'"
    if course_name != "None":
        if count > 0:
            query += ' And '
        count += 1
        query += f"Course_name Like '%{course_name}%'"
    query += ';'
        
    if count == 0: # All argument is "None" (No keyword for search)
        return "Instructor_name and Course_name cannot be both empty."
    
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)


def find_reserved_room_on_date(event_date):
    query =   """
            Select c.Room_name, sep.Event_period
            From "STUDY_EVENT_PERIOD" As sep
            Join "CLASSROOM" As c On sep.Classroom_id = c.Classroom_id
            Where sep.Event_date = %s;
            """
    # print(cur.mogrify(query, [event_date]))
    cur.execute(query, [event_date])
    return print_table(cur)



# ============================= function for Admin =============================
def append_classroom(building_name, capacity_size, floor_number, room_name):
    query = """
            Insert Into "CLASSROOM" (Building_name, Capacity_size, Floor_number, Room_name)
            Values (%s, %s, %s, %s)
            RETURNING Classroom_id;
            """
    
    # print(cur.mogrify(query, [building_name, capacity_size, floor_number, room_name]))
    cur.execute(query, [building_name, capacity_size, floor_number, room_name])
    classroom_id = cur.fetchone()[0]
    db.commit()
    return classroom_id

def classroom_exist(classroom_id):
    query = """
            Select count(*)
            From "CLASSROOM"
            Where Classroom_id = %s;
            """
    cur.execute(query, [classroom_id])
    return cur.fetchone()[0] > 0

def remove_classroom(classroom_id):
    query = """
            Delete From "CLASSROOM"
            Where Classroom_id = %s;
            """
    
    cur.execute(query, [classroom_id])
    db.commit()

def update_classroom(classroom_id, item, new_value):
    query = f"""
            Update "CLASSROOM"
            Set {item} = %s
            Where Classroom_id = %s;
            """
    
    cur.execute(query, [new_value, classroom_id])
    db.commit()

def search_classroom(building_name, capacity_size, floor_number, room_name):
    query =   """
            Select *
            From "CLASSROOM"
            Where 
            """
    count = 0
    if building_name != "None":
        count += 1
        query += f"Building_name Like '%{building_name}%'"
    if capacity_size != "None":
        if count > 0:
            query += ' And '
        count += 1
        query += f"Capacity_size = {capacity_size}"
    if floor_number != "None":
        if count > 0:
            query += ' And '
        count += 1
        query += f"Floor_number = {floor_number}"
    if room_name != "None":
        if count > 0:
            query += ' And '
        count += 1
        query += f"Room_name Like '%{room_name}%'"
    query += ';'
        
    if count == 0: # All argument is "None" (No keyword for search)
        return "Search column cannot be all empty."
    
    # print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)

def append_course(course_name, instructor_name, department_name, lecture_time, commit=True):
    query = """
            Insert Into "COURSE" (Course_name, Instructor_name, Department_name, Lecture_time)
            Values (%s, %s, %s, %s)
            RETURNING Course_id;
            """
    
    # print(cur.mogrify(query, [course_name, instructor_name, department_name, lecture_time]))
    cur.execute(query, [course_name, instructor_name, department_name, lecture_time])
    print(f'After exec')
    course_id = cur.fetchone()[0]
    if commit:
        db.commit()
    return course_id

def upload_courses(df):
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    try:
        for idx, row in df.iterrows():
            append_course(row["課程名稱"], row["授課教師"], row["授課對象"], row["時間"], commit=False)
        db.commit()
        return "Successfully append courses."
    
    except psycopg2.DatabaseError as error:
        print(f'psycopg2 db error')
        if db:
            db.rollback()
        return f"Database upload error. Rollback. Error: {error}"
        
    except Exception as error:
        print(f'Error: {error}. Rollback.')
        if db:
            db.rollback()
        return f"Rollback. Error: {error}"

def course_exist(course_id):
    query = """
            Select count(*)
            From "COURSE"
            Where Course_id = %s;
            """
    cur.execute(query, [course_id])
    return cur.fetchone()[0] > 0

def remove_course(course_id):
    query = """
            Delete From "COURSE"
            Where Course_id = %s;
            """
    
    cur.execute(query, [course_id])
    db.commit()

def update_course(course_id, item, new_value):
    query = f"""
            Update "COURSE"
            Set {item} = %s
            Where Course_id = %s;
            """
    
    cur.execute(query, [new_value, course_id])
    db.commit()


def list_user_info(user_id):
    cmd =   """
            Select *
            From "USER"
            Where User_id = %s;
            """
    cur.execute(cmd, [user_id])
    return print_table(cur)


def search_study_event(course_name):
    query = f"""
            Select *
            From "STUDY_EVENT" As se
            Join "COURSE" As c On se.Course_id = c.Course_id
            Where c.Course_name Like '%{course_name}%';
            """
    
    cur.execute(query)

    return print_table(cur)
