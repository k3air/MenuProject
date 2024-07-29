import openai
import speech_recognition as sr
import tkinter as tk
from datetime import datetime

# Set up OpenAI API credentials
openai.api_key = ''

# Function to get current time formatted as a string
def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].message['content'].strip()
    return message

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "quit speaking this gibberish bozo."
    except sr.RequestError:
        return "Sorry, my speech recognition service is currently down."

class ChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Billionairebot")
        self.window.geometry("600x400")

        self.scroll_frame = tk.Frame(self.window)
        self.scroll_frame.pack(side="top", fill="both", expand=True)

        self.chat_history = tk.Text(self.scroll_frame, wrap="word", state="disabled")
        self.chat_history.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.scroll_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_history.configure(yscrollcommand=self.scrollbar.set)

        self.question_entry = tk.Entry(self.window, width=60, font=("Arial", 12))
        self.question_entry.pack(pady=10, padx=10, side="left")

        self.ask_button = tk.Button(self.window, text="Ask", width=10, command=self.ask_question, font=("Arial", 12))
        self.ask_button.pack(pady=10, padx=10, side="left")

        self.listen_button = tk.Button(self.window, text="Speak", width=10, command=self.listen_question, font=("Arial", 12))
        self.listen_button.pack(pady=10, padx=10, side="left")

        self.clear_button = tk.Button(self.window, text="Clear", width=10, command=self.clear_all, font=("Arial", 12))
        self.clear_button.pack(pady=10, padx=10, side="left")

        self.window.mainloop()

    def clear_all(self):
        self.chat_history.configure(state="normal")
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.configure(state="disabled")

    def ask_question(self):
        question = self.question_entry.get().strip()
        if question != "":
            response = ask_openai(question)
            self.update_chat_history(question, response)

    def listen_question(self):
        question = recognize_speech()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, question)
        response = ask_openai(question)
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state="normal")
        
        # Insert user question
        self.chat_history.insert("end", f"{current_time()} User: {question}\n", "user")
        self.chat_history.tag_configure("user", justify="left", foreground="#218aff", font=("Arial", 12))

        # Insert bot response
        self.chat_history.insert("end", f"{current_time()} Bot: {response}\n", "bot")
        self.chat_history.tag_configure("bot", justify="left", foreground="#aeb9cc", font=("Arial", 12))

        self.chat_history.configure(state="disabled")
        self.chat_history.yview(tk.END)

if __name__ == "__main__":
    gui = ChatbotGUI()
    