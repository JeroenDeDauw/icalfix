'''
Created on Apr 5, 2011

@licence GNU GPL v3+
@author: Jeroen De Dauw
'''

import sys
import getopt
import urllib

class IcalTimezoneFix(object):
    '''
    Simple to modify the times in an iCalendar file to match another timezone
    '''
    
    def fix(self, ical, timezone):
        return '\n'.join([self.fixLine(line, timezone) for line in ical.split('\n')])
    
    def fixLine(self, line, timezone):
        if ['DTSTART', 'DTEND'].count(line.split(':')[0]) == 1:
            parts = line.split(':')
            parts[1] = self.fixTime(parts[1], timezone)
            line = ';'.join(parts)
        return line
    
    def fixTime(self, fulltime, timezone):
        return "TZID=%s:%s" % (timezone, fulltime)

def show_help():
    print """
icalfix.py -s source [-t timezone] [-? help]

Offsets the times in an iCalendar file by a number of hours to fix timezone fails.    

  -s, --source source
                URL pointing to the source iCal file
                * http://tinyurl.com/0x20Calendar
                * http://tinyurl.com/HsbCalendar
  -t --timezone timezone
                Timezone. Defaults to Europe/Brussels
  -?, --help
                Shows this help.
    """

def main():
    try:
        opts, a = getopt.getopt(sys.argv[1:], "s:t:?", ["source=", "timezone=", "help"])
    except getopt.GetoptError, err:
        print str(err) 
        show_help()
        sys.exit(2)
    
    source=None
    timezone="Europe/Brussels"
    
    for opt, arg in opts:
        if opt in ("-s", "--source"):
            source = arg
        elif opt in ("-t", "--timezone"):
            timezone = arg
        elif opt in ("-?", "--help"):
            show_help()
            sys.exit()
        else:
            assert False, "unhandled option" 
    
    if not source:
        print "Missing source option"
        show_help()
        sys.exit(1)
    
    fixer = IcalTimezoneFix()
    f = urllib.urlopen(source)
    #f = open('demo.ics', 'r')
    print fixer.fix(f.read(), timezone)

if __name__ == '__main__':
    main()
