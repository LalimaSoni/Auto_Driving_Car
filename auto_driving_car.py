class Field:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers.")
        self.width = width
        self.height = height
        self.cars = {}

    def is_within_bounds(self, x, y):
        """Check if the given coordinates are within the field's boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_occupied(self, x, y):
        """Check if a position is occupied by any car."""
        return any(car['x'] == x and car['y'] == y for car in self.cars.values())

    def add_car(self, name, x, y, direction):
        """Adds a car to the field with a unique name, starting position, and direction."""
        if name in self.cars:
            raise ValueError(f"Car with name '{name}' already exists.")
        if not self.is_within_bounds(x, y) or self.is_occupied(x, y):
            raise ValueError("Car position is out of bounds or occupied.")
        if direction not in ('N', 'E', 'S', 'W'):
            raise ValueError("Invalid direction. Use N, S, E, or W.")
        self.cars[name] = {'x': x, 'y': y, 'direction': direction, 'active': True}

    def move_cars(self, command_sequences):
        """Moves all cars step by step while checking for collisions."""
        directions = ['N', 'E', 'S', 'W']

        max_length = max(len(cmds) for cmds in command_sequences.values())

        for step in range(max_length):
            new_positions = {}

            for name, commands in command_sequences.items():
                if step < len(commands) and self.cars[name]['active']:

                    car = self.cars[name]
                    command = commands[step]
                    new_x, new_y = car['x'], car['y']
                    step = step

                    if command == 'L':
                        car['direction'] = directions[(directions.index(car['direction']) - 1) % 4]
                    elif command == 'R':
                        car['direction'] = directions[(directions.index(car['direction']) + 1) % 4]
                    elif command == 'F':
                        if car['direction'] == 'N':
                            new_y += 1
                        elif car['direction'] == 'E':
                            new_x += 1
                        elif car['direction'] == 'S':
                            new_y -= 1
                        elif car['direction'] == 'W':
                            new_x -= 1

                        if self.is_within_bounds(new_x, new_y):
                            new_positions[name] = (new_x, new_y)
                        else:
                            new_positions[name] = (car['x'], car['y'])

            # Detect collisions
            seen_positions = {}
            for name, pos in new_positions.items():

                if pos in seen_positions:
                    # print('occupied position by car1')
                    self.cars[name]['active'] = False
                    self.cars[seen_positions[pos]]['active'] = False
                else:
                    seen_positions[pos] = name

           

            # Update positions
            for name, (x, y) in new_positions.items():
                if self.cars[name]['active']:
                    self.cars[name]['x'] = x
                    self.cars[name]['y'] = y
                    self.cars[name]['pos'] = new_positions[name]
                    self.cars[name]['step'] = step

                else:
                    self.cars[name]['step'] = step + 1
                    self.cars[name]['pos'] = new_positions[name]
                    if name in list(new_positions.keys()):
                        self.cars[name]['oppo'] = list(filter(lambda x: x != name, new_positions.keys()))

    def __repr__(self):
        return f"Field({self.width}, {self.height}, Cars: {self.cars})"


def main():
    print("Welcome to Auto Driving Car Simulation!\n")
    width, height = map(int, input("Please enter the width and height of the simulation field in x y format: ").split())
    field = Field(width, height)
    print(f"You have created a field of {width} x {height}.\n")

    command_sequences = {}

    while True:
        print("Please choose from the following options:")
        print("[1] Add a car to field")
        print("[2] Run simulation")
        print("[3] Exit")
        choice = input()

        if choice == "1":

            name = input("Please enter the name of the car: ")
            x, y, direction = input(f"Please enter initial position of car {name} in x y Direction format: ").split()
            field.add_car(name, int(x), int(y), direction)
            commands = input(f"Please enter the commands for car {name}: ")


            command_sequences[name] = commands
            print("Your current list of cars are: \n")
            for name, car in field.cars.items():
                print(f"-- {name}, ({car['x']},{car['y']}) {car['direction']},  {command_sequences[name]}\n")


        elif choice == "2":
            print("Your current list of cars are: \n")
            for name, car in field.cars.items():
                print(f"-- {name}, ({car['x']},{car['y']}) {car['direction']},  {command_sequences[name]}\n")
            field.move_cars(command_sequences)
            print("After simulation, the result is: \n")
            for name, car in field.cars.items():
                if car['active']:
                    status = "Active"
                    print(f"-- {name}: {car['pos']} {car['direction']} \n")
                else:
                    status = (f"collides with")
                    print(f"-- {name}: {status} {car['oppo']} at {car['pos']} at step {car['step']}\n")

            while True:
                print("[1] Start Over")
                print("[2] Exit")
                choice = input()

                if choice == "1":
                    return main()

                elif choice == "2":
                    print("Thank you for running the simulation. Goodbye!")
                    return

        elif choice == "3":
            print("Thank you for running the simulation. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()

