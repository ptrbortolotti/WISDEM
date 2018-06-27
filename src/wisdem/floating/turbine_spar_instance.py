from wisdem.floating.floating_turbine_instance import FloatingTurbineInstance, NSECTIONS, NPTS, vecOption
from floatingse.instance import SparInstance
from commonse import eps
import numpy as np
import offshorebos.wind_obos as wind_obos
import time

NDEL = 0

class TurbineSparInstance(FloatingTurbineInstance):
    def __init__(self, RefBlade):
        super(TurbineSparInstance, self).__init__(RefBlade)

        # Parameters beyond those in superclass
        self.params['number_of_auxiliary_columns'] = 0
        self.params['cross_attachment_pontoons_int'] = 0
        self.params['lower_attachment_pontoons_int'] = 0
        self.params['upper_attachment_pontoons_int'] = 0
        self.params['lower_ring_pontoons_int'] = 0
        self.params['upper_ring_pontoons_int'] = 0
        self.params['outer_cross_pontoons_int'] = 0
 
        # Typically design (OC3)
        self.params['base_freeboard'] = 10.0
        self.params['fairlead'] = 5 #70.0
        self.set_length_base(130.0)
        self.params['base_section_height'] = np.array([36.0, 36.0, 36.0, 8.0, 14.0])
        self.params['base_outer_diameter'] = 2*np.array([4.7, 4.7, 4.7, 4.7, 3.25, 3.25])
        self.params['base_wall_thickness'] = 0.05
        self.params['fairlead_offset_from_shell'] = 5.2-4.7
        self.params['base_permanent_ballast_height'] = 10.0
        
        # OC3
        self.params['water_depth'] = 320.0
        self.params['wave_height'] = 10.8
        self.params['wave_period'] = 9.8
        self.params['wind_reference_speed'] = 11.0
        self.params['wind_reference_height'] = 119.0
        self.params['shearExp'] = 0.11
        self.params['morison_mass_coefficient'] = 2.0

        self.params['number_of_mooring_lines'] = 3
        self.params['mooring_line_length'] = 902.2
        self.params['anchor_radius'] = 853.87
        self.params['mooring_diameter'] = 0.09
        
        self.params['substructure'] =                 wind_obos.Substructure.SPAR
        self.params['anchor'] =                       wind_obos.Anchor.DRAGEMBEDMENT
        self.params['turbInstallMethod'] =            wind_obos.TurbineInstall.INDIVIDUAL
        self.params['towerInstallMethod'] =           wind_obos.TowerInstall.ONEPIECE
        self.params['installStrategy'] =              wind_obos.InstallStrategy.PRIMARYVESSEL

        # Change scalars to vectors where needed
        self.check_vectors()

        
    def get_constraints(self):
        conList = SparInstance().get_constraints()
        for con in conList:
            con[0] = 'sm.' + con[0]

        conList.extend( [['rotor.Pn_margin', None, 1.0, None],
                         ['rotor.P1_margin', None, 1.0, None],
                         ['rotor.Pn_margin_cfem', None, 1.0, None],
                         ['rotor.P1_margin_cfem', None, 1.0, None],
                         ['rotor.rotor_strain_sparU', -1.0, None, None],
                         ['rotor.rotor_strain_sparL', None, 1.0, None],
                         ['rotor.rotor_strain_teU', -1.0, None, None],
                         ['rotor.rotor_strain_teL', None, 1.0, None],
                         ['rotor.rotor_buckling_sparU', None, 1.0, None],
                         ['rotor.rotor_buckling_sparL', None, 1.0, None],
                         ['rotor.rotor_buckling_teU', None, 1.0, None],
                         ['rotor.rotor_buckling_teL', None, 1.0, None],
                         ['rotor.rotor_damage_sparU', None, 0.0, None],
                         ['rotor.rotor_damage_sparL', None, 0.0, None],
                         ['rotor.rotor_damage_teU', None, 0.0, None],
                         ['rotor.rotor_damage_teL', None, 0.0, None],
                         ['tcons.frequency_ratio', None, 1.0, None],
                         ['tcons.tip_deflection_ratio', None, 1.0, None],
                         ['tcons.ground_clearance', 30.0, None, None],
        ])
        return conList


def deriv_check():
   # ----------------
    myspar = TurbineSparInstance()
    myspar.evaluate('psqp')
    f = open('deriv_total_spar.dat','w')
    out = myspar.prob.check_total_derivatives(f)#, compact_print=True)
    f.close()
    tol = 1e-4
    for comp in out.keys():
        if ( (out[comp]['rel error'][0] > tol) and (out[comp]['abs error'][0] > tol) ):
            print comp, out[comp]['magnitude'][0], out[comp]['rel error'][0], out[comp]['abs error'][0]

    
if __name__ == '__main__':
    #deriv_check()
    pass
