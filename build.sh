rm -rf dist/
#pyinstaller --onefile main.py   -y --clean --paths /mnt/d/bin/Qt/5.11.1/winrt_x64_msvc2017/bin/
#nuitka3 --recurse-all  main.py
#mv /mnt/d/tmp/desktopapp/dist/{main,target.exe}
pyinstaller main.spec
