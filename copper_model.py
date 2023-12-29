# importing the required packages
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

# Function to load the regression model
def load_regressor():
    with open("C:\\Users\\hp\\copper_regressor_pkl",'rb') as files:
        reg_model=pickle.load(files)
    return(reg_model)

# Function to load the classifier model
def load_classifier():
    with open("C:\\Users\\hp\\copper_classifier_pkl",'rb') as files:
        class_model=pickle.load(files)
    return(class_model)

# Funtion to predict the values
def prediction_model(model,a,b,c,d,e,f,g,h,i):
        pred=model.predict([[a,b,c,d,e,f,g,h,i]])
        return pred

# streamlit page set up
st.set_page_config(page_title='Copper modelling',
                   page_icon=':bar_chart:',
                   layout='wide')
st.header('INDUSTRIAL COPPER MODELLING')

# Dictionaries and list for selectbox
df = pd.read_csv(r"C:\\Users\\hp\\Downloads\\copperdf.csv")
status_dict = dict(zip(df['status'].unique(), df['status_code'].unique()))
status_list=df['status'].unique()
country_list=df['country'].unique()
type_dict=dict(zip(df['item type'].unique(),df['type_code'].unique()))
type_list=df['item type'].unique()
application_list=df['application'].unique()
product_list=df['product_ref'].unique()

tab1,tab2=st.tabs(["SELLING PRICE PREDICTION","STATUS PREDICTION"])
with tab1:
    # Selling price prediction model
    with st.expander('Enter features for selling price prediction'):
        quantity_reg = st.number_input('QUANTITY OF THE ORDER',value=1,placeholder='Enter quantity in ton')
        if quantity_reg is not None:
            if not quantity_reg<=0:
                quantity_id=np.log(int(quantity_reg))
            else:
                st.error("Quantity can't be negative or 0")
        else:
            st.error("Quantity cant't be empty")

        customer_reg = st.text_input('CUSTOMER ID FOR PURCHASE',value=None,placeholder='Enter customer id (Ex:30156308)')
        if customer_reg is not None:
            if len(customer_reg) !=8 or not customer_reg.isdigit():
                st.error('Customer id should be 8 digit number')
            else:
                customer_id=int(customer_reg)

        country_reg = int(st.selectbox('COUNTRY OF PURCHASE',options=country_list,placeholder='Enter country code'))

        status_key_reg = st.radio('STATUS OF TRANSACTION',options=status_list,horizontal=True)

        type_key_reg = st.selectbox('ITEM_TYPE',options=type_list,placeholder='Select item type')

        application_reg = st.selectbox('APPLICATION OF THE PRODUCT',options=application_list)

        thickness_reg = np.log(st.number_input('THICKNESS OF THE MATERIAL',value=0.18))
        
        width_reg = st.number_input('WIDTH OF THE MATERIAL',value=1)
        if width_reg is not None and width_reg <=0:
            st.error('Width should not be lessthan 0')
        else:
            pass

        product_reg = st.selectbox('PRODUCT REF NUMBER',options=product_list)


    if st.button('Predict the selling price'):
        with st.spinner('Predicting'):
            time.sleep(3)
            status_reg=status_dict[status_key_reg]
            item_type_reg=type_dict[type_key_reg]
            try:
                regress_value=np.exp(prediction_model(load_regressor(),quantity_id,customer_id,country_reg,status_reg,item_type_reg,application_reg,thickness_reg,width_reg,product_reg))
                st.balloons()
                st.success(f'Predicted Price: {regress_value[0]:,.2f}')
            except:
                st.error('Invalid feature')

with tab2:
    # Model for predicting status
    status_pred_dict={1:'WON',2:'LOST'}
    with st.expander('Enter features for status prediction'):
        quantity_cls = st.number_input('QUANTITY',value=1,placeholder='Enter quantity in ton')
        if quantity_cls is not None:
            if not quantity_cls<=0:
                quantity_id_cls=np.log(int(quantity_cls))
            else:
                st.error("Quantity can't be negative or 0")
        else:
            st.error("Quantity cant't be empty")

        customer_cls = st.text_input('CUSTOMER ID',value=None,placeholder='Enter customer id (Ex:30156308)')
        if customer_cls is not None:
            if len(customer_cls) !=8 or not customer_cls.isdigit():
                st.error('Customer id should be 8 digit number')
            else:
                customer_id_cls=int(customer_cls)

        country_cls = int(st.selectbox('COUNTRY',options=country_list,placeholder='Enter country code'))

        type_key_cls = st.selectbox('ITEM TYPE',options=type_list,placeholder='Select item type')

        application_cls = st.selectbox('APPLICATION',options=application_list)

        thickness_cls = np.log(st.number_input('THICKNESS',value=0.18))
        
        width_cls = st.number_input('WIDTH',value=1)
        if width_cls is not None and width_cls <=0:
            st.error('Width should not be lessthan 0')
        else:
            pass

        product_cls = st.selectbox('PRODUCT REF',options=product_list)

        selling_price_clss=st.number_input('SELLING PRICE',placeholder='Enter the selling price')
    
    if st.button('Predict the satus'):
        with st.spinner('Predicting'):
            time.sleep(3)
            item_type_cls=type_dict[type_key_cls]
            try:
                class_value=prediction_model(load_classifier(),quantity_id_cls,customer_id_cls,country_cls,item_type_cls,application_cls,thickness_cls,width_cls,product_cls,selling_price_clss)
                key = int(class_value[0])
                pred_status=status_pred_dict[key]
                st.balloons()
                st.success(pred_status)
            except:
                st.error('Invalid feature')
        
    






