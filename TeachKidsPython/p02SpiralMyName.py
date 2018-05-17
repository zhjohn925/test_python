import turtle

# https://docs.python.org/3.3/library/turtle.html?highlight=turtle

t = turtle.Turtle()
turtle.bgcolor('black')

colors = ['red', 'yellow', 'blue', 'green']

# the first parameter is prompt window title
your_name = turtle.textinput('Enter your name', 'What is your name?')

for x in range(50):
    t.pencolor(colors[x%4])
    t.penup()
    t.forward(x*4)
    t.pendown()
    # font (fontname, fontsize, fonttype)
    t.write(your_name, font=('Arial', int((x+4)/4), 'bold'))
    t.left(92)

while True:
    t.hideturtle()
