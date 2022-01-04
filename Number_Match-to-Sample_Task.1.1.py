'''
This is a fac-simile of the experiment used in my master's thesis.
The experimental paradigm is a Match-to-Sample, in which a sample and a target stimulus are displayed sequentially in time.
In the first block, sample and target are both dots (non-symbolic), while in the second block the target is an Arabic digit.
The subject is required to tell whethet the quantity between the sample and the target is equal or not.
Timing is identical to that one used in my thesis, while numerosity range has been increased (from 8 to 10).
Difference between sample and target is always 1 at maximum (so 'distance effect' is always identical).
Size and coordinates design has been improved and constructed by using python also.

Python 3.8.8, pygame 2.1.0, psychopy 2021.2.3
Number_Match-to-Sample_Task.1.1.py
'''

# Importing many important modules
import os
from datetime import datetime
from psychopy import logging, visual, core, event, clock, gui
import numpy as np
import pandas as pd
import random

from Constants_NMTS import n_max, n_rep, positions_array_from_constants, s_min, s_max, DISPSIZE, fullscr

# Clear the command output / set the logging to critical
os.system('cls' if os.name == 'nt' else 'clear')
logging.console.setLevel(logging.CRITICAL)
print('************************************************')
print('"NUMBER" MATCH-TO-SAMPLE TASK: version alpha')
print('************************************************')
print(datetime.now())
print('************************************************')

# Create structure and trials
positions_array = positions_array_from_constants # Store in a vector
sizes_array = list(range(s_min, s_max)) # A vector of  values for the radius od each dot
sizes_array = np.tile(sizes_array, n_rep) # Augment the pool of the sizes

n_max = n_max # Max number of dots
n_sample_circles_array = [] # To append later
n_target_circles_array = [] # To append later
seq_sample_array = [] # To append later
trial_type_array = [] # To append later

for n_max in range(0, n_max):
    if n_max + 1 == 1 or n_max + 1 == 10: # Number '1' and '10' are repeated only two times, because '0' and '11' are excluded
        n_sample_circles_array.append(n_max + 1)
        n_sample_circles_array.append(n_max + 1)
    else:
        n_sample_circles_array.append(n_max + 1) # Every other number is repeated three times
        n_sample_circles_array.append(n_max + 1)
        n_sample_circles_array.append(n_max + 1)

    seq_sample_array.append(n_max + 1) # Just to create the target structure

    n_target_circles_array.append(seq_sample_array[n_max] - 1) # The gap between the sample and the target is '1' at max. Conditions are '-1' and '1' (non-match) and 0 (match)
    n_target_circles_array.append(seq_sample_array[n_max])
    n_target_circles_array.append(seq_sample_array[n_max] + 1)

n_target_circles_array = [exc for exc in n_target_circles_array if exc != 0] # '0' and '11' are excluded
n_target_circles_array = [exc for exc in n_target_circles_array if exc != 11]

n_sample_circles_array = np.tile(n_sample_circles_array, n_rep) # Sample and target arrays are doubled
n_target_circles_array = np.tile(n_target_circles_array, n_rep)

for i in range(0, len(n_sample_circles_array)): # Match trials are referred to as '1', non-match as '0'
    if n_sample_circles_array[i] == n_target_circles_array[i]:
        trial_type_array.append(1)
    else:
        trial_type_array.append(0)

conditions = pd.DataFrame({'Sample': n_sample_circles_array,
                            'Target': n_target_circles_array,
                            'Trial Type': trial_type_array
                            }) # Create a pandas dataframe
conditions_random = conditions.sample(frac=1) # Randomize trials, 56 per block

# Define variables to declare
trial_no_array = [] # Number of total trials
sub_id_array = [] # To append later
date_value_array = [] # To append later
date_val = datetime.now().strftime('%d%m%Y')
time_value_array = [] # To append later
click_key_array = [] # To append later
final_n_sample_circles_array = [] # The real sequence of  used by the loop. To append later
final_n_target_circles_array = [] # The real sequence of used by the loop. To append later
final_trial_type_array = []  # The real sequence of match/non-match trials used by the loop. To append later
response_latency = [] # To append later

# Setup our experiment
myDlg = gui.Dlg(title = '"Number" Match-to-Sample Task (version alpha)') # The dialog window poping when experiment opens
myDlg.addText('Subject Info')
myDlg.addField('Exp Date', date_val)
myDlg.addField('Number:')
myDlg.addField('Sex:', choices = ['Male', 'Female', 'Prefer not to say'])
myDlg.addField('Age:')
show_dlg = myDlg.show()

if myDlg.OK:
    print(show_dlg)
    save_file_name = show_dlg[0] + '_' + show_dlg[1] + '_NMTS.csv'
    print(save_file_name)

else:
    print('User cancelled')

# Create a save filepath (GUI)
save_path = gui.fileSaveDlg(initFileName = save_file_name, prompt = 'Select Save File')
print('Output form save dialog')
print(save_path)

if save_path == None:
    print('Experiment must be saved first')
    core.quit()

# Create window
window = visual.Window(size = DISPSIZE,
                        color = (0, 0, 0),
                        fullscr = fullscr,
                        monitor = 'testMonitor',
                        screen = 1,
                        allowGUI = True,
                        pos = (0, 0),
                        units = 'pix')

# Create mouse input
mouse = event.Mouse(visible = False,
                    win = window)

# Create fixation cross
def fixation_cross():
    fix_cross_horiz = visual.Rect(window,
                                  width = 15,
                                  height = 1.5,
                                  units = 'pix',
                                  lineColor = [-1,-1,-1],
                                  fillColor = [-1,-1,-1],
                                  pos = (0,0))
    fix_cross_vert = visual.Rect(window,
                                 width = 1.5,
                                 height = 15,
                                 units = 'pix',
                                 lineColor = [-1,-1,-1],
                                 fillColor = [-1,-1,-1],
                                 pos = (0,0))
    fix_cross_horiz.draw() #This will draw the line onto the window
    fix_cross_vert.draw()

# Create blank screen
def blank_screen():
    blank = visual.Rect(window,
                        width = DISPSIZE[0],
                        height = DISPSIZE[1],
                        units = 'pix',
                        lineColor = [0, 0, 0],
                        fillColor = [0, 0, 0],
                        pos = (0,0))
    blank.draw()

# Create non-symbolic stimulus
def stimulus(number, color, positions, sizes):
    stim = visual.ElementArrayStim(window,
                                    units = 'pix',
                                    fieldPos = (0, 0),
                                    fieldSize = (800, 800),
                                    fieldShape = 'sqr',
                                    nElements = number,
                                    xys = positions,
                                    elementTex = None,
                                    elementMask = "circle",
                                    sizes = sizes,
                                    colors = color)
    stim.draw()

# Create symbolic stimulus
def sym_stimulus(number):
    digit = visual.TextStim(window,
                                text = number,
                                pos = (0, 0),
                                color = (-1, -1, -1),
                                units = 'pix',
                                height = 45,
                                bold = True)
    digit.draw()

# Create two styles of text
def text_bold(text, pos = (0, 0)): # Default position is set at 0,0
    text_bold = visual.TextStim(window,
                                text = text,
                                pos = pos,
                                color = (-1, -1, -1),
                                units = 'pix',
                                height = 32,
                                bold = True)
    text_bold.draw()

def text(text, pos = (0, 0)):
    text = visual.TextStim(window,
                                text = text,
                                pos = pos,
                                color = (-1, -1, -1),
                                units = 'pix',
                                height = 32)
    text.draw()

# Wait for subjects to press enter (when they're ready)
text_bold('PRESS ENTER TO START')
window.flip()

key = event.waitKeys(maxWait = 9999,
                     keyList = ('return', 'q'),
                     clearEvents = True)

if 'return' in key:
    window.flip()
    pass # Go on in the code

if 'q' in key: # Exit whenever you want
    window.close()
    core.quit()
    print('OK, program and window closed.')

# Update the subject on what task to do (training)
text('This is the Training Block', (0, 200))
text('YOU ARE GOING TO SEE SETS OF DOTS:', (0, 100))
text_bold('IF NUMEROSITY IS THE SAME PRESS THE LEFT KEY', (0, 0))
text_bold('OTHERWISE PRESS THE RIGHT KEY', (0, -100))
text('Press Enter to Start', (0, -200))
window.flip()

keys = event.waitKeys(maxWait = 9999,
                      keyList = ['return','q'],
                      clearEvents = True)

if 'return' in key:
    window.flip()
    pass # Go on in the code

if 'q' in keys:
    window.close()
    core.quit()

# Training loop (non-symbolic)
for i in range(0, 5):

    event.clearEvents()
    fixation_cross()
    window.flip()
    core.wait(0.4)

    positions = []
    np.random.shuffle(positions_array)
    for n in range(0, conditions_random.iloc[i, 0]):
        positions.append(positions_array[n])

    sizes = []
    np.random.shuffle(sizes_array)
    for n in range(0, conditions_random.iloc[i, 0]):
        sizes.append([sizes_array[n]])

    blank_screen()
    core.wait(0.15)

    stimulus(conditions_random.iloc[i, 0], [-1, -1, -1], positions, sizes)
    window.flip()
    core.wait(0.3)

    positions = []
    np.random.shuffle(positions_array)
    for n in range(0, conditions_random.iloc[i, 1]):
        positions.append(positions_array[n])

    sizes = []
    np.random.shuffle(sizes_array)
    for n in range(0, conditions_random.iloc[i, 1]):
        sizes.append([sizes_array[n]])

    event.clearEvents()
    blank_screen()
    window.flip()
    core.wait(1)

    event.clearEvents()

    clock = core.Clock()
    clock.add(2)

    while clock.getTime() < 0.0:

        click = mouse.getPressed(getTime = True)

        stimulus(conditions_random.iloc[i, 1], [1, 1, 1], positions, sizes)
        window.flip()

        quitkey = event.getKeys(keyList = ['q'])
        if 'q' in quitkey:
            window.close()
            core.quit()

        elif click[0][0]:
            break

        elif click[0][2]:
            break

        while clock.getTime() > 0.0:

            click = mouse.getPressed(getTime = True)
            window.flip()

            quitkey = event.getKeys(keyList = ['q'])
            if 'q' in quitkey:
                window.close()
                core.quit()

            elif click[0][0]:
                break

            elif click[0][2]:
                break

# Update the subject on what task to do (test)
text('This is the Test Block', (0, 200))
text('YOU ARE GOING TO SEE SETS OF DOTS:', (0, 100))
text_bold('IF NUMEROSITY IS THE SAME PRESS THE LEFT KEY', (0, 0))
text_bold('OTHERWISE PRESS THE RIGHT KEY', (0, -100))
text('Press Enter to Start', (0, -200))

window.flip()

keys = event.waitKeys(maxWait = 9999,
                      keyList = ['return','q'],
                      clearEvents = True)

if 'return' in key:
    window.flip()
    pass # Go on in the code

if 'q' in keys:
    window.close()
    core.quit()

# Main loop (non-symbolic)
for i in range(0, len(n_sample_circles_array)):

    trial_no_array.append(i)
    sub_id_array.append(show_dlg[1])
    date_value_array.append(date_val)
    time_value_array.append(datetime.now().strftime('%H%M%S'))

    final_n_sample_circles_array.append(conditions_random.iloc[i, 0])
    final_n_target_circles_array.append(conditions_random.iloc[i, 1])
    final_trial_type_array.append(conditions_random.iloc[i, 2])

    event.clearEvents() # Avoid bugs
    fixation_cross()
    window.flip()
    core.wait(0.4)

    positions = [] # This vector is emptied every iteration
    np.random.shuffle(positions_array)
    for n in range(0, conditions_random.iloc[i, 0]):
        positions.append(positions_array[n]) # The length of 'position' vector is dependent on the 'number' expressed in the dataframe column,
                                            # as a consequence a specic number of coordinates (couple) are extracted from the initial array

    sizes = [] # This vector is emptied every iteration
    np.random.shuffle(sizes_array)
    for n in range(0, conditions_random.iloc[i, 0]):
        sizes.append([sizes_array[n]]) # The length of 'sizes' vector is dependent on the 'number' expressed in the dataframe column,
                                            # as a consequence a specic number of sizes are extracted from the initial array

    blank_screen()
    core.wait(0.15)

    stimulus(conditions_random.iloc[i, 0], [-1, -1, -1], positions, sizes) # Sample stimulus is always black
    window.flip()
    core.wait(0.3)

    positions = [] # This vector is emptied every iteration again for the target construction
    np.random.shuffle(positions_array)
    for n in range(0, conditions_random.iloc[i, 1]):
        positions.append(positions_array[n]) # Functioning is the same

    sizes = [] # This vector is emptied every iteration again for the target construction
    np.random.shuffle(sizes_array)
    for n in range(0, conditions_random.iloc[i, 1]):
        sizes.append([sizes_array[n]]) # Functioning is the same

    event.clearEvents() # Avoid bugs
    blank_screen()
    window.flip()
    core.wait(1)
    event.clearEvents() # Avoid bugs

    clock = core.Clock()
    clock.add(2) # Duration of the target stimulus

    start_time = clock.getTime() # Starting our timer

    while clock.getTime() < 0.0:

        click = mouse.getPressed(getTime = True)

        stimulus(conditions_random.iloc[i, 1], [1, 1, 1], positions, sizes)
        window.flip()

        quitkey = event.getKeys(keyList = ['q'])
        if 'q' in quitkey:
            window.close()
            core.quit()

        elif click[0][0]: # In case of left key
            stop_timer = clock.getTime()
            response = 0 # It is stored as '0'
            break

        elif click[0][2]:  # In case of right key
            stop_timer = clock.getTime()
            response = 2 # It is stored as '2'
            break

        while clock.getTime() > 0.0: # When time is expired, stimulus disappears, blank screen is displayed for a infinite time
                                    # Commands are the same

            click = mouse.getPressed(getTime = True)
            window.flip()

            quitkey = event.getKeys(keyList = ['q'])
            if 'q' in quitkey:
                window.close()
                core.quit()

            elif click[0][0]:
                stop_timer = clock.getTime()
                response = 0
                break

            elif click[0][2]:
                stop_timer = clock.getTime()
                response = 2
                break

    click_key_array.append(response)
    response_latency.append('%.4f' %((stop_timer - start_time)*1000)) # Rounded to four digits. Converted in milliseconds

########################################################################################################################################################################

# Define variables to declare
trial_no_sym_array = []
sub_id_array = []
time_value_sym_array = []
click_key_sym_array = []
final_n_sample_sym__array = [] # Conditions are identical to those ones in the previous block
final_n_target_sym__array = []
final_trial_type_sym_array = []
response_latency_sym = []

# Update the subject on what task to do (training)
text('This is the Training Block', (0, 200))
text('YOU ARE GOING TO SEE SETS OF DOTS AND DIGITS:', (0, 100))
text_bold('IF NUMEROSITY IS THE SAME PRESS THE LEFT KEY', (0, 0))
text_bold('OTHERWISE PRESS THE RIGHT KEY', (0, -100))
text('Press Enter to Start', (0, -200))
window.flip()

keys = event.waitKeys(maxWait = 9999,
                      keyList = ['return','q'],
                      clearEvents = True)

if 'return' in key:
    window.flip()
    pass # Go on in the code

if 'q' in keys:
    window.close()
    core.quit()

# Training loop (symbolic)
for i in range(0, 5):

    event.clearEvents()
    fixation_cross()
    window.flip()
    core.wait(0.4)

    positions = []
    np.random.shuffle(positions_array)
    for n in range(0, conditions_random.iloc[i, 0]):
        positions.append(positions_array[n])

    sizes = []
    np.random.shuffle(sizes_array)
    for n in range(0, conditions_random.iloc[i, 0]):
        sizes.append([sizes_array[n]])

    blank_screen()
    core.wait(0.15)

    stimulus(conditions_random.iloc[i, 0], [-1, -1, -1], positions, sizes) # Sample is always a set of dots
    window.flip()
    core.wait(0.3)

    event.clearEvents()
    blank_screen()
    window.flip()
    core.wait(1)
    event.clearEvents()

    clock = core.Clock()
    clock.add(2)

    while clock.getTime() < 0.0:

        click = mouse.getPressed(getTime = True)

        sym_stimulus(conditions_random.iloc[i, 1]) # This time, target is a digit, only numeorsity changes. Size and position don't
        window.flip()

        quitkey = event.getKeys(keyList = ['q'])
        if 'q' in quitkey:
            window.close()
            core.quit()

        elif click[0][0]:
            break

        elif click[0][2]:
            break

        while clock.getTime() > 0.0:

            click = mouse.getPressed(getTime = True)
            window.flip()

            quitkey = event.getKeys(keyList = ['q'])
            if 'q' in quitkey:
                window.close()
                core.quit()

            elif click[0][0]:
                break

            elif click[0][2]:
                break

# Update the subject on what task to do (Test)
text('This is the Test Block', (0, 200))
text('YOU ARE GOING TO SEE SETS OF DOTS AND DIGITS:', (0, 100))
text_bold('IF NUMEROSITY IS THE SAME PRESS THE LEFT KEY', (0, 0))
text_bold('OTHERWISE PRESS THE RIGHT KEY', (0, -100))
text('Press Enter to Start', (0, -200))
window.flip()

keys = event.waitKeys(maxWait = 9999,
                      keyList = ['return','q'],
                      clearEvents = True)

if 'return' in key:
    window.flip()
    pass # Go on in the code

if 'q' in keys:
    window.close()
    core.quit()

# Main loop (symbolic)
for i in range(0, len(n_sample_circles_array)):

    trial_no_sym_array.append(i)
    sub_id_array.append(show_dlg[1])
    time_value_sym_array.append(datetime.now().strftime('%H%M%S'))
    final_n_sample_sym__array.append(conditions_random.iloc[i, 0])
    final_n_target_sym__array.append(conditions_random.iloc[i, 1])
    final_trial_type_sym_array.append(conditions_random.iloc[i, 2])

    event.clearEvents()
    fixation_cross()
    window.flip()
    core.wait(0.4)

    positions = []
    np.random.shuffle(positions_array)
    for n in range(0, conditions_random.iloc[i, 0]):
        positions.append(positions_array[n])

    sizes = []
    np.random.shuffle(sizes_array)
    for n in range(0, conditions_random.iloc[i, 0]):
        sizes.append([sizes_array[n]])

    blank_screen()
    core.wait(0.15)

    stimulus(conditions_random.iloc[i, 0], [-1, -1, -1], positions, sizes)
    window.flip()
    core.wait(0.3)

    event.clearEvents()
    blank_screen()
    window.flip()
    core.wait(1)
    event.clearEvents()

    clock = core.Clock()
    clock.add(2)

    start_time = clock.getTime() # Starting our timer

    while clock.getTime() < 0.0:

        click = mouse.getPressed(getTime = True)

        sym_stimulus(conditions_random.iloc[i, 1])
        window.flip()

        quitkey = event.getKeys(keyList = ['q'])
        if 'q' in quitkey:
            window.close()
            core.quit()

        elif click[0][0]:
            stop_timer = clock.getTime()
            response = 0
            break

        elif click[0][2]:
            stop_timer = clock.getTime()
            response = 2
            break

        while clock.getTime() > 0.0:

            click = mouse.getPressed(getTime = True)
            window.flip()

            quitkey = event.getKeys(keyList = ['q'])
            if 'q' in quitkey:
                window.close()
                core.quit()

            elif click[0][0]:
                stop_timer = clock.getTime()
                response = 0
                break

            elif click[0][2]:
                stop_timer = clock.getTime()
                response = 2
                break

    click_key_sym_array.append(response)
    response_latency_sym.append('%.4f' %((stop_timer - start_time)*1000)) # Rounded to four digits. Converted in milliseconds

# Create our output table in pandas including all blocks
output_file = pd.DataFrame({'SubID': sub_id_array,
                            'Trial_No': trial_no_array,
                            'Date': date_value_array,
                            'Time': time_value_array,
                            'Real Sample': final_n_sample_circles_array,
                            'Real Target': final_n_target_circles_array,
                            'Real Trial Type': final_trial_type_array,
                            'Sub_response': click_key_array,
                            'Latency_ms': response_latency,
                            'Trial_No_Sym': trial_no_sym_array,
                            'Time_Sym': time_value_sym_array,
                            'Real Sym Sample': final_n_sample_sym__array,
                            'Real Sym Target': final_n_target_sym__array,
                            'Real Sym Trial Type': final_trial_type_sym_array,
                            'Sub_response_sym': click_key_sym_array,
                            'Latency_ms_sym': response_latency_sym
                            })

output_file.to_csv(save_file_name, sep = ',', index = True) # Saving it as .csv in the path declared at the start.

# Thanks
text_bold('THANK YOU FOR YOUR TIME')
window.flip()
core.wait(3)

window.close()
print('OK, program and window closed.')
