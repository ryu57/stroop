import expyriment
import os
import pandas as pd
import time



directory_path = "stroop_test_data/"
os.makedirs(directory_path, exist_ok=True)

# Start Expyriment
exp = expyriment.design.Experiment(name="Stroop Test")
expyriment.control.initialize(exp)
exp.mouse.show_cursor()
clock = expyriment.misc.Clock()
kb = expyriment.io.Keyboard()

# DataFrame
df_pdata = pd.DataFrame(columns=["Participant Code", "Total Correct", "Total Time","Congruent", "Correct", "Time"])

# Button Canvas
canvas = expyriment.stimuli.Canvas((700, 700))

# Button Data
button_text = ["RED", "BLUE", "GREEN", "YELLOW", "WHITE"]
colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0),  (255, 255, 0), (255, 255, 255)]
button_positions = [(-160, -60),(0, -60),(160, -60),(-80, -150),(80, -150)]


def plot_buttons(canvas):
    buttons = []
    for i in range(len(button_positions)):
        text = expyriment.stimuli.TextLine(button_text[i], text_size=30, position=button_positions[i])
        rect = expyriment.stimuli.Rectangle((140, 70), line_width = 2, position=button_positions[i])
        buttons.append((button_text[i],text,rect))
        text.plot(canvas)
        rect.plot(canvas)
    return buttons

def plot_buttons_red(canvas, match):
    buttons = []
    for i in range(len(button_positions)):
        for i in range(len(button_positions)):
            if button_text[i] == match:
                text = expyriment.stimuli.TextLine(button_text[i], text_size=30,
                                                   position=button_positions[i])
                rect = expyriment.stimuli.Rectangle((140, 70), line_width=2,
                                                    position=button_positions[
                                                        i], colour=(255, 0, 0))
                buttons.append((button_text[i], text, rect))
                text.plot(canvas)
                rect.plot(canvas)
    return buttons

def plot_buttons_green(canvas, match):
    buttons = []
    for i in range(len(button_positions)):
        if button_text[i] == match:
            text = expyriment.stimuli.TextLine(button_text[i], text_size=30,
                                               position=button_positions[i])
            rect = expyriment.stimuli.Rectangle((140, 70), line_width=2,
                                                position=button_positions[i], colour=(0,255,0))
            buttons.append((button_text[i], text, rect))
            text.plot(canvas)
            rect.plot(canvas)
    return buttons


# Trial Data
practice_trial = [(1,1),(2,4),(0,0),(0,2),(4,4),(2,1),(2,3),(2,2),(2,0),(3,3)]
trial = [[3, 3], [2, 1], [0, 0], [3, 2], [0, 0], [4, 1], [2, 3], [0, 0], [3, 0], [0, 0], [2, 4], [2, 4], [1, 3], [2, 0], [2, 3], [1, 4], [4, 3], [0, 2], [1, 3], [3, 0], [4, 0], [2, 3], [3, 1], [1, 0], [0, 4], [3, 0], [4, 1], [4, 4], [2, 0], [0, 2], [0, 1], [4, 0], [1, 1], [0, 1], [0, 3], [1, 4], [0, 0], [4, 2], [4, 4], [3, 3], [1, 1], [4, 0], [1, 0], [2, 2], [3, 1], [3, 0], [1, 4], [4, 4], [3, 0], [4, 2], [1, 1], [0, 2], [2, 4], [4, 4], [2, 4], [1, 1], [0, 0], [4, 0], [2, 1], [4, 0], [4, 2], [3, 2], [0, 3], [2, 1], [1, 1], [0, 4], [0, 0], [3, 1], [4, 3], [1, 2], [1, 2], [0, 1], [4, 0], [2, 3], [2, 0], [1, 4], [4, 4], [3, 1], [2, 1], [1, 2]]

def check_for_mouse(buttons, color):
    start_time = time.time()
    not_pressed = True
    while not_pressed:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time > 2:
            return 0, None
        exp.keyboard.check()  # Press ESC to exit
        if exp.mouse.check_button_pressed(0):
            exp.mouse.wait_press(0, wait_for_buttonup=True)
            pos = exp.mouse.position
            for button in buttons:
                if button[2].overlapping_with_position(pos, mode="surface"):
                    if button[0] == color:
                        return 1, button[0]
                    else:
                        return 0, button[0]

def run_experiment():
    # Non Trial Canvas for displaying instructions
    instruction_canvas = expyriment.stimuli.Canvas((700, 700))
    # Instruction 1
    instruction_header = expyriment.stimuli.TextLine("Press ESC to Quit Early",
                                                     text_size=60,
                                                     position=(0, 00))

    instruction_prompt = expyriment.stimuli.TextLine(
        "Press Spacebar to Continue...", text_size=30, position=(0, -200))

    instruction_header.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    kb.wait_char(' ')
    instruction_canvas.unload()


    # Ask for participant code
    name = ""
    while name == "":
        name = expyriment.io.TextInput("Participant code, to be filled by the RA:", message_text_size=30, user_text_size=30).get()

    # Instruction 1
    instruction_long_content = "In the next task of today’s study, color names will be shown in different ink colors on the screen. Your job is to ignore the word and click on the color of the ink on the screen. You will have two seconds to click after each word appears, and there will be a half-second wait time between each trial. There will be a practice round with 10 trials, after which your errors will be counted, and your time will be recorded. Again, try to be as accurate and as fast as you can. Read the instructions on the screen carefully, and call the RA whenever you need assistance. Please feel free to ask any questions you might have before moving to the next page.."
    instruction_header = expyriment.stimuli.TextLine("Instructions",
                                                     text_size=60,
                                                     position=(0, 310))
    instruction_text = expyriment.stimuli.TextBox(
        instruction_long_content,(500,500), text_size=25,
        position=(0, 0))
    instruction_prompt = expyriment.stimuli.TextLine(
        "Press Spacebar to Continue...", text_size=30, position=(0, -230))
    text = expyriment.stimuli.TextLine("GREEN", text_size=60, position=(0, 70),
                                       text_colour=(255, 0, 0))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    # text.plot(instruction_canvas)
    instruction_canvas.present()
    kb.wait_char(' ')
    instruction_canvas.unload()

    # Instruction 1
    instruction_header = expyriment.stimuli.TextLine("Instructions", text_size=60, position=(0,240))
    instruction_text = expyriment.stimuli.TextLine("You will be shown colored words like so:", text_size=30, position=(0,150))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Continue...", text_size=30, position=(0,-200))
    text = expyriment.stimuli.TextLine("GREEN", text_size=60, position=(0, 70), text_colour=(255, 0, 0))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    text.plot(instruction_canvas)
    instruction_canvas.present()
    kb.wait_char(' ')
    instruction_canvas.unload()

    # Instruction 2
    instruction_header = expyriment.stimuli.TextLine("Instructions", text_size=60, position=(0,240))
    instruction_text = expyriment.stimuli.TextLine("Click on the button that matches the colour of the word", text_size=28, position=(0,170))
    instruction_text1 = expyriment.stimuli.TextLine("as fast as possible", text_size=28, position=(0,140))
    text = expyriment.stimuli.TextLine("GREEN", text_size=60, position=(0, 70), text_colour=(255, 0, 0))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_text1.plot(instruction_canvas)
    text.plot(instruction_canvas)
    buttons = plot_buttons(instruction_canvas)

    instruction_canvas.present()
    start_time = time.time()
    clicked_colour = None
    while clicked_colour is None:
        correct, clicked_colour = check_for_mouse(buttons, "RED")

    if correct == 1:
        plot_buttons_green(instruction_canvas,clicked_colour)
    else:
        plot_buttons_red(instruction_canvas, clicked_colour)
    instruction_canvas.present()
    clock.wait(100)

    instruction_canvas.unload()

    while correct == 0:
        instruction_header = expyriment.stimuli.TextLine("Instructions",
                                                         text_size=60,
                                                         position=(0, 240))
        instruction_text = expyriment.stimuli.TextLine(
            "Try Again",
            text_size=30, position=(0, 150))

        text = expyriment.stimuli.TextLine("GREEN", text_size=60, position=(0, 70),
                                           text_colour=(255, 0, 0))
        instruction_header.plot(instruction_canvas)
        instruction_text.plot(instruction_canvas)

        text.plot(instruction_canvas)
        buttons = plot_buttons(instruction_canvas)
        instruction_canvas.present()

        clicked_colour = None
        while clicked_colour is None:
            correct, clicked_colour = check_for_mouse(buttons, "RED")

        if correct == 1:
            plot_buttons_green(instruction_canvas, clicked_colour)
        else:
            plot_buttons_red(instruction_canvas, clicked_colour)
        instruction_canvas.present()
        clock.wait(100)

        instruction_canvas.unload()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Instruction 3
    instruction_header = expyriment.stimuli.TextLine("Instructions", text_size=60, position=(0,240))
    instruction_text = expyriment.stimuli.TextLine("Correct!", text_size=40, position=(0,150))
    instruction_time = expyriment.stimuli.TextLine(f"Time Taken: {elapsed_time:.3f} seconds", text_size=35, position=(0,80))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Continue...", text_size=30, position=(0,-200))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_time.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char(' ')

    # Instruction 3
    instruction_header = expyriment.stimuli.TextLine("Instructions",
                                                     text_size=60,
                                                     position=(0, 240))
    if elapsed_time > 2:
        instruction_time = expyriment.stimuli.TextLine(
            f"Time Taken: {elapsed_time:.3f} seconds", text_size=35,
            position=(0, 80), text_colour=(255,0,0))
        instruction_text1 = expyriment.stimuli.TextLine(
            "Too Slow! You will only have 2 seconds in the actual task", text_size=26, position=(0, 0))
    else:
        instruction_time = expyriment.stimuli.TextLine(
            f"Time Taken: {elapsed_time:.3f} seconds", text_size=35,
            position=(0, 80), text_colour=(0, 255, 0))
        instruction_text1 = expyriment.stimuli.TextLine(
            "Good Job! You clicked within 2 seconds", text_size=40, position=(0, 0))
    instruction_prompt = expyriment.stimuli.TextLine(
        "Press Spacebar to Continue...", text_size=30, position=(0, -200))

    instruction_header.plot(instruction_canvas)
    # instruction_text.plot(instruction_canvas)
    instruction_time.plot(instruction_canvas)
    instruction_text1.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char(' ')

    repeat = True
    while repeat:
        # Instruction 4
        instruction_header = expyriment.stimuli.TextLine("Practice Round", text_size=60, position=(0,240))
        instruction_text1 = expyriment.stimuli.TextLine("When you are ready", text_size=30, position=(0,-150))
        instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Start...", text_size=30, position=(0,-200))

        instruction_header.plot(instruction_canvas)
        instruction_text1.plot(instruction_canvas)
        instruction_prompt.plot(instruction_canvas)
        instruction_canvas.present()
        instruction_canvas.unload()
        kb.wait_char(' ')

        fs = expyriment.stimuli.FixCross(size=(25, 25), line_width=3, colour=(127, 127, 127))

        # Practice Trial
        correct_total = 0
        for i in range(len(practice_trial)):
            fs.present()
            clock.wait(150)
            canvas.unload()
            text = expyriment.stimuli.TextLine(button_text[practice_trial[i][0]], text_size=60, position=(0, 70), text_colour=colors[practice_trial[i][1]])
            text.plot(canvas)
            buttons = plot_buttons(canvas)
            canvas.present()
            correct, clicked_colour = check_for_mouse(buttons, button_text[practice_trial[i][1]])
            correct_total += correct

            if clicked_colour is not None:
                if correct == 1:
                    plot_buttons_green(canvas, clicked_colour)
                else:
                    plot_buttons_red(canvas, clicked_colour)
                canvas.present()
                clock.wait(100)
            canvas.unload()

            if clicked_colour is None:
                result_text = expyriment.stimuli.TextLine("Too Slow!",
                                                             text_size=60,
                                                             position=(0, 0), text_colour=(255,0,0))
            elif correct == 1:
                result_text = expyriment.stimuli.TextLine("Correct!",
                                                          text_size=60,
                                                          position=(0, 0),
                                                          text_colour=(0, 255, 0))
            else:
                result_text = expyriment.stimuli.TextLine("Wrong!",
                                                          text_size=60,
                                                          position=(0, 0),
                                                          text_colour=(255, 0, 0))
            result_text.present()
            clock.wait(1000)


        # Instruction 5
        instruction_header = expyriment.stimuli.TextLine("Practice Results", text_size=60, position=(0,240))
        instruction_text = expyriment.stimuli.TextLine(f"{correct_total} out of 10 Correct", text_size=40, position=(0,150))

        instruction_prompt2 = expyriment.stimuli.TextLine(
            "Press R to Try Again", text_size=30, position=(0, -150))
        instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Proceed...", text_size=30, position=(0,-200))

        instruction_header.plot(instruction_canvas)
        instruction_text.plot(instruction_canvas)
        instruction_prompt.plot(instruction_canvas)
        instruction_prompt2.plot(instruction_canvas)
        instruction_canvas.present()
        instruction_canvas.unload()
        key, rt = kb.wait_char(["r", " "])
        if key == " ":
            repeat = False

    # Instruction 6
    instruction_text1 = expyriment.stimuli.TextLine("The Actual Task is Next", text_size=40, position=(0,80))
    instruction_text2 = expyriment.stimuli.TextLine("If you have any questions for the RA",
                                                    text_size=30,
                                                    position=(0, 20))
    instruction_text3 = expyriment.stimuli.TextLine(
        "Now is the time",
        text_size=30,
        position=(0, -20))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Continue...", text_size=30, position=(0,-200))

    instruction_text3.plot(instruction_canvas)
    instruction_text2.plot(instruction_canvas)
    instruction_text1.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char(' ')

    # Instruction 7
    instruction_text = expyriment.stimuli.TextLine("Remember to click as fast as possible", text_size=40, position=(0,150))
    instruction_text1 = expyriment.stimuli.TextLine("When you are ready", text_size=30, position=(0,-150))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Start...", text_size=30, position=(0,-200))

    instruction_text.plot(instruction_canvas)
    instruction_text1.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char(' ')

    # Trial
    correct_total = 0
    congruency = []
    correctness = []
    react_time = []
    for i in range(len(trial)):
        fs.present()
        clock.wait(150)
        canvas.unload()
        text = expyriment.stimuli.TextLine(button_text[trial[i][0]], text_size=60, position=(0, 70), text_colour=colors[trial[i][1]])
        text.plot(canvas)
        buttons = plot_buttons(canvas)
        canvas.present()

        start_time = time.time()
        correct, clicked_colour = check_for_mouse(buttons, button_text[trial[i][1]])
        end_time = time.time()
        elapsed_time = end_time - start_time

        if clicked_colour is not None:
            if correct == 1:
                plot_buttons_green(canvas, clicked_colour)
            else:
                plot_buttons_red(canvas, clicked_colour)
            canvas.present()
            clock.wait(100)
        canvas.unload()

        correct_total += correct
        if correct == 1:
            correctness.append(True)
        else:
            correctness.append(False)

        if trial[i][0] == trial[i][1]:
            congruency.append(True)
        else:
            congruency.append(False)

        react_time.append(elapsed_time * 1000)

        if clicked_colour is None:
            result_text = expyriment.stimuli.TextLine("Too Slow!",
                                                         text_size=60,
                                                         position=(0, 0), text_colour=(255,0,0))
        elif correct == 1:
            result_text = expyriment.stimuli.TextLine("Correct!",
                                                      text_size=60,
                                                      position=(0, 0),
                                                      text_colour=(0, 255, 0))
        else:
            result_text = expyriment.stimuli.TextLine("Wrong!",
                                                      text_size=60,
                                                      position=(0, 0),
                                                      text_colour=(255, 0, 0))
        result_text.present()
        clock.wait(1000)

    df_pdata["Congruent"] = congruency
    df_pdata["Correct"] = correctness
    df_pdata["Time"] = react_time
    df_pdata["Participant Code"] = [name] + [None] * (len(correctness) - 1)
    df_pdata["Total Time"] = [sum(react_time)] + [None] * (len(correctness) - 1)
    df_pdata["Total Correct"] = [sum(correctness)] + [None] * (len(correctness) - 1)

    # Instruction 8
    instruction_header = expyriment.stimuli.TextLine("Trial Results", text_size=60, position=(0,240))
    instruction_text = expyriment.stimuli.TextLine(f"{correct_total} out of 80 Correct", text_size=40, position=(0,150))
    instruction_prompt = expyriment.stimuli.TextLine("Press Spacebar to Continue...", text_size=30, position=(0,-200))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_prompt.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char(' ')

    # Instruction 9
    instruction_header = expyriment.stimuli.TextLine("Thank You", text_size=60, position=(0,240))
    instruction_text = expyriment.stimuli.TextLine(f"The RA will take over from here", text_size=40, position=(0,150))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char('\r\n')

    # Save and upload data
    final_file_directory = "stroop_test_data/"
    final_file_name = f"stroop_data_{name}.csv"
    df_pdata.to_csv(final_file_directory + final_file_name, index=False)



    # Instruction 10
    instruction_header = expyriment.stimuli.TextLine("Please Remain At Your Seat",
                                                     text_size=55,
                                                     position=(0, 240))
    instruction_text = expyriment.stimuli.TextLine(
        f"The RA will prepare the next task", text_size=40, position=(0, 150))

    instruction_header.plot(instruction_canvas)
    instruction_text.plot(instruction_canvas)
    instruction_canvas.present()
    instruction_canvas.unload()
    kb.wait_char('\r\n')

    expyriment.control.end()

