clear all; clc; close all

%% IMPORT
x = dlmread('fg_sac.npa');
x = x(500:length(x)-500);  % zoom
x = detrend(x);

%% PICK
[p_aic, p_aic_err_low, p_aic_err_high, aic_cf] = aurem_aic(x);
fprintf('AIC pick: %d  LowErr: %d  HighErr: %d  TotalERROR: %d\n', ...
        p_aic, -p_aic_err_low, p_aic_err_high, p_aic_err_low + p_aic_err_high)

[p_rec, p_rec_err_low, p_rec_err_high, rec_cf] = aurem_rec(x);
fprintf('REC pick: %d  LowErr: %d  HighErr: %d  TotalERROR: %d\n', ...
        p_rec, -p_rec_err_low, p_rec_err_high, p_rec_err_low + p_rec_err_high)

%% PLOT
xplot = normalize(x, 'range', [-1 1]);
aic_cf_plot = normalize(aic_cf, 'range', [0 1]);
rec_cf_plot = normalize(rec_cf, 'range', [0 1]);

figure(); hold on
tr = plot(xplot, 'DisplayName', 'Trace');
aic = plot(aic_cf_plot, 'DisplayName', 'AIC-cf');
aicpick = xline(p_aic, 'DisplayName', 'AIC-pick');
rec = plot(rec_cf_plot, 'DisplayName', 'REC-cf');
recpick = xline(p_rec, 'DisplayName', 'REC-pick');

legend


axis tight








