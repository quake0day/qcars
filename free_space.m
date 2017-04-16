%*********************************************************************
%***Author:  	       Danda B. Rawat
%***Department:        ECE, ODU, Norfolk, VA, USA
%***Date:              02/06/2007
%***Modified:          02/06/2007
%***Email:             dbrawat@gmail.com
%*********************************************************************
%Program for free sapace model and plane earth model for wave propagation

function [lp_freespace_dB] = free_space(f,R_free_space)
%f=800000000; %in Hz
c=300000000; %in m/s
%R_free_space = 1:10:40000; %in meter
lp_freespace =((4*pi*R_free_space*f)/c).^2;
lp_freespace_dB = 10*log10(lp_freespace);

end
%subplot(2,2,1); 
%plot(R_free_space,lp_freespace)
%xlabel('x--> R (distance in Meter)'); 
%ylabel('y--> Lp (Path loss)'); 
%title('Free space model'); 
%grid on

%subplot(2,2,2); 
%plot(R_free_space,10*log(lp_freespace))
%xlabel('x--> R (distance in Meter)'); 
%ylabel('y--> Lp (Path loss in dB)'); 
%title('Free space model'); 
%grid on






