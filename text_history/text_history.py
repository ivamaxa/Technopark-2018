class TextHistory:
    def __init__(self, text='', version=0, actions=None):
        if actions is None:
            self._actions=[]
        else:
            self._actions=actions
        self._text=text
        self._version=version
        

    
    @property       
    def text(self):
        return self._text

    @property
    def version(self):
        return self._version


    def action(self, action):
        if (action.from_version<0 or action.to_version<0 or action.to_version<=action.from_version):
            raise ValueError
        self._text=action.apply(self._text)
        self._actions.append(action)
        self._version=action.to_version
        return self._version
    
    def insert(self, text,  pos=None):
        if pos is None:
            pos=len(self._text)
        act=InsertAction(pos, text, self._version, self._version+1)
        
        return self.action(act)
    
    def replace(self, text, pos=None):
        act=ReplaceAction(pos, text, self._version, self._version+1)
        
        return self.action(act)
        

    def delete(self, pos, length):
        act=DeleteAction(pos, length, self._version, self._version+1)
        
        return self.action(act)

    def get_actions(self, from_version=None, to_version=None):
        if from_version is None:
            from_version=0
        if to_version is None:
            to_version=self._version

        if (to_version <= from_version != 0) or (to_version<0) or (from_version<0):
            raise ValueError
        if not from_version and to_version>from_version:
            raise ValueError
        mas=[]
        for act in self._actions:
            if act.from_version >= from_version and act.to_version <= to_version:
                mas.append(act)
        i=0
        while i < (len(mas)-1):
            if isinstance(mas[i], InsertAction) and isinstance(mas[i+1], InsertAction):
                if mas[i].pos == mas[i+1].pos-1:
                    mas[i+1].pos=mas[i].pos
                    mas[i+1].text+=mas[i].text
                    mas[i+1].from_version=mas[i].from_version
                    mas.pop(i)
            if isinstance(mas[i], ReplaceAction) and isinstance(mas[i+1], ReplaceAction):
                if mas[i].pos == mas[i+1].pos:
                    mas[i+1].from_version = mas[i].from_version
                    mas.pop(i)
            if isinstance(mas[i], DeleteAction) and isinstance(mas[i+1], DeleteAction):
                if mas[i]._pos == mas[i+1].pos-1:
                    mas[i+1].pos=mas[i].pos
                    mas[i+1].length+=mas[i].length
                    mas[i+1].from_version=mas[i].from_version
                    mas[i+1].to_version=mas[i].to_version
                    mas.pop(i)

            
            i+=1
        return mas
            
class Action:
    def __init__(self, from_version, to_version):
        self.from_version=from_version
        self.to_version=to_version

    
class InsertAction(Action):
    def __init__(self, pos, text, from_version, to_version):
    
        self.text=text
        self.pos=pos
        
        super().__init__(from_version, to_version)

    def apply(self, text_apply):
        
        if self.pos<0 or self.pos>len(text_apply):
            raise ValueError
        else:
            pos=self.pos
        
        return text_apply[:pos] + self.text + text_apply[pos:]
    

class ReplaceAction(Action):
    def __init__(self, pos, text, from_version, to_version):
        self.text=text
        self.pos=pos
        super().__init__(from_version, to_version)

    def apply(self, text_apply):
        if self.pos is None:
            pos=len(text_apply)
        elif self.pos<0 or self.pos>len(text_apply):
            raise ValueError 
        else:
            pos=self.pos
        return text_apply[:pos] + self.text + text_apply[(pos+1):]
                
        


class DeleteAction(Action):
    def __init__(self, pos, length, from_version, to_version):
        self.length=length
        self.pos=pos
        super().__init__(from_version, to_version)
    
    def apply(self, text_apply):
        if self.pos is None:
            pos=len(text_apply)
        elif self.pos<0 or (self.pos+self.length)>len(text_apply):
            raise ValueError
        else:
            pos=self.pos
        return text_apply[:pos] + text_apply[(pos+self.length):]


