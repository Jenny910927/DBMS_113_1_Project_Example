import sys
import psycopg2
from tabulate import tabulate
from threading import Lock

DB_NAME = "STUDY_GROUP_2"
DB_USER = "DBTA"
DB_HOST = "127.0.0.1"
DB_PORT = 5432

cur = None
db = None
create_event_lock = Lock()

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
        # fetch_data(cur, "test")
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
        cur.execute('select count(*) from "USER";')

        for tup in cur.fetchall():
            print(f'fetch: {tup}')
    if cmd == "login":
        cmd =   """
            select * 
            from "USER" u
            join user_role r on u.User_id = r.User_id
            where u.User_id = %s;
            """
        cur.execute(cmd, [1])

        for tup in cur.fetchall():
            print(f'fetch: {tup}')


def print_table(cur):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    return tabulate(rows, headers=columns, tablefmt="github")


# ============================= System function =============================
def db_register_user(username, pwd, email):
    # print(f'db_register_user | ')
    cmd =   """
            insert into "USER" (User_name, Password, Email) values (%s, %s, %s)
            RETURNING User_id;
            """
    cur.execute(cmd, [username, pwd, email])
    userid = cur.fetchone()[0]
    # print(f'Generate userid: {userid}')

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
    
    # print(f'username_exist | Enter')
    cmd =   """
            select count(*) from "USER"
            where User_name = %s;
            """
    print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [username])

    # print(f'username_exist | After exec')


    count = cur.fetchone()[0]
    # print(f'username_exist | Get count: {count}')
    return count > 0
    
def userid_exist(userid):
    cmd =   """
            select count(*) 
            from "USER"
            where User_id = %s;
            """
    cur.execute(cmd, [userid])
    count = cur.fetchone()[0]
    # print(f'username_exist | Get count: {count}')
    return count > 0



# ============================= function for User =============================
def update_user_info(userid, item, new_value):
    cmd =  f"""
            update "USER"
            set {item} = %s
            where User_id = %s;
            """
    print(f'Update User Info | {userid}: {item}->{new_value}')
    # print(cur.mogrify(cmd, [item, new_value, userid]))
    cur.execute(cmd, [new_value, userid])
    print(f'After update')
    db.commit()
    return

def check_available(event_date, event_period_start, event_duration, classroom_id):
    pass #TODO

def create_study_group(content, user_max, course_id, user_id, 
                       event_date, event_period_start, event_duration, classroom_id):
    
    create_event_lock.acquire()

    query = "select Create_Study_Group(%s, %s, %s, %s, %s, %s, %s, %s);"
    cur.execute(query, [content, user_max, course_id, user_id, 
                       event_date, event_period_start, event_duration, classroom_id])
    # cmd =   """
    #         Insert Into STUDY_EVENT (Content, Status, User_max, Course_id, Owner_id)
    #         Values (%s, 'Ongoing', %s, %s, %s);
    #         Set @newID = last_insert_id();
    #         Insert Into STUDY_EVENT_PERIOD (Event_date, Event_period, Classroom_id, Event_id)
    #         Values (%s, %s, %s, @newID);
    #         """
    # # print(cmd)

    # for hour in range(event_duration):
    #     cur.execute(cmd, [content, user_max, course_id, user_id, 
    #                       event_date, event_period_start + hour, classroom_id])

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
            Select se.*
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
    
    if instructor_name != "None" and course_name != "None":
        query = query + f"Instructor_name Like '%{instructor_name}%' And Course_name Like '%{course_name}%';"
    elif instructor_name != "None":
       query = query + f"Instructor_name Like '%{instructor_name}%';" 
    elif course_name != "None":
       query = query + f"Course_name Like '%{course_name}%';" 
    else:
        return "Instructor_name and Course_name cannot be both empty."
    
    print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)


def find_reserved_room_on_date(event_date):
    query =   """
            Select c.Room_name, sep.Event_period
            From "STUDY_EVENT_PERIOD" As sep
            Join "CLASSROOM" As c On sep.Classroom_id = c.Classroom_id
            Where sep.Event_date = %s;
            """
    print(cur.mogrify(query, [event_date]))
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
    classrooom_id = cur.fetchone()[0]
    db.commit()
    return classrooom_id

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
    
    print(cur.mogrify(query))
    cur.execute(query)

    return print_table(cur)

def list_user_info(cur, user_id):
    cmd =   """
            Select *
            From "USER"
            Where User_id = %s;
            """
    return # TODO
    cur.execute(cmd, [user_id])

def list_course_info(cur, course_name):
    cmd =   """
            Select se.*
            From "STUDY_EVENT" As se
            Join "COURSE" As c On se.Course_id = c.Course_id
            Where c.Course_name = %s;
            """
    
    return # TODO
    cur.execute(cmd, [course_name])


