---
title: read iphone temp
date: 2024-08-25
---
# My iphone has been overheating lately, 🤔
Read one good tip, forget where, just try to avoid using your phone while charging it if it is starting to overheat. But also, if it is really heating up, to stop charging it just in case. Makes sense. Going to try that next time.

## But what is the temp anyway?
Nice, learned from here, https://www.guidingtech.com/how-to-check-iphone-temperature/, you can access your iphone temp through the Privacy Settings, Analytics data. Looks like I had this turned on so I downloaded two of my last files there, 
```sh
Analytics-2024-08-23-200007.ips.ca.synced
Analytics-2024-08-24-200007.ips.ca.synced
```
and changed them to `.jsonl` since they look like json lines files.

## read that and also noticed , nice polars has a sql read interface?
Because appeared that the temp key `last_value_AverageTemperature` is nested.

{{< figure src="https://s3.amazonaws.com/my-blog-content/2024-08-25-iphone-temp/Screenshot 2024-08-25 at 11.24.48 AM.jpeg" width="75%">}}


```python
import json
import polars as pl
from pathlib import Path

data0823 = Path("Analytics-2024-08-23-200007.ips.ca.synced.jsonl").read_text()
from pathlib import Path
data0823 = Path("Analytics-2024-08-23-200007.ips.ca.synced.jsonl").read_text()


df23 = pl.from_dicts(
[json.loads(x) for x in data0823.splitlines()]
)
df24 = pl.from_dicts(
[json.loads(x) for x in data0824.splitlines()]
)
df23.shape, df24.shape
```
```
# Out[12]: ((1216, 37), (1151, 37))
```

## cool looking schema
```python
In [18]: df23.schema
Out[18]: 
Schema([('bug_type', String),
        ('timestamp', String),
        ('os_version', String),
        ('roots_installed', Int64),
        ('incident_id', String),
        ('_marker', String),
        ('_preferredUserInterfaceLanguage', String),
        ('_userInterfaceLanguage', String),
        ('_userSetRegionFormat', String),
        ('basebandChipset', String),
        ('basebandFirmwareVersion', String),
        ('configDbVersion', Int64),
        ('configParentUuid', String),
        ('configUuid', String),
        ('currentCountry', String),
        ('deviceCapacity', Int64),
        ('dramSize', Float64),
        ('homeCarrierBundleVersion', String),
        ('homeCarrierCountry', String),
        ('homeCarrierName', String),
        ('isDualSim', Boolean),
        ('market', String),
        ('optIn3rdParty', Boolean),
        ('productSku', String),
        ('rolloverReason', String),
        ('servingCarrierName', String),
        ('startTimestamp', String),
        ('stateDbType', String),
        ('stateDbVersion', Int64),
        ('trialExperiments', String),
        ('trialRollouts', String),
        ('version', String),
        ('deviceId', String),
        ('message',
         Struct({'Count': Int64, 'last_value_AlgoChemID': Int64, 'last_value_AppleRawMaxCapacity': Int64, 'last_value_AverageTemperature': Int64, 'last_value_BatteryHealthMetric': Int64, 'last_value_BatterySerialChanged': Boolean, 'last_value_ChemID': Int64, 'last_value_ChemicalWeightedRa': Int64, 'last_value_CycleCount': Int64, 'last_value_CycleCountLastQmax': Int64, 'last_value_DOFU': Null, 'last_value_DailyMaxSoc': Int64, 'last_value_DailyMinSoc': Int64, 'last_value_Flags': Int64, 'last_value_FlashWriteCount': Int64, 'last_value_GGUpdateStatus': Null, 'last_value_GasGaugeFirmwareVersion': Int64, 'last_value_HighAvgCurrentLastRun': Int64, 'last_value_ITMiscStatus': Int64, 'last_value_KioskModeHighSocDays': Int64, 'last_value_KioskModeHighSocSeconds': Int64, 'last_value_KioskModeLastHighSocHours': Int64, 'last_value_LastUPOTimestamp': Float64, 'last_value_LifetimeUPOCount': Int64, 'last_value_LowAvgCurrentLastRun': Int64, 'last_value_MaximumCapacityPercent': Int64, 'last_value_MaximumChargeCurrent': Int64, 'last_value_MaximumDeltaVoltage': Int64, 'last_value_MaximumDischargeCurrent': Int64, 'last_value_MaximumFCC': Int64, 'last_value_MaximumOverChargedCapacity': Int64, 'last_value_MaximumOverDischargedCapacity': Int64, 'last_value_MaximumPackVoltage': Int64, 'last_value_MaximumQmax': Int64, 'last_value_MaximumRa0_8': Int64, 'last_value_MaximumRa8': Int64, 'last_value_MaximumTemperature': Int64, 'last_value_MinimumDeltaVoltage': Int64, 'last_value_MinimumFCC': Int64, 'last_value_MinimumPackVoltage': Int64, 'last_value_MinimumQmax': Int64, 'last_value_MinimumRa0_8': Int64, 'last_value_MinimumRa8': Int64, 'last_value_MinimumTemperature': Int64, 'last_value_NCCMax': Int64, 'last_value_NCCMin': Int64, 'last_value_NominalChargeCapacity': Int64, 'last_value_OriginalBattery': Int64, 'last_value_QmaxCell0': Int64, 'last_value_QmaxUpdFailCount': Int64, 'last_value_QmaxUpdSuccessCount': Int64, 'last_value_RDISCnt': Int64, 'last_value_RSS': Int64, 'last_value_RaTable_1': Int64, 'last_value_RaTable_10': Int64, 'last_value_RaTable_11': Int64, 'last_value_RaTable_12': Int64, 'last_value_RaTable_13': Int64, 'last_value_RaTable_14': Int64, 'last_value_RaTable_15': Int64, 'last_value_RaTable_2': Int64, 'last_value_RaTable_3': Int64, 'last_value_RaTable_4': Int64, 'last_value_RaTable_5': Int64, 'last_value_RaTable_6': Int64, 'last_value_RaTable_7': Int64, 'last_value_RaTable_8': Int64, 'last_value_RaTable_9': Int64, 'last_value_ResetCnt': Int64, 'last_value_ResetDataComms': Int64, 'last_value_ResetDataFirmware': Null, 'last_value_ResetDataHardware': Null, 'last_value_ResetDataSoftware': Null, 'last_value_ResetDataWatchDog': Null, 'last_value_ServiceOption': Int64, 'last_value_TemperatureSamples': Int64, 'last_value_TimeAbove95Perc': Null, 'last_value_TotalOperatingTime': Int64, 'last_value_UpdateTime': Int64, 'last_value_WeekMfd': Int64, 'last_value_WeightedRa': Int64, 'last_value_Wom_1': Int64, 'last_value_Wom_2': Null, 'last_value_batteryServiceFlags': Int64, 'last_value_calibrationFlags': Null, 'last_value_xFlags': Int64, 'bucketed_isOwnerUser': Int64, 'bucketed_isPrimaryResident': Int64, 'bucketed_numAccessories': Int64, 'bucketed_numCapableSiriEndpointAccessories': Int64, 'bucketed_numEnabledSiriEndpointAccessories': Int64, 'bucketed_numHAPAccessories': Int64, 'bucketed_numHomePodMinis': Int64, 'bucketed_numHomePods': Int64, 'bucketed_numUsers': Int64, 'homeCreationCohortWeek': Int64, 'bug_type': String, 'error': String, 'saved': Int64, 'reason': String, 'isSupported': Boolean, 'language': String, 'activityName': String, 'activityShouldWake': Boolean, 'daily_total_numEvents': Int64, 'isFMFDevice': Boolean, 'isHH2Enabled': Boolean, 'biologicalSex': String, 'bucketed_age': Int64, 'hasCompatiblePairedAppleWatch': Null, 'isImproveHealthAndActivityAllowed': Boolean, 'isOnboarded': Int64, 'settings_fertilityNotificationEnabled': Boolean, 'settings_fertilityPredictionEnabled': Null, 'settings_logBasalBodyTemperatureEnabled': Boolean, 'settings_logCervicalMucusQualityEnabled': Boolean, 'settings_logOvulationTestResultEnabled': Boolean, 'settings_logSexualActivityEnabled': Boolean, 'settings_logSpottingEnabled': Boolean, 'settings_logSymptomsEnabled': Boolean, 'settings_periodNotificationEnabled': Boolean, 'settings_periodPredictionEnabled': Null, 'weeksSinceOnboardedV2': Null, 'daily_maximum_attemptCount': Int64, 'daily_maximum_totalHomeCategoryBitMask': Int64, 'daily_total_autoEndCount': Int64, 'daily_total_autoStartCount': Int64, 'daily_total_dryRunEndCount': Int64, 'daily_total_dryRunStartCount': Int64, 'daily_total_endCount': Int64, 'daily_total_errorCount': Int64, 'daily_total_isHH2EnabledCount': Int64, 'daily_total_manualEndCount': Int64, 'daily_total_manualStartCount': Int64, 'daily_total_startCount': Int64, 'errorCode': Int64, 'errorDomain': String, 'numAdminUsers': Int64, 'numAppleAudioAccessories': Int64, 'numAppleMediaAccessories': Int64, 'numAppleTVAccessories': Int64, 'numHAPAccessories': Int64, 'numHomes': Int64, 'numMatterAccessories': Int64, 'numNonEmptyHomes': Int64, 'numOwnedHomes': Int64, 'numResidentEnabledHomes': Int64, 'numSmartHomeAccessories': Int64, 'numThirdPartyMediaAccessories': Int64, 'numThreadAccessories': Int64, 'numUsers': Int64, 'underlyingErrorCode': Null, 'underlyingErrorDomain': Null, 'TimeInterval': Int64, 'first_value_AudioOnDuration': Int64, 'first_value_ScreenOnDuration': Int64, 'first_value_WakeDuration': Int64})),
        ('name', String),
        ('sampling', Float64),
        ('uuid', String)])
```

## Ok here looks like my phone's average temp past two days has been 26 C
More granular temp would be nice though
```python

df23.sql("select message.last_value_AverageTemperature as last_value_AverageTemperature from self where message.last_value_AverageTemperature is not null")
```
```python
Out[27]: 
shape: (5, 1)
┌───────────────────────────────┐
│ last_value_AverageTemperature │
│ ---                           │
│ i64                           │
╞═══════════════════════════════╡
│ 26                            │
│ 26                            │
│ 26                            │
│ 26                            │
│ 26                            │
└───────────────────────────────┘

```
```python
df24.sql("select message.last_value_AverageTemperature as last_value_AverageTemperature from self where message.last_value_AverageTemperature is not null")
```
```python
Out[28]: 
shape: (5, 1)
┌───────────────────────────────┐
│ last_value_AverageTemperature │
│ ---                           │
│ i64                           │
╞═══════════════════════════════╡
│ 26                            │
│ 26                            │
│ 26                            │
│ 26                            │
│ 26                            │
└───────────────────────────────┘
```

## also noticed other temp keys
Can look at them another time, but noticed casually, some of them have pretty wild values actually.
```
last_value_BatteryTemperature
first_value_BatteryTemperature
last_value_MaximumTemperature
last_value_MinimumTemperature
```
 I saw the line `"last_value_MinimumTemperature":-21` ! And `"last_value_MaximumTemperature":459`, putting all of the values validity into question hmm.
