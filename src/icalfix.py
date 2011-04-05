'''
Created on Apr 5, 2011

@author: jeroen
'''

class IcalTimezoneFix(object):
    '''
    Simple to modify the times in an iCalendar file to match another timezone
    '''
    
    def fix(self, ical, offset=2):
        pass

def main():
    fixer = IcalTimezoneFix()
    f = open('/tmp/workfile', 'r')
    print fixer.fix(f.read())

if __name__ == '__main__':
    main