import matplotlib.pyplot as plt
import numpy as np
import math


class Task:
    def __init__(self, task_id, duration):
        self.id = task_id
        self.duration = duration
        self.successors = []
        self.predecessors = []
        self.earliest_start = 0
        self.latest_start = math.inf


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
    end_tasks = [task for task in tasks.values() if not task.successors]

    min_time = calculate_schedule_length(tasks)

    for end_task in end_tasks:
        end_task.latest_start = min_time - end_task.duration

    visited = set()
    stack = end_tasks[:]

    while stack:
        current_task = stack.pop()
        visited.add(current_task.id)

        for pred_id in current_task.predecessors:
            predecessor = tasks[pred_id]
            predecessor.latest_start = min(predecessor.latest_start,
                                           current_task.latest_start - predecessor.duration)
            if all(succ_id in visited for succ_id in predecessor.successors):
                stack.append(predecessor)


def find_critical_path(tasks):
    critical_path = []
    for task_id, task in tasks.items():
        if task.earliest_start == task.latest_start:
            critical_path.append(task.id)
    return critical_path


def calculate_schedule_length(tasks):
    return max(task.earliest_start + task.duration for task in tasks.values())


def harmonogram(tasks):
    _, ax = plt.subplots()

    sorted_tasks = sorted(tasks.values(), key=lambda x: x.earliest_start)

    machines = []
    machine_end_times = []

    cmap = plt.get_cmap('tab20')

    for task in sorted_tasks:
        machine_found = False
        for i, machine_end_time in enumerate(machine_end_times):
            if task.earliest_start >= machine_end_time:
                machines[i].append(task)
                machine_end_times[i] = task.earliest_start + task.duration
                machine_found = True
                break

        if not machine_found:
            machines.append([task])
            machine_end_times.append(task.earliest_start + task.duration)

    colors = [cmap(i) for i in np.linspace(0, 1, len(sorted_tasks))]

    for i, machine_tasks in enumerate(machines):
        for task in machine_tasks:
            color_index = sorted_tasks.index(task)
            ax.broken_barh([(task.earliest_start, task.duration)],
                           (i + 0.6, 0.8),
                           facecolors=colors[color_index])
            ax.text(task.earliest_start + task.duration / 2, i + 1,
                    f'Z{task.id}',
                    ha='center', va='center', color='white', weight='bold')

    ax.set_xlabel('Czas trwania zadania')
    ax.set_ylabel('Numer maszyny')
    ax.set_xticks(np.arange(0, max(machine_end_times) + 1, step=1))
    ax.set_yticks(np.arange(1, len(machines) + 1, step=1))

    plt.show()


def main():
    file_name = "zadania.txt"

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

    print(f"\nŚcieżka krytyczna: {", ".join(f"Z{x}" for x in critical_path)}")
    print(f"\nDługość uszeregowania: {schedule_length}")

    harmonogram(tasks)


if __name__ == "__main__":
    main()
