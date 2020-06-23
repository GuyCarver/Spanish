import ui
import os
import json
import console
from sound import play_effect
import random
from datetime import datetime
import newword
import wordlist
import pronounce

#Todo:
#undo
#word type, noun, verb, adj, adv, phrase
#add browser back/forward
#Change whole system to a list?

class Spanish(ui.View):
  COLORS = ('#ffffffff', '#ffff80ff')
  WORDFILE = 'words.txt'
  BACKUP = 'backup'
  OPTFILE = 'opts.json'
  
  def __init__(self):
    self.curword = None
    self._insubview = None
    self.detachfn = None
    self.file = ''
    self._index = 0 #this is words index * 2 + spanish/english index
    self._seed = 0
    self.words = []
    self.indexes = []

  @property
  def lang(self):
    return self['lang'].selected_index
    
  @lang.setter
  def lang(self, aValue):
    self['lang'].selected_index = 1 if aValue else 0

  @property
  def side( self ): return self._index & 1

  @side.setter
  def side( self, aValue ):
    self._index = self._index & -2 | aValue
 
  @property
  def index( self ):
    return self._index >> 1 #get just index into words list.

  @index.setter
  def index( self, aValue ):
    #_index = words index * 2 + spanish/english index (card side)
    if aValue >= len(self.words):
      aValue = 0
    self._index = (aValue << 1) + self.side

  @property
  def optionpanel(self):
    return self._insubview

  @optionpanel.setter
  def optionpanel(self, vw):
    if self._insubview != vw:
      if self._insubview:
        self.remove_subview(self._insubview)
        self.set_needs_display()

      self._insubview = vw
      if vw:
        vw.x = (self.width - vw.width) // 2
        self.add_subview(vw)
        
  def did_load(self):
    self.loadwords(Spanish.WORDFILE)
    self.loadopts()
    self.updatecur()

  def will_close(self):
    self.saveopts()

  def loadopts(self):
    with open(Spanish.OPTFILE) as f:
      opts = json.load(f)
      self._index = opts[0]
      self.lang = opts[1]
      self.setrandom(opts[2])
      self['random'].value = self._seed

  def saveopts(self):
    with open(Spanish.OPTFILE, 'w') as f:
      opts = [self._index, self.lang, self._seed]
      json.dump(opts, f)
      
  def loadwords(self, afile):
    self.file = afile
    with open(afile, encoding='utf-8', errors='ignore') as wrdf:
      wrds = wrdf.readlines()

      def getpair(wrdp):
        names = wrdp.split(',')
        if len(names) == 2:
          sp = names[0].strip()
          en = names[1].strip()
          return (sp, en)
        else:
          return ('','')
      
      self.words = [getpair(w) for w in wrds if len(w) > 4]
    self['total'].text = ':' + str(len(self.words))
    
  def next(self):     
    i = self._index + 1
    if (i >> 1) >= len(self.words):
      i = 0
    self._index = i
    if i & 1:
      play_effect('casino:CardSlide3', .25)
    else:
      play_effect('casino:CardSlide4', .25)

    self.updatecur()
    
  def updatecur(self):
    i = self.indexes[self.index] #use index to get shuffled index for randomization.
    self.curword = self.words[i]
    if self.curword != None:
      c = self.side ^ self.lang
      self['card'].title = self.curword[c]
      self['card'].background_color = Spanish.COLORS[self.side]
      self['current'].text = str((self.index) + 1)

  def detaching(self, data = None ):
    '''This is called by some subview when they are done.  It calls the
        detachfn function if it is set to perform any action that needs
        to happen for the subview.'''
    if data != None and self.detachfn:
      self.detachfn(data)
    self.optionpanel = None
    self.detachfn = None
  
  def setrandom(self, aseed):
    self.indexes = [i for i in range(len(self.words))]
    self._seed = aseed
    if aseed:
      random.seed(aseed)
      random.shuffle(self.indexes)

  def flip(btn):
    if v.curword != None:
        v.next()
    
  def restart(btn):
    v._index = 0
    v.updatecur()
    
  def randtoggle(btn):
    if btn.value:
      ms = datetime.now().microsecond
      play_effect('casino:CardFan1')
    else:
      ms = 0
      play_effect('casino:CardOpenPackage1')
    v.setrandom(ms)
    v.updatecur()
    
  def back(btn):
    if v.side: #if on side 2 just go back to side 1.
      v.side = 0
    elif v._index: #else go back a whole card.
      v.index -= 1
    v.updatecur()
    
  def language(btn):
    v.updatecur()
    
  def addit(self, data):
    for w in self.words:
      if data[0] == w[0] or data[1] == w[1]:
        message = '{} already in as {}'.format(data, w)
        console.alert('Duplicate Word', message, hide_cancel_button=True)
        return
    self.words.append(data)
    with open(self.file, 'a', encoding = 'utf_8') as wrdf:
      wrdf.write(str(data[0]) + ', ' + str(data[1]) + '\n')
    
  def addword(btn):
    v.detachfn = v.addit
    nw = newword.load()
    v.optionpanel = nw
    
  def detail(btn):
    v.optionpanel = pronounce.load(v.curword[0])

  def backup(self):
    os.rename(self.file, Spanish.BACKUP)
    try:
      os.remove(Spanish.BACKUP + ' 6.txt')
    except:
      pass

  def endlist(self, tf):
    if tf:
      if self.index >= len(self.words):
        self._index = 0
      self.backup()
      with open(self.file, 'w', encoding = 'utf_8') as wrdf:
        for d in self.words:
          wrdf.write(str(d[0]) + ', ' + str(d[1]) + '\n')
    
  def listwords(btn):
    w = wordlist.load(v.words)
    w.set_needs_display()
    v.detachfn = v.endlist
    v.optionpanel = w

  def load(self, afile):
    self.file = afile
    with open(afile) as wrdf:
      wrds = wrdf.readlines()

      def getpair(wrdp):
        names = wrdp.split(',')
        if len(names) == 2:
          sp = names[0].strip()
          en = names[1].strip()
          return (sp, en)
        else:
          return ('','')
      
      self.words = [getpair(w) for w in wrds]

v = ui.load_view()
v.present('full_screen')
