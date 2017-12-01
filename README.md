unfortunately the app is currently under construction.

But the wordcloud is made of only nound and verbs!!
and, the form looks nice, cmon :)

due to an installation issue on my local machine, many rabbit holes have wasted much time
although the world cloud was working, and very sexy at that, when running now it throws a RuntimeError
`RuntimeError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are using (Ana)Conda please install python.app and replace the use of 'python' with 'pythonw'. See 'Working with Matplotlib on OSX' in the Matplotlib FAQ for more information`
This is due to using anaconda on my local machine, and the same issue does not arise in production. <octopuswords.appspot.com>

continued work is going on, after the local installation is fixed, the rest of the implementation will be fixed

to setup locally you need to setup a CloudSQL Proxy,
check here: https://cloud.google.com/python/getting-started/using-cloud-sql
use the requirements.txt file with pip and virtualenv or venv
then run
