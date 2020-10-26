from __future__ import print_function, division, absolute_import

import unittest

import numpy as np
from openmdao.api import Problem, Group, IndepVarComp
from openmdao.utils.assert_utils import assert_check_partials, assert_near_equal

from lcapy import R

from boring.util.spec_test import assert_match_spec
from boring.src.sizing.circuit import Circuit


class TestCircuit(unittest.TestCase):



    def setUp(self):
        p1 = self.prob = Problem(model=Group())
        p1.model.add_subsystem('circ', subsys=Circuit())

        p1.setup(force_alloc_complex=True)

        Rexe = 0.0000001
        Rexc = 0.0000001
        Rwe = 0.2545383947014702
        Rwke = 0.7943030881649811
        Rv = 8.852701208752846e-06
        Rintere = 0.00034794562965549745
        Rinterc = 0.00017397281482774872
        Rwkc = 0.39715154408249054
        Rwka = 744.3007160198263
        Rwa = 456.90414284754644
        Rwc = 0.1272691973507351
        self.prob['circ.Rex_e.R'] = Rexe
        self.prob['circ.Rex_c.R'] = Rexc
        self.prob['circ.Rwe.R'] = Rwe
        self.prob['circ.Rwke.R'] = Rwke
        self.prob['circ.Rv.R'] = Rv
        self.prob['circ.Rinter_e.R'] = Rintere
        self.prob['circ.Rinter_c.R'] = Rinterc
        self.prob['circ.Rwkc.R'] = Rwkc
        self.prob['circ.Rwka.R'] = Rwka
        self.prob['circ.Rwa.R'] = Rwa
        self.prob['circ.Rwc.R'] = Rwc
        self.prob['circ.Rex_e.T_in'] = 100
        self.prob['circ.Rex_c.T_out'] = 20


        p1.run_model()
        p1.model.list_outputs(values=True, prom_name=True)

 
    def test_resistance(self):

        Rexe = 0.0000001
        Rexc = 0.0000001
        Rwe = 0.2545383947014702
        Rwke = 0.7943030881649811
        Rv = 8.852701208752846e-06
        Rintere = 0.00034794562965549745
        Rinterc = 0.00017397281482774872
        Rwkc = 0.39715154408249054
        Rwka = 744.3007160198263
        Rwa = 456.90414284754644
        Rwc = 0.1272691973507351

        Rtot = (R(Rexe) + (R(Rwa) | R(Rwe) + (R(Rwka)|R(Rwke)+R(Rintere)+R(Rv)+R(Rinterc)+R(Rwkc))+ R(Rwc))+ R(Rexc))

        print(Rtot.simplify())
        ans = 16731692103737332239244353077427184638278095509511778941./10680954190791611228174081719413008273307025000000000000.

        Rtot2 = (self.prob.get_val('circ.n1.T')-self.prob.get_val('circ.n8.T'))/self.prob.get_val('circ.Rex_c.q')

        assert_near_equal(Rtot2, ans, tolerance=1.0E-5)

        draw = True # plot the thermal network
        if draw:
            Rtot.draw('Thermal_Network.pdf')

if __name__ =='__main__':
    unittest.main()