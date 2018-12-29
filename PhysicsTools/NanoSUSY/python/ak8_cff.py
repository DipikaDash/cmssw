import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *
from Configuration.Eras.Modifier_run2_miniAOD_80XLegacy_cff import run2_miniAOD_80XLegacy

# ---------------------------------------------------------


def setupCustomizedAK8(process, runOnMC=False, path=None):
    # recluster Puppi jets, add N-Subjettiness and ECF
    bTagDiscriminators = [
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfBoostedDoubleSecondaryVertexAK8BJetTags',
    ]
    subjetBTagDiscriminators = [
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfDeepCSVJetTags:probb',
        'pfDeepCSVJetTags:probbb',
    ]
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']

    # from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox
    from PhysicsTools.NanoSUSY.jetToolbox_cff import jetToolbox
    jetToolbox(process, 'ak8', 'dummySeq', 'out', associateTask=False,
               PUMethod='Puppi', JETCorrPayload='AK8PFPuppi', JETCorrLevels=JETCorrLevels,
               Cut='pt > 170.0 && abs(rapidity()) < 2.4',
               miniAOD=True, runOnMC=runOnMC,
               addNsub=True, maxTau=3, addEnergyCorrFunc=True,
               addSoftDrop=True, addSoftDropSubjets=True, subJETCorrPayload='AK4PFPuppi', subJETCorrLevels=JETCorrLevels,
               bTagDiscriminators=bTagDiscriminators, subjetBTagDiscriminators=subjetBTagDiscriminators)

    if runOnMC:
        process.ak8GenJetsNoNu.jetPtMin = 100
        process.ak8GenJetsNoNuSoftDrop.jetPtMin = 100

    # DeepAK8
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    from RecoBTag.MXNet.pfDeepBoostedJet_cff import _pfDeepBoostedJetTagsProbs, _pfMassDecorrelatedDeepBoostedJetTagsProbs
    updateJetCollection(
        process,
        jetSource=cms.InputTag('packedPatJetsAK8PFPuppiSoftDrop'),
        rParam=0.8,
        jetCorrections=('AK8PFPuppi', cms.vstring(['L2Relative', 'L3Absolute']), 'None'),
        btagDiscriminators=bTagDiscriminators + _pfDeepBoostedJetTagsProbs + _pfMassDecorrelatedDeepBoostedJetTagsProbs,
        postfix='AK8WithPuppiDaughters',
    )


    process.customAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src=cms.InputTag("selectedUpdatedPatJetsAK8WithPuppiDaughters"),
        name=cms.string("DeepAK8"),
        cut=cms.string(""),
        doc=cms.string("customized ak8 puppi jets for DeepAK8"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            # jetId=Var("userInt('tightId')*2+4*userInt('tightIdLepVeto')", int, doc="Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"),
            # area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            # rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            # tau1=Var("userFloat('NjettinessAK8Puppi:tau1')", float, doc="Nsubjettiness (1 axis)", precision=10),
            # tau2=Var("userFloat('NjettinessAK8Puppi:tau2')", float, doc="Nsubjettiness (2 axis)", precision=10),
            # tau3=Var("userFloat('NjettinessAK8Puppi:tau3')", float, doc="Nsubjettiness (3 axis)", precision=10),
            # n2b1=Var("userFloat('ak8PFJetsPuppiSoftDropValueMap:nb1AK8PuppiSoftDropN2')", float, doc="N2 with beta=1", precision=10),
            # n3b1=Var("userFloat('ak8PFJetsPuppiSoftDropValueMap:nb1AK8PuppiSoftDropN3')", float, doc="N3 with beta=1", precision=10),
            # msoftdrop=Var("groomedMass()", float, doc="Corrected soft drop mass with PUPPI", precision=10),
            # btagCSVV2=Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')", float, doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)", precision=10),
            # btagHbb=Var("bDiscriminator('pfBoostedDoubleSecondaryVertexAK8BJetTags')", float, doc="Higgs to BB tagger discriminator", precision=10),
            # subJetIdx1=Var("?nSubjetCollections()>0 && subjets().size()>0?subjets()[0].key():-1", int,
                 # doc="index of first subjet"),
            # subJetIdx2=Var("?nSubjetCollections()>0 && subjets().size()>1?subjets()[1].key():-1", int,
                 # doc="index of second subjet"),
            # nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            # nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
            # # BEST Tagger
            # bestT=Var("userFloat('BEST:dnn_top')", float, doc="Boosted Event Shape Tagger score Top", precision=-1),
            # bestW=Var("userFloat('BEST:dnn_w')", float, doc="Boosted Event Shape Tagger score W", precision=-1),
            # bestZ=Var("userFloat('BEST:dnn_z')", float, doc="Boosted Event Shape Tagger score Z", precision=-1),
            # bestH=Var("userFloat('BEST:dnn_higgs')", float, doc="Boosted Event Shape Tagger score Higgs", precision=-1),
            # bestQCD=Var("userFloat('BEST:dnn_qcd')", float, doc="Boosted Event Shape Tagger score QCD", precision=-1),
            # bestB=Var("userFloat('BEST:dnn_b')", float, doc="Boosted Event Shape Tagger score B", precision=-1),
        )
    )
    run2_miniAOD_80XLegacy.toModify(process.customAK8Table.variables, jetId=Var("userInt('tightId')*2+userInt('looseId')", int, doc="Jet ID flags bit1 is loose, bit2 is tight"))
    process.customAK8Table.variables.pt.precision = 10

    # add DeepAK8 scores: nominal
    for prob in _pfDeepBoostedJetTagsProbs:
        name = prob.split(':')[1].replace('prob', 'nn')
        setattr(process.customAK8Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    # add DeepAK8 scores: mass decorrelated
    for prob in _pfMassDecorrelatedDeepBoostedJetTagsProbs:
        name = prob.split(':')[1].replace('prob', 'nnMD')
        setattr(process.customAK8Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    process.customizedAK8Task = cms.Task(
        # process.tightJetIdCustomAK8,
        # process.tightJetIdLepVetoCustomAK8,
        # process.customAK8WithUserData,
        process.customAK8Table,
        # process.customAK8SubJetTable
        )

    if runOnMC:
        process.customGenJetAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
            src=cms.InputTag("ak8GenJetsNoNu"),
            cut=cms.string("pt > 100."),
            name=cms.string("CustomGenJetAK8"),
            doc=cms.string("AK8 GenJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.customGenJetAK8Table.variables.pt.precision = 10

        process.customGenSubJetAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
            src=cms.InputTag("ak8GenJetsNoNuSoftDrop", "SubJets"),
            cut=cms.string(""),
            name=cms.string("CustomGenSubJetAK8"),
            doc=cms.string("AK8 Gen-SubJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.customGenSubJetAK8Table.variables.pt.precision = 10

        # process.customizedAK8Task.add(process.customGenJetAK8Table)
        # process.customizedAK8Task.add(process.customGenSubJetAK8Table)


    if path is None:
        process.schedule.associate(process.customizedAK8Task)
    else:
        getattr(process, path).associate(process.customizedAK8Task)
# ---------------------------------------------------------
