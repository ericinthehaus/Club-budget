import cherrypy
import datetime

semester_end_date = datetime.date(2020,5,22)
days_remaining = semester_end_date - datetime.date.today()

days_rem =  days_remaining.days
weeks_rem = days_rem / 7

# this page asks for username and password. 
index_html = """
<html>
<body>
<h1>Welcome, club admins!</h1>

    <form method="get" action=handle_password>
      User name:<br>
          <input type="text" name="username"><br>
          User password:<br>
          <input type="password" name="psw">
          <button type="submit">Enter!</button>
    </form>

</body>
</html>
"""

# the page which asks for your overall semester budget

budget_form_html = """
<html>
<body>

<p>have you wondered how much money you can spend this week? how much will it affect your remaining budget? </p>

 <form method="get" action="handle_budget_form">
  What is your remaining budget for the semester?
   <input type="number" name="quantity" min="100"/>
   <button type="submit">Submit!</button>
 </form>
 
</body>
</html>
"""

# this page displays your weekly budget and asks for what kind of purchase you want to submit

purchase_type_form_html = """
<html>
<body>
<p>Your weekly budget= <b> $%.2f </b>
</p>

 <form action=handle_purchase_type>
     <input type="radio" name="purchase_type" value="ordinary" > Ordinary Weekly Expenses <br>
     <input type="radio" name="purchase_type" value="fun" > New purchase out of the ordinary expenses <br>
     <input type="submit" >
 </form>

</body>
</html>
"""

# The page displays weekly budget and asks for ordinary expenses :
purchase_form_html = """
<html>
<body>
<h1>Thank you</h1>
<p>Your weekly budget= <b> $%.2f </b>
</p>

<form method="get" action=handle_purchase_form>
  What is the total cost of your expenses for this week? 
   <input type="number" name="cost" min="1"/>
   <button type="submit">Submit!</button>
 </form>

</body>
</html>
"""

# this page displays new weekly and asks for a new purchase out of the ordinary:
fun_purchase_form_html = """
<html>
<body>
<h1>Thank you</h1>
<p>Your weekly budget= <b> $%.2f </b>
</p>

<form method="get" action=handle_fun_purchase_form>
  What is the cost of your new purchase today? 
   <input type="number" name="cost" />
   <button type="submit">Submit!</button>
 </form>

</body>
</html>
"""

# this page displays new weekly budgets due to new extra purchases

new_budget_page_extra_html = """

<html>
<body>
<h1>Thank you again, %s</h1>
<p>Your <i>old</i> weekly budget= $%.2f
<p>Your <i>new</i> weekly budget= <b> $%.2f </b>
<p>Since you payed $%.2f extra this week on expenses with a $%.f budget,
your weekly value for the new purchase is <b>$%.2f</b>
</p>

 <a href="/">Click here to go to our landing  page.</a>

<p> If you would like to learn more about how i calculated these budgets,
I'll post some formulas soon :) </p>

<br><br>
<form method="get" action="handle_budget_form_again">
  Would you like to record another purchase?
   <button type="submit">Yes one more!</button>
 </form>

</body>
</html>
"""

# this page displays new weekly budget and the change in weekly budget for ordinary expenses  

new_budget_page_ordinary_html = """

<html>
<body>
<h1>Thank you again, %s</h1>
<p>Your <i>old</i> weekly budget= $%.2f
<p>Your <i>new</i> weekly budget= <b> $%.2f </b>
<p>Since you payed $%.2f this week on expenses with a $%.f budget,
your weekly budget changed by <b>$%.2f</b> (%.1f percent)
</p>

 <a href="/">Click here to go to our landing  page.</a>
<br>
<p> <small>If you would like to learn more about how i calculated these budgets,
I'll post some formulas soon :) </small> </p>

<br><br>
<form method="get" action="handle_budget_form_again">
  Would you like to record another purchase?
   <button type="submit">Yes one more!</button>
 </form>


</body>
</html>
"""

variables = [.001,.001 ,.001 ,.001 ,.001]

# Now we create the class that will basically define which pages exist on our site and how they work:

# the method called 'index' generates the landing page of our site (the "root" or "top-level" page)
# we are free to name all other methods as we wish. a method called xyz will generate the page the user
# sees when they visit http://ec2-54-88-152-165.compute-1.amazonaws.com:8100/xyz

# in all cases, the page served to the user is the string returned by the method

class HelloWorldWebApp:

    
    @cherrypy.expose
    def index(self):
        return index_html

    @cherrypy.expose
    def handle_password(self, username, psw):
        variables[0] = username
        variables[1] = psw
        if psw == "psw1234":
            return budget_form_html
        else:
            return "Your password was incorrect. Try again"

    @cherrypy.expose
    def handle_purchase_type(self, purchase_type):
        if purchase_type=="ordinary":
            return purchase_form_html % float(variables[3])
        else:
            return fun_purchase_form_html % float(variables[3])

    

    @cherrypy.expose
    def handle_budget_form(self, quantity):
        variables[2] = quantity
        weekly_budget = int(quantity) / weeks_rem
        variables[3] = float (weekly_budget)
        return purchase_type_form_html % weekly_budget

    @cherrypy.expose
    def handle_budget_form_again(self):
        variables[3] = variables[4]
        weekly_budget = variables[3]
        return purchase_type_form_html % weekly_budget

    @cherrypy.expose
    def handle_purchase_form(self, cost):
        new_weekly_budget =  ( float(variables[2])  - float(cost) )/ float(weeks_rem-1) 
        variables[4] = new_weekly_budget
        return new_budget_page_ordinary_html % ( variables[0],
                                        float(variables[3]) ,
                                        float(new_weekly_budget),
                                        float (cost),
                                        float (variables[2]),
                                        float (new_weekly_budget - variables[3] ),
                                        float ( 100*(new_weekly_budget-variables[3])/variables[3] )
                                    )
    @cherrypy.expose
    def handle_fun_purchase_form(self, cost):
        new_weekly_budget =  ( float(variables[2])  - float(cost) )/ float(weeks_rem)
        variables[4] = new_weekly_budget
        old_budget = float(variables[2])
        variables[2] = float(variables[2])  - float(cost)  # new budget is variables[2]
        return new_budget_page_extra_html % ( variables[0],
                                        float(variables[3]) ,
                                        float(new_weekly_budget),
                                        float (cost),
                                        old_budget,
                                        float(cost)/ float (weeks_rem)
                                    )

our_app = HelloWorldWebApp()
static_file_config = {'/static': {'tools.staticdir.on': True, 'tools.staticdir.dir': '/home/ubuntu/teamXX/static'} }
cherrypy.quickstart(our_app, '/', static_file_config)
    
