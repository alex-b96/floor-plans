import os

'''
I wanted to rename the DataSet into something more readable, so I removed the prefix from each of the file name,
remaining only with the termination number.
'''

if __name__ == '__main__':

    PATH = 'data/raw/'
    for _, _, files in os.walk(PATH):
        for f in files:
            os.rename(PATH + f, PATH + f.split('.')[0].split('-')[1] + '.jpg')
        break
