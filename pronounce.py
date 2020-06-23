import ui
#import webbrowser
import urllib

wordview = None
SPANDICT = 'https://www.spanishdict.com/translate/'

class mydelegate(object):
#  def webview_did_start_load(self, webview):
#    print('loading')
    
#  def webview_did_finish_load(self, webview):
#    print('loaded')

  def webview_did_fail_load(self, webview, error_code, error_msg):
    print(error_code, error_msg)
  
def load(aWord):
  global wordview
  if not wordview:
    wordview = ui.load_view('pronounce')
    
  web = wordview['web']
#  web.delegate = mydelegate()
  webword = urllib.parse.quote(aWord, safe='')
  url = SPANDICT + webword
#  print(url)
  web.load_url(str(url))
#  webbrowser.get('safari').open(url)
  return wordview

def unload():
  '''Unload and clear the word view.'''
  global wordview
  if wordview:
    wordview.detach()
    wordview = None
    
def closeit(btn):
  wordview.superview.detaching()

if __name__ == '__main__':  #start server and open browser
  v = load('la luciérnaga')
  v.present('sheet')
