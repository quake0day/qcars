%this file generates randome topology
%It returns two matrix: Z describes the distance among transmitters with a
%boundry. D is the distance between each trasnmitter to server


%function [D] = topology(n,distance_BOUND,space)
function [Z,D] = topology(Num,distance_BOUND,space)
%n is number of nodes, also the maximum distance of x and y
%== code follows ==
% X = randn(50,2);
% randn - normal  vs rand - uniform
% guassian distribution
% Y = reshape(1:100,50,2);
% plotmatrix(X)
% scatter(X(:,1),X(:,2));
%figure;
S = [0.5*space,0.5*space];%server location assumes to be in the center;


Y = rand(double(Num),2)*double(space);
%scatter(Y(:,1),Y(:,2));
D = zeros(Num,1); %distance between each trasnmitter to server

%find interference source
Z = zeros (Num,Num);
for i=1:Num
    D(i) = sqrt((Y(i,1)-S(1))^2+(Y(i,2)-S(2))^2); %distance between transmitters to server
    for j=i+1:Num
        dist = sqrt((Y(i,1)-Y(j,1))^2+(Y(i,2)-Y(j,2))^2);
        if dist<distance_BOUND
            Z(i,j)=dist;
            Z(j,i)=dist;
        end
    end
end
end

