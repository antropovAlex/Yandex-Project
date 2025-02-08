import random


def generate_dungeon():
    dungeon = [[1 for _ in range(5)] for _ in range(5)]

    start_x = random.randint(0, 4)
    start_y = random.randint(0, 4)
    start_pos = (start_x, start_y)

    visited = set()
    visited.add(start_pos)
    neighbors = [(start_x, start_y)]

    adjacency_list = {}

    while neighbors:
        if len(adjacency_list) == 6:
            break
        else:
            current = neighbors.pop()
            x, y = current

            potential_neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 5 and 0 <= ny < 5 and (nx, ny) not in visited:
                    potential_neighbors.append((nx, ny))

            if potential_neighbors:
                neighbor = random.choice(potential_neighbors)
                neighbors.append(neighbor)
                visited.add(neighbor)

                if current not in adjacency_list:
                    adjacency_list[current] = []
                adjacency_list[current].append(neighbor)

                if neighbor not in adjacency_list:
                    adjacency_list[neighbor] = []
                adjacency_list[neighbor].append(current)

    # Определяем комнату босса - самую дальнюю от стартовой по наибольшему числу переходов
    def find_farthest_room(start, adjacency_list):
        visited = set()
        queue = [(start, 0)]
        farthest_room = start
        max_distance = 0

        while queue:
            room, distance = queue.pop(0)
            if distance > max_distance:
                max_distance = distance
                farthest_room = room
            visited.add(room)
            for neighbor in adjacency_list.get(room, []):
                if neighbor not in visited:
                    queue.append((neighbor, distance + 1))

        return farthest_room

    boss_room = find_farthest_room(start_pos, adjacency_list)

    return start_pos, boss_room, adjacency_list


def check_boss_defeated(boss_health):
    return boss_health <= 0


def can_exit_boss_room(current_room, boss_room, boss_health):
    if current_room == boss_room and not check_boss_defeated(boss_health):
        return False
    return True


start_room, boss_room, dungeon_structure = generate_dungeon()
print("Начальная комната:", start_room)
print("Комната босса:", boss_room)
print("Структура подземелья:", dungeon_structure)
