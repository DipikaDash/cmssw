from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10_ext1-v1/MINIAODSIM'
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'prod2018MC_NANO.py'
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.outputPrimaryDataset = 'MinBias'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 10
NJOBS = 10  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'CMSDAS2019_CRAB3_TTBAR_RELVAL'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
