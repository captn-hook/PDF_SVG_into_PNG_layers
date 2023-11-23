import sys
import os

target = sys.argv[1]

for svg in os.listdir(target):
    if svg.endswith(".svg"):
        print(svg)

        header = ""
        clipPaths = "" #each individual clip path will be 3 lines instead of 1, open, path, close
        transistion = ""
        paths = "" #each path will probably refresh the clip path with url(#clipPathid)
        footer = ""

        #read lines
        with open(target + svg) as f:
            lines = f.readlines()
        print(len(lines))
        mode = "header"
        for i in range(len(lines)):
            if mode == 'header':
                header += lines[i]
                #ignore leading whitespace
                if lines[i].startswith(' <defs'):
                    mode = 'clipPath'
            elif mode == 'clipPath':
                if lines[i].startswith(' </defs'):
                    transistion += lines[i]
                    mode = 'transition'
                else:
                    clipPaths += lines[i]
            elif mode == 'transition':
                if lines[i].startswith(' <g'):
                    transistion += lines[i]
                    mode = 'path'
                else:
                    #error
                    print('error')
            elif mode == 'path':
                if lines[i].startswith(' </g'):
                    footer += lines[i]
                    mode = 'footer'
                else:
                    paths += lines[i]
            elif mode == 'footer':
                footer += lines[i]
            else:
                print('error')

        #print len of each section
        print("header: " + str(len(header.splitlines())) + " clipPaths: " + str(len(clipPaths.splitlines())) + " transistion: " + str(len(transistion.splitlines())) + " paths: " + str(len(paths.splitlines())) + " footer: " + str(len(footer.splitlines())))

                    
        paths_using_clipPaths = []
        paths_not_using_clipPaths = []
        paths_using_clipPaths_IDS = []
        new_clipPaths = []
        clipPaths_IDS = []
        
        #remove any line that uses clip-path="url(#clipPathid)" to paths_using_clipPaths
        for line in paths.splitlines():
            if "clip-path" in line:
                paths_using_clipPaths.append(line)
                paths_using_clipPaths_IDS.append(line.split('url(#')[1].split(')')[0])
            else:
                paths_not_using_clipPaths.append(line)

        #split clipPaths into individual clipPaths, because they are 3 lines each
        for line in clipPaths.splitlines():
            if line.startswith('  <clipPath'):
                new_clipPaths.append(line)
                clipPaths_IDS.append(line.split('id="')[1].split('"')[0])
            else:
                new_clipPaths[-1] += line

        print('paths_using_clipPaths: ' + str(len(paths_using_clipPaths)))
        print('paths_not_using_clipPaths: ' + str(len(paths_not_using_clipPaths)))
        print('new_clipPaths: ' + str(len(new_clipPaths)))
        print('clipPaths_IDS: ' + str(len(clipPaths_IDS)))

        #looks like we have 1 clipPath for each path that uses clip-path="url(#clipPathid)", meaning no duplicates

        size = sys.argv[2] #number of paths to put in each file
        size = int(size)

        #create new files for paths not using clipPaths
        for i in range(0, len(paths_not_using_clipPaths), size):
            with open(target + svg + str(i) + '.svg', 'w') as f:
                f.write(header)
                f.write(transistion)
                for line in paths_not_using_clipPaths[i:i+size]:
                    f.write(line + '\n')
                f.write(footer)

        #create dict by id for both clipPaths and paths
        clipDict = {}
        for i in range(len(clipPaths_IDS)):
            clipDict[clipPaths_IDS[i]] = new_clipPaths[i]
        pathDict = {}
        for i in range(len(paths_using_clipPaths_IDS)):
            pathDict[paths_using_clipPaths_IDS[i]] = paths_using_clipPaths[i]

        #create new files for paths using clipPaths
        for i in range(0, len(paths_using_clipPaths_IDS), size):
            ids_to_use = paths_using_clipPaths_IDS[i:i+size]
            with open(target + svg + str(i) + '.svg', 'w') as f:
                f.write(header)
                #get defs frop clipDict
                for id in ids_to_use:
                    f.write(clipDict[id] + '\n')
                f.write(transistion)
                #get paths from pathDict
                for id in ids_to_use:
                    f.write(pathDict[id] + '\n')

                f.write(footer)

                
                               
