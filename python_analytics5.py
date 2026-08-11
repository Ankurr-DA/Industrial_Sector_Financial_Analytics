# -----------------------------------------------------------------------------
# LOAD SQL VIEWS INTO PANDAS DATAFRAMES
# -----------------------------------------------------------------------------
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

USER = 'root'
PASSWORD = 'ankur'  
HOST = 'localhost'
PORT = '3306'
DATABASE = 'sql_analytics5' 
 
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

#importing views from SQL
sql_query1 = 'select * from v_invoices;'
sql_query2 = 'select * from v_payments;'

df_invoices = pd.read_sql(sql_query1, con=engine)
df_payments = pd.read_sql(sql_query2, con=engine)

# Merged the DataFrames 
df_transaction = pd.merge(df_invoices,df_payments,on='invoice_id',how='left')

# Fixing invoice_amount
df_transaction['invoice_amount'] = df_transaction['invoice_amount'].str.replace('-', '').str.replace('₹', '').str.replace(',', '').str.strip()
df_transaction['invoice_amount'] = pd.to_numeric(df_transaction['invoice_amount'],errors='coerce')
df_transaction['invoice_amount'] = df_transaction['invoice_amount'].fillna(0)

# Fixing due_date
df_transaction['due_date'] = pd.to_datetime(df_transaction['due_date'],dayfirst=False,errors='coerce')

# Fixing client_segment
df_transaction['client_segment'] = df_transaction['client_segment'].fillna('Unassigned')
df_transaction['client_segment'] = df_transaction['client_segment'].str.replace('-',' ')
df_transaction['client_segment'] = df_transaction['client_segment'].str.strip().str.upper()

# Fixing industry
df_transaction['industry'] = df_transaction['industry'].fillna('Unknown')
df_transaction['industry'] = df_transaction['industry'].str.strip().str.upper()

# Fixing agreed_terms
a = {'net15':'Net-15','15 days':'Net-15',
     'net30':'Net-30','30 days':'Net-30',
     'net60':'Net-60','60 days':'Net-60'}
df_transaction['agreed_terms'] = df_transaction['agreed_terms'].fillna('Net-30') #Provided a baseline contract credit term
df_transaction['agreed_terms'] = df_transaction['agreed_terms'].str.strip().replace(a)
df_transaction['agreed_terms'] = df_transaction['agreed_terms'].str.upper()

# Fixing payment_date
df_transaction['payment_date'] = pd.to_datetime(df_transaction['payment_date'],dayfirst=False,errors='coerce')

# Fixing amount_paid
df_transaction['amount_paid'] = pd.to_numeric(df_transaction['amount_paid'],errors='coerce')
df_transaction['amount_paid'] = df_transaction['amount_paid'].abs()
df_transaction['amount_paid'] = df_transaction['amount_paid'].fillna(0)

# Fixing discount_applied
df_transaction['discount_applied'] = pd.to_numeric(df_transaction['discount_applied'],errors='coerce')
df_transaction['discount_applied'] = df_transaction['discount_applied'].abs()
df_transaction['discount_applied'] = df_transaction['discount_applied'].fillna(0)

# Creating conditions for Audit Status Column
today = pd.Timestamp.today().normalize()
conditions = [
    (df_transaction['invoice_amount'] == 0) | (df_transaction['due_date'].isnull()) |
    ((df_transaction['amount_paid'] > 0)&(df_transaction['payment_date'].isnull())) | 
    ((df_transaction['amount_paid'] == 0) & (df_transaction['due_date'] < today)),
    (df_transaction['amount_paid'] == 0) & (df_transaction['due_date'] >= today),
]
label = ['Incomplete', 'Pending']
df_transaction['Audit Status'] = np.select(conditions, label, default='Complete')

# Report 1 -----------------------------------------------------------------------------------------------
report1 = df_transaction.groupby(['industry','Audit Status']).agg(
    Invoice_Volume = ('invoice_id','count'),
    Billed_Value = ('invoice_amount','sum'),
    Collected_Revenue = ('amount_paid','sum'),
).reset_index()
report1['Outstanding Balance'] = report1['Billed_Value'] - report1['Collected_Revenue']
report1['Collection Rate'] = ((report1['Collected_Revenue']/report1['Billed_Value'])*100).round(2)
report1['Collection Rate'] = report1['Collection Rate'].map('{}%'.format)

report1.to_excel('Industry_Billing.xlsx',index=False)
print('Industry_Billing.xlsx Exported Successfully')
#---------------------------------------------------------------------------------------------------------

# Report 2 -----------------------------------------------------------------------------------------------
report2 = df_transaction.groupby(['client_segment', 'Audit Status']).agg(
    Invoices_Issued = ('invoice_id','count'),
    Billed_Exposure = ('invoice_amount','sum'),
    Cash_Recovered = ('amount_paid','sum')
).reset_index()
report2['Uncollected_Exposure'] = report2['Billed_Exposure'] - report2['Cash_Recovered']

report2.to_excel('Segment_Billing.xlsx',index=False)
print('Segment_Billing.xlsx Exported Successfully')
#---------------------------------------------------------------------------------------------------------
