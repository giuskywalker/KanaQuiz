import random
import tkinter as tk
from tkinter import font as tkFont
import os
import sys

# Everforest color palette
BACKGROUND = "#2B3339"  # Dark background
FOREGROUND = "#D3C6AA"  # Light text
ACCENT = "#A7C080"      # Green accent
ERROR = "#E67E80"       # Red for errors
SECONDARY = "#7FBBB3"   # Teal for secondary elements

# Define the kana and their corresponding romaji
hiragana = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo', 'ん': 'n'
}

katakana = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヲ': 'wo', 'ン': 'n'
}

class KanaQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kana Quiz")
        self.root.geometry("500x400")
        self.root.configure(bg=BACKGROUND)

        # Load custom font
        self.font_path = self.resource_path("JetBrainsMono NFM.ttf")  # Get font path
        self.custom_font = tkFont.Font(family="JetBrainsMono NFM", size=12)
        self.title_font = tkFont.Font(family="JetBrainsMono NFM", size=18, weight="bold")

        self.score = 0
        self.wrong = 0
        self.kana_set = None  # To store the current kana set (hiragana or katakana)

        # Create a frame to center the menu vertically
        self.menu_frame = tk.Frame(self.root, bg=BACKGROUND)
        self.menu_frame.pack(expand=True, fill="both")

        self.create_widgets()

    def resource_path(self, relative_path):
        """Get the absolute path to a resource, works for dev and PyInstaller."""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        # Clear the window
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        # Add padding to the top to center vertically
        self.menu_frame.grid_rowconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure(4, weight=1)
        self.menu_frame.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            self.menu_frame,
            text="Bem-vindo ao Quiz de Kana!",
            font=self.title_font,
            fg=FOREGROUND,
            bg=BACKGROUND
        )
        self.title_label.grid(row=1, column=0, pady=20)

        self.hiragana_button = tk.Button(
            self.menu_frame,
            text="Hiragana",
            font=self.custom_font,
            bg=ACCENT,
            fg=BACKGROUND,
            activebackground=SECONDARY,
            activeforeground=BACKGROUND,
            command=lambda: self.start_quiz(hiragana)
        )
        self.hiragana_button.grid(row=2, column=0, pady=10, ipadx=10, ipady=5)

        self.katakana_button = tk.Button(
            self.menu_frame,
            text="Katakana",
            font=self.custom_font,
            bg=ACCENT,
            fg=BACKGROUND,
            activebackground=SECONDARY,
            activeforeground=BACKGROUND,
            command=lambda: self.start_quiz(katakana)
        )
        self.katakana_button.grid(row=3, column=0, pady=10, ipadx=10, ipady=5)

        self.quit_button = tk.Button(
            self.menu_frame,
            text="Sair",
            font=self.custom_font,
            bg=ERROR,
            fg=BACKGROUND,
            activebackground=SECONDARY,
            activeforeground=BACKGROUND,
            command=self.root.quit
        )
        self.quit_button.grid(row=4, column=0, pady=10, ipadx=10, ipady=5)

    def start_quiz(self, kana_set):
        self.kana_set = kana_set  # Set the current kana set
        self.score = 0
        self.wrong = 0
        self.kana_list = list(self.kana_set.keys())
        random.shuffle(self.kana_list)
        self.current_kana_index = 0
        self.show_question()

    def show_question(self):
        # Clear the window
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        # Add padding to the top to center vertically
        self.menu_frame.grid_rowconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure(4, weight=1)
        self.menu_frame.grid_columnconfigure(0, weight=1)

        if self.current_kana_index < len(self.kana_list):
            kana = self.kana_list[self.current_kana_index]
            self.current_kana = kana
            self.correct_answer = self.kana_set[kana]

            # Display score
            self.score_label = tk.Label(
                self.menu_frame,
                text=f"Pontuação: {self.score} Corretas | {self.wrong} Incorretas",
                font=self.custom_font,
                fg=FOREGROUND,
                bg=BACKGROUND
            )
            self.score_label.grid(row=0, column=0, pady=10)

            self.question_label = tk.Label(
                self.menu_frame,
                text=f"Qual é o romaji para: {kana}",
                font=self.custom_font,
                fg=FOREGROUND,
                bg=BACKGROUND
            )
            self.question_label.grid(row=1, column=0, pady=20)

            self.answer_entry = tk.Entry(
                self.menu_frame,
                font=self.custom_font,
                bg=BACKGROUND,
                fg=FOREGROUND,
                insertbackground=FOREGROUND
            )
            self.answer_entry.grid(row=2, column=0, pady=10)

            # Bind the Enter key to the check_answer method
            self.answer_entry.bind("<Return>", lambda event: self.check_answer())

            self.submit_button = tk.Button(
                self.menu_frame,
                text="Submeter",
                font=self.custom_font,
                bg=ACCENT,
                fg=BACKGROUND,
                activebackground=SECONDARY,
                activeforeground=BACKGROUND,
                command=self.check_answer
            )
            self.submit_button.grid(row=3, column=0, pady=10, ipadx=10, ipady=5)

            # Add "Voltar ao Menu" button
            self.back_button = tk.Button(
                self.menu_frame,
                text="Voltar ao Menu",
                font=self.custom_font,
                bg=SECONDARY,
                fg=BACKGROUND,
                activebackground=ACCENT,
                activeforeground=BACKGROUND,
                command=self.create_widgets
            )
            self.back_button.grid(row=4, column=0, pady=10, ipadx=10, ipady=5)

            # Focus on the entry widget
            self.answer_entry.focus_set()
        else:
            self.show_final_results()

    def check_answer(self, event=None):  # Added event=None to handle Enter key binding
        user_answer = self.answer_entry.get().strip().lower()
        if user_answer == self.correct_answer:
            self.score += 1
            self.show_custom_message("Resposta", "Correto!", ACCENT)
        else:
            self.wrong += 1
            self.show_custom_message("Resposta", f"Incorreto. A resposta correta é: {self.correct_answer}", ERROR)

        self.current_kana_index += 1
        self.show_question()

    def show_final_results(self):
        result_message = f"Quiz concluído!\nSua pontuação final é: {self.score} Corretas | {self.wrong} Incorretas"
        self.show_custom_message("Resultado Final", result_message, SECONDARY)
        self.create_widgets()  # Return to the main menu

    def show_custom_message(self, title, message, color):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x200")
        popup.configure(bg=BACKGROUND)

        label = tk.Label(
            popup, text=message, font=self.custom_font, fg=color, bg=BACKGROUND
        )
        label.pack(pady=20)

        ok_button = tk.Button(
            popup,
            text="OK",
            font=self.custom_font,
            bg=ACCENT,
            fg=BACKGROUND,
            activebackground=SECONDARY,
            activeforeground=BACKGROUND,
            command=lambda: [popup.destroy(), self.answer_entry.focus_set()]
        )
        ok_button.pack(pady=10)

        popup.transient(self.root)  # Mantém o popup na frente da janela principal
        popup.grab_set()  # Bloqueia interações na janela principal até o popup ser fechado
        popup.focus_force()  # Garante que o popup receba foco imediatamente


        # Add OK button
   
    
        ok_button.pack(pady=10)

        # Bind Enter key to close the popup
        popup.bind("<Return>", lambda event: popup.destroy())

        # Center the popup relative to the main window
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")

        # Wait for the popup to be closed
        self.root.wait_window(popup)

if __name__ == "__main__":
    root = tk.Tk()
    app = KanaQuizApp(root)
    root.mainloop()
