from tkinter import *
from PIL import ImageTk, Image
from algo_setup import game_run, mh_problem_partial
import pygame
import random


def create_new_window(frame_destroy=None):
    # Destroy previous frame
    if frame_destroy != None:
        frame_destroy.destroy()
    new_frame = Frame(width=650, height=500)
    new_frame.pack(fill="both", expand=True)

    # Setting the padding between columns
    for i in range(3):
        new_frame.columnconfigure(i, weight=10)

    # Place the background image
    Label(new_frame, image=background_img).place(x=0, y=0)
    return new_frame


def human_run(main_frame):
    # Create new frame for 'Human Run'
    first_human_frame = create_new_window(main_frame)

    Label(first_human_frame, text="Make your choice").grid(column=1, row=0, pady=10)

    # Render 3 curtain images & 3 buttons to choose from
    for i in range(3):
        Label(first_human_frame, image=curtains_img).grid(column=i, row=1)
        Button(
            first_human_frame,
            text="No." + str(i + 1),
            command=lambda: human_sec_choice(i, first_human_frame),
        ).grid(column=i, row=2, pady=10)

    root.mainloop()


def human_sec_choice(first_choice, first_frame):
    # Create new frame for screen after 1st choice
    second_human_frame = create_new_window(first_frame)

    # Run the Monty Hall algorithm -> return the exposed goat index & list
    exposed_goat_index, obj_list = mh_problem_partial(first_choice)

    Label(second_human_frame, text="Would you like to change your choice?").grid(
        column=1, row=0, pady=10
    )

    for i in range(3):
        if i == exposed_goat_index:
            image_label = Label(second_human_frame, image=goat_img)
        else:
            image_label = Label(second_human_frame, image=curtains_img)
            if i == 0:
                Button(
                    second_human_frame,
                    text="Change" if i != first_choice else "Stand",
                    command=lambda: human_results(
                        first_choice, 0, obj_list, second_human_frame
                    ),
                ).grid(column=i, row=2)
            elif i == 1:
                Button(
                    second_human_frame,
                    text="Change" if i != first_choice else "Stand",
                    command=lambda: human_results(
                        first_choice, 1, obj_list, second_human_frame
                    ),
                ).grid(column=i, row=2)
            else:
                Button(
                    second_human_frame,
                    text="Change" if i != first_choice else "Stand",
                    command=lambda: human_results(
                        first_choice, 2, obj_list, second_human_frame
                    ),
                ).grid(column=i, row=2)
        image_label.grid(column=i, row=1)
    root.mainloop()


def human_results(first_choice, second_choice, obj_list, second_human_frame):
    # Create new frame for displaying the results
    human_results_frame = create_new_window(second_human_frame)

    ci = obj_list.index("car")

    # Render texts conditionally, depends on Win / Lose
    Label(
        human_results_frame, text="You Won!" if ci == second_choice else "You Lost!"
    ).place(relx=0.5, rely=0.2, anchor=CENTER)
    Label(
        human_results_frame,
        text="Choice changed"
        if first_choice != second_choice
        else "Choice not changed",
    ).place(relx=0.5, rely=0.25, anchor=CENTER)

    # Render image conditionally, depends on Win / Lose
    image_label = Label(
        human_results_frame, image=car_img if ci == second_choice else goat_img
    )
    image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    if ci == second_choice:
        play_sound("sounds/ApplauseSound.wav")
    else:
        play_sound("sounds/GoatSound.mp3")

    # Restart button
    Button(
        human_results_frame,
        text="Restart",
        command=lambda: main_screen(human_results_frame),
    ).place(relx=0.5, rely=0.7, anchor=CENTER)

    root.mainloop()


def pc_multirun(main_frame):
    # Create new frame for 'PC Multi-Run'
    pc_multirun_frame = create_new_window(main_frame)

    Label(pc_multirun_frame, text="Times to run:").grid(column=1, row=0, pady=10)

    # Times to run radio buttons
    times_to_run = [
        ("100", 100),
        ("1000", 1000),
        ("10,000", 10000),
        ("100,000", 100000),
    ]
    v = IntVar()
    v.set(100)
    i = 0
    for times, val in times_to_run:
        b = Radiobutton(
            pc_multirun_frame, text=times, variable=v, command=v.get(), value=val
        )
        b.grid(column=1, row=1 + i)
        i += 1

    # Times to run select button
    Button(
        pc_multirun_frame,
        text="Select",
        command=lambda: pc_multirun_res(pc_multirun_frame, v.get()),
    ).grid(column=1, row=6, pady=10)


def pc_multirun_res(pc_multirun_frame, n):
    # Create new frame for displaying the results
    pc_multirun_frame_res = create_new_window(pc_multirun_frame)

    # Run the Monty Hall algorithm -> returns Win (True) / Lose (False)
    text_box = Label(pc_multirun_frame_res, width=100, text="")
    text_box.grid(column=0, row=0)
    wins = game_run(n, False, text_box)

    # Play sound conditionally, depends on Win / Lose
    play_sound("sounds/ApplauseSound.wav" if wins else "sounds/GoatSound.mp3")

    # Render image conditionally, depends on Win / Lose
    Label(pc_multirun_frame_res, image=car_img if wins else goat_img).place(
        relx=0.5, rely=0.5, anchor=CENTER
    )

    # Render texts conditionally, depends on Win / Lose
    Label(pc_multirun_frame_res, text="You Won!" if wins else "You Lost!").place(
        relx=0.5, rely=0.2, anchor=CENTER
    )
    Label(pc_multirun_frame_res, text="Choice changed").place(
        relx=0.5, rely=0.25, anchor=CENTER
    )

    # Restart button
    Button(
        pc_multirun_frame_res,
        text="Restart",
        command=lambda: main_screen(pc_multirun_frame_res),
    ).place(relx=0.5, rely=0.7, anchor=CENTER)


def pc_single_run(main_frame):
    # Create new frame for 'PC Single Run'
    pc_single_frame = create_new_window(main_frame)

    # Randomize a choice
    choice = random.randint(0, 2)
    Label(pc_single_frame, text="\nThe PC choice was No." + str(choice + 1)).grid(
        column=1, row=0, pady=10
    )

    # Render 3 curtain images
    for i in range(3):
        Label(pc_single_frame, image=curtains_img).grid(column=i, row=1)

    # Next step button
    Button(
        pc_single_frame,
        text="Next Step",
        command=lambda: pc_single_run_p2(pc_single_frame, choice),
    ).grid(column=1, row=2, pady=10)


def pc_single_run_p2(pc_single_frame, choice):
    # Create new frame for next step
    pc_single_p2_frame = create_new_window(pc_single_frame)

    # Run the Monty Hall algorithm -> return the exposed goat index & list
    exposed_goat_index, obj_list = mh_problem_partial(choice)
    text_box = Label(
        pc_single_p2_frame,
        text="\nThe PC first choice was No."
        + str(choice + 1)
        + "\nThe game show expose curtain NO."
        + str(exposed_goat_index + 1),
    )
    text_box.grid(column=1, row=0, pady=10)
    Label(pc_single_p2_frame, image=goat_img).grid(column=exposed_goat_index, row=1)
    for i in range(3):
        if i != exposed_goat_index:
            Label(pc_single_p2_frame, image=curtains_img).grid(column=i, row=1)

    print("old choice: " + str(choice))
    print("expose goat: " + str(exposed_goat_index))
    ci = obj_list.index("car")
    arr = [0, 1, 2]
    arr.remove(choice)
    arr.remove(exposed_goat_index)
    print("new choice: " + str(arr[0]))
    Button(
        pc_single_p2_frame,
        text="Next Step",
        command=lambda: pc_single_run_res(pc_single_p2_frame, arr[0], ci),
    ).grid(column=1, row=2, pady=10)


def pc_single_run_res(pc_single_p2_frame, new_choice, ci):
    pc_single_res_frame = create_new_window(pc_single_p2_frame)

    text_box = Label(
        pc_single_res_frame, text="\nThe PC changed choice to No." + str(new_choice + 1)
    )
    text_box.place(relx=0.5, rely=0.2, anchor=CENTER)

    if ci == new_choice:
        Label(pc_single_res_frame, image=car_img).place(
            relx=0.5, rely=0.5, anchor=CENTER
        )
        play_sound("sounds/ApplauseSound.wav")
        text_box_res = Label(pc_single_res_frame, text="PC Won!!!")

    else:
        Label(pc_single_res_frame, image=goat_img).place(
            relx=0.5, rely=0.5, anchor=CENTER
        )
        play_sound("sounds/GoatSound.mp3")
        text_box_res = Label(pc_single_res_frame, text="PC Lost...")
    text_box_res.place(relx=0.5, rely=0.3, anchor=CENTER)

    Button(
        pc_single_res_frame,
        text="Restart",
        command=lambda: main_screen(pc_single_res_frame),
    ).place(relx=0.5, rely=0.7, anchor=CENTER)


# Function to play different sounds
def play_sound(sound_path: str):
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(loops=0)


# Initiate
root = Tk()
root.title("Monty Hall Problem")
root.geometry("650x500")
root.resizable(False, False)
pygame.mixer.init()

# Function to load image (image: name, width, height)
def load_image(image_name: str, width: int, height: int) -> PhotoImage:
    image = Image.open(image_name).resize((width, height))
    image_tk = ImageTk.PhotoImage(image)
    return image_tk


# Load images
curtains_img = load_image("images/curtains_image.webp", 200, 150)  # Curtains Image
goat_img = load_image("images/goat_image.jpg", 200, 150)  # Goat Image
car_img = load_image("images/car_image.jpg", 200, 150)  # Car Image
background_img = load_image("images/bg_img.jpg", 650, 500)  # Background Image

# Function to load main (initial) screen
def main_screen(frame=None):
    main_frame = create_new_window(frame)

    # Title
    Label(main_frame, text="Welcome To The Monty Hall Game").grid(
        column=1, row=0, pady=10
    )

    # Render 3 curtain images to screen
    for i in range(3):
        Label(main_frame, image=curtains_img).grid(column=i, row=1)

    Label(main_frame, text="Choose Game Type:").grid(column=1, row=3, pady=10)

    # PC Single-Run button
    Button(
        main_frame, text="PC Single-Run", command=lambda: pc_single_run(main_frame)
    ).grid(column=0, row=4, pady=10)
    # PC Multi-Run button
    Button(main_frame, text="Statistics", command=lambda: pc_multirun(main_frame)).grid(
        column=1, row=4, pady=10
    )
    # Human Run button
    Button(main_frame, text="Human Run", command=lambda: human_run(main_frame)).grid(
        column=2, row=4, pady=10
    )

    root.mainloop()


if __name__ == "__main__":
    main_screen()
