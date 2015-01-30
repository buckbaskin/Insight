connection = zeros(37,37);
for i = 1:37
    connection(i,i) = 1;
end

connection(1,13) = 1;
for i = 2:16
    connection(i,1) = 1;
end
connection(16,24) = 1;
connection(16,25) = 1;
connection(17,13) = 1;
connection(18,13) = 1;
connection(19,13) = 1;
connection(19,21) = 1;
connection(21,23) = 1;
connection(22,23) = 1;
connection(23,25) = 1;
connection(23,28) = 1;
connection(24,25) = 1;
connection(24,28) = 1;
connection(25,24) = 1;
connection(26,25) = 1;
connection(27,25) = 1;
connection(27,28) = 1;
connection(27,37) = 1;
connection(28,23) = 1;
connection(29,25) = 1;
connection(29,28) = 1;
connection(29,30) = 1;
connection(31,25) = 1;
connection(31,28) = 1;
connection(32,28) = 1;
connection(33,32) = 1;
connection(34,28) = 1;
connection(35,28) = 1;
connection(36,35) = 1;

create = magic(37);
create = create(:,18);

retweet = magic(37);
retweet = retweet(:,23);

value = twitRank(create, retweet, connection);