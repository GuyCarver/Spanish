import ui

nwview = None

def load():
  '''Load newword view and return it.'''
  global nwview
  if not nwview:
    nwview = ui.load_view('newword')
    spv = nwview['spanishwd']
    env = nwview['englishwd']
    spv.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
    env.autocapitalization_type = ui.AUTOCAPITALIZE_NONE

  return nwview

def unload():
  '''Unload and clear the newword view.'''
  global nwview
  if nwview:
    nwview.detatch()
    nwview = None

def ok(btn):
    '''Add a word'''
    spv = nwview['spanishwd']
    env = nwview['englishwd']

    sp = spv.text
    en = env.text
    data = (sp, en) if len(sp) and len(en) else None
    nwview.superview.detaching(data)
    spv.text = ''
    env.text = ''    

def cancel(btn):
  nwview.superview.detaching()
