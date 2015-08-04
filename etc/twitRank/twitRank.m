function [ val_matrix ] = twitRank( create_matrix, retweet_matrix, connection_matrix )
%TWITRANK Summary of this function goes here
%   Detailed explanation goes here
    change_matrix = connection_matrix;
    size_in = size(connection_matrix);
    size_in = size_in(1);
    % times in the creation values for each person
    for i = 1:size_in
        change_matrix(i,i) = change_matrix(i,i)*create_matrix(i);
    end
    
    % calculate total tweets for each person
    total_out_matrix = create_matrix + retweet_matrix;
    total_in_matrix = zeros(size_in);
    total_in_matrix = total_in_matrix(:,1);
    for i = 1:size_in
        for j = 1:size_in
            if j ~= i
                total_in_matrix(i) = total_in_matrix(i) + total_out_matrix(j)*connection_matrix(i,j);
            end
        end
    end
    % calculate retweet values for each person
    for i = 1:size_in
        for j = 1:size_in
            if j ~= i
                if (total_in_matrix(i) ~= 0)
                    change_matrix(i,j) = connection_matrix(i,j)*max(1,(retweet_matrix(i)/total_in_matrix(i)))*total_out_matrix(j);
                else
                    change_matrix(i,j) = 0;
                end
            end
        end
    end
    disp('change matrix');
    disp(change_matrix);
    val_matrix = ones(size_in,1);
    for i = 1:50
        val_matrix = change_matrix*val_matrix;
        val_matrix = val_matrix*(1/sum(val_matrix));
    end
    disp('create_matrix');
    disp(create_matrix);
    disp('retweet_matrix');
    disp(retweet_matrix);
    %disp('connection_matrix');
    %disp(connection_matrix);
    disp('val_matrix');
    disp(val_matrix);
end

