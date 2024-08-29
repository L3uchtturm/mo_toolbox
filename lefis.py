from dataclasses import dataclass, field


@dataclass
class AnredeVar:
    pers_anr: str
    var_weiblich: str
    var_maennlich: str
    var_gruppe: str
    var: dict[str, str] = field(init=False)

    """
    Wählt den richtigen Text anhand der Anrede
    pers_anr: str
    var_weiblich: str
    var_maennlich: str
    var_gruppe: str
    """
    def __post_init__(self):
        self.var = {
            '0': self.var_gruppe,
            '1000': self.var_weiblich,
            '2000': self.var_maennlich,
            '3000': self.var_maennlich
        }
        try:
            return self.var[self.pers_anr]
        except KeyError:
            return f'{self.var_weiblich} / {self.var_maennlich} / {self.var_gruppe}'


@dataclass
class FlstVar:
    anz_flst: int
    var_single: str
    var_multiple: str
    var: dict[str, str] = field(init=False)

    def __post_init__(self):
        """
        Wählt den richtigen Text anhand der Fluirstuecksanzahl
        anz_flst: int
        var_single: str
        var_multiple: str
        """
        return self.var_single if self.anz_flst == 1 else self.var_multiple
