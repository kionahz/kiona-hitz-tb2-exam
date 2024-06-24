import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

# define color variables
bg_color = '#44464a'
bg_lighter_color = '#707070'
button_color = '#31353d'
button_selected_color = '#607d8b'
button_cta_color = '#358477'

# define font variables
font_heading1 = 'arial 18 bold'
font_heading2 = 'arial 15 bold'
font_text = 'arial 15'

# definition of global data variables, to ensure that the variables can be changed inside of functions
# calendar page
calendar_week = 38
buttons_string = ''

# personal data page
firstname = ''
lastname = ''
email = ''
library = ''
address = ''
birthday = ''

card_visibility = False


# load the Welcome Page
def load_page_welcome():

    # login button and create user button
    # User in db hinterlegen
    # user mit db vergleichen
    # admin bekommt extra button zum drucken der tabelle
    #

    # destroy the Welcome page and open the Calendar Page
    def press_start_page_calendar():
        page_welcome.destroy()
        load_page_calendar()

    # Welcome label
    welcome_label = tk.Label(page_welcome, text='Welcome to the\nVideo Studio\nCalendar\nPress REC to begin',
                             font=font_heading2, bg='black', fg='white')
    welcome_label.place(relx=0.365, rely=0.49, relwidth=0.14, relheight=0.16, anchor='center')

    # create Play Button with a photo as the button
    # open image play button
    open_play_image = Image.open('images/record_button.png')
    # resize image
    resized_play = open_play_image.resize((70, 70), Image.LANCZOS)
    play_image = ImageTk.PhotoImage(resized_play)
    # create label with the resized image
    info_label = tk.Label(page_welcome, image=play_image)
    info_label.image = play_image
    # make it into a button and reshape cursor, to make the button more visible
    play_button = tk.Button(page_welcome,
                            image=play_image,
                            bg='black',
                            cursor='hand2',
                            activebackground='black',
                            activeforeground='white',
                            command=lambda: press_start_page_calendar(),
                            borderwidth=0)
    play_button.place(relx=0.53, rely=0.55, anchor='center')


# load the Calendar Page
# in a later version the booking data will be stored in a database, and the already booked timeslots will be displayed
# in a different color, and will not be selectable,
# this is not implemented here, because it is outside my current knowledge
def load_page_calendar():
    # retrieve the variable, to change it inside this function
    global calendar_week

    # increment week when the next week button is clicked
    def next_week():
        global calendar_week
        # there aren´t more than 52 weeks in a year
        if calendar_week < 52:
            calendar_week += 1
        refresh_timetable()

    # decrement week when the last week button is clicked
    def last_week():
        global calendar_week
        # there aren´t less than 1 week in a year
        if calendar_week > 1:
            calendar_week -= 1
        refresh_timetable()

    # refresh the timetable to display the new week
    def refresh_timetable():
        timetable_frame.destroy()
        load_page_calendar()

    # create list to store which time slots where clicked
    clicked_timeslots = []

    # define what happens when a timeslot button is clicked, (transfer the text of the clicked button)
    def on_button_click(text):
        # go through all the child widgets
        for button in timetable_frame.winfo_children():
            # check if the widget is a button, since there are other widget types than only buttons
            # in the child widgets, and the text matches the text of the button,
            # to find the button that matches the text that was transferred
            if type(button) is tk.Button and button['text'] == text:
                # check if the timeslot is already in the list
                if button in clicked_timeslots:
                    # remove timeslot from the list and change color back to button_color when deselected
                    clicked_timeslots.remove(button)
                    button.config(bg=button_color)
                else:
                    # add timeslot to the list and change color when selected
                    clicked_timeslots.append(button)
                    button.config(bg=button_selected_color)
                # refresh the list and break the loop when clicked timeslot is found
                sort_clicked_timeslots()
                break

    # sort the clicked buttons list, by day and then by time
    def sort_clicked_timeslots():

        # retrieve the variable, to change it inside this function
        global buttons_string

        # function that returns the sort value of a given timeslot text
        def sort_key(timeslot_text):
            # define the value, by which the list should be sorted
            weekdays_order = {'MON': 1, 'TUE': 2, 'WED': 3, 'THU': 4, 'FRI': 5}
            time_order = {'8:15': 1, '10:15': 2, '12:15': 3, '14:15': 4, '16:15': 5}

            # since it should be sorted by two different values, the button text that was transferred,
            # needs to be split into two parts, separated by the space,which is the default parameter
            parts = timeslot_text.split()
            weekday = parts[0]
            time = parts[1]

            # return the sort values of the weekday and time (numbers 1-5) of the given timeslot text
            return weekdays_order[weekday], time_order[time]

        # create a list of the text of the buttons which are currently in the clicked_timeslots list
        clicked_button_texts = [button['text'] for button in clicked_timeslots]
        # the above created list will be sorted with the values of the function sort_key
        sorted_buttons = sorted(clicked_button_texts, key=sort_key)
        # convert the list into a string
        buttons_string = ", ".join(sorted_buttons)

    # destroy the Calendar page and open the Personal Data Page
    def press_start_page_persdata():
        page_calendar.destroy()
        load_page_persdata()

    # create the Calendar page frame
    page_calendar = tk.Frame(root, bg=bg_color)
    page_calendar.place(x=0, y=0, relwidth=1, relheight=1)
    # header
    header_label = tk.Label(page_calendar, text='Here you can book timeslots for the Video Studio'
                                                'at the Leuphana University Lüneburg.\n'
                                                'Please select a week and then up to 5 timeslots'
                                                'within this week.',
                            font=font_heading1, bg=bg_color, fg='white')
    header_label.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.2, anchor='center')

    # Calendar Week change frame
    change_calendar_week_frame = tk.LabelFrame(page_calendar, bg=bg_lighter_color)
    change_calendar_week_frame.place(relx=0.075, rely=0.2, relwidth=0.7, relheight=0.1)
    # widgets
    last_week_button = tk.Button(change_calendar_week_frame, text=' < Last Week', font=font_text,
                                 bg=button_color, fg='white',
                                 relief=tk.RAISED, borderwidth=5, command=lambda: last_week())
    calendar_week_label = tk.Label(change_calendar_week_frame, text=f'Week {calendar_week}', font=font_text,
                                   bg=bg_lighter_color, fg='white')
    next_week_button = tk.Button(change_calendar_week_frame, text='Next Week >', font=font_text, bg=button_color,
                                 fg='white',
                                 relief=tk.RAISED, borderwidth=5, command=lambda: next_week())
    # layout
    last_week_button.place(relx=0.25, rely=0.1, relwidth=0.17, relheight=0.8, anchor='n')
    next_week_button.place(relx=0.75, rely=0.1, relwidth=0.17, relheight=0.8, anchor='n')
    calendar_week_label.place(relx=0.5, rely=0, relwidth=0.33, relheight=1, anchor='n')

    # timetable frame
    timetable_frame = tk.LabelFrame(page_calendar, bg=bg_color)
    timetable_frame.place(relx=0.075, rely=0.3, relwidth=0.7, relheight=0.5)
    # weekday labels
    monday_label = tk.Label(timetable_frame, text='Monday', font=font_text, bg=bg_color, fg='white')
    tuesday_label = tk.Label(timetable_frame, text='Tuesday', font=font_text, bg=bg_color, fg='white')
    wednesday_label = tk.Label(timetable_frame, text='Wednesday', font=font_text, bg=bg_color, fg='white')
    thursday_label = tk.Label(timetable_frame, text='Thursday', font=font_text, bg=bg_color, fg='white')
    friday_label = tk.Label(timetable_frame, text='Friday', font=font_text, bg=bg_color, fg='white')
    # hour labels
    eight_label = tk.Label(timetable_frame, text='8:15-9:45', font=font_text, bg=bg_color, fg='white')
    ten_label = tk.Label(timetable_frame, text='10:15-11:45', font=font_text, bg=bg_color, fg='white')
    twelve_label = tk.Label(timetable_frame, text='12:15-13:45', font=font_text, bg=bg_color, fg='white')
    fourteen_label = tk.Label(timetable_frame, text='14:15-15:45', font=font_text, bg=bg_color, fg='white')
    sixteen_label = tk.Label(timetable_frame, text='16:15-17:45', font=font_text, bg=bg_color, fg='white')
    empty_label = tk.Label(timetable_frame, text='', bg=bg_color)
    # weekday layout
    monday_label.place(relx=0.25, rely=0, relwidth=0.167, relheight=0.167, anchor='n')
    tuesday_label.place(relx=0.5, rely=0, relwidth=0.167, relheight=0.167, anchor='ne')
    wednesday_label.place(relx=0.5, rely=0, relwidth=0.167, relheight=0.167)
    thursday_label.place(relx=0.75, rely=0, relwidth=0.167, relheight=0.167, anchor='n')
    friday_label.place(relx=1, rely=0, relwidth=0.167, relheight=0.167, anchor='ne')
    # hour layout
    eight_label.place(relx=0, rely=0.25, relwidth=0.167, relheight=0.167, anchor='w')
    ten_label.place(relx=0, rely=0.5, relwidth=0.167, relheight=0.167, anchor='sw')
    twelve_label.place(relx=0, rely=0.5, relwidth=0.167, relheight=0.168)
    fourteen_label.place(relx=0, rely=0.75, relwidth=0.167, relheight=0.167, anchor='w')
    sixteen_label.place(relx=0, rely=1, relwidth=0.167, relheight=0.167, anchor='sw')
    empty_label.place(relx=0, rely=0, relwidth=0.167, relheight=0.168)

    # configure buttons in a single list, to be able to run through all buttons in a single loop
    button_configurations = [
        # monday buttons
        {'text': 'MON 8:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('MON 8:15'),
         'relx': 0.25, 'rely': 0.25, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'center'},
        {'text': 'MON 10:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('MON 10:15'),
         'relx': 0.25, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 's'},
        {'text': 'MON 12:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('MON 12:15'),
         'relx': 0.25, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.168, 'anchor': 'n'},
        {'text': 'MON 14:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('MON 14:15'),
         'relx': 0.25, 'rely': 0.75, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'center'},
        {'text': 'MON 16:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('MON 16:15'),
         'relx': 0.25, 'rely': 1, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 's'},

        # tuesday buttons
        {'text': 'TUE 8:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('TUE 8:15'),
         'relx': 0.5, 'rely': 0.25, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'e'},
        {'text': 'TUE 10:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('TUE 10:15'),
         'relx': 0.5, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'se'},
        {'text': 'TUE 12:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('TUE 12:15'),
         'relx': 0.5, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.168, 'anchor': 'ne'},
        {'text': 'TUE 14:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('TUE 14:15'),
         'relx': 0.5, 'rely': 0.75, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'e'},
        {'text': 'TUE 16:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('TUE 16:15'),
         'relx': 0.5, 'rely': 1, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'se'},

        # wednedsday buttons
        {'text': 'WED 8:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('WED 8:15'),
         'relx': 0.5, 'rely': 0.25, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'w'},
        {'text': 'WED 10:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('WED 10:15'),
         'relx': 0.5, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'sw'},
        {'text': 'WED 12:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('WED 12:15'),
         'relx': 0.5, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.168, 'anchor': 'nw'},
        {'text': 'WED 14:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('WED 14:15'),
         'relx': 0.5, 'rely': 0.75, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'w'},
        {'text': 'WED 16:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('WED 16:15'),
         'relx': 0.5, 'rely': 1, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'sw'},

        # thursday buttons
        {'text': 'THU 8:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('THU 8:15'),
         'relx': 0.75, 'rely': 0.25, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'center'},
        {'text': 'THU 10:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('THU 10:15'),
         'relx': 0.75, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 's'},
        {'text': 'THU 12:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('THU 12:15'),
         'relx': 0.75, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.168, 'anchor': 'n'},
        {'text': 'THU 14:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('THU 14:15'),
         'relx': 0.75, 'rely': 0.75, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'center'},
        {'text': 'THU 16:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('THU 16:15'),
         'relx': 0.75, 'rely': 1, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 's'},

        # friday buttons
        {'text': 'FRI 8:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('FRI 8:15'),
         'relx': 1, 'rely': 0.25, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'e'},
        {'text': 'FRI 10:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('FRI 10:15'),
         'relx': 1, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'se'},
        {'text': 'FRI 12:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('FRI 12:15'),
         'relx': 1, 'rely': 0.5, 'relwidth': 0.167, 'relheight': 0.168, 'anchor': 'ne'},
        {'text': 'FRI 14:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('FRI 14:15'),
         'relx': 1, 'rely': 0.75, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'e'},
        {'text': 'FRI 16:15', 'font': font_text, 'bg': button_color, 'fg': 'white',
         'relief': tk.RAISED, 'borderwidth': 5,
         'command': lambda: on_button_click('FRI 16:15'),
         'relx': 1, 'rely': 1, 'relwidth': 0.167, 'relheight': 0.167, 'anchor': 'se'}
    ]

    # create and place all buttons using a loop going through the list above
    for config in button_configurations:
        button = tk.Button(timetable_frame, text=config['text'], font=config['font'], bg=config['bg'], fg=config['fg'],
                           relief=config['relief'], borderwidth=config['borderwidth'],
                           command=config['command'])
        button.place(relx=config['relx'], rely=config['rely'], relwidth=config['relwidth'],
                     relheight=config['relheight'], anchor=config['anchor'])

    # frame legend
    weeks_booked_frame = tk.Frame(page_calendar, bg=bg_color)
    weeks_booked_frame.place(relx=0.825, rely=0.2, relwidth=0.1, relheight=0.6)
    # widgets
    selected_color_label = tk.LabelFrame(weeks_booked_frame, text='', bg=button_selected_color)
    selected_label = tk.Label(weeks_booked_frame, text='Slot selected\n by you', font=font_text,
                              bg=bg_color, fg='white')
    booked_color_label = tk.LabelFrame(weeks_booked_frame, text='', bg='#600202')
    booked_label = tk.Label(weeks_booked_frame, text='Slot already\n booked', font=font_text,
                            bg=bg_color, fg='white')
    # layout
    selected_color_label.place(relx=0.5, rely=0.45, relwidth=0.6, relheight=0.09, anchor='s')
    selected_label.place(relx=0.5, rely=0.45, relwidth=1, relheight=0.15, anchor='n')
    booked_color_label.place(relx=0.5, rely=0.75, relwidth=0.6, relheight=0.09, anchor='s')
    booked_label.place(relx=0.5, rely=0.75, relwidth=1, relheight=0.15, anchor='n')

    # continue button
    enter_page_persdata_button = tk.Button(page_calendar, text='Continue', font=font_heading2,
                                           bg=button_cta_color, fg='white',
                                           relief=tk.RAISED, borderwidth=5, command=lambda: press_start_page_persdata())
    enter_page_persdata_button.place(relx=0.8, rely=0.85, relwidth=0.2, relheight=0.08, anchor='n')


# load the Personal Data Page
def load_page_persdata():
    # switch the library card image on or off when info is clicked
    def click_info():

        # retrieve the variable, to change it inside this function
        global card_visibility

        if card_visibility == False:
            # display the card image
            card_label.config(image=card_image)
            card_visibility = True
        else:
            # display blank image to make the card image invisible
            card_label.config(image=blank_image)
            card_visibility = False

    # check personal data input if its complete, then destroy the Personal Data page and open the Confirmation Page,
    # else show a messagebox with an error
    def press_start_page_confirmation():
        # retrieve the variables, to change them inside this function
        global firstname
        global lastname
        global email
        global library
        global address
        global birthday

        # get the entry of the name and email
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        email = email_entry.get()

        # only continues if first, last name and email are filled out
        if firstname and lastname and email:
            # get the entry of the library no., address and birthday
            library = library_entry.get()
            address = address_entry.get()
            birthday = birthday_entry.get()

            # destroy the Personal Data page and open the Confirmation Page
            page_persdata.destroy()
            load_page_confirmation()

        # when the name and/or email are not filled out
        else:
            # show a messagebox on top of the frame with an error
            tk.messagebox.showwarning(title='Error', message='First and Last Name and Email are required')

            # reload page to let the user put in personal data again
            page_persdata.destroy()
            load_page_persdata()

    # create the Personal Data Page frame
    page_persdata = tk.Frame(root, bg=bg_color)
    page_persdata.place(x=0, y=0, relwidth=1, relheight=1)
    # header
    header_label = tk.Label(page_persdata, text='Please enter your Personal Information here',
                            font=font_heading1, bg=bg_color, fg='white')
    header_label.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.2, anchor='center')

    # Personal Data Entry frame
    pers_data_frame = tk.LabelFrame(page_persdata, bg=bg_color)
    pers_data_frame.place(relx=0.075, rely=0.2, relwidth=0.85, relheight=0.6)
    # widgets
    first_name_label = tk.Label(pers_data_frame, text='First Name', font=font_text, bg=bg_color, fg='white')
    first_name_entry = tk.Entry(pers_data_frame, font=font_text)
    last_name_label = tk.Label(pers_data_frame, text='Last Name', font=font_text, bg=bg_color, fg='white')
    last_name_entry = tk.Entry(pers_data_frame, font=font_text)
    email_label = tk.Label(pers_data_frame, text='Email (Leuphana)', font=font_text, bg=bg_color, fg='white')
    email_entry = tk.Entry(pers_data_frame, font=font_text)
    library_label = tk.Label(pers_data_frame, text='Library Number', font=font_text, bg=bg_color, fg='white')
    library_entry = tk.Entry(pers_data_frame, font=font_text)
    # layout
    first_name_label.place(relx=0.025, rely=0.077, relheight=0.075, anchor='w')
    first_name_entry.place(relx=0.25, rely=0.154, relwidth=0.45, relheight=0.075, anchor='center')
    last_name_label.place(relx=0.525, rely=0.077, relheight=0.075, anchor='w')
    last_name_entry.place(relx=0.75, rely=0.154, relwidth=0.45, relheight=0.075, anchor='center')
    email_label.place(relx=0.025, rely=0.231, relheight=0.075, anchor='w')
    email_entry.place(relx=0.5, rely=0.308, relwidth=0.95, relheight=0.075, anchor='center')
    library_label.place(relx=0.025, rely=0.385, relheight=0.075, anchor='w')
    library_entry.place(relx=0.5, rely=0.462, relwidth=0.95, relheight=0.075, anchor='center')

    # create Info Button with a photo as the button
    # open image play button
    info_image = Image.open('images/info-button-green.png')
    # resize image
    resized_info = info_image.resize((30, 30), Image.LANCZOS)
    info_image_photo = ImageTk.PhotoImage(resized_info)
    # create label with the resized image
    info_label = tk.Label(pers_data_frame, image=info_image_photo, bg=bg_color)
    info_label.image = info_image_photo
    # make it into a button
    info_button = tk.Button(pers_data_frame,
                            image=info_image_photo,
                            bg=bg_color,
                            cursor='hand2',
                            activebackground=bg_color,
                            activeforeground='white',
                            command=click_info,
                            borderwidth=0)
    info_button.place(relx=0.17, rely=0.385, anchor='center')

    # create blank image, to make the library card image invisible
    open_blank_image = Image.open('images/blank_image.png')
    blank_image = ImageTk.PhotoImage(open_blank_image)
    # create label with the image
    blank_label = tk.Label(pers_data_frame, image=blank_image, bg=bg_color)
    blank_label.image = blank_image
    # place it where the library card image should appear
    blank_label.place(relx=0.2, rely=0.232)

    # open image library card
    open_card_image = Image.open('images/bib-ausweis.jpg')
    # resize image
    resized_card = open_card_image.resize((228, 144), Image.LANCZOS)
    card_image = ImageTk.PhotoImage(resized_card)

    # create label with the blank image, where the library card image should appear later
    card_label = tk.Label(pers_data_frame, image=blank_image, bg=bg_color)
    card_label.place(relx=0.2, rely=0.232)

    # if user has no library card widgets
    nocard_title_label = tk.Label(pers_data_frame,
                                  text='\nIf you don´t own a library card please enter your address and birthday here:',
                                  font=font_heading2, bg=bg_color, fg='white')
    nocard_title_label.place(relx=0.5, rely=0.539, anchor='n')
    # widgets
    address_label = tk.Label(pers_data_frame, text='Address', font=font_text, bg=bg_color, fg='white')
    address_entry = tk.Entry(pers_data_frame, font=font_text)
    birthday_label = tk.Label(pers_data_frame, text='Birthday', font=font_text, bg=bg_color, fg='white')
    birthday_entry = tk.Entry(pers_data_frame, font=font_text)
    # layout
    address_label.place(relx=0.025, rely=0.693, relheight=0.075, anchor='w')
    address_entry.place(relx=0.5, rely=0.77, relwidth=0.95, relheight=0.075, anchor='center')
    birthday_label.place(relx=0.025, rely=0.847, relheight=0.075, anchor='w')
    birthday_entry.place(relx=0.5, rely=0.924, relwidth=0.95, relheight=0.075, anchor='center')

    # Confirm Button
    page_persdata_enter_button = tk.Button(page_persdata, text='Show booking overview',
                                           font=font_heading2,
                                           bg=button_cta_color, fg='white',
                                           relief=tk.RAISED, borderwidth=5,
                                           command=lambda: press_start_page_confirmation())
    page_persdata_enter_button.place(relx=0.8, rely=0.85, relwidth=0.2, relheight=0.08, anchor='n')


# load the Confirmation Page
def load_page_confirmation():
    # retrieve the variables, to change them inside this function
    global firstname
    global lastname
    global email
    global library
    global address
    global birthday
    global calendar_week
    global buttons_string

    # destroy the Confirmation Data page and open the End Page
    def press_start_page_end():
        page_confirmation.destroy()
        load_page_end()

    # Confirmation Page frame
    page_confirmation = tk.Frame(root, bg=bg_color)
    page_confirmation.place(x=0, y=0, relwidth=1, relheight=1)
    # header
    header_label = tk.Label(page_confirmation, text=f'Thank you {firstname}\n Please check your reservation',
                            font=font_heading1, bg=bg_color, fg='white')
    header_label.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.2, anchor='center')

    # Confirmation Entry frame
    conf_data_frame = tk.LabelFrame(page_confirmation, bg=bg_color)
    # widgets personal data
    empty_beginning_label = tk.Label(conf_data_frame, text='',
                                     font=font_text, bg=bg_color, fg='white')
    overview_data_label = tk.Label(conf_data_frame, text='\nYour Personal Data:',
                                   font=font_heading2, bg=bg_color, fg='white')
    firstname_header_label = tk.Label(conf_data_frame, text='First Name: ',
                                      font=font_text, bg=bg_color, fg='white')
    firstname_data_label = tk.Label(conf_data_frame, text=firstname,
                                    font=font_text, bg=bg_color, fg='white')
    lastname_header_label = tk.Label(conf_data_frame, text='Last Name: ',
                                     font=font_text, bg=bg_color, fg='white')
    lastname_data_label = tk.Label(conf_data_frame, text=lastname,
                                   font=font_text, bg=bg_color, fg='white')
    email_header_label = tk.Label(conf_data_frame, text='E-Mail: ',
                                  font=font_text, bg=bg_color, fg='white')
    email_data_label = tk.Label(conf_data_frame, text=email,
                                font=font_text, bg=bg_color, fg='white')
    library_header_label = tk.Label(conf_data_frame, text='Library Number: ',
                                    font=font_text, bg=bg_color, fg='white')
    library_data_label = tk.Label(conf_data_frame, text=library,
                                  font=font_text, bg=bg_color, fg='white')
    address_header_label = tk.Label(conf_data_frame, text='Address: ',
                                    font=font_text, bg=bg_color, fg='white')
    address_data_label = tk.Label(conf_data_frame, text=address,
                                  font=font_text, bg=bg_color, fg='white')
    birthday_header_label = tk.Label(conf_data_frame, text='Birthday: ',
                                     font=font_text, bg=bg_color, fg='white')
    birthday_data_label = tk.Label(conf_data_frame, text=birthday,
                                   font=font_text, bg=bg_color, fg='white')
    # widgets booking
    overview_booking_label = tk.Label(conf_data_frame, text='\nYour selected Week and the corresponding time slots:',
                                      font=font_heading2, bg=bg_color, fg='white')
    week_header_label = tk.Label(conf_data_frame, text='Calendar Week: ',
                                 font=font_text, bg=bg_color, fg='white')
    week_data_label = tk.Label(conf_data_frame, text=calendar_week,
                               font=font_text, bg=bg_color, fg='white')
    booking_header_label = tk.Label(conf_data_frame, text='Booked Slots: ',
                                    font=font_text, bg=bg_color, fg='white')
    booking_data_label = tk.Label(conf_data_frame, text=buttons_string,
                                  font=font_text, bg=bg_color, fg='white')
    # layout
    conf_data_frame.place(relx=0.075, rely=0.2, relwidth=0.85, relheight=0.6)
    # layout personal data
    empty_beginning_label.grid(row=0, column=0, pady=5, padx=10)
    overview_data_label.grid(row=0, column=1, pady=5, padx=10, sticky='w')
    firstname_header_label.grid(row=1, column=1, pady=5, padx=10, sticky='w')
    firstname_data_label.grid(row=1, column=2, pady=5, sticky='w')
    lastname_header_label.grid(row=2, column=1, pady=5, padx=10, sticky='w')
    lastname_data_label.grid(row=2, column=2, pady=5, sticky='w')
    email_header_label.grid(row=3, column=1, pady=5, padx=10, sticky='w')
    email_data_label.grid(row=3, column=2, pady=5, sticky='w')
    library_header_label.grid(row=4, column=1, padx=10, pady=5, sticky='w')
    library_data_label.grid(row=4, column=2, pady=5, sticky='w')
    address_header_label.grid(row=5, column=1, padx=10, pady=5, sticky='w')
    address_data_label.grid(row=5, column=2, pady=5, sticky='w')
    birthday_header_label.grid(row=6, column=1, padx=10, pady=5, sticky='w')
    birthday_data_label.grid(row=6, column=2, pady=5, sticky='w')
    # layout booking
    overview_booking_label.grid(row=8, column=1, pady=5, padx=10, columnspan=2, sticky='w')
    week_header_label.grid(row=9, column=1, pady=5, padx=10, sticky='w')
    week_data_label.grid(row=9, column=2, pady=5, sticky='w')
    booking_header_label.grid(row=10, column=1, pady=5, padx=10, sticky='w')
    booking_data_label.grid(row=10, column=2, pady=5, sticky='w')

    # Confirm, Restart or Cancel frame
    conf_button_frame = tk.Frame(page_confirmation, bg=bg_color)
    conf_button_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.1)
    # widgets
    cancel_button = tk.Button(page_confirmation, text='Cancel', command=lambda: root.quit(),
                              font=font_heading2, bg=button_color, fg='white')
    restart_button = tk.Button(page_confirmation, text='Restart', command=lambda: load_page_calendar(),
                               font=font_heading2, bg=button_color, fg='white')
    confirm_button = tk.Button(page_confirmation, text='Confirm', command=lambda: press_start_page_end(),
                               font=font_heading2, bg=button_cta_color, fg='white')
    # layout
    cancel_button.place(relx=0.2, rely=0.85, relwidth=0.2, relheight=0.08, anchor='n')
    restart_button.place(relx=0.5, rely=0.85, relwidth=0.2, relheight=0.08, anchor='n')
    confirm_button.place(relx=0.8, rely=0.85, relwidth=0.2, relheight=0.08, anchor='n')


# load the End Page
def load_page_end():
    # retrieve the variables, to change them inside this function
    global firstname
    global email

    # End Page frame
    page_end = tk.Frame(root, bg=bg_color)
    page_end.place(x=0, y=0, relwidth=1, relheight=1)
    # header
    end_header_label = tk.Label(page_end, text=f'Thank you {firstname} for booking the Video Studio\n\n',
                                font=font_heading1, bg=bg_color, fg='white')
    end_header_label.pack(expand=True, anchor='s')
    # second header
    header2_label = tk.Label(page_end,
                             text=f'A confirmation with your booking information will be sent to your Email-Address:'
                                  f'\n{email}',
                             font=font_heading2, bg=bg_color, fg='white')
    header2_label.pack(expand=True, anchor='n')
    # close website button
    close_button = tk.Button(page_end, text='Close Window', command=lambda: root.quit(),
                             font=font_heading2, bg=button_cta_color, fg='white')

    close_button.place(relx=0.8, rely=0.85, relwidth=0.2, relheight=0.08, anchor='n')

    # a confirmation Email with the booking overview should be sent at that moment
    # to the user and to the Video Studio staff, which is not implemented here,
    # because it is outside my current knowledge
    print('Confirmation Email should be sent now')


# initialize Website
root = tk.Tk()
# set title of the Website
root.title("Video Studio Calendar")
# set icon of the Website to the calendar logo
root.iconbitmap('images/calendar.ico')
root.configure(background=bg_color)
root.geometry('1400x788')
# set minimum size of window, to not reduce window to 0
root.minsize(900, 530)
# close the window with escape
root.bind('<Escape>', lambda event: root.quit())

# create Welcome page frame
page_welcome = tk.Frame(root)
# load the image
videostudio_img = Image.open('images/camera.png')
# resize the image
videostudio_resized = videostudio_img.resize((1400, 788), Image.LANCZOS)
# Convert the resized image to PhotoImage
videostudio_pic = ImageTk.PhotoImage(videostudio_resized)
# Create a label with the image
videostudio_label = tk.Label(page_welcome, image=videostudio_pic)
# center the image
videostudio_label.pack(expand=True, fill='both')
page_welcome.pack(expand=True, fill='both')

# load the Welcome Page
load_page_welcome()

# execute the code
root.mainloop()
