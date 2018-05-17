import turtle

# https://docs.python.org/3.3/library/turtle.html?highlight=turtle

t1 = turtle.Turtle()   # or use alias turtle.Pen()
t2 = turtle.Turtle()

t1.pencolor('blue')
t1.penup()
t1.setpos(100, 100)
t1.pendown()
t2.pencolor('pink')

for x in range(30):
    t1.forward(x)  # move forward x pixels
    #t1.left(90)   # turn left 90 degrees
    #what happens if we try 
    t1.left(91) 
    # change forward() to circle()   
    t2.circle(x)   # radius of x pixels
    t2.left(90)

while True:
    t1.hideturtle()
    t2.hideturtle()
