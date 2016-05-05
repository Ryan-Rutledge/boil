#!/usr/bin/env python3

# r !boil -m green --title Blue -l python2 -n -s 2

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

c = Tester('c', '.c',
'''#include <stdio.h>

int main() {
	return 0;
}
''',

'''#include <stdio.h>

void green()
{
  return;
}

int main()
{
  return 0;
}
''')

cpp = Tester('c++', '.cpp',
'''#include <iostream>

using namespace std;

int main() {
	return 0;
}
''',

'''#include <iostream>

using namespace std;

void green()
{
  return;
}

int main()
{
  return 0;
}
''')

html5 = Tester('html5', '.html',
'''<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>DEFAULT_NAME</title>

		<meta name="description" content="">
		<meta name="viewport" content="width=device-width, initial-scale=1">
	</head>

	<body></body>
</html>
''',

'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Blue</title>

    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>

  <body>
    <div id="green">
    </div>
  </body>
</html>
''')

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

python2 = Tester('python2', '.py',
'''#!/usr/bin/env python2

def main():
	pass

if __name__ == '__main__':
	main()
''',

'''#!/usr/bin/env python2

def green():
  pass

def main():
  pass

if __name__ == '__main__':
  main()
''')

python3 = Tester('python3', '.py',
'''#!/usr/bin/env python3

def main():
	pass

if __name__ == '__main__':
	main()
''',

'''#!/usr/bin/env python3

def green():
  pass

def main():
  pass

if __name__ == '__main__':
  main()
''')
