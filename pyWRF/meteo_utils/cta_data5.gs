'open proves_d02_2012-05-10_00_00_00'
'set lat 28.76'
'set lon 342.12'
'set gxout print'
'set prnopts %0.2f'
outputfile='prova.txt'
tt=1
while(tt<=20)
    level=775
    'set t 'tt
    while(level>=70)
        'set lev 'level
        'q time'
        time=subwrd(result,3)
        dummy=write(outputfile,time)
        'define pres=(p+pb)'
        'define tempk=t+300'
        'define power=pow(pres/100000,0.286)'
        'define temp=tempk*power'
        'define gpm=(ph+phb)/9.81'
        'define density=pres*10000/(287.05*temp)'
        'define tc=temp-273.15'
        'define esat=6.11176750+tc*(0.443986062+tc*(0.0143053301+tc*(0.000265027242+tc*(0.00000302246994+tc*(0.0000000203886313+tc*0.0000000000638780966)))))'
        'define qsat=0.622*(esat/(((p+pb)/100)-esat))'
        'define RH=(qvapor/qsat)'
        'd pres'
        ds=sublin(result,2)
        dummy=write(outputfile,ds,append)
        'd temp'
        tp=sublin(result,2)
        dummy=write(outputfile,tp,append)
        'd gpm'
        gp=sublin(result,2)
        dummy=write(outputfile,gp,append)
        'd density'
        den=sublin(result,2)
        dummy=write(outputfile,den,append)
        'd u'
        uwind=sublin(result,2)
        dummy=write(outputfile,uwind,append)
        'd v'
        vwind=sublin(result,2)
        dummy=write(outputfile,vwind,append)
        'd qvapor'
        qv=sublin(result,2)
        dummy=write(outputfile,qv,append)
        'd RH'
        rhsfc=sublin(result,2)
        dummy=write(outputfile,rhsfc,append)
        level=level-25
    endwhile
    tt=tt+1
endwhile
'close 1'
