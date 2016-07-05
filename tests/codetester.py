#!/usr/bin/env python3

'''Unit test language data'''

# r !boil -m green --title Blue -l python2 -n -s 2

OPTIONS = {
    'funcs' : ['green'],
    'newlines' : True,
    'name' : 'Blue',
    'spaces' : 2
}

def lang_tester(lang, ext, default, advanced):
    '''Creates a dictionary of language info for testing.'''

    return {
        'lang': lang,
        'ext': ext,
        'default': default,
        'advanced': advanced
    }

LANG = {}

LANG['c'] = lang_tester('c', '.c',
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

LANG['cpp'] = lang_tester('c++', '.cpp',
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

LANG['html5'] = lang_tester('html5', '.html',
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

LANG['java'] = lang_tester('java', '.java',
                           '''public class DEFAULT_NAME {
	public static void main(String[] args) {
		return;
	}
}
''',
                           '''public class Blue
{
  public static void main(String[] args)
  {
    return;
  }

  public static void green()
  {
    return;
  }
}
''')

LANG['python'] = lang_tester('python', '.py',
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

LANG['python2'] = lang_tester('python2', '.py',
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

LANG['python3'] = lang_tester('python3', '.py',
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
