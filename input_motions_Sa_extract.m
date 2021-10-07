%%-------------------------------------------------------------------------
%   Mott MacDonald, Inc.
%   Wenyong Rong (c)
%   June 10, 2021
%
%   This matlab script automatically read into a bunch of input motion
%   output spreadsheets from DEEPSOIL, so that the duhamel integral of Sa
%   at the soil horizon can be extracted without copying and pasting the
%   values from each tab in an individual spreadsheet.

%   To use this script for automatic processing, please make sure this script
%   (.m) and the DEEPSOIL output spreadsheets (.xlsx) in the same folder and
%   make sure it's been added to path in Matlab.
%
%%-------------------------------------------------------------------------

clc;
clear all;
close all;

%   read the tab names in the motion output spreadsheet from DEEPSOIL
tab = sheetnames('Zone 1 MCEr FNFP Input Motions.xlsx')

%   Extract data of interest in a bunch of DEEPSOIL ouput spreadsheet
for i = 1:length(tab)/2
    j = 2*i - 1;
    if j == 1
        %   Extract PSA at soil horizon
        table1 = readtable('Zone 1 MCEr FNFP Input Motions','Sheet',j);
        Period = table1(1:113,8);
        Soil_Horizon_PSA(:,i) = table1(1:113,10);
    else
        table1 = readtable('Zone 1 MCEr FNFP Input Motions','Sheet',j);
        Soil_Horizon_PSA(:,i) = table1(1:113,10);
    end
end

% Arrange data and write it out as .csv, so that .csv can be copied and
% pasted into the SRA template

Soil_Horizon_PSA = [Period, Soil_Horizon_PSA];
writetable(Soil_Horizon_PSA,'Soil_Horizon_PSA_MCEr.csv');