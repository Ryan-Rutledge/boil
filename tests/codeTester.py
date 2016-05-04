#!/usr/bin/env python3

options = {
    'funcs'    : ['green'],
    'newlines' : True,
    'name'     : 'Blue',
    'spaces'   : 2
}

class Tester:
    '''Output comparison class'''

    def __init__(self, lang, ext, default, advanced):
        self.lang     = lang
        self.ext      = ext
        self.default  = default
        self.advanced = advanced

java = Tester('java', '.java',
'''public class DEFAULT_NAME {
	public static void main(String[], args) {
		return;
	}
}
''',

'''public class Blue
{
  public static void main(String[], args)
  {
    return;
  }

  public static void green()
  {
    return;
  }
}
''')

python = Tester('python', '.py',
'''#!/usr/bin/env python

def main():
	pass

if __name__ == '__main__':
	main()
''',

'''#!/usr/bin/env python

def green():
  pass

def main():
  pass

if __name__ == '__main__':
  main()
''')
