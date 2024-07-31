""" a simple to-do list program that also allows user to add, edit or delete tasks."""

import time
import csv

headings = ["checkbox", "no.", "task"]


# creates a new .csv file if it doesn't already exist
def initialize_csv():
    try:
        with open("tasks.csv", "x", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headings)
            writer.writeheader()
    except FileExistsError:
        pass


# main code
def main():
    initialize_csv()

    print(
        f"\nWelcome to your personal to-do list manager! This program helps you stay organized by \n"
        f"allowing you to add, edit, delete, and mark tasks as completed. Your tasks are saved \n"
        f"so you can pick up right where you left off!\n"
    )
    time.sleep(1)

    print(f"Type 'help' to get a list of all the available commands!")
    time.sleep(1)

    # checks for user commands
    user_input = ""
    while True:
        try:
            user_input = input("\nWhat would you like to do?: ")

            if user_input == "help":
                task_help()
                continue

            elif user_input == "add":
                task_add()
                continue

            elif user_input == "edit":
                task_edit()
                continue

            elif user_input == "del":
                task_delete()
                continue

            elif user_input == "view":
                task_view()
                continue

            elif user_input == "mark":
                task_mark()
                continue

            elif user_input == "unmark":
                task_unmark()
                continue

            elif user_input == "clear":
                while True:
                    clear_input = input(
                        "Are you sure you want to clear all the tasks? (y/n) "
                    )
                    # checks if the user has cancelled the command
                    if clear_input == "cancel":
                        task_cancel()
                        break

                    # checks if the user has entered a valid input
                    try:
                        if clear_input == "y":
                            task_clear()
                            break
                        elif clear_input == "n":
                            print("The list was not cleared.")
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print("Please enter 'y' for yes or 'n' for no! \n")
                        continue

            elif user_input == "exit":
                exit()

            else:
                raise ValueError

        except ValueError:
            print(f'"{user_input}" is not recognised as a valid command!')
            continue


def task_help():
    print(
        f"\nAvailable commands: \n"
        f"\nadd: adds a task.\n"
        f"edit: edits an existing task.\n"
        f"del: deletes an existing task.\n"
        f"view: displays all the tasks.\n"
        f"mark: marks a task as done.\n"
        f"unmark: marks a task as undone.\n"
        f"cancel: cancel the current command.\n"
        f"clear: clears the to-do list.\n"
        f"exit: saves and exits the program."
    )


def task_cancel():
    print("Command has been cancelled.")


# adds a task
def task_add():
    # prompts the user for the task name
    arg = input("Task: ")

    # checks if the user has cancelled the command
    if arg == "cancel":
        task_cancel()
        return

    n = 1
    with open("tasks.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for _ in reader:
            n += 1

    with open("tasks.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headings)
        writer.writerow({"checkbox": "[ ]", "no.": f"{n})", "task": arg})

    print(f"'{arg}' has been added to the list!")


def task_edit():
    arg = ""
    tasks_data = []

    # asks the user for a valid task number
    while True:
        try:
            arg = input("Enter task number: ")
            # checks if the user has cancelled the command
            if arg == "cancel":
                task_cancel()
                return

            _ = int(arg)
            break
        except ValueError:
            print("Please enter a valid integer!\n")
            continue

    # reads the csv file
    try:
        with open("tasks.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # noinspection PyTypeChecker
                tasks_data.append(
                    {
                        "checkbox": row["checkbox"],
                        "no.": row["no."],
                        "task": row["task"],
                    }
                )
    except KeyError:
        pass

    # edits the task name
    task_found = False
    for _ in tasks_data:
        if _["no."] == f"{arg})":
            task_found = True
            _["task"] = input("Enter new task: ")
            # checks if the user has cancelled the command
            if _["task"] == "cancel":
                task_cancel()
                return

            break

    if not task_found:
        print("No task found! Did you enter the correct number?")

    # rewrites the csv file
    if task_found:
        with open("tasks.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headings)
            writer.writeheader()
            writer.writerows(tasks_data)

        print("Task name successfully edited!")


# deletes a task
def task_delete():
    arg = ""
    tasks_data = []

    # asks the user for a valid task number
    while True:
        try:
            arg = input("Enter task number: ")
            # checks if the user has cancelled the command
            if arg == "cancel":
                task_cancel()
                return

            _ = int(arg)
            break
        except ValueError:
            print("Please enter a valid integer!\n")
            continue

    # reads the csv file
    try:
        with open("tasks.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # noinspection PyTypeChecker
                tasks_data.append(
                    {
                        "checkbox": row["checkbox"],
                        "no.": row["no."],
                        "task": row["task"],
                    }
                )
    except KeyError:
        pass

    # deletes the task
    tasks_to_keep = []
    task_found = False
    for _ in tasks_data:
        if _["no."] == f"{arg})":
            delete_confirm = input("Are you sure you want to delete this task? (y/n): ")

            # checks if the user has cancelled the command
            if delete_confirm == "cancel":
                task_cancel()
                return

            # checks if the user has entered a valid input
            try:
                if delete_confirm == "y":
                    task_found = True
                    continue

                elif delete_confirm == "n":
                    print("The task was not deleted.")
                    return

                else:
                    raise ValueError
            except ValueError:
                print("Please enter 'y' for yes or 'n' for no! ")
                return

        # Add tasks to the new list if not deleted
        tasks_to_keep.append(_)

    if not task_found:
        print("No task found! Did you enter the correct number?")

    # edits the number in each dictionary
    if task_found:
        for i, task in enumerate(tasks_to_keep):
            task["no."] = f"{i + 1})"

    # rewrites the data in csv file
    if task_found:
        with open("tasks.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headings)
            writer.writeheader()
            writer.writerows(tasks_to_keep)

            print("The task was deleted.")


# prints all the tasks
def task_view():
    tasks_data = []

    with open("tasks.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # noinspection PyTypeChecker
            tasks_data.append(
                {"checkbox": row["checkbox"], "no.": row["no."], "task": row["task"]}
            )

    # checks if the .csv file is empty
    if not tasks_data:
        print("No tasks found! Add new tasks using 'add'.")
    else:
        print("")
        for task in tasks_data:
            print(f"{task['checkbox']} {task['no.']} {task['task']} ")


# marks a task as done
def task_mark():
    arg = ""
    tasks_data = []

    # asks the user for a valid task number
    while True:
        try:
            arg = input("Enter task number: ")
            # checks if the user has cancelled the command
            if arg == "cancel":
                task_cancel()
                return

            _ = int(arg)
            break
        except ValueError:
            print("Please enter a valid integer!\n")
            continue

    # reads the csv file
    try:
        with open("tasks.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # noinspection PyTypeChecker
                tasks_data.append(
                    {
                        "checkbox": row["checkbox"],
                        "no.": row["no."],
                        "task": row["task"],
                    }
                )
    except KeyError:
        pass

    # edits the checkbox
    task_found = False
    for _ in tasks_data:
        if _["no."] == f"{arg})":
            # noinspection PyUnusedLocal
            task_found = True
            if _["checkbox"] == "[*]":
                print("This task has already been marked done!")
                break
            else:
                _["checkbox"] = "[*]"
                break

    if not task_found:
        print("No task found! Did you enter the correct number?")

    # updates the task data in .csv file
    if task_found:
        with open("tasks.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headings)
            writer.writeheader()
            writer.writerows(tasks_data)

            print(f"Task number {arg} marked as done!")


def task_unmark():
    arg = ""
    tasks_data = []

    # asks the user for a valid task number
    while True:
        try:
            arg = input("Enter task number: ")
            # checks if the user has cancelled the command
            if arg == "cancel":
                task_cancel()
                return

            _ = int(arg)
            break
        except ValueError:
            print("Please enter a valid integer!\n")
            continue

    # reads the csv file
    try:
        with open("tasks.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # noinspection PyTypeChecker
                tasks_data.append(
                    {
                        "checkbox": row["checkbox"],
                        "no.": row["no."],
                        "task": row["task"],
                    }
                )
    except KeyError:
        pass

    # edits the checkbox
    task_found = False
    for _ in tasks_data:
        if _["no."] == f"{arg})":
            # noinspection PyUnusedLocal
            task_found = True
            if _["checkbox"] == "[ ]":
                print("This task has already been marked undone!")
                break
            else:
                _["checkbox"] = "[ ]"
                break

    if not task_found:
        print("No task found! Did you enter the correct number?")

    # updates the task data in .csv file
    if task_found:
        with open("tasks.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headings)
            writer.writeheader()
            writer.writerows(tasks_data)

            print(f"Task number {arg} marked as undone!")


# clears the list
def task_clear():
    with open("tasks.csv", "w") as csvfile:
        _ = csv.writer(csvfile)

    # rewrites the headings in the cleared .csv file
    with open("tasks.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headings)
        writer.writeheader()

    print("All tasks have been cleared!")


if __name__ == "__main__":
    main()
