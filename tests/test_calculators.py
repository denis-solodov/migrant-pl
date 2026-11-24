import sys
import unittest
from pathlib import Path
from datetime import date
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from calculators import income, deadline, period, schengen
D=date.fromisoformat
class Tests(unittest.TestCase):
    def test_strict(self): self.assertEqual(income('1000',3,'3000','gt')['shortfall_pln'],'0.01')
    def test_equal(self): self.assertTrue(income('1000',3,'3000','ge')['numeric_test_passed'])
    def test_fraction(self): self.assertEqual(income('10.005',1,'10.00','ge')['minimum_passing_pln'],'10.01')
    def test_bad_money(self):
        for bad in ('NaN','-1','Infinity'):
            with self.assertRaises(ValueError): income(bad,1,'1','gt')
    def test_bad_multiplier(self):
        with self.assertRaises(ValueError): income('1',0,'1','gt')
    def test_day(self): self.assertEqual(deadline(D('2026-01-01'),14,'days')['end'],'2026-01-15')
    def test_month(self): self.assertEqual(deadline(D('2024-01-31'),1,'months')['end'],'2024-02-29')
    def test_year(self): self.assertEqual(deadline(D('2024-02-29'),1,'years')['end'],'2025-02-28')
    def test_roll(self): self.assertEqual(deadline(D('2026-01-02'),1,'days',True,[D('2026-01-05')],True)['end'],'2026-01-06')
    def test_no_roll(self): self.assertEqual(deadline(D('2026-01-02'),1,'days')['end'],'2026-01-03')
    def test_unverified(self):
        with self.assertRaises(ValueError): deadline(D('2026-01-02'),1,'days',True)
    def test_overlap(self): self.assertEqual(period([(D('2026-01-01'),D('2026-01-10')),(D('2026-01-05'),D('2026-01-15'))]),15)
    def test_reverse(self):
        with self.assertRaises(ValueError): period([(D('2026-02-01'),D('2026-01-01'))])
    def test_window(self): self.assertEqual(schengen(D('2026-07-01'),[(D('2025-01-01'),D('2026-07-01'))])['days_present'],180)
    def test_empty(self): self.assertEqual(schengen(D('2026-07-01'),[])['remaining_in_window'],90)
    def test_future(self): self.assertEqual(schengen(D('2026-07-01'),[(D('2026-07-02'),D('2026-07-05'))])['days_present'],0)
    def test_inclusive(self): self.assertEqual(period([(D('2026-01-01'),D('2026-01-01'))]),1)
if __name__=='__main__': unittest.main()
