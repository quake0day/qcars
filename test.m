%test

C = 1; %number of channel
S = 1; %scenario
Num = 5;%number of nodes
space = 10; %simulation space
distance_BOUND = 2/space; %distance_BOUND for a transmiter that serve as interference to another transmitter
T = 100;
C = 1;
SA = zeros(C,T+13);
%topology
[Z,D] = topology(Num,distance_BOUND,space);
R = [1,1,3,2;1,2,3,3;2,1,3,3;2,5,3,4];


for t=1:100
    R=[t 1 3 2; t 2 3 4; t 3 2 5];%request 
    
    %%%%function call for EarliestFirst and SmallestFirst
    %[Decision, SortedR, AvaiChanal,row,Trans] = SmallestFirst(D,R,S,SA);
    %[Decision, SortedR, AvaiChanal,row,Trans] = EarliestFirst(D,R,S,SA);
    %update the spectrum allocation matrix
    %if AvaiChanal ~= 0
    %    for j=1:AvaiChanal
    %            SA(row(j),t:t+Trans(j)) = SortedR(j,2);
    %    end
    %end
    
    %%%%function call for FCFS
    [Decision,row,Trans,p] = FCFS(D,R,S,SA);
    if find(p)~=0
        for j=1:size(p)
            SA(row(j),t:t+Trans(j)) = R(p(j),2);
        end
    end
end