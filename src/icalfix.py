'''
Created on Apr 5, 2011

@author: jeroen
'''

class IcalTimezoneFix(object):
    '''
    Simple to modify the times in an iCalendar file to match another timezone
    '''
    
    def fix(self, ical, offset=2):
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
        
        return date + 'T' + str(hour).rjust(2,'0') + minutes + ' - ' + fulltime

def main():
    fixer = IcalTimezoneFix()
    f = open('demo.ics', 'r')
    print fixer.fix(f.read())

if __name__ == '__main__':
    main()
