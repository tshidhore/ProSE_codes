################################################################################
# Single particle compression
# Units - um, ns, GPa
################################################################################

[Mesh]
  type = FileMesh
  file = compression.msh
  second_order = false
  displacements = 'ux uy'
[]
################################################################################

[Variables]
  [./ux]
    family = LAGRANGE
    order = FIRST
  [../]
  [./uy]
    family = LAGRANGE
    order = FIRST
  [../]
  [./c]
    family = LAGRANGE
    order = FIRST
  [../]
  [./b]
    family = LAGRANGE
    order = FIRST
  [../]
  [./temp]
    order = FIRST
    family = LAGRANGE
    initial_condition = 300.0
  [../]
[]
################################################################################

[AuxVariables]
  [./stressxx]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./stressyy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./stressxy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./strainxx]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./strainyy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./strainxy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./vx]
    family = LAGRANGE
    order = FIRST
  [../]
  [./ax]
    family = LAGRANGE
    order = FIRST
  [../]
  [./vy]
    family = LAGRANGE
    order = FIRST
  [../]
  [./ay]
    family = LAGRANGE
    order = FIRST
  [../]
  [./psi_pos]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./dcdx]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./dcdy]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./friction_normal_force]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./slide_velocity_parallel]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./f_x]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./f_y]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./s_x]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./s_y]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./heat_rate]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./e_xx]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./e_yy]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./e_xy]
   order = CONSTANT
   family = MONOMIAL
 [../]
 [./crack_rho]
   order = CONSTANT
   family = MONOMIAL
 [../]
[]
################################################################################
# Internal order of definitions will change from file to file
# Function definition: f(x,yz,t)
[Functions]
  [./initial_crack]
    type = ParsedFunction

# min ensures that the phase field variable does not exceed 1 (see end of file)
# cracks delimted by '+'

    value = 'min(exp(-abs(y-528)/n)*if(max(n+1-abs(y-528),0),1,0)*if(max(50+1-abs(x-506),0),1,0)+exp(-abs(x-871)/p)*if(max(p+1-abs(x-871),0),1,0)*if(max(62.5+1-abs(y-812.5),0),1,0)+0.90736*exp(-abs(y-tan(-4.6009*pi/180)*x-1101.3747)/m)*if(max(m+1-abs(y-tan(-4.6009*pi/180)*x-1101.3747),0),1,0)*if(max(103.5024+1-abs(y+cot(-4.6009*pi/180)*x+5564.0765),0),1,0)+0.9529*exp(-abs(y-tan(-10.8651*pi/180)*x-960.8750)/m)*if(max(m+1-abs(y-tan(-10.8651*pi/180)*x-960.8750),0),1,0)*if(max(37.7380+1-abs(y+cot(-10.8651*pi/180)*x+2767.7372),0),1,0)+0.56349*exp(-abs(y-tan(14.3643*pi/180)*x-587.3179)/m)*if(max(m+1-abs(y-tan(14.3643*pi/180)*x-587.3179),0),1,0)*if(max(105.1034+1-abs(y+cot(14.3643*pi/180)*x-3963.1710),0),1,0)+0.95669*exp(-abs(y-tan(14.0786*pi/180)*x-905.7789)/m)*if(max(m+1-abs(y-tan(14.0786*pi/180)*x-905.7789),0),1,0)*if(max(137.0582+1-abs(y+cot(14.0786*pi/180)*x-4854.1124),0),1,0)+0.81618*exp(-abs(y-tan(-38.9196*pi/180)*x-1334.6844)/m)*if(max(m+1-abs(y-tan(-38.9196*pi/180)*x-1334.6844),0),1,0)*if(max(97.1113+1-abs(y+cot(-38.9196*pi/180)*x+659.0050),0),1,0)+0.54877*exp(-abs(y-tan(-1.3523*pi/180)*x-1006.4014)/m)*if(max(m+1-abs(y-tan(-1.3523*pi/180)*x-1006.4014),0),1,0)*if(max(116.2143+1-abs(y+cot(-1.3523*pi/180)*x+29345.3944),0),1,0)+0.63925*exp(-abs(y-tan(-7.4196*pi/180)*x-1046.1367)/m)*if(max(m+1-abs(y-tan(-7.4196*pi/180)*x-1046.1367),0),1,0)*if(max(105.4410+1-abs(y+cot(-7.4196*pi/180)*x+2545.4864),0),1,0)+0.77344*exp(-abs(y-tan(28.2468*pi/180)*x-385.7939)/m)*if(max(m+1-abs(y-tan(28.2468*pi/180)*x-385.7939),0),1,0)*if(max(69.3796+1-abs(y+cot(28.2468*pi/180)*x-1504.9916),0),1,0)+0.97875*exp(-abs(y-tan(49.1970*pi/180)*x-192.9402)/m)*if(max(m+1-abs(y-tan(49.1970*pi/180)*x-192.9402),0),1,0)*if(max(90.2855+1-abs(y+cot(49.1970*pi/180)*x-1273.4299),0),1,0)+0.98244*exp(-abs(y-tan(49.9173*pi/180)*x+718.5182)/m)*if(max(m+1-abs(y-tan(49.9173*pi/180)*x+718.5182),0),1,0)*if(max(52.4451+1-abs(y+cot(49.9173*pi/180)*x-1108.5907),0),1,0)+0.57881*exp(-abs(y-tan(-38.8644*pi/180)*x-759.6258)/m)*if(max(m+1-abs(y-tan(-38.8644*pi/180)*x-759.6258),0),1,0)*if(max(111.0938+1-abs(y+cot(-38.8644*pi/180)*x+330.1427),0),1,0)+0.9853*exp(-abs(y-tan(3.4812*pi/180)*x-723.6083)/m)*if(max(m+1-abs(y-tan(3.4812*pi/180)*x-723.6083),0),1,0)*if(max(39.8525+1-abs(y+cot(3.4812*pi/180)*x-15301.7596),0),1,0)+0.97858*exp(-abs(y-tan(-54.6353*pi/180)*x-1750.7627)/m)*if(max(m+1-abs(y-tan(-54.6353*pi/180)*x-1750.7627),0),1,0)*if(max(42.5895+1-abs(y+cot(-54.6353*pi/180)*x-636.9779),0),1,0)+0.74269*exp(-abs(y-tan(-50.1075*pi/180)*x-2298.4160)/m)*if(max(m+1-abs(y-tan(-50.1075*pi/180)*x-2298.4160),0),1,0)*if(max(51.6675+1-abs(y+cot(-50.1075*pi/180)*x-356.3355),0),1,0)+0.90014*exp(-abs(y-tan(-0.3082*pi/180)*x-404.9091)/m)*if(max(m+1-abs(y-tan(-0.3082*pi/180)*x-404.9091),0),1,0)*if(max(0.0000+1-abs(y+cot(-0.3082*pi/180)*x+109727.4060),0),1,0)+0.57094*exp(-abs(y-tan(68.9684*pi/180)*x+477.6968)/m)*if(max(m+1-abs(y-tan(68.9684*pi/180)*x+477.6968),0),1,0)*if(max(130.3433+1-abs(y+cot(68.9684*pi/180)*x-1003.8006),0),1,0)+0.71088*exp(-abs(y-tan(-34.6350*pi/180)*x-1086.2158)/m)*if(max(m+1-abs(y-tan(-34.6350*pi/180)*x-1086.2158),0),1,0)*if(max(91.3817+1-abs(y+cot(-34.6350*pi/180)*x+48.0794),0),1,0)+0.95787*exp(-abs(y-tan(16.7120*pi/180)*x-63.1893)/m)*if(max(m+1-abs(y-tan(16.7120*pi/180)*x-63.1893),0),1,0)*if(max(53.5775+1-abs(y+cot(16.7120*pi/180)*x-2819.9658),0),1,0)+0.8961*exp(-abs(y-tan(-10.1513*pi/180)*x-715.8037)/m)*if(max(m+1-abs(y-tan(-10.1513*pi/180)*x-715.8037),0),1,0)*if(max(127.9604+1-abs(y+cot(-10.1513*pi/180)*x+3144.6821),0),1,0)+0.97975*exp(-abs(y-tan(50.2810*pi/180)*x+282.4165)/m)*if(max(m+1-abs(y-tan(50.2810*pi/180)*x+282.4165),0),1,0)*if(max(20.0969+1-abs(y+cot(50.2810*pi/180)*x-925.0222),0),1,0),1)'
    vals = '40 80 60' 
# multiple variables in single inverted commas and separated by space in same order as below
    vars = 'm n p' 
# multiple variables in single inverted commas and separated by space.
  [../]
[]
################################################################################

[Kernels]
  [./pfbulk]
    type = SplitPFFractureBulkRate
    variable = c
    width = 40
    beta = b
    viscosity = 100
    gc = 'gc_prop'
    G0 = 'G0_pos'
    dG0_dstrain = 'dG0_pos_dstrain'
    displacements = 'ux uy'
  [../]
  [./DynamicTensorMechanics]
    displacements = 'ux uy'
  [../]
  [./solid_x]
    type = PhaseFieldFractureMechanicsOffDiag
    variable = ux
    component = 0
    c = c
  [../]
  [./solid_y]
    type = PhaseFieldFractureMechanicsOffDiag
    variable = uy
    component = 1
    c = c
  [../]
  [./dcdt]
    type = TimeDerivative
    variable = c
  [../]
  [./pfintvar]
    type = Reaction
    variable = b
  [../]
  [./pfintcoupled]
    type = LaplacianSplit
    variable = b
    c = c
  [../]
  [./inertiax]
    type = InertialForce
    variable = ux
    velocity = vx
    acceleration = ax
    beta = 0.3025
    gamma = 0.6
  [../]
  [./inertiay]
    type = InertialForce
    variable = uy
    velocity = vy
    acceleration = ay
    beta = 0.3025
    gamma = 0.6
  [../]
  [./hc]
    type = HeatConduction
    variable = temp
    diffusion_coefficient = thermal_conductivity
  [../]
  [./hct]
    type = HeatConductionTimeDerivative
    variable = temp
    specific_heat = specific_heat
    density_name = density
  [../]
  [./friction]
    type = CrackFrictionHeatSource
    variable = temp
    friction_coefficient = 1.0
    dcdx = dcdx
    dcdy = dcdy
  [../]
[]
################################################################################

[AuxKernels]
  [./stressxx]
    type = RankTwoAux
    variable = stressxx
    rank_two_tensor = stress
    index_j = 0
    index_i = 0
    execute_on = timestep_end
  [../]
  [./stressyy]
    type = RankTwoAux
    variable = stressyy
    rank_two_tensor = stress
    index_j = 1
    index_i = 1
    execute_on = timestep_end
  [../]
  [./stressxy]
    type = RankTwoAux
    variable = stressxy
    rank_two_tensor = stress
    index_j = 1
    index_i = 0
    execute_on = timestep_end
  [../]
  [./strainxx]
    type = RankTwoAux
    variable = strainxx
    rank_two_tensor = total_strain
    index_j = 0
    index_i = 0
    execute_on = timestep_end
  [../]
  [./strainyy]
    type = RankTwoAux
    variable = strainyy
    rank_two_tensor = total_strain
    index_j = 1
    index_i = 1
    execute_on = timestep_end
  [../]
    [./strainxy]
    type = RankTwoAux
    variable = strainxy
    rank_two_tensor = total_strain
    index_j = 1
    index_i = 0
    execute_on = timestep_end
  [../]
  [./ax]
    type = NewmarkAccelAux
    variable = ax
    displacement = ux
    velocity = vx
    beta = 0.3025
    execute_on = timestep_end
  [../]
  [./vx]
    type = NewmarkVelAux
    variable = vx
    acceleration = ax
    gamma = 0.6
    execute_on = timestep_end
  [../]
  [./ay]
    type = NewmarkAccelAux
    variable = ay
    displacement = uy
    velocity = vy
    beta = 0.3025
    execute_on = timestep_end
  [../]
  [./vy]
    type = NewmarkVelAux
    variable = vy
    acceleration = ay
    gamma = 0.6
    execute_on = timestep_end
  [../]
  [./psi_pos]
   variable = psi_pos
   type = MaterialRealAux
   property = G0_pos
   execute_on = timestep_end
 [../]
 [./e_xx]
   type = RankTwoAux
   variable = e_xx
   rank_two_tensor = strain_rate
   index_j = 0
   index_i = 0
   execute_on = timestep_end
 [../]
 [./e_yy]
   type = RankTwoAux
   variable = e_yy
   rank_two_tensor = strain_rate
   index_j = 1
   index_i = 1
   execute_on = timestep_end
 [../]
 [./e_xy]
   type = RankTwoAux
   variable = e_xy
   rank_two_tensor = strain_rate
   index_j = 1
   index_i = 0
   execute_on = timestep_end
 [../]
 [./dcdx]
   type = VariableGradientComponent
   variable = dcdx
   gradient_variable = c
   component = 'x'
 [../]
 [./dcdy]
   type = VariableGradientComponent
   variable = dcdy
   gradient_variable = c
   component = 'y'
 [../]
 [./crack_rho]
   type = MaterialRealAux
   variable = crack_rho
   property = crack_surface_density
 [../]
 [./heat_rate]
   type = MaterialRealAux
   variable = heat_rate
   property = heat_source_rate
 [../]
 [./f_x]
   type = MaterialStdVectorAux
   variable = f_x
   property = friction_force
   index = 0
 [../]
 [./f_y]
   type = MaterialStdVectorAux
   variable = f_y
   property = friction_force
   index = 1
 [../]
 [./s_x]
   type = MaterialStdVectorAux
   variable = s_x
   property = slide_velocity
   index = 0
 [../]
 [./s_y]
   type = MaterialStdVectorAux
   variable = s_y
   property = slide_velocity
   index = 1
 [../]
 [./friction_normal_force]
   type = MaterialRealAux
   variable = friction_normal_force
   property = friction_normal_force
 [../]
 [./slide_velocity_parallel]
   type = MaterialRealAux
   variable = slide_velocity_parallel
   property = slide_velocity_parallel
 [../]
[]
################################################################################

[ICs]
  [./compression_ic]
    type = ConstantIC
    variable = vx
    boundary = left
    value = 0.01
  [../]
  [./initial_damage]
    type = FunctionIC
    function = initial_crack
    variable = c
    block = particle
  [../]
  [./initial_damage_gradient]
    type = FunctionIC
    function = initial_gradient
    variable = b
    block = particle
  [../]
[]
################################################################################

[BCs]
  [./comp_left]
    type = PresetVelocity
    variable = ux
    boundary = 0
    velocity = 0.01
  [../]
  [./x_right]
    type = PresetBC
    variable = ux
    boundary = 2
    value = 0
  [../]
  [./y_bottom]
    type = PresetBC
    variable = uy
    boundary = 1
    value = 3
  [../]
  [./y_top]
    type = PresetBC
    variable = uy
    boundary = 3
    value = 5
  [../]
[]
################################################################################

[Materials]
  [./pfbulkmat_matrix]
    type = PFFracBulkRateMaterial
    block = matrix
    gc = 0.400
  [../]
  [./elastic_damage_particle]
    type = LinearIsoElasticPFDamage
    c = c
    block = particle
    kdamage = 1E-6
  [../]
  [./elastic_damage_polymer]
    type = PositiveVolumetricStrainPFDamage
    c = c
    block = 'interface matrix'
    kdamage = 1E-6
  [../]
  [./elasticity_tensor_matrix]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = 0.005
    poissons_ratio = 0.49
    block = 'interface matrix'
  [../]
  [./strain]
    type = ComputeIncrementalSmallStrain
    displacements = 'ux uy'
  [../]
  [./density_particle]
# Does this order stay preserved? (i.e. does type,bloc,prop_name,prop_value appear)
    type = GenericConstantMaterial
    block = particle
    prop_names = density
    prop_values = 1.9
  [../]
  [./thermal_conductivity_hmx]
    type = GenericConstantMaterial
    block = particle
    prop_names = 'thermal_conductivity'
    prop_values = '0.31e-6'
  [../]
  [./specific_heat_hmx]
    type = GenericConstantMaterial
    block = particle
    prop_names = 'specific_heat'
    prop_values = '1200e-6'
  [../]
  [./thermal_conductivity_matrix]
    type = GenericConstantMaterial
    block = 'matrix interface'
    prop_names = 'thermal_conductivity'
    prop_values = '0.22e-6'
  [../]
  [./specific_heat_matrix]
    type = GenericConstantMaterial
    block = 'matrix interface'
    prop_names = 'specific_heat'
    prop_values = '2500e-6'
  [../]
  [./crackfrictionheatenergy]
    type = ComputeCrackFrictionHeatEnergyDienes
    friction_coefficient = 1.0
    dcdx = dcdx
    dcdy = dcdy
    c = c
    l = 40
  [../]
[]
################################################################################

[Preconditioning]
  [./smp]
    type = SMP
    full = true
  [../]
[]
################################################################################

[Executioner]
  type = Transient
  start_time = 0.0
  dt = 1
  dtmin = 1
  end_time = 50000.0
  nl_rel_tol = 1E-6
  nl_abs_tol = 1E-8
  solve_type = PJFNK
  petsc_options_iname = '-ksp_gmres_restart -pc_type -pc_hypre_type -pc_hypre_boomeramg_max_iter'
  petsc_options_value = '201 hypre boomeramg 20'
  line_search = 'none'
[]
################################################################################

[Outputs]
  interval = 50
  exodus = true
[]

exp(-abs(y-528)/m)*if(max(m+1-abs(y-528),0),1,0)*if(max(50+1-abs(x-506),0),1,0)
