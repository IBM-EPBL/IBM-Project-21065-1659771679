from flask import Flask, render_template, request, redirect, session
import ibm_db
import ibm_db_dbi
import re

app = Flask(__name__)


app.secret_key = 'a'

# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mbs46040;PWD=MIEpZ1DoqwMRpGvs",'','')
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=nxp94278;PWD=XdzphucSHe8uQRe1", '', '')
connection = ibm_db_dbi.Connection(conn)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
    id VARCHAR(50) NOT NULL, 
    date DATE NOT NULL, 
	expensename VARCHAR(50) NOT NULL, 
	amount FLOAT NOT NULL, 
	paymode VARCHAR(50) NOT NULL, 
    category VARCHAR(50) NOT NULL
    )''')
# HOME--PAGE


@app.route("/home")
def home():
    return render_template("homepage.html")


@app.route("/")
def add():
    return render_template("home.html")


# SIGN--UP--OR--REGISTER


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM register WHERE username = ?", (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute("INSERT INTO register VALUES ( ?, ?, ?)",
                           (username, email, password))
            connection.commit()
            msg = 'You have successfully registered !'
            return render_template('signup.html', msg=msg)

 # LOGIN--PAGE


@app.route("/signin")
def signin():
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM register WHERE username = ? AND password = ?", (username, password),)
        account = cursor.fetchone()
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid = account[0]
            session['username'] = account[1]

            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


# ADDING----DATA


@app.route("/add")
def adding():
    return render_template('add.html')


@app.route('/addexpense', methods=['GET', 'POST'])
def addexpense():

    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']

    # cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO expenses VALUES ( ?, ?, ?, ?, ?, ?)",
                   (session['id'], date, expensename, amount, paymode, category))
    connection.commit()
    print(date + " " + expensename + " " +
          amount + " " + paymode + " " + category)

    return redirect("/display")


# DISPLAY---graph

@app.route("/display")
def display():
    print(session["username"], session['id'])

    # cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM expenses WHERE id = ? ORDER BY date DESC', (session['id'],))
    expense = cursor.fetchall()

    return render_template('display.html', expense=expense)


# delete---the--data

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete(id):
    #  cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM expenses WHERE  userid = ?", (id,))
    connection.commit()
    print('deleted successfully')
    return redirect("/display")


# UPDATE---DATA

@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    # cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE  userid = ?", (id,))
    row = cursor.fetchall()

    print(row[0])
    return render_template('edit.html', expenses=row[0])


@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':

        date = request.form['date']
        expensename = request.form['expensename']
        amount = request.form['amount']
        paymode = request.form['paymode']
        category = request.form['category']

    #   cursor = mysql.connection.cursor()

        cursor.execute("UPDATE `expenses` SET `date` = ? , `expensename` = ? , `amount` = ?, `paymode` = ?, `category` = ? WHERE `expenses`.`userid` = ? ",
                       (date, expensename, amount, str(paymode), str(category), id))
        connection.commit()
        print('successfully updated')
        return redirect("/display")

 # limit


@app.route("/limit")
def limit():
    return redirect('/limitn')


@app.route("/limitnum", methods=['POST'])
def limitnum():
    if request.method == "POST":
        number = request.form['number']
        #  cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO limits VALUES (?, ?) ",
                       (session['id'], number))
        connection.commit()
        return redirect('/limitn')


@app.route("/limitn")
def limitn():
    # cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM limits ORDER BY  id DESC")
    x = cursor.fetchone()
    s = x  # [0]

    return render_template("limit.html", y=s)

# REPORT


@app.route("/today")
def today():
    #   cursor = mysql.connection.cursor()
    print("HI")

    print("HIII")
    #cursor.execute('SELECT * FROM expenses WHERE userid = {0} AND DATE(date) = DATE(NOW()) AND date ORDER BY `expenses`.`date` DESC'.format(str(session['id'])))
    cursor.execute("SELECT * FROM EXPENSES WHERE DATE = CURRENT_DATE ")

    expense = cursor.fetchall()

    total = 0
    t_food = 0
    t_entertainment = 0
    t_business = 0
    t_rent = 0
    t_EMI = 0
    t_other = 0

    for x in expense:
        print(x[3])
        total += x[3]
        if x[5] == "food":
            t_food += x[3]

        elif x[5] == "entertainment":
            t_entertainment += x[3]

        elif x[5] == "business":
            t_business += x[3]
        elif x[5] == "rent":
            t_rent += x[3]

        elif x[5] == "EMI":
            t_EMI += x[3]

        elif x[5] == "other":
            t_other += x[3]

    print(total)

    print(t_food)
    print(t_entertainment)
    print(t_business)
    print(t_rent)
    print(t_EMI)
    print(t_other)

    return render_template("today.html", expense=expense,  total=total,
                           t_food=t_food, t_entertainment=t_entertainment,
                           t_business=t_business,  t_rent=t_rent,
                           t_EMI=t_EMI,  t_other=t_other)


@app.route("/month")
def month():
    #   cursor = mysql.connection.cursor()
    #   cursor.execute("SELECT DATE(date), SUM(amount) FROM expenses WHERE userid= ? AND MONTH(DATE(date))= MONTH(now()) GROUP BY DATE(date) ORDER BY DATE(date) ",(str(session['id'])))
    #   texpense = cursor.fetchall()
    #   print(texpense)

    #   cursor = mysql.connection.cursor()
    #   cursor.execute("SELECT * FROM expenses WHERE userid = ? AND MONTH(DATE(date))= MONTH(now()) AND date ORDER BY `expenses`.`date` DESC",(str(session['id'])))
    cursor.execute(
        "SELECT * FROM EXPENSES WHERE DATE <= THIS_MONTH(CURRENT_DATE + 1 MONTH) AND DATE > THIS_MONTH(CURRENT_DATE) ")
    expense = cursor.fetchall()
    print(expense)

    total = 0
    t_food = 0
    t_entertainment = 0
    t_business = 0
    t_rent = 0
    t_EMI = 0
    t_other = 0

    for x in expense:
        total += x[3]
        if x[5] == "food":
            t_food += x[3]

        elif x[5] == "entertainment":
            t_entertainment += x[3]

        elif x[5] == "business":
            t_business += x[3]
        elif x[5] == "rent":
            t_rent += x[3]

        elif x[5] == "EMI":
            t_EMI += x[3]

        elif x[5] == "other":
            t_other += x[3]

    print(total)

    print(t_food)
    print(t_entertainment)
    print(t_business)
    print(t_rent)
    print(t_EMI)
    print(t_other)

    return render_template("month.html", expense=expense,  total=total,
                           t_food=t_food, t_entertainment=t_entertainment,
                           t_business=t_business,  t_rent=t_rent,
                           t_EMI=t_EMI,  t_other=t_other)


@app.route("/year")
def year():
    #   cursor = mysql.connection.cursor()
    #   cursor.execute("SELECT MONTH(date), SUM(amount) FROM expenses WHERE userid= ? AND YEAR(DATE(date))= YEAR(now()) GROUP BY MONTH(date) ORDER BY MONTH(date) ",(str(session['id'])))
    #   texpense = cursor.fetchall()
    #   print(texpense)

    #   cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM EXPENSES WHERE DATE <= THIS_YEAR(CURRENT_DATE + 1 YEAR) AND DATE > THIS_YEAR(CURRENT_DATE) ")
    expense = cursor.fetchall()

    total = 0
    t_food = 0
    t_entertainment = 0
    t_business = 0
    t_rent = 0
    t_EMI = 0
    t_other = 0

    for x in expense:
        total += x[3]
        if x[5] == "food":
            t_food += x[3]

        elif x[5] == "entertainment":
            t_entertainment += x[3]

        elif x[5] == "business":
            t_business += x[3]
        elif x[5] == "rent":
            t_rent += x[3]

        elif x[5] == "EMI":
            t_EMI += x[3]

        elif x[5] == "other":
            t_other += x[3]

    print(total)

    print(t_food)
    print(t_entertainment)
    print(t_business)
    print(t_rent)
    print(t_EMI)
    print(t_other)

    return render_template("year.html", expense=expense,  total=total,
                           t_food=t_food, t_entertainment=t_entertainment,
                           t_business=t_business,  t_rent=t_rent,
                           t_EMI=t_EMI,  t_other=t_other)

# log-out


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
