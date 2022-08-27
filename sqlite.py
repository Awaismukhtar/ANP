import sqlite3


class SqlLite:
    def Connect(self):
        conn = sqlite3.connect('database.db')
        print("Opened database successfully")
        return conn

    def CreateUserTable(self):
        conn = self.Connect()
        conn.execute(
            'CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, password TEXT)')
        print("Table created successfully")
        conn.close()

    def CreateVehicleTable(self):
        conn = self.Connect()
        conn.execute('CREATE TABLE IF NOT EXISTS VehicleInfo (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT NOT NULL, age INT NOT NULL, address CHAR(50) NOT NULL, car_car_model VARCHAR(50) NOT NULL, license_no VARCHAR(50)  NOT NULL)')
        print("VehicleInfo table created")
        # ADD DATA OR RECORD IN TABLE
        conn.execute("INSERT or IGNORE INTO VehicleInfo (name,age,address,car_model,license_no) \
                    VALUES ('Paul', 32, 'California','GLI','BARBUS' )")
        conn.execute("INSERT or IGNORE INTO VehicleInfo (name,age,address,car_model,license_no) \
                    VALUES ('Mark', 25, 'Rich-Mond ','MEHRAN','HR26BR9044')")
        conn.execute("INSERT or IGNORE INTO VehicleInfo (name,age,address,car_model,license_no) \
                    VALUES ('lark', 65, 'domb-rich ','CIVIC','BJY98Z')")
        conn.execute("INSERT or IGNORE INTO VehicleInfo (name,age,address,car_model,license_no) \
                    VALUES ('ENGLAND', 55, 'MARRY ','COROLLA','COVid19')")
        conn.execute("INSERT or IGNORE INTO VehicleInfo (name,age,address,car_model,license_no) \
                    VALUES ('UK', 30, 'CHARLIE ','WAGONR','H982FKL')")
        conn.commit()
        print("Records in VehicleInfo created successfully")
        #  DISPLAY ALL THE RECORDS IN DATABASE
        cursor = conn.execute(
            "SELECT id, name, address, car_model, license_no from VehicleInfo")
        # for row in cursor:
        #     print("id = ", row[0])
        #     print("name = ", row[1])
        #     print("address = ", row[2])
        #     print("car_model = ", row[3])
        #     print("license_no = ", row[4]), "\n"
        #     print("Operation done successfully")
        conn.close()
