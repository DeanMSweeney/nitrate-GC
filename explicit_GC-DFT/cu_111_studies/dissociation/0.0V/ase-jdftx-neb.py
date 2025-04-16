from ase.io import read, write
from JDFTx_BT import JDFTx
from ase.neb import NEB
from ase.optimize.fire import FIRE as QuasiNewton
from ase.constraints import FixAtoms

#Build images and set calculator
nimg=5
images = read('neb.traj@-7:')
for i in range(nimg):
    images[i+1].calc = JDFTx(runDir='0'+str(i+1),       #must specify runDir, and all jdftx inputs as commands
                ntask=8,
                ncpu=14,
                commands={'initial-state' : '$VAR',
                          'coulomb-interaction' : 'Periodic',
                          'elec-cutoff' : '20 100',
                          'core-overlap-check' : 'none',
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
                          'target-mu' : '-0.171251755',
                          'dump-name' : '$VAR',
                          'dump' : 'Ionic Ecomponents EigStats Forces IonicPositions State'
                          })
#Initiate NEB
neb=NEB(images,parallel=True,climb=True)
#Optimize NEB
qn=QuasiNewton(neb, trajectory='neb.traj')
qn.run(fmax=0.05,steps=100)

