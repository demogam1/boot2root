import turtle

# Initialiser la tortue
t = turtle.Turtle()

# Première partie : Tourner à gauche de 90 degrés et avancer de 50 espaces
t.left(90)
t.forward(50)

# Deuxième partie : Avancer de 1 espace et tourner à gauche de 1 degré 360 fois
for _ in range(360):
    t.forward(1)
    t.left(1)

# Troisième partie : Avancer de 1 espace et tourner à droite de 1 degré 360 fois
for _ in range(360):
    t.forward(1)
    t.right(1)

# Quatrième partie : Avancer de 1 espace et tourner à droite de 1 degré 360 fois
for _ in range(360):
    t.forward(1)
    t.right(1)

# Tourner à droite de 1 degré et avancer de 50 espaces
t.right(1)
t.forward(50)

# Nouvelle partie des instructions
t.forward(210)
t.backward(210)
t.right(90)
t.forward(120)

t.right(10)
t.forward(200)
t.right(150)
t.forward(200)
t.backward(100)
t.right(120)
t.forward(50)

# Ajouter la dernière partie des instructions
# Avancer de 1 espace et tourner à gauche de 1 degré 180 fois
for _ in range(180):
    t.forward(1)
    t.left(1)

# Terminer le dessin
turtle.done()
