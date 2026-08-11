use sql_analytics5;

-- Checking for Missing Values in clients ----------------------------------------------------------------------
select 
sum(client_segment is null) as null_client_segment,
sum(industry is null) as null_industry,
sum(agreed_terms is null) as null_agreed_terms
from clients;

-- Checking for Missing Values in invoices ----------------------------------------------------------------------
select 
sum(invoice_amount is null) as null_invoice_amount,
sum(due_date is null) as null_due_date
from invoices;

-- Checking for Missing Values in payments ----------------------------------------------------------------------
select 
sum(payment_date is null) as null_payment_date,
sum(amount_paid is null) as null_amount_paid,
sum(discount_applied is null) as null_discount_applied
from payments;

--  Auditing Messy Columns for Python Transformations in clients
select distinct client_segment from clients;

select distinct industry from clients;

select distinct agreed_terms from clients;

--  Auditing Messy Columns for Python Transformations in invoices
select invoice_amount from invoices
where invoice_amount like '%₹%' or invoice_amount like '%Rs.%' 
or invoice_amount like '%,%' or invoice_amount < 0;

select due_date from invoices 
where due_date not like '____-__-__';

--  Auditing Messy Columns for Python Transformations in payments
select payment_date from payments 
where payment_date not like '____-__-__';

select amount_paid from payments
where amount_paid like '%₹%' or amount_paid like '%Rs.%' 
or amount_paid like '%,%' or amount_paid < 0;

select discount_applied from payments
where discount_applied like '%₹%' or discount_applied like '%Rs.%' 
or discount_applied like '%,%' or discount_applied < 0;

-- Identify Dublicate Rows (Primary Keys with more then 1 appearence)
select client_id, count(*) as Dublicate_Count from clients 
group by client_id
having count(*) > 1;

select invoice_id, count(*) as Dublicate_Count from invoices 
group by invoice_id
having count(*) > 1;

select payment_id, count(*) as Dublicate_Count from payments 
group by payment_id
having count(*) > 1;

-- Excluding duplicate records -----------------------------
create table clients_clean as 
select * from (select *, row_number() over(partition by client_id) as R from clients) x
where R = 1;

create table invoices_clean as 
select * from (select *, row_number() over(partition by invoice_id) as R from invoices) x
where R = 1;

create table payments_clean as 
select * from (select *, row_number() over(partition by payment_id) as R from payments) x
where R = 1;


-- Orphan Invoices -----------------------------
select i.* from invoices i 
left join clients c on i.client_id = c.client_id
where c.client_id is null;

-- Orphan Payments -----------------------------
select p.* from payments p 
left join invoices i on p.invoice_id = i.invoice_id 
where i.invoice_id is null;

-- View 1 (Excluding Orphan Invoices)------------------------------------------------
create view v_invoices as
select 
    i.invoice_id,
    i.client_id,
    i.invoice_amount,
    i.due_date,
    c.client_segment,
    c.industry,
    c.agreed_terms
from invoices_clean i
inner join clients_clean c on i.client_id = c.client_id;

-- View 2 (Excluding Orphan Payments) -----------------------------
create view v_payments as
select 
    p.payment_id,
    p.invoice_id,
    p.payment_date,
    p.amount_paid,
    p.discount_applied
from payments_clean p
inner join invoices_clean i on p.invoice_id = i.invoice_id;

