from ..Action import Action
from DB_utils import append_classroom
from tabulate import tabulate
import pandas as pd

class UploadCourses(Action):
    def exec(self, conn):
        file_size = self.read_input(conn, "[CSV]csv filename")
       
        if file_size == "[NOTFOUND]":
            print(f'File not found')
            return

        file_size = int(file_size)
        print(f'file_size = {file_size}')
        conn.send("Ready to receive the file.".encode('utf-8'))

        data = b""
        while len(data) < file_size:
            packet = conn.recv(1024)
            if not packet:
                break
            data += packet
        
        # csv_data = io.BytesIO(data)

        with open('receive_course.csv', 'wb') as f:
                f.write(data)
        
        print("Finish receive csv file.")

        df_csv = pd.read_csv('receive_course.csv', encoding='Big5')
        print(f'Finish read csv to df')
        # print(df_csv)


        df_csv = df_csv.loc[:, ["流水號", "課程名稱", "授課教師", "授課對象", "時間"]]

        print(tabulate(df_csv, headers = 'keys', tablefmt = 'psql'))


        # classrooom_id = append_classroom(building_name, capacity_size, floor_number, room_name)

        # conn.send(f'\nCreate new classroom successfully! New Classrooom_id: {classrooom_id}\n'.encode('utf-8'))