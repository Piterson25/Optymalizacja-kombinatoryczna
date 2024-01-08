import matplotlib.pyplot as plt
import numpy as np


class Task:
    def __init__(self, task_id, duration):
        self.id = task_id
        self.duration = duration
        self.successors = []
        self.predecessors = []
        self.earliest_start = 0
        self.latest_start = float('inf')


def read_from_file(file_name):
    tasks = {}
    with open(file_name, 'r') as file:
        for line in file:
            data = line.split()
            task_id = int(data[0])
            duration = int(data[1])

            task = Task(task_id, duration)
            tasks[task_id] = task

            if len(data) > 2:
                predecessors_ids = list(map(int, data[2:]))
                for pred_id in predecessors_ids:
                    tasks[task_id].predecessors.append(pred_id)
                    tasks[pred_id].successors.append(task_id)
    return tasks


def earliest_start(tasks):
    visited = set()
    stack = []

    for task_id, task in tasks.items():
        if not task.predecessors:
            stack.append(task)

    while stack:
        current_task = stack.pop()
        visited.add(current_task.id)

        for successor_id in current_task.successors:
            successor = tasks[successor_id]
            successor.earliest_start = max(successor.earliest_start,
                                           current_task.earliest_start + current_task.duration)
            if all(pred_id in visited for pred_id in successor.predecessors):
                stack.append(successor)


def latest_start(tasks):
    sorted_tasks = sorted(tasks.values(), key=lambda x: x.earliest_start,
                          reverse=True)

    for task in sorted_tasks:
        if not task.successors:
            task.latest_start = task.earliest_start

        for predecessor_id in task.predecessors:
            predecessor = tasks[predecessor_id]
            task.latest_start = min(task.latest_start,
                                    predecessor.latest_start - task.duration)


def find_critical_path(tasks):
    critical_path = []
    for task_id, task in tasks.items():
        if task.earliest_start == task.latest_start:
            critical_path.append(task.id)
    return critical_path


def calculate_schedule_length(tasks):
    return max(task.earliest_start + task.duration for task in tasks.values())


def harmonogram(tasks, num_machines):
    _, ax = plt.subplots()

    ax.set_ylim(0, num_machines + 1)

    machine_tasks = {}

    for task_id, task in tasks.items():
        machine_id = task.id % num_machines
        if machine_id not in machine_tasks:
            machine_tasks[machine_id] = []
        machine_tasks[machine_id].append(
            (task.earliest_start, task.duration, task_id))

    num_colors = len(tasks)
    cmap = plt.get_cmap('tab20')
    colors = [cmap(i) for i in np.linspace(0, 1, num_colors)]

    for machine_id, tasks_list in machine_tasks.items():
        tasks_list.sort(key=lambda x: x[0])
        y = num_machines - machine_id
        for i, (start, duration, task_id) in enumerate(tasks_list):
            color_index = task_id % num_colors
            ax.broken_barh([(start, duration)], (y - 0.4, 0.8),
                           facecolors=colors[color_index])

            text_x = start + duration / 2
            text_y = y
            ax.text(text_x, text_y, f'Z{task_id}',
                    ha='center', va='center', color='white', weight='bold')

    ax.set_xlabel('Czas trwania zadania')
    ax.set_ylabel('Numer maszyny')

    ax.set_xticks(np.arange(0, max(
        task.earliest_start + task.duration for task in tasks.values()) + 1,
                            step=1))
    ax.set_yticks(np.arange(1, num_machines + 1, step=1))

    plt.show()


def main():
    file_name = "zadania.txt"
    num_machines = 5

    tasks = read_from_file(file_name)
    earliest_start(tasks)
    latest_start(tasks)

    critical_path = find_critical_path(tasks)
    schedule_length = calculate_schedule_length(tasks)

    print("Zadanie | Najwcześniejszy czas | Najpóźniejszy czas")
    for task_id, task in tasks.items():
        print(
            f"Z{task_id:02}     | {task.earliest_start:20} | "
            f"{task.latest_start:18}")

    print(f"\nŚcieżka krytyczna: {critical_path}")
    print(f"\nDługość uszeregowania: {schedule_length}")

    harmonogram(tasks, num_machines)


if __name__ == "__main__":
    main()
