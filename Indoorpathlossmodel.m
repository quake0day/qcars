%ITU Indoor Path-Loss Model in dB
%n is number of floors between the transmitter and receiver
%d is distance between transmitter and receiver in meter
%N is the distance power loss coefficient
%pf is the floor loss penetration factor
%f is frequency in MHz
%m indicate residential(1), office(2), commercial(3)
function [PL_900] = Indoorpathlossmodel(n,d,m)
%PL = 20*log(f)+N*log(d)+Pf-28;
if m==1
    %900 MHz residential area
    PL_900 = 20*log(900)+log(d)-28;
%900 MHz office area
elseif m==2
    if n==1
        PL_900 = 20*log(900)+33*log(d)+9-28;%number of floors n=1
    elseif n==2
        PL_900 = 20*log(900)+33*log(d)+19-28;%number of floors n=2
    elseif n==3
        PL_900 = 20*log(900)+33*log(d)+24-28;%number of floors n=3
    end
elseif m==3
%900 MHz commercial area
    PL_900 = 20*log(900)+20*log(d)-28;
end

%1.8GHz residential area
PL_1800R = 20*log(1800)+28*log(d)+4*n-28;

%1.8GHz office area
PL_1800O = 20*log(1800)+30*log(d)+(15+4*(n-1))-28;

%1.8 GHz commercial area
PL_1800C = 20*log(1800)+22*log(d)+(6+3*(n-1))-28;

%5.2 GHz residential area
PL = 20*log(5200)+28*log(d)-28;

%5.2 GHz office area
PL = 20*log(5200)+31*log(d)+16-28;

%5.2 GHz commercial area
PL = 20*log(5200)+log(d)-28;
end