import os,subprocess
print(os.system('tasklist'))
#os.system('taskkill /f /pid 11172')
os.system('taskkill /f /im python.exe')
