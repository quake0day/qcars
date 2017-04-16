%%%%%%%%%%input:
%%%1. D is the distance between each node and the server
%%%2. R is the transmission request from all nodes at each time epoch.
%%%There are four columns in the request: time epoc for the request, 
%%%node ID, packet size, and reqired finish time.
%%%3. C is the number of available channel
%%%4. S is scenario free space(1), indoor(2)

%%%%%%%%%notes
%%%1. coexistence is not considered in this case (one node per channel)
%%%2. malicious users that always send the smallest packet size is not
%%%considered
function [Decision,row,Trans,p] = FCFS(D,R,S,SA)
    %SA = zeros(C,T+13);
    Pt = 6; %transmission power level 1 watt in unlicensed band
    BW = 40*10^6; %Herts bandwidth for WiFi
    Floor = 1; %indoor path loss model input: number of floor (1-3)
    m = 1; %indoor path loss model input: residential(1), office(2), commercial(3)
    
    row = 0;
    Trans = zeros(numel(D));
    
    %T = 100; % total simulation duration
    %SA = zeros(C,T+threshold); %spectrum allocation matrix
    sz = size(R); %determine the size of R, function size will return a 1*2
    p = zeros(sz(1));%store the randomly generated number to determine which node can transmit
    %matrix, the first element is the number of rows in R and the second
    %one is the number of columns).
    Num = numel(D);%number of nodes
    N = zeros(Num,1); %noise level for each transceiver
    PL = zeros(Num,1); %pass loss for each node
    Signal = zeros(Num,1); %signal level for each node
    SNR = zeros(Num,1); %signal to noise ratio for each node
    Cap = zeros(Num,1); %transmission rate for each node
    Decision = R; %decision copy all columns in request 
    Decision = [Decision zeros(sz(1),1)]; %add one more column to the Decision
    %to indicate whether the node can transmit or not. 0 means no
    %transmission, 1 means the node can transmit.
    
    %%%%%%%%step 1: transmission rate for each node
    for i=1:Num
        if S == 1 %free space
            PL(i) = free_space(900*10^6,D(i)); %free space path loss in dB
        elseif Scenario == 2 %indoor
            PL(i) = Indoorpathlossmodel(Floor,D(i),m);%indoor path loss in dB
        end
        Signal(i) = 10^((10*log10(Pt)-PL(i))/10); %convert signal level from decible to power
        N(i) = 0.05; %assume noise level is the same for all nodes
        SNR(i) = Signal(i)/N(i); %signal to noise ratio in ratio
        Cap(i) = BW*log2(1+SNR(i)); %shannon capacity law to calculate transmission rate
    end
    %%%%%%%%step 2: spectrum allocation
    t=R(1,1); %request time 
    
    %if spectrum is occupied, nothing needs to be done, Decision stays the
    %same, since the decision columns is initilized from 0.
    %isempty returns 1 indicates the array is empty, 0 indicates the array
    %is not empty
    %if spectrum is available, in other words, there is at least one 
    %elements in SA(:,t) equals to 0
    if(isempty(find(SA(:,t)==0, 1))==0)
        %determine which channel is available
        [row]=find(~SA(:,t)); %row records the row number for each element==0
                   %row(1) is the first available channel, etc.
        AvaiChanal = numel(row); % total number of available channel
                   
        %determine which node can transmit
        if AvaiChanal<sz(1) %number of available channels is less than request
            p = randperm(sz(1),AvaiChanal); %randomly generate the row number that can transmit
        else %number of available channels is greater than request
            p = R(:,2); %all nodes can transmit
        end
        
        
        %determine the transmission time for this node
        for i=1:size(p)
            Trans(i) = ceil(R(p(i),3)/Cap(R(p(i),2))); %transmission duration
        end
        
        %update the spectrum allocation matrix (update in the main program)
        %for i=1:size(p)
        %    SA(row(i),t:t+Trans(i)) = R(p(i),2);
        %end
        
        %update the Decision matrix
        for i=1:size(p)
            Decision(p(i),5)=1;
        end
    end
        
        
    
end