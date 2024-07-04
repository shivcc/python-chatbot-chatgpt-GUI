import openai
import requests
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox


class Chatbot:
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_response(self, prompt):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def get_image(self, query):
        url = f"https://api.unsplash.com/photos/random?query={query}&client_id=YOUR_UNSPLASH_ACCESS_KEY"
        response = requests.get(url)
        if response.status_code == 200:
            image_url = response.json()['urls']['small']
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            return image
        else:
            return None
        
class ChatbotGUI:
    def __init__(self, chatbot):
        self.chatbot = chatbot

        self.root = tk.Tk()
        self.root.title("ChatGPT Chatbot")

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.chat_area.pack(pady=10)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5)

        self.input_field = tk.Entry(self.input_frame, width=50)
        self.input_field.pack(side=tk.LEFT, padx=10)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.root.bind('<Return>', lambda event: self.send_message())

    def send_message(self):
        user_message = self.input_field.get()
        if user_message:
            self.display_message("You: " + user_message, "black")
            self.input_field.delete(0, tk.END)

            bot_response = self.chatbot.get_response(user_message)
            self.display_message("Bot: " + bot_response, "blue")

            if "image:" in user_message.lower():
                image_query = user_message.split("image:", 1)[1].strip()
                image = self.chatbot.get_image(image_query)
                if image:
                    self.display_image(image)
                else:
                    messagebox.showerror("Error", "Could not fetch image")

    def display_message(self, message, color):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message + "\n", ('color', color))
        self.chat_area.tag_configure('color', foreground=color)
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)

    def display_image(self, image):
        image.show()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    api_key = "your-API-Key"  # Replace with your OpenAI API key
    chatbot = Chatbot(api_key)
    gui = ChatbotGUI(chatbot)
    gui.run()
