function [pick_sample, pick_err_low, pick_err_high, cf] = aurem_rec(x)
%% AUREM_REC
% RECiprocal - based Picker Information Criteria as implemented in 
% Madarshahian et al. 2020.
% This function is part of the AUtoREgressiveModel picker suite.
%
% The picking error is defined over the charachteristic function (CF).
% If CFmin represents the minimum and CFmax the maximum values in 
% the picking window, thrCF can be defined with a threshold (THR) of the 
% differential CF (Diehl et al. 2009)
%    thrCF = CFmin + (CFmax − CFmin)/THR
%
% Such a threshold could be changed inside the script-function. At the 
% moment the default values is set to 10.
%
% USAGE: AUREM_REC(arrayvector)
%
%   Input:
%       arrayvector: time-series
%
%   Output:
%       pick_sample:   pick idx based on the input array
%       pick_err_low:  lower boundary pick-error (in samples) respect to
%                      the actual pick.
%       pick_err_high: higher boundary pick-error (in samples) respect to
%                      the actual pick.
%       cf:            the REC characteristic function
%
% LICENSE:
%              GNU GENERAL PUBLIC LICENSE
%                Version 3, 29 June 2007
%


THR = 10;

%% Work
if ~isempty(x)
    n = length(x);
    cf = zeros(1, n-1);
    for i=1:n-1
        %compute variance in first part
        v1 = var(x(1:i));
        if v1 <= 0
            v1 = 0;
        else
            v1= i/v1;
        end
        %compute variance in second part
        v2 = var(x(i+1:n));
        if v2 <= 0
            v2 = 0;
        else
            v2= (n-i)/v2;
        end
        cf(i) = -v1 -v2 ;
    end

    %%% Pick
    pick_sample = find(cf==min(cf));
    
    %%% Define Error
    cf_thr = min(cf) + (max(cf) - min(cf))/THR;
    [~, low_bound] = (min(abs(cf(1:pick_sample) - cf_thr)));
    [~, high_bound] = (min(abs(cf(pick_sample:n-1) - cf_thr)));
    high_bound = pick_sample + high_bound;
    %
    pick_err_low = pick_sample - low_bound;    % in sample
    pick_err_high = high_bound - pick_sample;  % in sample
    % pick_err = pick_err_high + pick_err_low;   % in sample

else
    cf = nan;
    pick_sample = nan;
    pick_err_low = nan;      
    pick_err_high = nan;

end

return
