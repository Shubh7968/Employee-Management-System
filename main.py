import mysql.connector
import streamlit as st
import pandas as pd
import datetime

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shubham@79",
        database="employee"
        )

# ----------------- Session State -----------------
if 'employee_login' not in st.session_state:
    st.session_state['employee_login'] = False
    
if 'admin_login' not in st.session_state:
    st.session_state['admin_login'] = False
    
if 'employee_id' not in st.session_state:
    st.session_state['employee_id'] = None

if 'admin_id' not in st.session_state:
    st.session_state['admin_id'] = None
        
# ----------------- Streamlit Layout --------------

st.set_page_config(page_title="Employee Management System",page_icon="https://png.pngtree.com/png-vector/20210924/ourmid/pngtree-teamwork-flat-icon-png-image_3953902.png", layout="wide")
st.title("Employee Management System")

menu=st.sidebar.selectbox("Menu",("Home","Employee","Admin"))

# ----------------- Home --------------------------

if(menu=="Home"):
    st.write("This is an **Employee Management System** web application")
    st.image("https://5.imimg.com/data5/SELLER/Default/2022/9/KJ/ZA/CW/50406084/employee-transportation-500x500.png")
    st.markdown("""
    ### Features:
    - Employee Login → Profile, Attendance, Leave, Performance, Projects
    - Admin Login → Manage Employees, Attendance, Leaves, Performance, Projects
    """)

# ----------------- Employee Section --------------

elif(menu=="Employee"):
    st.header("Employee Login")
    emp_id = st.text_input("Enter Employee ID")
    emp_pwd = st.text_input("Enter Password",type="password")
    btn = st.button("Login as Employee")
    if btn:
        db = get_db()
        c = db.cursor()
        c.execute("select * from employee where emp_id=%s",(emp_id,))
        st.session_state['employee_id'] = emp_id
        for r in c:
            if(r[0]==emp_id and r[5]==emp_pwd):
                st.session_state['employee_login'] = True
                break
        if(not st.session_state['employee_login']):
            st.error("Incorrect Employee ID or Password!")
    if(st.session_state['employee_login']):
        st.status("Login Successful!")
        emp_choice = st.selectbox("Employee Features",("Profile","Mark Attendance","Apply Leave","View Performance","My Projects"))

        #------ Profile -------

        if emp_choice == "Profile":
            df = pd.read_sql("SELECT * FROM employee WHERE emp_id=%s", get_db(), params=(st.session_state['employee_id'],))
            st.dataframe(df)
            
        #------- Attendance------
            
        elif emp_choice == "Mark Attendance":
            today = datetime.date.today()
            status = st.selectbox("Status",["Present","Absent","Leave"])
            if st.button("Mark Attendance"):
                db = get_db()
                c = db.cursor()
                c.execute("insert into attendance values (%s,%s,%s)",
                          (st.session_state['employee_id'],today,status))
                db.commit()
                st.success("Attendance marked successfully.")
                
        #------- Apply for Leave -------

        elif emp_choice == "Apply Leave":
            start = st.date_input("Start Date")
            end = st.date_input("End Date")
            reason = st.text_area("Reason for Leave")
            if st.button("Apply Leave"):
                db = get_db()
                c = db.cursor()
                c.execute("INSERT INTO request (emp_id, start_date, end_date, reason) VALUES (%s,%s,%s,%s)",
                          (st.session_state['employee_id'], start, end, reason))
                db.commit()
                st.success("Leave request submitted successfully.")

        # ----- View Performance -------
        
        elif emp_choice == "View Performance":
            df = pd.read_sql("SELECT review_period, score, feedback FROM performance WHERE emp_id=%s", 
                             get_db(), params=(st.session_state['employee_id'],))
            if df.empty:
                st.info("No performance records found.")
            else:
                st.dataframe(df)

        # ----- View Projects -------
        
        elif emp_choice == "My Projects":
            df = pd.read_sql("""
                SELECT p.project_id, p.project_name, p.description, p.start_date, p.end_date, p.status, pa.role
                FROM projects p
                JOIN project_assignments pa ON p.project_id = pa.project_id
                WHERE pa.emp_id=%s
            """, get_db(), params=(st.session_state['employee_id'],))
            if df.empty:
                st.info("You are not assigned to any projects.")
            else:
                st.dataframe(df)
                
# ------- Admin Section ---------

elif menu == "Admin":
    st.header("Admin Login")

    adm_id = st.text_input("Enter Admin ID")
    adm_pwd = st.text_input("Enter your password", type="password")
    btn2 = st.button("Login as Admin")

    if btn2:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM admins WHERE admin_id=%s", (adm_id,))
        row = c.fetchone()

        if row and row[0] == adm_id and row[1] == adm_pwd:
            st.session_state['admin_login'] = True
            st.session_state['admin_id'] = adm_id
        else:
            st.error("Incorrect Admin ID or Password!")

    if st.session_state['admin_login']:
        st.success("Login Successful!")
        admin_choice = st.selectbox("Admin Features",(
            "None","Manage Employees","Manage Attendance","Manage Leaves",
            "Performance Management","Project Management"
            ))
        db = get_db()
        c = db.cursor()

        #----------- Employee -----------

        if admin_choice == "Manage Employees":
            emp_action = st.selectbox("Action",("View All","Add","Update","Delete"))

            if emp_action == "View all":
                df = pd.read_sql("select * from employee", db)
                st.dataframe(df)

            elif emp_action == "Add":
                eid = st.text_input("Employee ID to Add")
                ename = st.text_input("Name")
                dept = st.text_input("Department")
                desig = st.text_input("Designation")
                sal = st.number_input("Salary", 0)
                pwd = st.text_input("Enter Password",type="password")
                if st.button("Add Employee"):
                    c.execute("insert into employee values (%s,%s,%s,%s,%s,%s)",(eid,ename,dept,desig,sal,pwd))
                    db.commit()
                    st.success("Employee added Successfully.")

            elif emp_action == "Update":
                eid = st.text_input("Employee ID to Update")
                ename = st.text_input("Name")
                dept = st.text_input("Department")
                desig = st.text_input("Designation")
                sal = st.number_input("Salary", 0)
                pwd = st.text_input("Enter Password",type="password")
                if st.button("Update Employee"):
                    c.execute("update employee set emp_name=%s, department=%s, designation=%s, salary=%s, emp_pwd=%s where emp_id=%s",
                              (eid,ename,dept,desig,sal,pwd))
                    db.commit()
                    st.success("Employee updated Successfully.")

            elif emp_action == "Delete":
                eid = st.text_input("Employee ID to Delete")
                if st.button("Delete Employee"):
                    c.execute("delete from employee where emp_id=%s",(eid,))
                    db.commit()
                    st.success("Employee deleted Successfully.")

        # ---------- Attendance ------------            

        elif(admin_choice == "Manage Attendance"):
            df = pd.read_sql("select * from attendance",db)
            st.dataframe(df)

        # ------------ Leaves ----------------

        elif admin_choice == "Manage Leaves":
            df = pd.read_sql("SELECT * FROM request", db)
            st.dataframe(df)
            leave_id = st.text_input("Enter Employee ID for leave update")
            start = st.date_input("Start Date for leave")
            end = st.date_input("End Date for leave")
            status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
            if st.button("Update Leave Status"):
                c.execute("UPDATE request SET status=%s WHERE emp_id=%s AND start_date=%s AND end_date=%s",
                          (status, leave_id, start, end))
                db.commit()
                st.success("Leave status updated")

        # ---------- Performance --------------

        
        elif admin_choice == "Performance Management":
            perf_action = st.selectbox("Action", ("View All", "Add/Update", "Delete"))
            if perf_action == "View All":
                df = pd.read_sql("SELECT * FROM performance", db)
                st.dataframe(df)
            elif perf_action == "Add/Update":
                eid = st.text_input("Employee ID")
                period = st.text_input("Review Period")
                score = st.number_input("Score", 1, 10)
                feedback = st.text_area("Feedback")
                if st.button("Add/Update Performance"):
                    c.execute("""
                        INSERT INTO performance (emp_id, review_period, score, feedback)
                        VALUES (%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE score=%s, feedback=%s
                    """, (eid, period, score, feedback, score, feedback))
                    db.commit()
                    st.success("Performance record added/updated")
            elif perf_action == "Delete":
                eid = st.text_input("Employee ID to Delete Performance")
                period = st.text_input("Review Period")
                if st.button("Delete Performance"):
                    c.execute("DELETE FROM performance WHERE emp_id=%s AND review_period=%s", (eid, period))
                    db.commit()
                    st.success("Performance record deleted")

        # ------------- Project Management ---------------

        elif admin_choice == "Project Management":
            proj_action = st.selectbox("Action", ("View Projects", "Add Project", "Update Project", "Delete Project", "Assign Employee"))
            if proj_action == "View Projects":
                df = pd.read_sql("SELECT * FROM projects", db)
                st.dataframe(df)
            elif proj_action == "Add Project":
                pid = st.text_input("Project ID")
                pname = st.text_input("Project Name")
                desc = st.text_area("Description")
                start = st.date_input("Start Date")
                end = st.date_input("End Date")
                status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
                if st.button("Add Project"):
                    c.execute("INSERT INTO projects VALUES (%s,%s,%s,%s,%s,%s)", (pid,pname,desc,start,end,status))
                    db.commit()
                    st.success("Project added successfully")
            elif proj_action == "Update Project":
                pid = st.text_input("Project ID to Update")
                pname = st.text_input("New Project Name")
                desc = st.text_area("New Description")
                start = st.date_input("New Start Date")
                end = st.date_input("New End Date")
                status = st.selectbox("New Status", ["Not Started", "In Progress", "Completed"])
                if st.button("Update Project"):
                    c.execute("UPDATE projects SET project_name=%s, description=%s, start_date=%s, end_date=%s, status=%s WHERE project_id=%s",
                              (pname, desc, start, end, status, pid))
                    db.commit()
                    st.success("Project updated successfully")
            elif proj_action == "Delete Project":
                pid = st.text_input("Project ID to Delete")
                if st.button("Delete Project"):
                    c.execute("DELETE FROM projects WHERE project_id=%s", (pid,))
                    db.commit()
                    st.success("Project deleted successfully")
            elif proj_action == "Assign Employee":
                df = pd.read_sql("select * from project_assignments",db)
                st.dataframe(df)
                eid = st.text_input("Employee ID")
                pid = st.text_input("Project ID")
                role = st.text_input("Role")
                if st.button("Assign Employee"):
                    c.execute("INSERT INTO project_assignments VALUES (%s,%s,%s)", (eid, pid, role))
                    db.commit()
                    st.success("Employee assigned successfully")

                    
       
            
            


        
    
                
        
        
                
    
    

