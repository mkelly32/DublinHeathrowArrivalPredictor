a =[ 0.2132199 , -0.      ,    0.10763292 , 0.0051867  , 0.5024525,  0.   ,      -0.   ,      0.    ,     -0.1586784  ,-0.0052332 , -1.06483294 ,-0.     ,     0.    ,      0.      ,    0.    ,      0.   ,      -0.  ,0. ,        -0.       ,  -0.    ,     -0.    ,      0.00209548 , 0.06279668]
b = ["DTemp(Farrenheit)","DRain(mm/h)","DWindSpeed(knots)","DWindDirection(degrees)", "DVisibility","DCloudCoverage","LTemp(Farrenheit)","LRainDRain(mm/h)","LWindSpeed(knots)","LWindDirection(degrees)","LVisibility","LCloudCoverage","B788","B789","A320","A20N","A319","A330","A21N","B772","A333","Weighted DWindSpeed(knots)", "Weighted LWindSpeed(knots)"]

print(int(len(a)), " ", int(len(b)))
for i in range(0,len(a)):
    if(a[i] != 0.0):
        print(b[i] + ": " + str(a[i]))