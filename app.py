import tkinter as tk
from race_frame import RaceFrame
from horse_frame import HorseFrame
from analysis_frame import AnalysisFrame

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = []
        
        for F in [RaceFrame, HorseFrame, AnalysisFrame]:
            frame = F(container, self)
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(0)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
