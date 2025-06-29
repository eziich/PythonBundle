# Requirements: pandas, matplotlib
# Install with: pip install pandas matplotlib
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title('CSV Analytics App')
        self.df = None
        self.create_widgets()

    def create_widgets(self):
        self.upload_btn = tk.Button(self.root, text='Upload CSV', command=self.upload_csv)
        self.upload_btn.pack(pady=10)

        self.preview_label = tk.Label(self.root, text='Data Preview:')
        self.preview_label.pack()
        self.preview_text = tk.Text(self.root, height=10, width=80)
        self.preview_text.pack()

        self.stats_label = tk.Label(self.root, text='Summary Statistics:')
        self.stats_label.pack()
        self.stats_text = tk.Text(self.root, height=10, width=80)
        self.stats_text.pack()

        self.charts_frame = tk.Frame(self.root)
        self.charts_frame.pack(pady=10)

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if not file_path:
            return
        try:
            self.df = pd.read_csv(file_path)
            self.show_preview()
            self.show_stats()
            self.show_charts()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load CSV: {e}')

    def show_preview(self):
        self.preview_text.delete('1.0', tk.END)
        if self.df is not None:
            preview = self.df.head().to_string(index=False)
            self.preview_text.insert(tk.END, preview)

    def show_stats(self):
        self.stats_text.delete('1.0', tk.END)
        if self.df is not None:
            stats = self.df.describe(include='all').to_string()
            self.stats_text.insert(tk.END, stats)

    def show_charts(self):
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
        if self.df is None:
            return
        numeric_cols = self.df.select_dtypes(include='number').columns
        categorical_cols = self.df.select_dtypes(include='object').columns
        # Histograms for numeric columns
        for col in numeric_cols:
            fig, ax = plt.subplots(figsize=(3,2))
            self.df[col].hist(ax=ax, bins=10, color='skyblue', edgecolor='black')
            ax.set_title(f'Histogram: {col}')
            canvas = FigureCanvasTkAgg(fig, master=self.charts_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.LEFT, padx=5)
            plt.close(fig)
        # Bar/pie charts for categorical columns (if few unique values)
        for col in categorical_cols:
            value_counts = self.df[col].value_counts()
            if len(value_counts) <= 10:
                # Bar chart
                fig, ax = plt.subplots(figsize=(3,2))
                value_counts.plot(kind='bar', ax=ax, color='lightgreen', edgecolor='black')
                ax.set_title(f'Bar: {col}')
                canvas = FigureCanvasTkAgg(fig, master=self.charts_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.LEFT, padx=5)
                plt.close(fig)
                # Pie chart
                fig, ax = plt.subplots(figsize=(3,2))
                value_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%')
                ax.set_ylabel('')
                ax.set_title(f'Pie: {col}')
                canvas = FigureCanvasTkAgg(fig, master=self.charts_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.LEFT, padx=5)
                plt.close(fig)

def main():
    root = tk.Tk()
    app = CSVAnalyticsApp(root)
    root.mainloop()

if __name__ == '__main__':
    main() 