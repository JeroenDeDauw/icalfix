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
    
    def fix(self, ical, offset):
        return '\n'.join([self.fixLine(line, offset) for line in ical.split('\n')])
    
    def fixLine(self, line, offset):
        if ['DTSTART', 'DTEND'].count(line.split(':')[0]) == 1:
            parts = line.split(':')
            parts[1] = self.fixTime(parts[1], offset)
            line = ':'.join(parts)
        return line
    
    def fixTime(self, fulltime, offset):
        parts = fulltime.split('T')
        
        if len(parts) == 1:
            return fulltime
        
        date = parts[0]
        hour = int(parts[1][0:2])
        minutes = parts[1][2:] 
        
        hour += offset
        
        if hour > 23:
            dateoffset = 1
        elif hour < 0:
            dateoffset = -1
        else:
            dateoffset = 0
        
        hour += 24 * dateoffset
        
        if dateoffset != 0:
            # TODO: obviously this fails at month edges; fix
            date = date[:-2] + str(int(date[-2:]) + dateoffset)
        
        return date + 'T' + str(hour).rjust(2,'0') + minutes

def show_help():
    print """
icalfix.py -s source [-o offset] [-? help]

Offsets the times in an iCalendar file by a number of hours to fix timezone fails.    

  -s, --source source
                URL pointing to the source iCal file
                * http://tinyurl.com/0x20Calendar
                * http://tinyurl.com/HsbCalendar
  -o --offset offset
                Number of hours to offset, signed integer. Defaults to -2
  -?, --help
                Shows this help.
    """

def main():
    try:
        opts, a = getopt.getopt(sys.argv[1:], "s:o:?", ["source=", "offset=", "help"])
    except getopt.GetoptError, err:
        print str(err) 
        show_help()
        sys.exit(2)
    
    source=None
    offset=-2
    
    for opt, arg in opts:
        if opt in ("-s", "--source"):
            source = arg
        elif opt in ("-o", "--offset"):
            offset = arg
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
    print fixer.fix(f.read(), offset)

if __name__ == '__main__':
    main()
