import os, customtkinter, ctypes
import tkinter as tk
from pytube import YouTube


# Base window
class Root(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.title("Video/Mp3 Downloader")
        self.resizable(False, False)

        # Label
        self.label = customtkinter.CTkLabel(self, text="Video/Mp3 Downloader")
        self.label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # URL Input
        self.url_input = customtkinter.CTkEntry(
            self, placeholder_text="Enter YouTube URL"
        )
        self.url_input.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

        # Type Menu
        self.type_menu = customtkinter.CTkOptionMenu(
            self,
            values=["Video (.mp4)", "Audio (.mp3)"],
            command=selection,
            width=70,
            height=20,
        )
        self.type_menu.place(relx=0.7, rely=0.30, anchor=tk.CENTER)

        # Resolution Menu
        self.resolution_menu = customtkinter.CTkOptionMenu(
            self,
            values=[
                "Highest resolution",
                "Lowest resolution",
            ],
            width=70,
            height=20,
        )
        self.resolution_menu.place(relx=0.7, rely=0.50, anchor=tk.CENTER)

        # Download Button
        self.download_button = customtkinter.CTkButton(
            self, text="Download", command=download
        )
        self.download_button.place(relx=0.3, rely=0.8, anchor=tk.CENTER)

        # Clear Button
        self.clear_button = customtkinter.CTkButton(
            self, text="Clear URL", command=clear_url
        )
        self.clear_button.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

        self.toplevel_window = None


# Downloads the video
def download():

    try:
        yt = YouTube(root.url_input.get())

    except:
        ctypes.windll.user32.MessageBoxW(
            0, "Unsuported URL. Please enter a valid URL", "Error", 0
        )
        return

    try:
        yt.check_availability()
    except:
        ctypes.windll.user32.MessageBoxW(0, "Video not available", "Error", 0)
        return

    resolution = root.resolution_menu.get()
    type = root.type_menu.get()

    if type == "Video (.mp4)":
        if resolution == "Highest_resolution":
            download = yt.streams.get_highest_resolution()
        else:
            download = yt.streams.get_lowest_resolution()

    else:
        download = yt.streams.filter(only_audio=True).first()

    try:
        title = download.title
        print(title)
        title = title.replace("/", " ")
        title = title.replace("|", "-")
        folder_path = "downloaded_videos"

        if type == "Video (.mp4)":
            folder_path = "downloaded_videos"
            file_path = f"{title}.mp4"
        else:
            folder_path = "downloaded_audios"
            file_path = f"{title}.mp3"

        path = os.path.join(folder_path, file_path)

        if os.path.exists(path):
            ctypes.windll.user32.MessageBoxW(
                0, "Download unsuccessfull. File already exists!", "File found", 0
            )
            return

        download.download(folder_path, file_path)

        if type == "Video (.mp4)":
            ctypes.windll.user32.MessageBoxW(
                0, "Video downloaded successfully.", "Finished", 0
            )
        else:
            ctypes.windll.user32.MessageBoxW(
                0, "Audio downloaded successfully.", "Finished", 0
            )
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, str(e), "error", 0)


# Changes the state of the resolution menu
def selection(self):
    if root.type_menu.get() == "Video (.mp4)":
        root.resolution_menu.configure(state="normal")
    else:
        root.resolution_menu.configure(state="disabled")


# Clears the URL input
def clear_url():
    root.url_input.delete(0, tk.END)


# Start main loop
root = Root()
root.mainloop()
