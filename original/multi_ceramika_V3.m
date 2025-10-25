% otwieranie wielu plików z rozszerzeniem CSV
[files, path] = uigetfile({'*.csv', 'Pliki CSV (*.csv)'}, ...
                          'Wybierz pliki CSV', ...
                          'MultiSelect', 'on');


% sprawdzam, czy wybrałem plik
if isequal(files, 0)
    disp('Nie wybrano żadnych plików.');
    return; %kończy program, nie wracam do wyboru plików
end


% Jeśli wybrano tylko jeden plik, zamień char na cell, aby kolejne funkcje działały
if ischar(files)
    files = {files};
end


% Iteracja przez wszystkie wybrane pliki
for i = 1:length(files)
    filename = fullfile(path, files{i}); %łączenie ścieżki
    [~, ~, rozszerzenie] = fileparts(filename); %pobieranie rozszerzenia i ignorowanie ścieżki
    if strcmp(rozszerzenie, '.csv')
        rawLines = readlines(filename);% czytam plik CSV jako tekst
        rawLines = replace(rawLines, ",", ";"); % zamieniam przecinki na średniki
        writelines(rawLines, filename); % Zapisz z powrotem jako tekst
    else
        disp('Wybrane pliki nie są typu CSV.');
        return;
    end
end
disp('Gotowe.');