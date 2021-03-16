#!/usr/bin/python3
#
# MVG/Satimo to ADF antenna pattern conversion utility
#
# Copyright 2021 Farrant Consulting Ltd
# CloudRF.com
import csv
import sys

horizontal = []
vertical = []

if len(sys.argv) < 2:
    print("Usage: python3 satimo2adf.py {raw.csv}")
    quit()

# columns are H
# rows are V

# Column AW / -86 contains best H plane
# Row 50 / +90 contains best V plane

with open(sys.argv[1]) as csvfile:
    # First pass: Find best column and row
    reader = csv.reader(csvfile, delimiter=',')
    bestColumn=0
    bestRow=0
    r=1
    pos=0
    for row in reader:
        if "Phi" in row[0]: # Header
            header=row
        pos+=1
        if pos > 4 and float(row[180]):
                c=1
                for col in row[1:]:
                    if float(col) > bestColumn:
                        bestColumn=float(col)
                        bestColIdx=c
                        bestRowIdx=r
                    c+=1
        r+=1
    #print("Peak gain: %.3fdBi best column #%d best row #%d " % (bestColumn,bestColIdx,bestRowIdx))

gain = bestColumn

# second pass: Go straight for the best col/row
with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    r=0
    angle=-179
    for row in reader:
        r+=1
        if r > 4:
            c=0
            for col in row:
                c+=1
                if c == bestColIdx:
                    horizontal.append(str(angle)+","+str(round(float(col)-gain,3)))
                    angle+=1
                    horizontal.append(str(angle)+","+str(round(float(col)-gain,3)))
                    angle+=1

        if r == bestRowIdx:
            a=0
            offset=1 # Col 0 is Phi angles. Col 1 is first measurement
            while a < 360:
                pos = a + 90 # rot90
                if pos >= 360:
                    pos -= 360
                average = (float(row[int(pos/2)+offset])+float(row[int((pos+1)/2)+offset]))/2
                vertical.append(str(a-180)+","+str(round(average-gain,3)))
                a+=1

# Apply mirror image to H
a=1
while a < 181:
    horizontal.append(str(a)+","+horizontal[180-a].split(",")[1])
    a+=1

# CHANGE ME!
print("REVNUM:,TIA/EIA-804-B")
print("COMNT1:,Standard TIA/EIA Antenna Pattern Data")
print("ANTMAN:,COMPANY X")
print("MODNUM:,MODEL Y")
print("DESCR1:,DETAILED DESCRIPTION")
print("DESCR2:,Made with love at CloudRF.com")
print("DTDATA:,20210316")
print("LOWFRQ:,0")
print("HGHFRQ:,1000")
print("GUNITS:,DBD/DBR")
print("MDGAIN:,0.0")
print("AZWIDT:,360")
print("ELWIDT:,360")
print("CONTYP:,")
print("ATVSWR:,1.5")
print("FRTOBA:,0")
print("ELTILT:,0")
print("MAXPOW:,500")
print("ANTLEN:,")
print("ANTWID:,")
print("ANTWGT:,")
print("PATTYP:,Typical")
print("NOFREQ:,1")
print("PATFRE:,500")
print("NUMCUT:,2")

print("PATCUT:,H")
print("POLARI:,V/V")
print("NUPOIN:,360")
print("FSTLST:,-179,180")
for h in horizontal:
    print(h)
print("PATCUT:,V")
print("POLARI:,V/V")
print("NUPOIN:,360")
print("FSTLST:,-179,180")
for v in vertical:
    print(v)
print("ENDFIL:,EOF")
