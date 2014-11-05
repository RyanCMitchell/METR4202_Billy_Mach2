function [r1, r2, r3] = getRTC(handle)
  
    w1 = NXT_GetOutputState(0,handle);
    w2 = NXT_GetOutputState(1,handle);
    w3 = NXT_GetOutputState(2,handle);
    r1 = w1.RotationCount;
    r2 = w2.RotationCount;
    r3 = w3.RotationCount;
    

end