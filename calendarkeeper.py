class CalendarKeeper:
    def __init__(self, month, year):
        self.month = month
        self.year = year

    def getdateforendof(self):
        if self.year == 2017:
            return self.endof2017(self.month)
        if self.year == 2018:
            return self.endof2018(self.month)
        if self.year == 2019:
            return self.endof2019(self.month)

    def endof2017(self, month):
        months = {
                1: 31,
                2: 28,
                3: 31,
                4: 30,
                5: 31,
                6: 30,
                7: 31,
                8: 31,
                9: 30,
                10: 31,
                11: 30,
                12: 31
                }
        return months.get(month)

    def endof2018(self, month):
        months = {
                1: 31,
                2: 28,
                3: 31,
                4: 30,
                5: 31,
                6: 30,
                7: 31,
                8: 31,
                9: 30,
                10: 31,
                11: 30,
                12: 31
                }
        return months.get(month)

    def endof2019(self, month):
        months = {
                1: 31,
                2: 28,
                3: 31,
                4: 30,
                5: 31,
                6: 30,
                7: 31,
                8: 31,
                9: 30,
                10: 31,
                11: 30,
                12: 31
                }
        return months.get(month)
