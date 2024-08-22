import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

class PointPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Points Plotter")
        self.root.configure(bg='#2e2e2e')

        # Configure style for Tkinter widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2e2e2e')
        self.style.configure('TLabel', background='#2e2e2e', foreground='#cccccc', font=('Helvetica', 10))
        self.style.configure('TButton', background='#444444', foreground='#cccccc', font=('Helvetica', 10, 'bold'))
        self.style.map('TButton', background=[('active', '#555555')], foreground=[('active', '#ffffff')])
        self.style.configure('TEntry', fieldbackground='#555555', foreground='#cccccc')
        self.style.configure('TLabelframe', background='#2e2e2e', foreground='#cccccc', font=('Helvetica', 10, 'bold'))
        self.style.configure('TLabelframe.Label', background='#2e2e2e', foreground='#cccccc')

        self.create_widgets()

        # Initialize default point and line colors
        self.point_color = '#ff3333'
        self.line_color = '#33ccff'
        self.points = None
        self.canvas = None
        self.fig = None
        self.ax = None
        self.scatter = None
        self.distance_text = None

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Create input fields for Point 1
        self.frame_point1 = ttk.Labelframe(self.root, text="Point 1", style='TLabelframe')
        self.frame_point1.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(self.frame_point1, text="X1:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_x1 = ttk.Entry(self.frame_point1, style='TEntry')
        self.entry_x1.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_point1, text="Y1:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_y1 = ttk.Entry(self.frame_point1, style='TEntry')
        self.entry_y1.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame_point1, text="Z1:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_z1 = ttk.Entry(self.frame_point1, style='TEntry')
        self.entry_z1.grid(row=2, column=1, padx=5, pady=5)

        # Create input fields for Point 2
        self.frame_point2 = ttk.Labelframe(self.root, text="Point 2", style='TLabelframe')
        self.frame_point2.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(self.frame_point2, text="X2:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_x2 = ttk.Entry(self.frame_point2, style='TEntry')
        self.entry_x2.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_point2, text="Y2:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_y2 = ttk.Entry(self.frame_point2, style='TEntry')
        self.entry_y2.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame_point2, text="Z2:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_z2 = ttk.Entry(self.frame_point2, style='TEntry')
        self.entry_z2.grid(row=2, column=1, padx=5, pady=5)

        # Create plot button
        self.plot_button = ttk.Button(self.root, text="Plot Points and Line", command=self.plot_points, style='TButton')
        self.plot_button.pack(pady=10)

        # Create buttons to choose colors
        self.point_color_button = ttk.Button(self.root, text="Choose Point Color", command=self.choose_point_color, style='TButton')
        self.point_color_button.pack(pady=5)

        self.line_color_button = ttk.Button(self.root, text="Choose Line Color", command=self.choose_line_color, style='TButton')
        self.line_color_button.pack(pady=5)

        # Frame to hold the plot
        self.plot_frame = ttk.Frame(self.root, style='TFrame')
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def choose_point_color(self):
        # Open color chooser dialog for point color
        self.point_color = colorchooser.askcolor(title="Choose Point Color")[1]
        if self.points is not None:
            self.update_plot()

    def choose_line_color(self):
        # Open color chooser dialog for line color
        self.line_color = colorchooser.askcolor(title="Choose Line Color")[1]
        if self.points is not None:
            self.update_plot()

    def on_scroll(self, event):
        # Handle mouse scroll for zooming in and out
        scale_factor = 1.05 if event.button == 'up' else 0.95
        xlim = self.ax.get_xlim3d()
        ylim = self.ax.get_ylim3d()
        zlim = self.ax.get_zlim3d()

        xdata = event.xdata
        ydata = event.ydata
        zdata = (zlim[1] + zlim[0]) / 2

        x_centered = [(x - xdata) * scale_factor + xdata for x in xlim]
        y_centered = [(y - ydata) * scale_factor + ydata for y in ylim]
        z_centered = [(z - zdata) * scale_factor + zdata for z in zlim]

        self.ax.set_xlim3d(x_centered)
        self.ax.set_ylim3d(y_centered)
        self.ax.set_zlim3d(z_centered)

        self.canvas.draw()

    def update_entries(self):
        # Update the entry fields with the new coordinates of the points
        x1, y1, z1 = self.points[0]
        x2, y2, z2 = self.points[1]
        self.entry_x1.delete(0, tk.END)
        self.entry_x1.insert(0, str(x1))
        self.entry_y1.delete(0, tk.END)
        self.entry_y1.insert(0, str(y1))
        self.entry_z1.delete(0, tk.END)
        self.entry_z1.insert(0, str(z1))

        self.entry_x2.delete(0, tk.END)
        self.entry_x2.insert(0, str(x2))
        self.entry_y2.delete(0, tk.END)
        self.entry_y2.insert(0, str(y2))
        self.entry_z2.delete(0, tk.END)
        self.entry_z2.insert(0, str(z2))

    def update_plot(self):
        # Update the plot with the new coordinates and colors
        self.ax.clear()
        x1, y1, z1 = self.points[0]
        x2, y2, z2 = self.points[1]
        self.scatter = self.ax.scatter(*zip(*self.points), c=self.point_color, marker='o')
        self.ax.plot([x1, x2], [y1, y2], [z1, z2], color=self.line_color)

        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        if self.distance_text:
            self.distance_text.remove()
        self.distance_text = self.ax.text2D(0.05, 0.95, f"Distance: {distance:.2f}", transform=self.ax.transAxes, color='white')

        self.ax.set_xlabel('X', color='white')
        self.ax.set_ylabel('Y', color='white')
        self.ax.set_zlabel('Z', color='white')
        self.ax.tick_params(colors='white')
        self.canvas.draw()

    def plot_points(self):
        # Get the coordinates from the entry fields and plot the points
        try:
            x1, y1, z1 = float(self.entry_x1.get()), float(self.entry_y1.get()), float(self.entry_z1.get())
            x2, y2, z2 = float(self.entry_x2.get()), float(self.entry_y2.get()), float(self.entry_z2.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for all coordinates.")
            return

        self.points = np.array([[x1, y1, z1], [x2, y2, z2]])

        if self.fig is None or self.ax is None:
            self.fig = plt.figure(facecolor='#2e2e2e')
            self.ax = self.fig.add_subplot(111, projection='3d', facecolor='#2e2e2e')
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.canvas.mpl_connect('scroll_event', self.on_scroll)

        self.update_plot()

    def on_closing(self):
        # Handle window close event
        self.root.quit()
        self.root.destroy()

root = tk.Tk()
app = PointPlotter(root)
root.mainloop()
