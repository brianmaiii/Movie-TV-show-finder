import omdb_api_model as model
from tkinter import *


class ViewSecond:

    def __init__(self):
        """Starts up the gui."""
        self.model_obj = model.Model()
        self.list_of_five = []
        self.window = Tk()
        self.window.title('TV Episode Finder')

        label=Label(self.window, text="Enter Show Title", font=('Helvetica', 14))
        self.entry=Entry(self.window)
        button_enter=Button(self.window, text="Enter", command=self.button_code)

        label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        button_enter.grid(row=0, column=2)
        self.window.mainloop()

    def print_all_episodes_gui(self, list_episodes):
        """Prints all the episodes."""
        self.textbox=Text(self.window, height=30, width=65, wrap='word',
                            font=('Helvetica', 12))
        vertscroll=Scrollbar(self.window)
        vertscroll.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=vertscroll.set)
        self.textbox.grid(column=0, row=1)
        vertscroll.grid(column=1, row=1, sticky='ns')
        for y in range(len(list_episodes)):
            for x in list_episodes[y]['Episodes']:
                self.textbox.insert(END, "Season: %s,  Episode: %s,  Title: %s\n" %
                                    (str(y+1), x["Episode"], x['Title']))
        self.window.mainloop()

    def print_five_episodes_gui(self, list_episodes):
        """Prints out the information for the 5 episodes needed."""
        self.text_summary.insert(END, "Summaries of the episodes Selected\n")
        self.text_summary.insert(END, "\n")
        for y in list_episodes:
            self.text_summary.insert(END, "Title: %s, Season: %s, Episode: %s, Plot: %s\n" %
                                     (y['Title'], y['Season'], y['Episode'], y['Plot']))
            self.text_summary.insert(END, "\n")
        self.text_summary.config(state=DISABLED)

    def button_code(self):
        """Button code that handels selecting episoides."""
        global select

        self.search=self.entry.get()
        search_url=self.model_obj.build_url(self.search)
        results=self.model_obj.get_result(search_url)
        numberSeaons=self.model_obj.get_total_seasons(results)
        list_seasons_url=self.model_obj.get_total_seasons_url(numberSeaons, self.search)
        self.list_episodes=self.model_obj.get_list_episodes(list_seasons_url)

        self.label=Label(self.window, text="Enter Season Number, space, and then the Episode Number (ex.1 2): ",
                           font=('Helvetica 14'))

        self.entry=Entry(self.window)
        self.button_enter = Button(
            self.window, text="Click Here to Add Episodes To Your List", command=self.create_list)
        self.text = Text(self.window)
        self.text.configure(font=' helvetica 12')
        self.text_selected = Text(self.window)
        self.button_search = Button(
            self.window, text="Click to Show Selected Episodes Summaries", command=self.show_summary)

        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.button_enter.grid(row=0, column=2)
        self.button_search.grid(row=2, column=2)
        self.text.grid(row=1, column=0)
        self.text_selected.grid(row=1, column=2)
        self.text_selected.insert(END, "Below are the Episodes you have selected:\n")
        self.text_selected.insert(END, "---> Note: You may only select up to 5 <---\n")
        self.text_selected.insert(END, '\n')
        self.text_selected.configure(font='helvetica 14')

        self.text_selected.config(state=DISABLED)
        self.print_all_episodes_gui(self.list_episodes)

    def create_list(self):
        """creates the list of selected episodes."""
        if len(self.list_of_five) >= 5:
            return
        episode = self.entry.get()
        if episode in self.list_of_five:
            return
        self.summary_episode = self.model_obj.input_episode(episode, self.list_episodes)
        self.list_of_five.append(self.summary_episode[0])
        self.show_selected_episodes()

    def show_summary(self):
        """Shows the summary."""
        self.list_of_five.sort()
        self.list_of_five = self.model_obj.sort_epi(self.list_of_five)
        self.text_selected.grid_forget()
        self.text.grid_forget()
        self.button_search.grid_forget()
        self.label.grid_forget()
        self.button_enter.grid_forget()
        seasons_url = self.model_obj.user_picks_five(self.list_of_five,
                                                     self.search)
        self.episode_list = self.model_obj.get_list_episodes(seasons_url)
        label = Label(
            self.window, text="Enter the name of the folder you would like to save your file in: ")
        button_enter = Button(self.window, text="Enter", command=self.create_csv)
        self.entry = Entry(self.window)
        self.text_summary = Text(self.window)
        label.grid(row=0, column=0)
        button_enter.grid(row=0, column=2)
        self.entry.grid(row=0, column=1)
        self.text_summary.grid(row=1, column=4)
        self.print_five_episodes_gui(self.episode_list)

    def create_csv(self):
        """Creates CSV file."""
        directory = self.entry.get()
        path = self.model_obj.create_path(directory)
        self.model_obj.create_csv(path, self.episode_list)

    def show_selected_episodes(self):
        """Shows the selected episodes."""
        self.text_selected.config(state=NORMAL)
        self.text_selected.insert(END, "Season %s, Episode %s\n" % (
            self.summary_episode[0][0], self.summary_episode[0][2:]))
        self.text_selected.config(state=DISABLED)

