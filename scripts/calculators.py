#!/usr/bin/env python3
"""Offline arithmetic only. Legal parameters must be independently verified."""
import argparse
import calendar
import json
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR

CENT = Decimal('0.01')

def money(value):
    try:
        v = Decimal(str(value))
        if not v.is_finite() or v < 0:
            raise ValueError('amount must be finite and nonnegative')
        return v
    except InvalidOperation as exc:
        raise ValueError('invalid amount') from exc

def income(threshold, multiplier, actual, comparison):
    if multiplier < 1 or comparison not in ('gt', 'ge'):
        raise ValueError('invalid multiplier or comparator')
    required = money(threshold) * multiplier
    observed = money(actual)
    if observed != observed.quantize(CENT):
        raise ValueError('actual PLN must be expressed to grosz precision')
    target = (required.quantize(CENT, rounding=ROUND_FLOOR) + CENT if comparison == 'gt'
              else required.quantize(CENT, rounding=ROUND_CEILING))
    return {'threshold_pln': str(required), 'actual_pln': str(observed),
            'comparison': comparison, 'minimum_passing_pln': str(target),
            'numeric_test_passed': observed >= target,
            'margin_pln': str(observed-required),
            'shortfall_pln': str(max(Decimal('0.00'), target-observed))}

def deadline(start, amount, unit, roll=False, holidays=(), holidays_verified=False):
    if amount < 1:
        raise ValueError('amount must be positive')
    if unit in ('days', 'weeks'):
        raw = start + timedelta(days=amount * (7 if unit == 'weeks' else 1))
    elif unit in ('months', 'years'):
        m = start.year * 12 + start.month - 1 + amount * (12 if unit == 'years' else 1)
        year, month = divmod(m, 12)
        month += 1
        raw = date(year, month, min(start.day, calendar.monthrange(year, month)[1]))
    else:
        raise ValueError('invalid unit')
    if roll and not holidays_verified:
        raise ValueError('rolling requires explicit holiday-list verification')
    end = raw
    while roll and (end.weekday() >= 5 or end in holidays):
        end += timedelta(days=1)
    return {'start': start.isoformat(), 'unadjusted': raw.isoformat(), 'end': end.isoformat(), 'roll_applied': roll}

def merged(stays):
    for a,b in stays:
        if a>b: raise ValueError('reversed interval')
    result = []
    for a,b in sorted(stays):
        if result and (a-result[-1][1]).days <= 1:
            result[-1] = (result[-1][0], max(b,result[-1][1]))
        else: result.append((a,b))
    return result

def period(stays):
    return sum((b-a).days+1 for a,b in merged(stays))

def schengen(on, stays):
    window = on-timedelta(days=179)
    clipped = [(max(a,window),min(b,on)) for a,b in merged(stays) if a<=on and b>=window]
    used = period(clipped)
    return {'window_start':window.isoformat(),'window_end':on.isoformat(),'days_present':used,
            'remaining_in_window':max(0,90-used),'over_limit_days':max(0,used-90)}

def parse_stay(s):
    a,b=s.split(':'); return date.fromisoformat(a),date.fromisoformat(b)

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    i=sub.add_parser('income'); i.add_argument('--threshold',required=True); i.add_argument('--multiplier',type=int,default=1); i.add_argument('--actual',required=True); i.add_argument('--comparison',choices=['gt','ge'],required=True); i.add_argument('--source',required=True); i.add_argument('--as-of',type=date.fromisoformat,required=True)
    d=sub.add_parser('deadline'); d.add_argument('--start',type=date.fromisoformat,required=True); d.add_argument('--amount',type=int,required=True); d.add_argument('--unit',choices=['days','weeks','months','years'],required=True); d.add_argument('--roll',action='store_true'); d.add_argument('--holidays-verified',action='store_true'); d.add_argument('--holiday',type=date.fromisoformat,action='append',default=[])
    for name in ('period','schengen'):
        s=sub.add_parser(name); s.add_argument('--stay',type=parse_stay,action='append',default=[])
        if name=='schengen': s.add_argument('--on',type=date.fromisoformat,required=True)
    a=p.parse_args()
    try:
        if a.command=='income':
            if not a.source.strip(): raise ValueError('source required')
            out=income(a.threshold,a.multiplier,a.actual,a.comparison); out.update(source_user_supplied=a.source,as_of=a.as_of.isoformat())
        elif a.command=='deadline': out=deadline(a.start,a.amount,a.unit,a.roll,a.holiday,a.holidays_verified)
        elif a.command=='schengen': out=schengen(a.on,a.stay)
        else: out={'inclusive_calendar_days':period(a.stay)}
    except (ValueError,ArithmeticError) as exc: p.error(str(exc))
    out['warning']='Arithmetic only; legal applicability and inputs are not independently verified by this script.'
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
