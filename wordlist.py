import ui

wordview = None

def load(aWords):
  '''Load word view and return it.'''
  global wordview
  if not wordview:
    wordview = ui.load_view('wordlist')
    table = wordview['words']
    table.allows_selection_during_editing = True
    table.data_source = WordDataSource(aWords)
    search = wordview['search']
    search.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
    search.delegate = searchdelegate(table)
    n = wordview['next']
    n.action = search.delegate.next
    p = wordview['prev']
    p.action = search.delegate.prev
  
  wordview.changed = False
  return wordview

def unload():
  '''Unload and clear the word view.'''
  global wordview
  if wordview:
    wordview.detach()
    wordview = None
    
def closeit(btn):
  wordview.superview.detaching(wordview.changed)
  
def toggleedit(btn):
  words = wordview['words']
  words.set_editing(btn.value, True)
  
class searchdelegate(object):
  def __init__(self, table):
    self.wordtable = table
    self.bg = wordview['background']
    self.found = -1
    
  def next(self, btn):
    if self.found >= 0:
      search = wordview['search']
      txt = search.text
      if len(txt) > 1:
        words = self.wordtable.data_source.words
        for i in range(self.found + 1, len(words)):
          w = words[i]
          if (w[0].find(txt) != -1) or (w[1].find(txt) != -1):
            self.found = i
#            print(w, i)
            self.wordtable.selected_row = i
            break

  def prev(self, btn):
    if self.found >= 0:
      search = wordview['search']
      txt = search.text
      if len(txt) > 1:
        words = self.wordtable.data_source.words
        for i in range(self.found - 1, -1, -1):
          w = words[i]
          if (w[0].find(txt) != -1) or (w[1].find(txt) != -1):
            self.found = i
#            print(w, i)
            self.wordtable.selected_row = i
            break
            
  def textfield_did_change(self, textfield):
    txt = textfield.text
    self.wordtable.selected_row = -1
    if len(txt) > 1:
      self.found = -1
      words = self.wordtable.data_source.words
      for i in range(len(words)):
        w = words[i]
        if (w[0].find(txt) != -1) or (w[1].find(txt) != -1):
          self.found = i
#          print(w, i)
          self.wordtable.selected_row = i
          break

class WordDataSource(object):
  def __init__(self, words):
    self.words = words
    
  def tableview_number_of_sections(self, tableview):
    # Return the number of sections (defaults to 1)
    return 1

  def tableview_number_of_rows(self, tableview, section):
    # Return the number of rows in the section
    return len(self.words)

  def tableview_cell_for_row(self, tableview, section, row):
    # Create and return a cell for the given section/row
    f = tableview.frame
    w = f[2] // 2
    cell = ui.TableViewCell()
    lbl = ui.Label()
    cell.selected_background_view = lbl
    lbl.background_color = '#cacaca'
    lbl.border_color = '#000000'
    lbl.border_width = 1
    word = self.words[row]
    row <<= 1
    self.addtext(cell, 'span', word[0], row, w)
    self.addtext(cell, 'eng', word[1], row + 1, w)
    return cell

  def tableview_title_for_header(self, tableview, section):
    # Return a title for the given section.
    # If this is not implemented, no section headers will be shown.
    return 'Spanish/English'

  def tableview_can_delete(self, tableview, section, row):
    # Return True if the user should be able to delete the given row.
    return True

  def tableview_can_move(self, tableview, section, row):
    # Return True if a reordering control should be shown for the given row (in editing mode).
    return True

  def tableview_delete(self, tableview, section, row):
    # Called when the user confirms deletion of the given row.
    wordview.changed = True
    self.words.pop(row)
    tableview.reload_data() #refresh the table.
    
  def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
    # Called when the user moves a row with the reordering control (in editing mode).
    wordview.changed = True
    w = self.words.pop(from_row)
    self.words.insert(to_row, w)

  def tableview_did_select(self, tableview, section, row):
    pass
     
  def addtext(self, cell, name, txt, index, wid):
    l = ui.TextField()
    l.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
    l.background_color = (1.0, 1.0, 1.0, 0.0)
    l.alpha = .75
    l.changed = False
    l.delegate = self
    l.index = index
    l.font = (l.font[0], 10)
    l.clear_button_mode = 'while_editing'

#    l.delegate = TextDelegate(item, self)
    l.name = name
    l.text = txt
    f = cell.frame
    l.frame = (wid * (index & 1), f[1], wid, f[3])
    l.bordered = True
    l.border_width = 1
    l.corner_radius = 1
    cell.content_view.add_subview(l)
    return l
      
  def textfield_should_return(self, textfield):
    textfield.end_editing()
    return True     
      
  def textfield_did_end_editing(self, textfield):
    if textfield.changed:
      wordview.changed = True
      textfield.changed = False
      t = textfield.text.strip()
      textfield.text = t
      #set new word in the words list.
      i = textfield.index
      r = i >> 1 #2 words per row.
      s, e = self.words[r]
      #1 for english, 0 for spanish.    
      self.words[r] = (s,t) if i & 1 else (t, e)
    
  def textfield_did_change(self, textfield):
    textfield.changed = True
    
if __name__ == '__main__':  #run with test data.
  def makeit(x):
    xs = str(x)
    return ('spanish'+xs, 'english'+xs)
    
  testwords = [makeit(x) for x in range(20)]
  load(testwords).present('sheet')
  
