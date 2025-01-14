def update_pbar(len_pbar: int, iteration: int, text: str) -> None:
    proz = 100 / len_pbar * iteration
    print(f'PROZ> {proz} % > {text}')


type INFO = 'INFO'
type ERR = 'ERR'


def update_meldung(level: INFO | ERR, text: str) -> None:
    print(f'{level}> ({text})')
