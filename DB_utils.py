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
    if cmd == "login":
        cmd =   """
            select * 
            from Users u
            join user_role r on u.User_id = r.User_id
            where u.User_id = %s;
            """
        cur.execute(cmd, [1])

        for tup in cur.fetchall():
            print(f'fetch: {tup}')



# ============================= System function =============================
def db_register_user(username, pwd, email):
    # print(f'db_register_user | ')
    cmd =   """
            insert into Users (User_name, Password, Email) values (%s, %s, %s)
            RETURNING User_id;
            """
    cur.execute(cmd, [username, pwd, email])
    userid = cur.fetchone()[0]
    # print(f'Generate userid: {userid}')

    cmd =   """
            insert into User_Role (User_id, Role) VALUES (%s, 'User');
            """
    cur.execute(cmd, [userid])
    db.commit()


    return userid

def fetch_user(userid): 
    cmd =   """
            select * 
            from Users u
            join user_role r on u.User_id = r.User_id
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
            userid, username, pwd, email, userid, role = row  #TODO: remove second userid
            
            if role == 'User':
                isUser = True
            elif role == 'Admin':
                isAdmin = True

    return username, pwd, email, isUser, isAdmin

def username_exist(username):
    # print(f'username_exist | Enter')
    cmd =   """
            select count(*) 
            from Users
            where User_name = %s;
            """
    cur.execute(cmd, [username])
    # print(f'username_exist | After exec')


    count = cur.fetchone()[0]
    # print(f'username_exist | Get count: {count}')
    return count > 0
    
def userid_exist(userid):
    cmd =   """
            select count(*) 
            from Users
            where User_id = %s;
            """
    cur.execute(cmd, [userid])
    count = cur.fetchone()[0]
    # print(f'username_exist | Get count: {count}')
    return count > 0


# ============================= function for User =============================
def update_user_info(userid, item, new_value):
    cmd =  f"""
            update Users
            set {item} = %s
            where User_id = %s;
            """
    print(f'Update User Info | {userid}: {item}->{new_value}')
    # print(cur.mogrify(cmd, [item, new_value, userid]))
    cur.execute(cmd, [new_value, userid])
    print(f'After update')
    db.commit()
    return

def create_study_group(content, user_max, course_id, user_id, 
                       event_date, event_period_start, event_duration, classroom_id):

    cmd =   """
            Insert Into STUDY_EVENT (Content, Status, User_max, Course_id, User_id)
            Values (%s, 'Ongoing', %s, %s, %s);
            Set @newID = last_insert_id();
            Insert Into STUDY_EVENT_PERIOD (Event_date, Event_period, Classroom_id, Event_id)
            Values (%s, %s, %s, @newID);
            """
    pass # TODO
    print(cmd)

    # for hour in range(event_duration):
    #     cur.execute(cmd, [content, user_max, course_id, user_id, 
    #                       event_date, event_period_start + hour, classroom_id])

    # db.commit()
    
def list_available_study_group():
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
    return # TODO
    cur.execute(cmd)
    
    # TODO: return or send fetch result 
    pass


def leave_study_group(cur, event_id, user_id):
    cmd =   """
            Delete From PARTICIPATION
            Where Event_id = %s And User_id = %s;
            """
    return # TODO
    cur.execute(cmd, [event_id, user_id])
    db.commit()
    
def list_history(cur, user_id):
    cmd =   """
            Select se.*
            From PARTICIPATION As p
            Join STUDY_EVENT As se On p.Event_id = se.Event_id
            Where p.User_id = %s;
            """
    return # TODO
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
    return # TODO
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
    return # TODO
    cur.execute(cmd, [event_date])
    # TODO: return or send fetch result 
    pass



# ============================= function for Admin =============================
def append_classroom(cur, building_name, capacity_size, floor_number, room_name):
    cmd =   """
            Insert Into CLASSROOM(%s, %s, %s, %s)
            Values ('共同', 120, 3, '312');
            """
    return # TODO
    cur.execute(cmd, [building_name, capacity_size, floor_number, room_name])
    db.commit()

def remove_classroom(cur, classroom_id):
    cmd =   """
            Delete From CLASSROOM
            Where Classroom_id = %s;
            """
    return # TODO
    cur.execute(cmd, [classroom_id])
    db.commit()

def update_classroom(cur, classroom_id, capacity_size):
    cmd =   """
            Update CLASSROOM
            Set Capacity_size = %s
            Where Classroom_id = %s;
            """
    return # TODO
    cur.execute(cmd, [classroom_id, capacity_size])
    db.commit()

def list_classroom(cur, building_name):
    cmd =   """
            Select *
            From CLASSROOM
            Where Building_name = %s;
            """
    return # TODO
    cur.execute(cmd, [building_name])
    db.commit()

def list_user_info(cur, user_id):
    cmd =   """
            Select *
            From USER
            Where User_id = %s;
            """
    return # TODO
    cur.execute(cmd, [user_id])

def list_course_info(cur, course_name):
    cmd =   """
            Select se.*
            From STUDY_EVENT As se
            Join COURSE As c On se.Course_id = c.Course_id
            Where c.Course_name = %s;
            """
    
    return # TODO
    cur.execute(cmd, [course_name])


