class Section:
    def __init__(self, CRN, courseNum, periods, prof, days, credits, courseName):
        self.CRN = CRN
        self.courseNum = courseNum
        self.periods = periods
        self.prof = prof
        self.days = days
        self.credits = credits
        self.courseName = courseName

class Schedule:
    days = {'M': 1, 'T':2, 'W':3, 'R':4, 'F': 5} 
    
    def __init__(self):
        self.schedule = []
        self.classes = []
        self.schedule.append(['', 'M', 'T', 'W', 'R', 'F'])
        self.id = '';
        for period in range (0, 10):
            self.schedule.append([period + 1, '', '', '', '', ''])
        
    def addClass(self, section):
        count = 0
        print section.days
        for day in section.days:
            for period in section.periods:
                if(self.schedule[period][self.days[day]] == ''):
                    print 'adding' + section.courseNum
                    self.schedule[period][self.days[day]] = section.courseNum
                    count = count + 1
        if count == len(section.days)*len(section.periods):
            self.classes.append(section)
            return 1
        else:
            return 0