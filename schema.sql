CREATE TABLE IF NOT EXISTS finance_entry (
    id             SERIAL PRIMARY KEY,
    user_name      TEXT NOT NULL,
    entry_date     DATE NOT NULL,
    main_category  TEXT NOT NULL,
    sub_category   TEXT,
    description    TEXT,
    amount         NUMERIC(10, 2) NOT NULL,
    payment_method TEXT
);
