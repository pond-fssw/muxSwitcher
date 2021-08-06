driveFields = ["50 kV/cm", "100 kV/cm", "150 kV/cm", "200 kV/cm", "250 kV/cm", "300 kV/cm"]
featuredProperties = ["Pr Max", "Pr+", "Pr-", "Ec+", "Ec-", "Imprint", "Loop Area"]
bipolarHeader = ["Electrode Name"]

for driveField in driveFields:
    props = [driveField]
    props += featuredProperties
    bipolarHeader += props

print(bipolarHeader)
print(len(bipolarHeader))