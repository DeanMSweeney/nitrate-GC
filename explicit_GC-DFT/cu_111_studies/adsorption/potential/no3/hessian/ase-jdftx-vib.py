from ase.io import read, write
from JDFTx_BT import JDFTx
from ase.vibrations import Vibrations
from ase.thermochemistry import HarmonicThermo

#Read structure
atoms=read('POSCAR')
vibatoms=[atom.index for atom in atoms if atom.symbol not in ['Cu']] #only vibrate adsorbate atoms

#Set-up JDFTx calculator
atoms.calc = JDFTx(ntask=8,
                    ncpu=8,
                commands={'initial-state' : '$VAR',
                          'coulomb-interaction' : 'Periodic',
                          'core-overlap-check' : 'none',
                          'elec-cutoff' : '20 100',
                          'spintype' : 'no-spin',
                          'symmetries' : 'automatic',
                          'elec-ex-corr' : 'gga-x-rpbe gga-c-pbe',
                          'kpoint' : '0.5 0.5 0.5 1',
                          'kpoint-folding' : '4 4 1',
                          'elec-smearing' : 'Fermi 0.00734',
                          'electronic-minimize' : 'nIterations 100 energyDiffThreshold 1E-7',
                          'fluid' : 'LinearPCM',
                          'pcm-variant' : 'CANDLE',
                          'fluid-solvent' : 'H2O',
                          'fluid-cation' : 'Na+ 1.',
                          'fluid-anion' : 'F- 1.',
                          'target-mu' : '-0.134502451',
                          'dump-name' : '$VAR',
                          'dump' : 'End Ecomponents Forces State'
                          })
#Set-up vibration run
vib = Vibrations(atoms,indices=vibatoms,delta=0.03)
vib.run()
#Write output and modes
vib.summary(method='standard')
vib.write_mode()
