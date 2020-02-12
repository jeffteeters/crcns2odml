function [] = clearEventSeriesHash_values()
%clearEventSeriesHash_values truncate long arrays in eventSeriesHash.value
%   truncate long arrays in eventSeriesHash.value
global obj;
% truncate timeSeriesArrayHash values
if (length(obj.timeSeriesArrayHash.value{1}.time) > 10)
    obj.timeSeriesArrayHash.value{1}.time = obj.timeSeriesArrayHash.value{1}.time(1:10);
    obj.timeSeriesArrayHash.value{1}.time(10) = inf;  % flag truncated
end
if (length(obj.timeSeriesArrayHash.value{1}.trial) > 10)
    obj.timeSeriesArrayHash.value{1}.trial = obj.timeSeriesArrayHash.value{1}.trial(1:10);
    obj.timeSeriesArrayHash.value{1}.trial(10) = inf;  % flag truncated
end
if (length(obj.timeSeriesArrayHash.value{1}.valueMatrix) > 10)
    obj.timeSeriesArrayHash.value{1}.valueMatrix = obj.timeSeriesArrayHash.value{1}.valueMatrix(1:10,:);
    obj.timeSeriesArrayHash.value{1}.valueMatrix(10,:) = inf;  % flag truncated
end
numValues = length(obj.eventSeriesHash.value);
fprintf('num eventSeriesHash Values=%i\n', numValues);
for i = 1:numValues
    if (length(obj.eventSeriesHash.value{i}.channel) > 10)
        nuniq_channels=length(unique(obj.eventSeriesHash.value{i}.channel));
        if (nuniq_channels ~= 1)
            error('num unique channels in i=%i not 1, found %i\n', i, nuniq_channels);
        end
    end
    % Using ev will not allow changes to original object, it will only
    % change a copy of it
    % ev = obj.eventSeriesHash.value{i};
    % truncate('eventTimes');
    if (length(obj.eventSeriesHash.value{i}.eventTimes) > 10)
        fprintf('truncating eventTimes %i\n', i);
       obj.eventSeriesHash.value{i}.eventTimes = obj.eventSeriesHash.value{i}.eventTimes(1:10);
       obj.eventSeriesHash.value{i}.eventTimes(10) = inf;  % flag truncated
    end
    % truncate('eventTrials');
    if (length(obj.eventSeriesHash.value{i}.eventTrials) > 10)
       obj.eventSeriesHash.value{i}.eventTrials = obj.eventSeriesHash.value{i}.eventTrials(1:10);
       obj.eventSeriesHash.value{i}.eventTrials(10) = inf;  % flag truncated
    end
    % truncate('channel');
    if (length(obj.eventSeriesHash.value{i}.channel) > 10)
       obj.eventSeriesHash.value{i}.channel = obj.eventSeriesHash.value{i}.channel(1:10);
       obj.eventSeriesHash.value{i}.channel(10) = inf;  % flag truncated
    end
    % truncate waveforms
    if (length(obj.eventSeriesHash.value{i}.waveforms) > 10)
        obj.eventSeriesHash.value{i}.waveforms = obj.eventSeriesHash.value{i}.waveforms(1:2,:);
        obj.eventSeriesHash.value{i}.waveforms(2,1) = inf;  % flag truncated
    end
%{
contents to be cleared are
    eventTimes: [1253×1 double]
    eventTrials: [1253×1 double]
      waveforms: [1253×29 double]
        channel: [1253×1 double]
%}
    
end
fprintf('all done\n');
end

