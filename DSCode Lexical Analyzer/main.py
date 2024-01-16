from lexer import lexical_analyzer

# GUI Library Import
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename
from tkinter import *
import tkinter as tk
from pil import Image, ImageTk

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("930x662")
        self.root.configure(bg = "#393E46")
        self.root.title("DSCODE Lexical Analyzer")
        self.root.resizable(False, False)
        

        # DSCODE Label
        label = Label(
            self.root, 
            text = "DSCODE", 
            fg = "white", 
            bg = "#393E46", 
            font = ("Inter", 35, "bold"))
        label.place(x = 35, y = 18)

        # Left Frame: Code Input
        self.left_frame = Frame(
            master = self.root, 
            width = 525, 
            height = 540, 
            bg = "#E2E2E2", 
            highlightthickness = 2.3, 
            highlightbackground = "black")
        self.left_frame.place(x = 35, y = 90)
        self.left_frame.pack_propagate(False)

        # Right Frame: Lexical Analysis
        self.right_frame = Frame(
            master = self.root, 
            width = 300, 
            height = 540, 
            bg = "#E2E2E2", 
            highlightthickness = 2.3, 
            highlightbackground = "black")
        self.right_frame.place(x = 595, y = 90)
        self.right_frame.pack_propagate(False)

        # Create a text widget for code input
        self.code_input = Text(self.left_frame, bg = "#E2E2E2", borderwidth = 0, padx = 5, pady = 5)
        self.code_input.place(relx = 0.01, rely = 0.01, relwidth = 0.98, height = 465)
        self.code_input.config(wrap = tk.WORD, font = ("Courier", 12))

        # Create a text widget for lexemes and tokens
        self.display = Text(self.right_frame, bg = "#E2E2E2", borderwidth = 0, padx = 5, pady = 5)
        self.display.place(relx = 0.05, y = 25, relwidth = 0.9, height = 400)
        
        # Add a sideway scrollbar for lexemes and tokens
        scrollbar = tk.Scrollbar(self.right_frame, orient = HORIZONTAL)
        scrollbar.config(command = self.display.xview, bg = "#E2E2E2")
        scrollbar.place(relx = 0.01, y = 450, relwidth = 0.98, height = 20)
        self.display.config(state = "disabled", width = self.display.winfo_screenwidth(), xscrollcommand = True, wrap = NONE, font = ("Courier", 10), spacing1 = 4)

        # Lexeme Label
        lexeme_label = Label(master = self.right_frame, text = "LEXEME", fg = "black", bg = "#E2E2E2", font = ("Inter", 10, "bold"))
        lexeme_label.place(relx = 0.05, y = 10)
        
        # Token Label
        token_label = Label(master = self.right_frame, text = "TOKEN", fg = "black", bg = "#E2E2E2", font = ("Inter", 10, "bold"))
        token_label.place(relx = 0.49, y = 10)

        # Open DSCODE file button
        original_image = Image.open(r'C:\GitHub\DSCode-Lexical-Analyzer\DSCode Lexical Analyzer\Images\open.png')
        resized_image = original_image.resize((50, 50))
        self.add_open_img = ImageTk.PhotoImage(resized_image)

        self.open_btn = Button (
            master = self.left_frame, 
            image = self.add_open_img, 
            borderwidth = 0, 
            highlightthickness = 0, 
            command = self.open_file
        )
        self.open_btn.place(relx = 0.07, rely = 1.26, anchor = 's', y = -150)

        # Save DSCODE file button
        original_save_image = Image.open(r'C:\GitHub\DSCode-Lexical-Analyzer\DSCode Lexical Analyzer\Images\save.png')
        resized_save_image = original_save_image.resize((50, 50))
        self.add_save_img = ImageTk.PhotoImage(resized_save_image)

        self.save_btn = Button (
            master = self.left_frame, 
            image = self.add_save_img, 
            borderwidth = 0, 
            highlightthickness = 0, 
            command = self.save_file
        )
        self.save_btn.place(relx = 0.19, rely = 1.26, anchor = 's', y = -150)

        # Run Lexical Analyzer button
        original_run_image = Image.open(r'C:\GitHub\DSCode-Lexical-Analyzer\DSCode Lexical Analyzer\Images\run.png')
        resized_run_image = original_run_image.resize((65, 65))
        self.add_run_img = ImageTk.PhotoImage(resized_run_image)
        self.run_btn = Button (
            master = self.left_frame, 
            image = self.add_run_img, 
            borderwidth = 0, 
            highlightthickness = 0, 
            command = self.run_file
        )
        self.run_btn.place(relx = 0.91, rely = 1.26, anchor = 's', y = -150)
        
        # Export Analysis button
        original_export_image = Image.open(r'C:\GitHub\DSCode-Lexical-Analyzer\DSCode Lexical Analyzer\Images\export.png')
        resized_export_image = original_export_image.resize((180, 35))
        self.add_export_img = ImageTk.PhotoImage(resized_export_image)

        self.export_btn = Button (
            master = self.right_frame, 
            image = self.add_export_img, 
            borderwidth = 0, 
            highlightthickness = 0,
            command = self.export_file
        )
        self.export_btn.place(relx = 0.5, rely = 1.24, anchor = 's', y = -150)
               
    # Open DSCODE file
    def open_file(self):
        # Open a specific type of file, for example, a .txt file
        file_path = askopenfilename(filetypes=[("DSCode Files", "*.dsc")])
        
        if file_path:
        # Read the file and use it as input in the text widget
            with open(file_path, "r") as file:
                self.code_input.delete(1.0, END)
                self.code_input.insert(END, file.read())
        
        
    # Save DSCODE file
    def save_file(self):
        file = asksaveasfile(mode = 'w', defaultextension='*.dsc', filetypes=[("DSCode Files", "*.dsc")])

        if file is None:
            return
        
        text = self.code_input.get(1.0, END)
        file.write(text)
        file.close()

    # Run Lexical Analyzer
    def run_file(self):
        code = self.code_input.get(1.0, END)
        self.lexemes, self.tokens = lexical_analyzer(code)
    
        self.display.config(state = "normal")
        self.display.delete(1.0, END)

        for item1, item2 in zip(self.lexemes, self.tokens):
            self.display.insert(END, f"{item1}\t\t{item2}\n")

        self.display.config(state = "disabled")

    # Export Analysis
    def export_file(self):
        # Create a text file and save it
        file_path2 = asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '.txt')])
        if not file_path2:
            return

        # Set the width for each column
        token_width = 30

        # Find the maximum length of lexemes
        max_lexeme_length = max(len(lexeme) for lexeme in self.lexemes)
        lexeme_width = max(max_lexeme_length, 30)  # Set a minimum width of 30 for lexemes

        # Text file contents
        with open(file_path2, mode='w') as export:
            export.write("\nSymbol Table\n\n")
            export.write(f"={'=' * lexeme_width}{'=' * (15 - lexeme_width)}==============================================\n")
            export.write(f"LEXEMES{' ' * (lexeme_width - 7)}TOKENS{' ' * (token_width - 6)}\n")
            export.write(f"={'=' * lexeme_width}{'=' * (15 - lexeme_width)}==============================================\n")
            for item1, item2 in zip(self.lexemes, self.tokens):
                # Left-justify the text in each column with the specified width
                export.write(f"{item1.ljust(lexeme_width)}{item2.ljust(token_width)}\n")

        export.close()
            
# Show the Application Window
app = GUI()
app.root.mainloop()
