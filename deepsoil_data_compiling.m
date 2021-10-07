%%-------------------------------------------------------------------------
%   Mott MacDonald, Inc.
%   Wenyong Rong (c)
%   June 10, 2021
%
%   This matlab script automatically read into a series of standardized output
%   spreadsheets (.xlsx) from DEEPSOIL runs and extract/compile the desired
%   data of interest in an organized format, so that it can be copied and 
%   pasted only once into the template spreadsheet for further calculation 
%   and plotting without opening and closing each individual output spreadsheet.
%
%   To use this script for automatic processing, please make sure this script
%   (.m) and the DEEPSOIL output spreadsheets (.xlsx) in the same folder and
%   make sure it's been added to path in Matlab.
%
%%-------------------------------------------------------------------------

clc;
clear all;
close all;

%   Define varibles in determining the name of the output spreadsheets from
%   DEEPSOIL
Prefix = {'Results_profile_0_motion'};
Zone = {'Zone1'};
Design = {'975'}; % The other options can be {'975'},{'MCAH'} or other design levels
GM = {'GM01';'GM02';'GM03';'GM04';'GM05';'GM06';'GM07';'GM08';'GM09';'GM10';'GM11'};
FNP = {'FN';'FP'};
%   Determine all the names of the DEEPSOIL output spreadsheets
for i = 1:length(Design)
    y = 22*(i-1)+1;
    for j = 1:length(GM)
        FN = [char(Prefix),'_',char(Zone),'_',char(Design),'_',char(GM(j)),'_',char(FNP(1))];
        FILE(y) = cellstr(FN);
        FN = [char(Prefix),'_',char(Zone),'_',char(Design),'_',char(GM(j)),'_',char(FNP(2))];
        FILE(y+1) = cellstr(FN);
        y = y+2;
    end
end
FILE = FILE.';
n = length(FILE);

%   Read and extract the desired data of interest in a bunch of spreadsheets,
%   the standardized four tabs in an individual output spreadsheet are 'Layer 1',
%   'Input Motion', 'Profile', 'Mobilized Shear Strength'
%   As an example, the following scripts read surface PSA (column i,j in tab 'Layer 1')
%   and maximum strain profile (column j,k in tab 'Profile') in each
%   DEEPSOIL run;

%   Read the tabs in the standardized DEEPSOIL output, the tab names (will
%   be referred) are stored in DESCR
%   [A, DESCR, FORMAT] = xlsfinfo(char(FILE(1)))

%   Extract data of interest in a bunch of DEEPSOIL ouput spreadsheet
for i = 1:n
    if i == 1
        %   Extract surface PSA
        table1 = readtable(char(FILE(i)),'Sheet','Layer 1');
        %   Extract max.strain profile
        table2 = readtable(char(FILE(i)),'Sheet','Profile');
        Period = table1(1:113,9);
        Depth = table2(1:46,10);
        Surface_PSA(:,i) = table1(1:113,10);
        Max_Strain(:,i) = table2(1:46,11);
    else
        table1 = readtable(char(FILE(i)),'Sheet','Layer 1');
        table2 = readtable(char(FILE(i)),'Sheet','Profile');
        Surface_PSA(:,i) = table1(1:113,10);
        Max_Strain(:,i) = table2(1:46,11);
    end
end

% Arrange data and write it out as .csv, so that .csv can be copied and
% pasted into the SRA template

Surface_PSA = [Period, Surface_PSA];
Max_Strain = [Depth, Max_Strain];
writetable(Surface_PSA,'Surface_PSA.csv');
writetable(Max_Strain,'Max_Strain.csv');