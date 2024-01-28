from tkinter import *
from paragraph_text import get_paragraph_topic, get_paragraph_text
import time

class TypingTest:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1500x600+0+0")
        self.window.title("Typing Speed And Accuracy Test")
        self.window.configure(bg="#f9977b")
        self.window.minsize(1500, 600)
        self.current_frame = Frame(self.window, bg="#1f2032", width=1000, height=600)
        self.current_frame.pack()
        self.para_count = IntVar()
        self.topic = StringVar()
        self.paragraph_topic = list(get_paragraph_topic())
        self.start_flag = 0

        self.seconds = 0
        self.minutes = 0
        self.backspace_count = 0


    def get_exit(self):
        self.window.quit()

    def clear_frame(self):
        for wid in self.current_frame.winfo_children():
            wid.destroy()

    def go_backward(self, backward, forward, title, place_holder):
        if self.para_count.get() == 0:
            backward.config(state=DISABLED)
        else:
            backward.config(state=NORMAL)

        forward.config(state=NORMAL)

        self.para_count.set(self.para_count.get() - 1)
        self.topic.set(self.paragraph_topic[self.para_count.get()])
        title.config(text=self.topic.get())

        self.paragraph = get_paragraph_text(self.topic.get())
        place_holder.config(text=self.paragraph)

    def go_forward(self, backward, forward, title, place_holder):
        if self.para_count.get() == (len(self.paragraph_topic) - 1):
            forward.config(state=DISABLED)
        else:
            forward.config(state=NORMAL)

        backward.config(state=NORMAL)

        self.para_count.set(self.para_count.get() + 1)
        self.topic.set(self.paragraph_topic[self.para_count.get()])
        title.config(text=self.topic.get())

        self.paragraph = get_paragraph_text(self.topic.get())
        place_holder.config(text=self.paragraph)

    def update_timer(self, s_time):
        current_time = time.time()

        if int(current_time - s_time) >= 0:
            self.seconds += 1
        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1

        min_p = '{:0>2d}'.format(int(self.minutes))
        sec_p = '{:0>2d}'.format(int(self.seconds))

        time_count.config(text=f'{min_p}:{sec_p}')
        time_count.after(1000, lambda: self.update_timer(s_time))

    def formatted_time(self, total_time):
        time_format = '{:0>2d}'.format(int(total_time / 60))
        time_format += ':' + '{:0>2d}'.format(int(total_time % 60))
        return time_format

    def calculate_result(self):
        total_time = int(self.end_time - self.start_time)

        wpm = correct_letters = correct_words = accuracy = actual_accuracy = 0

        correct_flag = 1
        for para_char, user_char in zip(self.paragraph, self.get_user_text):
            if para_char == user_char:
                correct_letters += 1
            else:
                correct_flag = 0

            if para_char in (' ', '\n', '\t'):
                correct_words += 1 if correct_flag == 1 else 0
                correct_flag = 1

        correct_words += 1 if correct_flag == 1 else 0
        wpm = correct_words / (float(total_time) / 60)

        accuracy = (correct_letters * 100) / len(self.paragraph)
        actual_accuracy = (correct_letters - self.backspace_count) * 100 / len(self.paragraph)

        return int(accuracy), int(actual_accuracy), int(wpm), self.formatted_time(total_time)

    def reset_data(self):
        self.start_flag = 0
        self.seconds = 0
        self.minutes = 0
        self.backspace_count = 0

    def back_to_home(self):
        self.reset_data()
        self.clear_frame()
        self.set_typing_home()

    def show_typing_result(self):
        self.clear_frame()

        (accuracy, actual_accuracy, wpm, total_time) = self.calculate_result()
        result = Label(self.current_frame, text="Result", fg='black', bg='skyblue1',
                       font='Lucida\ Calligraphy 26 underline')
        result.grid(row=0, columnspan=3, pady=40)

        lb_accuracy = Label(self.current_frame, text='Accuracy', fg='black', bg='LightSalmon2', font='Lucida\ Fax 22')
        lb_accuracy.grid(row=1, column=0)
        accuracy_val = Label(self.current_frame, text=f'{accuracy}%', fg='red', bg='khaki', font='Lucida\ Fax 22 bold')
        accuracy_val.grid(row=1, column=1, columnspan=2)

        lb_actual_accuracy = Label(self.current_frame, text='Actual Accuracy', fg='black', bg='LightSalmon2',
                                   font='Lucida\ Fax 22')
        lb_actual_accuracy.grid(row=2, column=0, pady=(25, 0))
        accuracy_actual_val = Label(self.current_frame, text=f'{actual_accuracy}%', fg='red', bg='khaki',
                                    font='Lucida\ Fax 22 bold')
        accuracy_actual_val.grid(row=2, column=1, columnspan=2, pady=(25, 0))

        lb_wpm = Label(self.current_frame, text="WPM", fg='black', bg='LightSalmon2', font='Lucida\ Fax 22')
        lb_wpm.grid(row=3, column=0)
        val_wpm = Label(self.current_frame, text=f'{wpm}', fg='red', bg='khaki', font='Lucida\ Fax 22 bold')
        val_wpm.grid(row=3, column=1, columnspan=2, pady=25)

        lb_time = Label(self.current_frame, text="Total Time", fg='black', bg='LightSalmon2', font='Lucida\ Fax 22')
        lb_time.grid(row=4, column=0)
        val_time = Label(self.current_frame, text=f'{total_time}', fg='red', bg='khaki', font='Lucida\ Fax 22 bold')
        val_time.grid(row=4, column=1, columnspan=2)

        lb_exit = Button(self.current_frame, text='EXIT', fg='red', bg='plum1', font='Verdana\ Pro 18 bold',
                         borderwidth=3, command=self.get_exit)
        lb_exit.grid(row=5, column=1, pady=50, padx=30)
        lb_home = Button(self.current_frame, text='HOME', fg='red', bg='plum1', font='Verdana\ Pro 18 bold',
                         borderwidth=3, command=self.back_to_home)
        lb_home.grid(row=5, column=2, pady=50, padx=30)

    def key_release(self, event):
        if self.start_flag == 0:
            self.start_flag = 1
            self.start_time = time.time()
            self.update_timer(self.start_time)

        self.get_user_text = self.user_input.get('1.0', 'end - 1c')

        if self.paragraph.startswith(self.get_user_text):
            self.user_input.config(fg='green')
        else:
            self.user_input.config(fg='red')

        if event.keysym == 'BackSpace':
            self.backspace_count += 1

        self.key_press_count = len(self.get_user_text)
        if self.key_press_count >= len(self.paragraph):
            self.end_time = time.time()
            self.show_typing_result()

    def start_typing(self):
        self.clear_frame()

        title = Label(self.current_frame, fg='black', bg='white', text=self.topic.get(),
                      font='Lucida\ Console 26 underline')
        title.grid(row=0, column=0, columnspan=1, pady=50)

        global time_count
        time_count = Label(self.current_frame, fg='red', bg='skyblue1', text='00:00', font='Lucida\ Console 22 bold')
        time_count.grid(row=0, column=2, pady=50)

        place_holder = Message(self.current_frame, text=self.paragraph, fg='black', bg='ivory3', width=1000,
                               justify='center', font='Verdana\ Pro 18')
        place_holder.grid(row=2, column=0, columnspan=3, padx=80, pady=40)

        self.user_input = Text(self.current_frame, width=80, height=10, bg='floral white', fg='black',
                               insertbackground='green', borderwidth=5, relief=RAISED, padx=5, pady=5,
                               font='Verdana\ Pro 16')

        self.user_input.grid(row=3, column=0, columnspan=3, padx=30)

        self.user_input.bind('<KeyRelease>', self.key_release)
        self.user_input.focus()
        self.user_input.bind('<Control-x>', lambda e: 'break')  # disable cut
        self.user_input.bind('<Control-c>', lambda e: 'break')  # disable copy
        self.user_input.bind('<Control-v>', lambda e: 'break')  # disable paste
        self.user_input.bind('<Button-3>', lambda e: 'break')  # disable right-click

    def set_typing_home(self):
        if self.current_frame is not None:
            self.clear_frame()

        self.para_count.set(0)
        self.topic.set(self.paragraph_topic[0])

        header = Label(self.current_frame,
                       text='Select Paragraph For Test',
                       font='rockwell 25 bold underline',
                       bg='white', fg='black')
        header.grid(row=0, column=1, pady=(40, 20))

        backward = Button(self.current_frame,
                          text='<<',
                          bg='lightblue1', fg='black', relief=RAISED,
                          font='Helvetica 20',
                          state=DISABLED, command=lambda: self.go_backward(backward, forward, title, place_holder))

        title = Label(self.current_frame, fg='black', bg='white', text=self.topic.get(), font='Helvetica 22')

        forward = Button(self.current_frame,
                         text='>>',
                         bg='lightblue1', fg='black', relief=RAISED,
                         font='Helvetica 20', command=lambda: self.go_forward(backward, forward, title, place_holder))

        backward.grid(row=1, column=0, pady=35)
        title.grid(row=1, column=1, pady=35)
        forward.grid(row=1, column=2, pady=(35))

        self.paragraph = get_paragraph_text(self.topic.get())

        place_holder = Message(self.current_frame, text=self.paragraph, fg='black', bg='ivory3', width=1000,
                               justify='center', font='Verdana\ Pro 18')
        place_holder.grid(row=3, column=0, columnspan=3)

        start_test = Button(self.current_frame, text="Start Test", font='Verdana\ Pro 15', borderwidth=3,
                            bg='lightblue1', fg='black', relief=RAISED, command=self.start_typing)
        start_test.grid(row=4, column=1, pady=10)

        exit_button = Button(self.current_frame,
                             text='Exit',
                             font='Verdana\ Pro 15',
                             borderwidth=3,
                             bg='lightblue1', fg='black', relief=RAISED,
                             command=self.get_exit)
        exit_button.grid(row=5, column=1)


if __name__ == '__main__':
    typing_test = TypingTest()
    typing_test.set_typing_home()
    typing_test.window.mainloop()