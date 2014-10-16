

array = []
array2 = []
for ztest = 0:360

[z,x,y] = forwardKin(ztest,ztest,ztest);
array = [array;z];
array2 = [array2;ztest];

end

figure
plot(array2, array );