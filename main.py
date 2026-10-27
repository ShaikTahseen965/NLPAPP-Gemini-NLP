
from tkinter import *
from tkinter import messagebox

from mydb import Database
from myapi import API


class NLPAPP:
    def __init__(self):
        self.root = Tk()
        self.root.title("NLPAPP - Natural Language Processing")
        self.root.geometry("850x600")
        self.root.minsize(700, 500)
        self.root.configure(bg="#f4f6f9")

        self.dbo = Database()

        try:
            self.apio = API()
            self.api_error = None
        except Exception as error:
            self.apio = None
            self.api_error = str(error)

        self.login_gui()
        self.root.mainloop()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle=None):
        Label(
            self.root,
            text=title,
            font=("Arial", 24, "bold"),
            bg="#f4f6f9",
            fg="#263238"
        ).pack(pady=(25, 8))

        if subtitle:
            Label(
                self.root,
                text=subtitle,
                font=("Arial", 11),
                bg="#f4f6f9",
                fg="#607d8b"
            ).pack(pady=(0, 18))

    def make_button(self, parent, text, command):
        return Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg="#1976d2",
            fg="white",
            activebackground="#1565c0",
            activeforeground="white",
            relief=FLAT,
            cursor="hand2",
            padx=14,
            pady=9
        )

    # ---------------- LOGIN ----------------

    def login_gui(self):
        self.clear()
        self.heading(
            "NLPAPP",
            "Natural Language Processing Application"
        )

        frame = Frame(self.root, bg="white", padx=35, pady=25)
        frame.pack(pady=15)

        Label(
            frame,
            text="Login",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#263238"
        ).pack(pady=(0, 15))

        Label(
            frame,
            text="Email",
            bg="white",
            anchor="w"
        ).pack(fill=X)

        self.login_email = Entry(frame, font=("Arial", 12), width=35)
        self.login_email.pack(pady=(5, 12), ipady=5)

        Label(
            frame,
            text="Password",
            bg="white",
            anchor="w"
        ).pack(fill=X)

        self.login_password = Entry(
            frame,
            font=("Arial", 12),
            width=35,
            show="*"
        )
        self.login_password.pack(pady=(5, 18), ipady=5)

        self.make_button(
            frame,
            "Login",
            self.perform_login
        ).pack(fill=X, pady=5)

        Button(
            frame,
            text="Create a new account",
            command=self.register_gui,
            bg="white",
            fg="#1976d2",
            relief=FLAT,
            cursor="hand2"
        ).pack(pady=(10, 0))

    def perform_login(self):
        email = self.login_email.get().strip()
        password = self.login_password.get()

        if not email or not password:
            messagebox.showwarning(
                "Missing information",
                "Please enter your email and password."
            )
            return

        try:
            result = self.dbo.search(email, password)
        except Exception as error:
            messagebox.showerror("Login error", str(error))
            return

        if result:
            self.home_gui()
        else:
            messagebox.showerror(
                "Login failed",
                "Invalid email or password."
            )

    # ---------------- REGISTRATION ----------------

    def register_gui(self):
        self.clear()
        self.heading("Create Account", "Register to use NLPAPP")

        frame = Frame(self.root, bg="white", padx=35, pady=25)
        frame.pack(pady=10)

        Label(
            frame,
            text="Full Name",
            bg="white",
            anchor="w"
        ).pack(fill=X)

        self.reg_name = Entry(frame, font=("Arial", 12), width=35)
        self.reg_name.pack(pady=(5, 12), ipady=5)

        Label(
            frame,
            text="Email",
            bg="white",
            anchor="w"
        ).pack(fill=X)

        self.reg_email = Entry(frame, font=("Arial", 12), width=35)
        self.reg_email.pack(pady=(5, 12), ipady=5)

        Label(
            frame,
            text="Password",
            bg="white",
            anchor="w"
        ).pack(fill=X)

        self.reg_password = Entry(
            frame,
            font=("Arial", 12),
            width=35,
            show="*"
        )
        self.reg_password.pack(pady=(5, 18), ipady=5)

        self.make_button(
            frame,
            "Register",
            self.perform_registration
        ).pack(fill=X, pady=5)

        Button(
            frame,
            text="Back to Login",
            command=self.login_gui,
            bg="white",
            fg="#1976d2",
            relief=FLAT,
            cursor="hand2"
        ).pack(pady=(10, 0))

    def perform_registration(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get()

        if not name or not email or not password:
            messagebox.showwarning(
                "Missing information",
                "Please fill in all fields."
            )
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning(
                "Invalid email",
                "Please enter a valid email address."
            )
            return

        try:
            # Database format: email -> [name, password]
            self.dbo.add_data(name, email, password)
        except Exception as error:
            messagebox.showerror(
                "Registration error",
                str(error)
            )
            return

        messagebox.showinfo(
            "Success",
            "Registration completed successfully."
        )
        self.login_gui()

    # ---------------- HOME ----------------

    def home_gui(self):
        self.clear()
        self.heading(
            "Welcome to NLPAPP",
            "Choose an NLP task to get started"
        )

        frame = Frame(self.root, bg="#f4f6f9")
        frame.pack(expand=True, fill=BOTH, padx=40, pady=10)

        self.make_button(
            frame,
            "Sentiment Analysis",
            self.sentiment_gui
        ).pack(fill=X, pady=8, ipady=5)

        self.make_button(
            frame,
            "Named Entity Recognition (NER)",
            self.ner_gui
        ).pack(fill=X, pady=8, ipady=5)

        self.make_button(
            frame,
            "Emotion Prediction",
            self.emotion_gui
        ).pack(fill=X, pady=8, ipady=5)

        Button(
            frame,
            text="Logout",
            command=self.login_gui,
            font=("Arial", 10),
            bg="#e0e0e0",
            relief=FLAT,
            cursor="hand2"
        ).pack(pady=25)

    # ---------------- SHARED ANALYSIS SCREEN ----------------

    def analysis_gui(self, title, description, command):
        self.clear()
        self.heading(title, description)

        frame = Frame(self.root, bg="white", padx=25, pady=20)
        frame.pack(fill=BOTH, expand=True, padx=35, pady=10)

        Label(
            frame,
            text="Enter your text:",
            font=("Arial", 11, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill=X, pady=(0, 8))

        self.input_text = Text(
            frame,
            height=6,
            font=("Arial", 12),
            wrap=WORD,
            relief=SOLID,
            bd=1
        )
        self.input_text.pack(fill=X, pady=(0, 15))

        self.make_button(
            frame,
            "Analyze",
            command
        ).pack(fill=X, pady=5)

        Label(
            frame,
            text="Result",
            font=("Arial", 11, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill=X, pady=(15, 5))

        self.output_text = Text(
            frame,
            height=7,
            font=("Arial", 11),
            wrap=WORD,
            relief=SOLID,
            bd=1,
            state=DISABLED
        )
        self.output_text.pack(fill=BOTH, expand=True)

        Button(
            self.root,
            text="Back to Home",
            command=self.home_gui,
            bg="#e0e0e0",
            relief=FLAT,
            cursor="hand2"
        ).pack(pady=(0, 15))

    def display_result(self, result):
        self.output_text.config(state=NORMAL)
        self.output_text.delete("1.0", END)
        self.output_text.insert(END, result)
        self.output_text.config(state=DISABLED)

    def get_input(self):
        text = self.input_text.get("1.0", END).strip()

        if not text:
            messagebox.showwarning(
                "Missing text",
                "Please enter some text to analyze."
            )
            return None

        return text

    def run_analysis(self, function, text):
        if self.apio is None:
            messagebox.showerror(
                "API configuration error",
                "Gemini could not be initialized.\n\n"
                + str(self.api_error)
            )
            return None

        try:
            return function(text)
        except Exception as error:
            messagebox.showerror(
                "Analysis error",
                "The analysis could not be completed.\n\n"
                + str(error)
            )
            return None

    # ---------------- SENTIMENT ANALYSIS ----------------

    def sentiment_gui(self):
        self.analysis_gui(
            "Sentiment Analysis",
            "Determine whether text expresses positive, negative, or neutral sentiment.",
            self.do_sentiment_analysis
        )

    def do_sentiment_analysis(self):
        text = self.get_input()

        if text is None:
            return

        result = self.run_analysis(
            self.apio.sentiment_analysis if self.apio else None,
            text
        )

        if result is None:
            return

        compound = result["compound"]
        positive = result["pos"]
        negative = result["neg"]
        neutral = result["neu"]

        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        output = (
            f"Predicted sentiment: {sentiment}\n\n"
            f"Compound score: {compound:.3f}\n"
            f"Positive score: {positive:.3f}\n"
            f"Negative score: {negative:.3f}\n"
            f"Neutral score: {neutral:.3f}\n\n"
            "Note: These scores are Gemini-generated estimates."
        )

        self.display_result(output)

    # ---------------- NAMED ENTITY RECOGNITION ----------------

    def ner_gui(self):
        self.analysis_gui(
            "Named Entity Recognition",
            "Identify people, places, organizations, dates, and other entities.",
            self.do_ner
        )

    def do_ner(self):
        text = self.get_input()

        if text is None:
            return

        result = self.run_analysis(
            self.apio.ner if self.apio else None,
            text
        )

        if result is None:
            return

        if not result:
            self.display_result("No named entities found.")
            return

        lines = ["Identified entities:\n"]

        for entity_text, label in result:
            lines.append(f"{entity_text} — {label}")

        self.display_result("\n".join(lines))

    # ---------------- EMOTION PREDICTION ----------------

    def emotion_gui(self):
        self.analysis_gui(
            "Emotion Prediction",
            "Identify the main emotion expressed in your text.",
            self.do_emotion
        )

    def do_emotion(self):
        text = self.get_input()

        if text is None:
            return

        result = self.run_analysis(
            self.apio.emotion_prediction if self.apio else None,
            text
        )

        if result is None:
            return

        self.display_result(
            f"Predicted emotion: {result}"
        )


if __name__ == "__main__":
    NLPAPP()
