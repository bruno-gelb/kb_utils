# math: strategymanual.ru/?action=KBdamageCalc&table=kbwon


import click

from units import units, Unit

MIN_MODIFIER = 0.333
MAX_MODIFIER = 3
LINE = 50 * '='


def calc_damage_modifier(attackers_attack: int, defenders_defend: int, enable_cap: bool = True) -> float:
    if attackers_attack >= defenders_defend:
        diff = attackers_attack - defenders_defend
        diff *= 0.0333
        modifier = 1 + diff
        if enable_cap and modifier > MAX_MODIFIER:
            modifier = MAX_MODIFIER
    else:
        diff = attackers_attack - defenders_defend
        diff *= 0.0333
        modifier = 1 / (1 + diff)
        if enable_cap and modifier < MIN_MODIFIER:
            modifier = MIN_MODIFIER
    return round(modifier, 3)


def calc_optimal_attack(target_defend: int) -> int:
    return int((MAX_MODIFIER - 1 + 0.0333 * target_defend) / 0.0333)


def calc_optimal_defend(target_attack: int) -> int:
    return int((1 / MIN_MODIFIER - 1 + target_attack * 0.0333) / 0.0333)


def versus(your: Unit, target: Unit) -> None:
    click.echo(LINE)
    click.echo(f'{your} attacking {target}: {your.attack} >> {target.defend}')
    modifier = calc_damage_modifier(your.attack, target.defend, enable_cap=False)
    click.echo(f'modifier is {modifier}')
    if modifier < MAX_MODIFIER:
        click.echo(f'{modifier} < {MAX_MODIFIER}, so the optimal attack for {your} against {target} should be higher')
        optimal_attack = calc_optimal_attack(target.defend)
        click.echo(f'optimal attack for the {your} would be {optimal_attack}, '
                   f'so you should acquire {optimal_attack - your.attack} additional attack points')
    elif modifier == MAX_MODIFIER:
        click.echo(f'{modifier} = {MAX_MODIFIER}. Your attack for {your} against {target} is optimal')
    elif modifier > MAX_MODIFIER:
        optimal_attack = calc_optimal_attack(target.defend)
        click.echo(f'optimal attack for the {your} would be {optimal_attack}, '
                   f'so you should lose {your.attack - optimal_attack} attack points')

    click.echo(LINE)
    click.echo(f'{target} attacking {your}: {target.attack} >> {your.defend}')
    modifier = calc_damage_modifier(target.attack, your.defend, enable_cap=False)
    click.echo(f'modifier is {modifier}')
    if modifier > MIN_MODIFIER:
        click.echo(f'{modifier} > {MIN_MODIFIER}, so the optimal defend for {your} against {target} should be higher')
        optimal_defend = calc_optimal_defend(target.attack)
        click.echo(f'optimal defend for the {your} would be {optimal_defend}, '
                   f'so you should acquire {optimal_defend - your.defend} additional defend points')
    elif modifier == MIN_MODIFIER:
        click.echo(f'{modifier} = {MIN_MODIFIER}. Your defend for {your} against {target} is optimal')
    elif modifier < MIN_MODIFIER:
        click.echo(f'{modifier} < {MIN_MODIFIER}, so your defend is suboptimally high!')
        optimal_defend = calc_optimal_defend(target.attack)
        click.echo(f'optimal defend for the {your} would be {optimal_defend}, '
                   f'so you should lose {optimal_defend - your.defend} defend points')
    click.echo(LINE)


@click.command()
def main():
    versus(units['giant'], units['gorgul'])


if __name__ == '__main__':
    main()
