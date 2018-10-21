class AbilityScore:
    SCORE_MIN=0
    SCORE_MAX=30
    def __init__(self, score=10): 
        self._check_score(score)
        self._score=self._check_score(score) #принимает score и сохраняет
   
    def _check_score(self, score):
       score =int(score)
       if score<self.SCORE_MIN:
           raise ValueError('{} is too low'.format(score))
       if score>self.SCORE_MAX:
           raise ValueError('{} is too much'.format(score))
       return score
   
    #def to_string(self):
    #    return '{score} [{modifier}]'.format(
    #            score=self._score,
    #            modifier=self._get_modifier_str()) 
    def to_string(self):
        return '{score} [{modifier}]'.format(
                score=self._score,
                modifier=self._modifier_to_str(self.get_modifier()),
        )
        
    def get_modifier(self):
        return(self._score-10)//2
    
    
    #def _get_modifier_str(self):
    #    modifier=self.get_modifier()
    #    return str(modifier) if modifier<0 else '+' + str(modifier)
    
    @staticmethod
    def _modifier_to_str(modifier):
        return str(modifier) if modifier<0 else '+' +str(modifier)

#dex=AbilityScore(12) #12
dex=AbilityScore() #10
print(dex.to_string())
#con=AbilityScore(40) #ValueError
