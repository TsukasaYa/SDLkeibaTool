from horse import HorseFilter
from form import FormFilter, FormEvaluator
import main


class QueryInterpreter:

    def __init__(self, hf:HorseFilter, ff:FormFilter, fe:FormEvaluator):
        self.hf = hf
        self.ff = ff
        self.fe = fe
    
    def interpret(self, query, fl):
        for stmt in query.split('&'):
            stmt = [token for token in stmt.split(' ') if token != '']
            if len(stmt) >= 1 and (stmt[0] == 'q' or stmt[0] == 'quit'):
                loop = False
                continue
            
            if stmt[0] == 'plot':
                main.plot_horses(fl)
            elif stmt[0] == 'dump':
                main.dump_horses(fl)
            elif len(stmt) < 2:
                input_error(stmt, ", self.few token")
                continue
            
            if stmt[0] == 'self.ff':
                if stmt[1] == 'clear' or stmt[1] == 'c':
                    self.ff.pre = None
                    self.ff.smile = None
                    self.ff.course = None
                    self.ff.race = None
                    self.ff.style = None
                    self.ff.post = None
                elif stmt[1] == 'pre':
                    if len(stmt)== 2:
                        self.ff.pre = None
                    else:
                        self.ff.pre = int(stmt[2])
                elif stmt[1] == 'smile':
                    if len(stmt)== 2:
                        self.ff.smile = None
                    else:
                        self.ff.smile = stmt[2:]
                elif stmt[1] == 'course':
                    if len(stmt)== 2:
                        self.ff.course = None
                    else:
                        self.ff.course = stmt[2:]
                elif stmt[1] == 'style':
                    if len(stmt)== 2:
                        self.ff.style = None
                    else:
                        self.ff.style = stmt[2:]
                elif stmt[1] == 'race':
                    if len(stmt)== 2:
                        self.ff.race = None
                    else:
                        self.ff.race = stmt[2]
                elif stmt[1] == 'post':
                    if len(stmt)== 2:
                        self.ff.post = None
                    else:
                        self.ff.post = int(stmt[2])
                elif stmt[1] == 'crear':
                    self.ff.post = None
                    self.ff.pre = None
                    self.ff.course = None
                    self.ff.race = None
                    self.ff.smile= None
                    self.ff.course = None
                else:
                    input_error(stmt, "at 2nd token")
            elif stmt[0] == 'self.fe':
                if stmt[1] == 'clear' or stmt[1] == 'c':
                    self.fe.win = None
                    self.fe.show = None
                    self.fe.rank = None
                    self.fe.last3f = None
                    self.fe.margin = None
                else:
                    try:
                        getattr(self.fe, stmt[1])
                        if len(stmt) == 3:
                            setattr(self.fe, stmt[1], float(stmt[2]))
                        elif len(stmt) == 4:
                            setattr(self.fe, stmt[1],[float(stmt[2]),float(stmt[3])])
                        else:
                            input_error(stmt)
                    except AttributeError:
                        input_error(stmt)
            elif stmt[0] == 'self.hf':
                if stmt[1] == 'clear' or stmt[1] == 'c':
                    self.hf.chaku = None
                    self.hf.ninki = None
                    self.hf.odds = None
                    self.hf.jockey = None
                    self.hf.waku = None
                    self.hf.umaban = None
                    self.hf.last = None
                    self.hf.dist = None
                    self.hf.rest = None
                    self.hf.style = None
                else:
                    try:
                        getattr(self.hf, stmt[1])
                        if len(stmt) == 2:
                            setattr(self.hf, stmt[1], None)
                        elif stmt[1] in ['style']:
                            setattr(self.hf, stmt[1], stmt[2:])
                        elif len(stmt) == 3:
                            if(stmt[1] in ['jockey','last','style']):
                                val = stmt[2]
                            elif(stmt[1] in ['odds','dist']):
                                val = float(stmt[2])
                            else:
                                val = int(stmt[2])
                            setattr(self.hf, stmt[1], val)
                        elif len(stmt) == 4:
                            if stmt[1] in ['odds','dist']:
                                val = [float(stmt[2]),float(stmt[3])]
                            else:
                                val = [int(stmt[2]), int(stmt[3])]
                            setattr(self.hf, stmt[1], val)
                        else:
                            input_error(stmt)
                    except AttributeError:
                        input_error(stmt)
            else:
                input_error(stmt, "at 1st token")

def input_error(stmt, opt = None):
    msg = '[main.py] input is not valid '
    if opt is not None:
        msg += opt
    
    msg += '"'
    for tk in stmt:
        msg = msg +tk
        if not tk == stmt[-1]:
            msg += ' '
    msg = msg + '"'

    print(msg)