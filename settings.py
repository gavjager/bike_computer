
MM_MI = 1.609e6
MM_KM = 1e6

class Settings:
    TIRES = {
            # tire: circumference in mm
            # see croasroadscyclingco.com article
            '700x25c': 2105,
            '700x38c': 2180
    }

    UNITS = ('IMPERIAL', 'METRIC')

    def __init__(self):
        self._units = 'METRIC'
        self._tires = '700x38c'

        self.tire_circumference = 0

        self.units = 'METRIC'
        self.tires = '700x38c'

    @property
    def tires(self):
        return self._tires

    @tires.setter
    def tires(self, tires: str):
        if tires not in self.TIRES:
            print(f"Invalid tire type: {tires}")
            return 
        self._tires = tires
        if self.units == "IMPERIAL":
            self.tire_circumference = self.TIRES[tires] / MM_MI
        elif self.units == "METRIC":
            self.tire_circumference = self.TIRES[tires] / MM_KM
        else:
            raise Exception(f"Invalid units {self.units}")

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units: str):
        if units not in self.UNITS:
            print(f"Invalid units: {units}")
            return
        if units != self._units:
            self._units = units
            # recalculate tires with new units
            self.tires = self._tires


