from tkinter import ttk
from tkinter import *

from algo_setup import statistics_calculate
from functions import create_new_window, play_sound, restart_program, load_image


def statistics(main_frame: Frame) -> None:
    # Create new frame for 'PC Multi-Run'
    pc_multirun_frame = create_new_window(main_frame)

    for i in range(3):
        pc_multirun_frame.grid_rowconfigure(i, weight=1)
        pc_multirun_frame.grid_columnconfigure(i, weight=1)

    Label(
        pc_multirun_frame,
        text="Times to run:",
        font=("Arial", 12, "bold"),
        bg="midnight blue",
    ).grid(column=0, row=0, columnspan=3, pady=(100, 0))

    times_to_run = ttk.Combobox(
        pc_multirun_frame,
        width=20,
        state="readonly",
        justify=CENTER,
        font=("Arial", "12"),
    )
    times_to_run["values"] = (
        100,
        500,
        1000,
        2500,
        5000,
        10000,
        25000,
        100000,
        500000,
        1000000,
    )
    times_to_run.set(100)
    times_to_run.grid(column=1, row=1)

    # Select button
    Button(
        pc_multirun_frame,
        text="Select",
        height=2,
        width=10,
        font=("Arial", 11, "bold"),
        command=lambda: statistics_res(pc_multirun_frame, int(times_to_run.get())),
    ).grid(column=0, row=2, columnspan=3, pady=(0, 100))
    mainloop()


def statistics_res(pc_multirun_frame: Frame, n: int) -> None:
    # Create new frame for displaying the results
    pc_multirun_frame_res = create_new_window(pc_multirun_frame)

    for i in range(6):
        pc_multirun_frame_res.grid_rowconfigure(i, weight=1)
    for i in range(4):
        pc_multirun_frame_res.grid_columnconfigure(i, weight=1)

    # Run the Monty Hall algorithm
    condition_bool, n, wins, losses = statistics_calculate(n)

    # Play sound conditionally, depends on Win / Lose
    play_sound(
        "assets/sounds/ApplauseSound.wav"
        if condition_bool
        else "assets/sounds/GoatSound.mp3"
    )

    # Number of games text
    stats_row(pc_multirun_frame_res, "Number of games: ", str(n), 0, True)

    # Wins text
    stats_row(pc_multirun_frame_res, "Number of wins: ", str(wins), 1)

    # Losses text
    stats_row(pc_multirun_frame_res, "Number of losses: ", str(losses), 2)

    # Ratio text
    stats_row(
        pc_multirun_frame_res,
        "Wins / Losses ratio: ",
        "{:.2f}".format(wins / losses),
        3,
    )

    # Render texts conditionally, depends on Win / Lose
    Label(
        pc_multirun_frame_res,
        text="The computer changed its choice every time and won!"
        if condition_bool
        else "You Lost!",
        bg="midnight blue",
        font=("Arial", 12, "bold"),
        fg="white",
    ).grid(column=0, row=4, columnspan=4, pady=10)

    # Render image conditionally, depends on Win / Lose
    goat_img = load_image("assets/images/goat_image.jpg", 200, 150)
    car_img = load_image("assets/images/car_image.jpg", 200, 150)
    Label(pc_multirun_frame_res, image=car_img if wins else goat_img).grid(
        column=0, row=5, columnspan=4
    )

    # Restart button
    Button(
        pc_multirun_frame_res,
        text="Restart",
        height=2,
        width=10,
        font=("Arial", 11, "bold"),
        command=lambda: restart_program(pc_multirun_frame_res),
    ).grid(column=0, row=6, columnspan=4, pady=40)
    mainloop()


def stats_row(
    frame: Frame, first_text: str, second_text: str, row: int, pad: bool = False
) -> None:
    Label(
        frame,
        text=first_text,
        bg="midnight blue",
        font=("Arial", 11, "bold"),
    ).grid(column=1, row=row, pady=(40, 0) if pad else None, sticky=W)
    Label(
        frame,
        text=second_text,
        bg="midnight blue",
        font=("Arial", 11, "bold"),
        fg="white",
    ).grid(column=2, row=row, pady=(40, 0) if pad else None, sticky=E)