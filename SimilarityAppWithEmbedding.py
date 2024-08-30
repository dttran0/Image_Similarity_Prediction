import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
from img_search import ImgSearcher
from TextSimilarity import TextSimilarity

class SimilarityApp:
    def __init__(self, root):
        self.model = ImgSearcher()
        self.root = root
        self.root.title("Similarity Calculator")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        # Set default font for the entire application
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.config(family="Helvetica", size=12)
        self.root.option_add("*Font", default_font)

        self.image1 = None
        self.image2 = None

        self.text1 = tk.StringVar()
        self.text2 = tk.StringVar()

        self.seed_image = None

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Set common dimensions
        common_width = 37
        common_height = 20
        canvas_size = 330  # Assuming each canvas is 300x300 pixels

        # Type selection
        self.type_frame = tk.Frame(self.root)
        self.type_frame.pack(pady=10)
        
        self.type_label = tk.Label(self.type_frame, text="Select type:")
        self.type_label.pack(side=tk.LEFT)

        self.type_var = tk.StringVar(value="Image")
        self.type_menu = ttk.Combobox(self.type_frame, textvariable=self.type_var)
        self.type_menu['values'] = ("Image", "Text", "Search Similar Pictures")
        self.type_menu.pack(side=tk.LEFT)
        self.type_menu.bind("<<ComboboxSelected>>", self.update_ui)

        # Image 1 frame
        self.frame1 = tk.Frame(self.root)
        self.label1 = tk.Label(self.frame1, text="Drop Image 1 here")
        self.label1.pack()
        self.canvas1 = tk.Canvas(self.frame1, width=canvas_size, height=canvas_size, bg="gray")
        self.canvas1.pack(expand=True)
        self.canvas1.bind("<Button-1>", self.load_image1)

        # Image 2 frame (hidden for Search Similar Pictures type)
        self.frame2 = tk.Frame(self.root)
        self.label2 = tk.Label(self.frame2, text="Drop Image 2 here")
        self.label2.pack()
        self.canvas2 = tk.Canvas(self.frame2, width=canvas_size, height=canvas_size, bg="gray")
        self.canvas2.pack(expand=True)
        self.canvas2.bind("<Button-1>", self.load_image2)

        # Text input fields (initially hidden)
        self.text_frame1 = tk.Frame(self.root)
        self.text_label1 = tk.Label(self.text_frame1, text="Enter Text 1")
        self.text_label1.pack()
        self.text_entry1 = tk.Text(self.text_frame1, width=common_width, height=common_height)
        self.text_entry1.pack()

        self.text_frame2 = tk.Frame(self.root)
        self.text_label2 = tk.Label(self.text_frame2, text="Enter Text 2")
        self.text_label2.pack()
        self.text_entry2 = tk.Text(self.text_frame2, width=common_width, height=common_height)
        self.text_entry2.pack()

        # seed Image frame
        self.seed_frame = tk.Frame(self.root)

        self.embedding_frame = tk.Frame(self.seed_frame)
        self.button_select_path = tk.Button(self.embedding_frame, text="Select Picture Path", command=self.select_directory)
        self.button_select_path.pack(side=tk.LEFT, padx=10)

        self.entry_path = tk.Entry(self.embedding_frame, width=40)
        self.entry_path.pack(side=tk.LEFT, padx=10)

        self.button_embedding = tk.Button(self.embedding_frame, text="Embedding", command=self.on_embedding_button_click)
        self.button_embedding.pack(side=tk.LEFT, padx=10)

        # Setup progress bar at the bottom
        self.progress_frame = ttk.Frame(self.root, padding=(20, 10))
        self.progress_label = ttk.Label(self.progress_frame, text="Embedding Progress:")
        self.progress_label.pack(side='left')

        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=200, mode='determinate')
        self.progress.pack(side='left', padx=5)

        self.progress_percent = ttk.Label(self.progress_frame, text="0%")
        self.progress_percent.pack(side='left', padx=5)


        self.embedding_frame.pack(side=tk.TOP, padx=10, pady=1, expand=True)

        self.seed_pic_frame = tk.Frame(self.seed_frame)
        self.seed_label = tk.Label(self.seed_pic_frame, text="Drop Image to Search")
        self.seed_label.pack(side=tk.TOP)
        self.seed_canvas = tk.Canvas(self.seed_pic_frame, width=120, height=120, bg="gray")
        self.seed_canvas.pack(side=tk.BOTTOM)
        self.seed_canvas.bind("<Button-1>", self.load_seed_image)
        self.seed_pic_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)


        # Results frame for displaying similar images
        self.results_frame = tk.Frame(self.seed_frame)

        # Add a frame at the bottom for the button and result label
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Move the calculate button and result label to the bottom frame
        self.calculate_button = tk.Button(self.bottom_frame, text="Calculate Similarity", command=self.calculate_similarity)
        self.calculate_button.pack(side=tk.LEFT, padx=10)

        self.result_label = tk.Label(self.bottom_frame, text="")
        self.result_label.pack(side=tk.LEFT, padx=10)

        self.update_ui()

    def update_ui(self, event=None):
        selection = self.type_var.get()
        self.clear_ui()

        if selection == "Image":
            self.text_frame1.pack_forget()
            self.text_frame2.pack_forget()
            self.seed_frame.pack_forget()
            self.results_frame.pack_forget()
            self.frame1.pack(side=tk.LEFT, padx=10, pady=10, expand=True)
            self.frame2.pack(side=tk.RIGHT, padx=10, pady=10, expand=True)

            self.calculate_button.config(text="Calculate Similarity", command=self.calculate_similarity)

        elif selection == "Text":
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.seed_frame.pack_forget()
            self.results_frame.pack_forget()

            self.text_frame1.pack(side=tk.LEFT, padx=10, pady=10)
            self.text_frame2.pack(side=tk.RIGHT, padx=10, pady=10)

            self.calculate_button.config(text="Calculate Similarity", command=self.calculate_similarity)

        elif selection == "Search Similar Pictures":
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.text_frame1.pack_forget()
            self.text_frame2.pack_forget()
            # self.seed_frame.pack(side=tk.LEFT, padx=10, pady=10)
            self.seed_frame.pack(side=tk.TOP, padx=10, pady=10)
            self.results_frame.pack(side=tk.RIGHT, padx=10, pady=10, expand=True)

            self.label1.config(text="Drop Image to Search")
            self.calculate_button.config(text="Find Similar Images", command=self.find_similar_images)

    def clear_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def clear_ui(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.text_frame1.pack_forget()
        self.text_frame2.pack_forget()
        self.seed_frame.pack_forget()
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")

    def on_embedding_button_click(self):
        self.progress_frame.pack(side='bottom', fill='x')
        self.root.update_idletasks()
        directory_path = self.entry_path.get()
        files = os.listdir(directory_path)
        self.progress['maximum'] = len(files)
        self.process_files(0, files)

    def process_files(self, index, files):
        if index < len(files):
            filename = files[index]
            directory_path = self.entry_path.get()
            file_path = os.path.join(directory_path, filename)
            
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                try:
                    self.model.add_img(file_path)  # Assuming self.model is defined elsewhere
                except Exception as e:
                    print(f"Could not process image {file_path}: {e}")

            self.update_progress(index + 1)
            self.root.after(10, self.process_files, index + 1, files)  # Schedule the next file processing
        else:
            self.embedding_finished()

    def update_progress(self, value):
        self.progress['value'] = value
        percentage = (value / self.progress['maximum']) * 100
        self.progress_percent.config(text=f"{percentage:.1f}%")
        self.root.update_idletasks()

    def embedding_finished(self):
        self.progress_frame.pack_forget()
        self.root.update_idletasks()

    def select_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, directory_path)

    def load_image1(self, event):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image1 = Image.open(file_path)
            self.display_image(self.image1, self.canvas1)

    def load_image2(self, event):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image2 = Image.open(file_path)
            self.display_image(self.image2, self.canvas2)

    def load_seed_image(self, event):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.seed_image = Image.open(file_path)
            self.display_image(self.seed_image, self.seed_canvas)

    def display_image(self, image, canvas):
        # Get the size of the canvas
        canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()

        # Calculate the scale factor to fit the image within the canvas
        image_ratio = image.width / image.height
        canvas_ratio = canvas_width / canvas_height

        if image_ratio > canvas_ratio:
            scale_factor = canvas_width / image.width
        else:
            scale_factor = canvas_height / image.height

        # Resize the image maintaining the aspect ratio
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        resized_image = image.resize((new_width, new_height))

        # Convert the image to a PhotoImage object
        image_tk = ImageTk.PhotoImage(resized_image)

        # Clear the canvas before displaying a new image
        canvas.delete("all")

        # Display the image in the center of the canvas
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=image_tk, anchor=tk.CENTER)

        # Keep a reference to the image object to prevent it from being garbage collected
        canvas.image = image_tk

    def calculate_similarity(self):
        selection = self.type_var.get()
        if selection == "Image":
            if self.image1 is None or self.image2 is None:
                messagebox.showerror("Error", "Please load both images")
                return
            score = self.calculate_pic_similarity(self.image1, self.image2)
            self.result_label.config(text=f"Similarity Score: {score:.2f}")

        elif selection == "Text":
            text1 = self.text_entry1.get("1.0", tk.END).strip()
            text2 = self.text_entry2.get("1.0", tk.END).strip()

            if not text1 or not text2:
                messagebox.showerror("Error", "Please enter both texts")
                return

            # Calculate text similarity using TF-IDF and cosine similarity
            score = self.calculate_text_similarity(text1, text2)
            self.result_label.config(text=f"Similarity Score: {score:.2f}")

    def calculate_pic_similarity(self, img1, img2):
        score = self.model.get_cosine_similarity(img1.filename, img2.filename)
        return score[0][0]

    def calculate_text_similarity(self, text1, text2):
        text_similarity = TextSimilarity()
        score = text_similarity.calculate_similarity(text1, text2)
        return score

    def resize_image(self, img_path, max_size=(120, 120)):
        with Image.open(img_path) as img:
            original_width, original_height = img.size

            ratio = min(max_size[0] / original_width, max_size[1] / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            img = img.resize((new_width, new_height))

            return img

    def sort_result(self, res):
        combined = list(zip(
            res['ids'][0],
            res['distances'][0],
            res['metadatas'][0],
            res['documents'][0],
        ))
        combined_sorted = sorted(combined, key=lambda x: x[1], reverse=True)
        res = {
            'ids': [[item[0] for item in combined_sorted]],
            'distances': [[item[1] for item in combined_sorted]],
            'metadatas': [[item[2] for item in combined_sorted]],
            'documents': [[item[3] for item in combined_sorted]]
        }
        return res

    def find_similar_images(self):
        if self.seed_image is None:
            messagebox.showerror("Error", "Please load an image to search")
            return

        # Calculate similarity with database images
        result = self.model.query(self.seed_image.filename, 4)

        # Reverse search results
        # result = self.sort_result(result)

        similar_images = result['documents'][0]
        distances = result['distances'][0]

        # Display top 5 similar images
        for i, (img_path, distance) in enumerate(zip(similar_images, distances)):
            row, col = divmod(i, 2)
            img = self.resize_image(img_path, (120, 120))
            # img = Image.open(img_path)
            # img = img.resize((120, 120))
            img_tk = ImageTk.PhotoImage(img)

            img_label = tk.Label(self.results_frame, image=img_tk)
            img_label.image = img_tk
            img_label.grid(row=row*2, column=col, padx=10, pady=5)  # Double row index for spacing

            distance_label = tk.Label(self.results_frame, text=f"{1 - distance:.4f}")
            distance_label.grid(row=row*2+1, column=col, padx=10, pady=1)  # Place below the image

        self.result_label.config(text="Top 4 similar images found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimilarityApp(root)
    root.mainloop()
