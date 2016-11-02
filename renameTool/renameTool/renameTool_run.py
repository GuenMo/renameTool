# coding:utf-8

import sys

def renameTool_run():
    try:
        filePath = __file__
        appPath = filePath.rpartition('\\')[0]
    except:
        print 'Environ Value {} not exist.'.format(appPath)
    
    else:
        path = appPath
        
        if not path in sys.path:
            sys.path.append(path)
        
        import view.mainUI as RenameToolUI
        reload(RenameToolUI)
        RenameToolUI.main()
        
if __name__ == 'renameTool_run':  
    renameTool_run()



