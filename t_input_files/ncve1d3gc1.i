################################################################################
# Units: Length-micrometer, Mass-femtogram, Time-nanosecond
# Domain size - 2D - 1000 x 1000 um
# Element - Quad of 10 um
# Material - Homogeneous, Isotropic, Linearly Elastic Polymer
# E = 0.0005 GPa, density = 2000 kg/m3, Gc = 1 J/m2
# No crack
# L0 = 40 um
# Loading - Engineering strain rate 10^4 s^-1
################################################################################

[Mesh]
  type = GeneratedMesh
  dim = 2
  xmin = 0
  xmax = 1000
  nx = 100
  ymin = 0
  ymax = 1000
  ny = 100
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
[]
################################################################################

[Functions]
  [./initial_crack]
    type = ParsedFunction
    value = 'min(exp(-abs(y-500)/m)*if(max(10-abs(y-500),0),1,0)*if(max(10-abs(x-500),0),1,0),1)'
    vals = 40
    vars = m
  [../]
  [./initial_gradient]
    type = ParsedFunction
    value = '(1/(m*m))*min(exp(-abs(y-500)/m)*if(max(10-abs(y-500),0),1,0)*if(max(10-abs(x-500),0),1,0),1)'
    vals = 40
    vars = m
  [../]
  [./topbc_loading]
    type = ParsedFunction
    value = '1E4*1E-9*500*t'
  [../]
  [./bottombc_loading]
    type = ParsedFunction
    value = '-1E4*1E-9*500*t'
  [../]
[]
################################################################################

[Kernels]
  [./pfbulk]
    type = PFFracBulkRate
    variable = c
    l = 40
    beta = b
    visco = 100
    gc_prop_var = 'gc_prop'
    G0_var = 'G0_pos'
    dG0_dstrain_var = 'dG0_pos_dstrain'
    disp_x = ux
    disp_y = uy
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
    type = PFFracIntVar
    variable = b
  [../]
  [./pfintcoupled]
    type = PFFracCoupledInterface
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
[]
################################################################################

[ICs]
  [./initial_damage]
    type = FunctionIC
    function = initial_crack
    variable = c
  [../]
  [./initial_damage_gradient]
    type = FunctionIC
    function = initial_gradient
    variable = b
  [../]
[]
################################################################################

[BCs]
  [./top_loading]
    type = FunctionPresetBC
    boundary = top
    variable = uy
    function = topbc_loading
  [../]
  [./bottom_loading]
    type = FunctionPresetBC
    boundary = bottom
    variable = uy
    function = bottombc_loading
  [../]
[]
################################################################################

[Materials]
  [./pfbulkmat]
    type = PFFracBulkRateMaterial
    gc = 0.001
  [../]
  [./elastic_damage_rdx]
    type = LinearIsoElasticPFDamage
    c = c
    kdamage = 1E-6
  [../]
  [./elasticity_tensor_rdx]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = 0.0005
    poissons_ratio = 0.48
  [../]
  [./strain]
    type = ComputeIncrementalSmallStrain
    displacements = 'ux uy'
  [../]
  [./density_particle]
    type = GenericConstantMaterial
    prop_names = density
    prop_values = 2.0
  [../]
[]
################################################################################

[Postprocessors]
  [./c]
    type = AverageNodalVariableValue
    variable = c
  [../]
  [./stressxxmax]
    type = ElementExtremeValue
    value_type = max
    variable = stressxx
  [../]
  [./stressxxmin]
    type = ElementExtremeValue
    value_type = min
    variable = stressxx
  [../]
  [./stressxymax]
    type = ElementExtremeValue
    value_type = max
    variable = stressxy
  [../]
  [./stressxymin]
    type = ElementExtremeValue
    value_type = min
    variable = stressxy
  [../]
  [./stressyymax]
    type = ElementExtremeValue
    value_type = max
    variable = stressyy
  [../]
  [./stressyymin]
    type = ElementExtremeValue
    value_type = min
    variable = stressyy
  [../]
  [./strainxxmax]
    type = ElementExtremeValue
    value_type = max
    variable = strainxx
  [../]
  [./strainxxmin]
    type = ElementExtremeValue
    value_type = min
    variable = strainxx
  [../]
  [./strainxymax]
    type = ElementExtremeValue
    value_type = max
    variable = strainxy
  [../]
  [./strainxymin]
    type = ElementExtremeValue
    value_type = min
    variable = strainxy
  [../]
  [./strainyymax]
    type = ElementExtremeValue
    value_type = max
    variable = strainyy
  [../]
  [./strainyymin]
    type = ElementExtremeValue
    value_type = min
    variable = strainyy
  [../]
  [./psiposmax]
    type = ElementExtremeValue
    value_type = max
    variable = psi_pos
  [../]
  [./psiposmin]
    type = ElementExtremeValue
    value_type = min
    variable = psi_pos
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
  dt = 10
  dtmin = 10
  end_time = 50E3
  nl_rel_tol = 1E-6
  nl_abs_tol = 1E-8
  solve_type = PJFNK
  petsc_options_iname = '-ksp_gmres_restart -pc_type -pc_hypre_type -pc_hypre_boomeramg_max_iter'
  petsc_options_value = '201 hypre boomeramg 20'
  line_search = 'none'
[]
################################################################################

[Outputs]
  interval = 10
  csv = true
[]
