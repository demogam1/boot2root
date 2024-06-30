import turtle

# Fonction pour lire les instructions depuis un fichier texte
def lire_instructions(fichier):
    instructions = []
    with open(fichier, 'r') as f:
        for ligne in f:
            parts = ligne.strip().split()
            action = parts[0]
            if action in ["Avance", "Recule"]:
                value = int(parts[1])  # Prendre la deuxième partie comme valeur numérique
                if action == "Avance":
                    instructions.append(("avance", value))
                elif action == "Recule":
                    instructions.append(("recule", value))
            elif action == "Tourne":
                value = int(parts[3])  # Prendre la quatrième partie comme valeur numérique
                direction = parts[1]
                if direction == "droite":
                    instructions.append(("tourne_droite", value))
                elif direction == "gauche":
                    instructions.append(("tourne_gauche", value))
    return instructions

# Initialiser la fenêtre et la tortue
window = turtle.Screen()
window.bgcolor("white")
t = turtle.Turtle()
t.speed(0)

# Définir une fonction pour les mouvements et les tours
def move_turtle(instructions):
    for instruction in instructions:
        action, value = instruction
        if action == "tourne_gauche":
            t.left(value)
        elif action == "tourne_droite":
            t.right(value)
        elif action == "avance":
            t.forward(value)
        elif action == "recule":
            t.backward(value)

# Lire les instructions depuis le fichier
instructions = lire_instructions('instructions.txt')

# Exécuter les instructions
move_turtle(instructions)

# Maintenir la fenêtre ouverte
window.mainloop()
