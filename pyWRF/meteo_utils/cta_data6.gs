'open wrfout_d03_2012-01-01_00_00_00'
'set lat 28.76'
'set lon 342.12'
'set gxout print'
'set prnopts %0.2f'
outputfile='density_prova.txt'
tt=1
while(tt<=20)
    'set t 'tt
        'q time'
        time=subwrd(result,3)
        dummy=write(outputfile,time)
        'd t2'
        temp2m=sublin(result,2)
        dummy=write(outputfile,temp2m,append)
        'd q2'
        q2m=sublin(result,2)
        dummy=write(outputfile,q2m,append)
        'd psfc'
        psfc2m=sublin(result,2)
        dummy=write(outputfile,psfc2m,append)
        'd u10'
        uwind10m=sublin(result,2)
        dummy=write(outputfile,uwind10m,append)
        'd v10'
        vwind10m=sublin(result,2)
        dummy=write(outputfile,vwind10m,append)
    tt=tt+1
endwhile
'close 1'
