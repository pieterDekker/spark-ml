-- Create the dataset table
CREATE KEYSPACE IF NOT EXISTS transactions WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS transactions.transactions_dataset (
    id INT PRIMARY KEY,
    date TIMESTAMP,
    step INT,
    customer TEXT,
    age TEXT,
    gender TEXT,
    zipcodeOri TEXT,
    merchant TEXT,
    zipMerchant TEXT,
    category TEXT,
    amount FLOAT,
    fraud boolean
);

CREATE TABLE IF NOT EXISTS transactions.limit20 (
    id INT PRIMARY KEY,
    date TIMESTAMP,
    step INT,
    customer TEXT,
    age TEXT,
    gender TEXT,
    zipcodeOri TEXT,
    merchant TEXT,
    zipMerchant TEXT,
    category TEXT,
    amount FLOAT,
    fraud boolean
);

 COPY transactions.transactions_dataset (id,date,step,customer,age,gender,zipcodeOri,merchant,zipMerchant,category,amount,fraud) from '/data/transactions-dataset.csv' WITH HEADER=true AND MAXINSERTERRORS=-1;
 COPY transactions.limit20 (id,date,step,customer,age,gender,zipcodeOri,merchant,zipMerchant,category,amount,fraud) from '/data/limit20.csv' WITH HEADER=true AND MAXINSERTERRORS=-1;
