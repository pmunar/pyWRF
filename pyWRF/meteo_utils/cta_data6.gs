'open wrfout_d03_2012-01-01_00_00_00'
'set lat 28.76'
'set lon 342.12'
'set gxout print'
'set prnopts %0.2f'
outputfile='density_prova.txt'
tt=1
while(tt<=20)
    'set t 'tt
        'define tc=t2-273.15'
        'define esat=6.11176750+tc*(0.443986062+tc*(0.0143053301+tc*(0.000265027242+tc*(0.00000302246994+tc*(0.0000000203886313+tc*0.0000000000638780966)))))'
        'define qsat=0.622*(esat/(((psfc)/100)-esat))'
        'define RH=(q2/qsat)'
        'q time'
        time=subwrd(result,3)
        dummy=write(outputfile,time)
        'd t2'
        temp2m=sublin(result,2)
        dummy=write(outputfile,temp2m,append)
        'd RH'
        rhsfc=sublin(result,2)
        dummy=write(outputfile,rhsfc,append)
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
