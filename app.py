import raceList
from race import Race
from horse import Horse, HorseFilter
import form
from interpreter import QueryInterpreter

import tkinter as tk
from race_frame import RaceFrame
from horse_frame import HorseFrame
from analysis_frame import AnalysisFrame

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.race_name = ''
        self.races = []
        self.horce_list = []

        self.ff = form.FormFilter()
        self.fe = form.FormEvaluator()
        self.hf = HorseFilter()
        self.qi = QueryInterpreter(self.hf,self.ff,self.fe)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = []
        
        for F in [RaceFrame, HorseFrame, AnalysisFrame]:
            frame = F(container, self)
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.exec_frame(0)
    
    def exec_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.after(10 ,frame.start_process)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
