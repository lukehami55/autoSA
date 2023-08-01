import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from localAutomation import autosa


class ButtonSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button Selection Ordering")

        self.selected_buttons = []
        self.buttons = ["Total", "Targeting", "Goal", "Type", "Portfolio"]

        self.style = ttk.Style()
        self.style.configure("My.TButton", background="gray")  # Set the background color for the buttons

        self.button_frame = tk.Frame(self.root)
        self.text_frame = tk.Frame(self.root)

        self.text_box = tk.Text(self.text_frame, height=2, width=50)
        self.text_box.pack()

        self.create_choice_buttons()
        self.hide_buttons()  # Initially hide buttons A, B, C, D and the text box

        title_label = tk.Label(root, text="Automated Sponsored Advertising", font=("Helvetica", 24))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)

        initial_desc = "Please select an automation option:"
        self.desc_label = tk.Label(root, text=initial_desc, font=("Helvetica", 12))
        self.desc_label.grid(row=1, column=0, columnspan=4, pady=5)

        self.choices = ["Auto SA", "Auto SA Delta", "Auto SA Delta Targeting", "Auto SA Delta YoY"]
        self.choice_buttons = []
        for i, choice in enumerate(self.choices):
            button = ttk.Button(root, text=choice, style="My.TButton", command=lambda i=i: self.on_choice_select(i))
            button.grid(row=2, column=i, padx=5)
            self.choice_buttons.append(button)

        self.index_selected = False
        self.true_false_button = ttk.Button(root, text="Index", style="My.TButton", command=self.toggle_index)

        submit_button = tk.Button(root, text="Run", command=self.submit)
        submit_button.grid(row=6, column=0, columnspan=4, pady=20)

    def create_choice_buttons(self):
        for button_label in self.buttons:
            button = tk.Button(self.button_frame, text=button_label, width=10,
                               command=lambda label=button_label: self.on_button_click(label))
            button.grid(row=0, column=self.buttons.index(button_label), padx=5, pady=5)

    def on_button_click(self, label):
        if label in self.selected_buttons:
            self.selected_buttons.remove(label)
        else:
            self.selected_buttons.append(label)

        self.update_text_box()

    def update_text_box(self):
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, " then ".join(self.selected_buttons))

    def on_choice_select(self, choice_num):
        self.choice = choice_num
        for button in self.choice_buttons:
            button.configure(style="My.TButton")  # Set the style for all buttons to "My.TButton"
        self.choice_buttons[self.choice].configure(style="TButton")  # Set the style for the selected button to default

        if self.choice == 0:
            self.true_false_button.grid(row=3, column=0, columnspan=4, pady=10)
            if self.index_selected:
                self.true_false_button.config(bg="blue")
                self.desc_label.config(text="Auto SA with Index")
            else:
                self.true_false_button.config(bg="gray")
                self.desc_label.config(text="Auto SA")
            self.show_buttons()  # Show buttons A, B, C, D
        else:
            self.true_false_button.grid_forget()
            self.desc_label.config(text=f"{self.choices[self.choice]}")
            self.hide_buttons()  # Hide buttons A, B, C, D

    def show_buttons(self):
        self.button_frame.grid(row=4, pady=10, columnspan=4)
        self.text_frame.grid(row=5, pady=5, columnspan=4)

    def hide_buttons(self):
        self.button_frame.grid_forget()
        self.text_frame.grid_forget()

    def toggle_index(self):
        self.index_selected = not self.index_selected
        if self.index_selected:
            self.true_false_button.config(bg="blue")
            self.desc_label.config(text="Auto SA with Index")
        else:
            self.true_false_button.config(bg="gray")
            self.desc_label.config(text="Auto SA")

    def submit(self):
        # params = self.selected_buttons
        # params = params.insert(0, "Total")
        if self.choice == 0:
            print(self.selected_buttons)
            autosa(self.selected_buttons, self.index_selected, self.desc_label)
        elif self.choice == 1:
            print("choice1")
        elif self.choice == 2:
            print("choice2")
        elif self.choice == 3:
            print("choice3")


if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonSelectionApp(root)
    root.mainloop()
