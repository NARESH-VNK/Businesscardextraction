import easyocr as easyocr
import re
import pandas as pd
import psycopg2 as psycopg2
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine
import streamlit as st
from PIL import Image


# create a PostgreSQL connection
conn = psycopg2.connect(
    host='localhost',
    user="postgres",
    password="naresh",
    port=5432,
    database="businesscard"
)
nk = conn.cursor()

# creating connection btwn psycopg2 and postgressql to insert a dataframe
engine = create_engine('postgresql+psycopg2://postgres:naresh@localhost/businesscard')

def biz(img):

    final = {'Name': [], 'Designation': [],  'EmailID': [], 'Website': [], 'Pincodes': [], 'Mobile_Number': []}
    reader = easyocr.Reader(['en'])
    results = reader.readtext(img)
    data = []
    final['Name'].append(results[0][1])
    final['Designation'].append(results[1][1])

    for i in range(2, len(results)):
      data.append(results[i][1])
    m = []
    for j in data:
      if j in (re.findall(r'[+]?\d+\W+\d+\W+\d+', j)):
        m.append(re.findall(r'[+]?\d+\W+\d+\W+\d+', j))

      if j in (re.findall(r'www.+[a-zA-z][^.]+\.com', j, re.IGNORECASE) or re.findall(r'www.+[a-zA-z]', j,re.IGNORECASE) or re.findall(r'[^.@]+\.com', j, re.IGNORECASE)):
        final['Website'].append((re.findall(r'www.+[a-zA-z][^.]+\.com', j, re.IGNORECASE) or re.findall(r'www.+[a-zA-z]', j,re.IGNORECASE) or re.findall(r'[^.@]+\.com', j, re.IGNORECASE))[0])

      if j in (re.findall(r'\b\w+@\w+\.com\b', j, re.IGNORECASE)):
        final['EmailID'].append(re.findall(r'\b\w+@\w+\.com\b', j, re.IGNORECASE)[0])

      a = re.findall(r'[0-9]{6}', j)
      if len(a) == 1:
        final['Pincodes'].append(a[0])
    final['Mobile_Number'].append(m[0][0])
    final['Pincodes'] = pd.to_numeric(final['Pincodes'][0])
    df = pd.DataFrame(final)
    return (df)



content = ['About','WorkFlow',"Image and Data","Outcomes"]
with st.sidebar:
       opt = st.sidebar.selectbox('MENU',content)

if opt == 'About':
    st.title("EXTRACTION OF BUSINESS CARD DETAILS")
    st.subheader("INTRODUCTION")
    st.write("- The extraction of business cards using EasyOCR is a feature that allows you to scan and extract information from business cards using optical character recognition (OCR) technology.")
    st.write("- EasyOCR is a Python library that provides a simple interface for performing OCR tasks, including text recognition from images.EasyOCR supports multiple languages and can accurately extract information from various types of business cards, including those with different fonts, layouts, and colors.")
    st.write("- Traditionally, when you receive a business card, you would manually enter the information into a digital format such as a contact management system or a spreadsheet. ")
    st.write("- However, this manual process can be time-consuming and prone to errors.By leveraging EasyOCR for business card extraction, you can automate this process and save valuable time.")
    st.write("- The library works by taking an image of a business card as input and then using advanced algorithms to recognize and extract the text from the image.")
    st.subheader("AIM")
    st.write("- To develop  a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR.")
    st.subheader("NEEDS OF THIS PROJECT")
    st.write("- The process of capturing and Storing business card information digitally makes it easily accessible and searchable,thus reducing the chances of losing or misplacing important contact details.")
    st.write("- This saves time and effort by eliminating the need for manual data entry.")
    st.write("- Extracted business card data can be further processed and analyzed for generating insights.")

    st.subheader("[Sample Dataset Link](https://drive.google.com/drive/folders/1FhLOdeeQ4Bfz48JAfHrU_VXvNTRgajhp)")

if opt == 'Image and Data':
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            expander = st.expander(uploaded_file.name)
            expander.image(image, caption='Uploaded Business Card Image')

        else:
            st.write("#### Upload the Business card")


        if st.button('Click to insert Data'):
            st.write("### Extraction Process is Initiated...")
            output = biz(img=uploaded_file.name)
            st.write('#### Extracted Data from Above Business Card...')
            output.to_sql('bizcard', engine, if_exists='replace', index=False)
            st.dataframe(output)



        if st.button("Click to Download Data") :
            query = ("select * from bizcard")
            nk.execute(query)
            x = nk.fetchall()
            fetch = pd.DataFrame(x, columns=['Name', 'Designation', 'Emailid', 'Website', 'Pincodes', 'Mobile_number'])


            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')
            csv = convert_df(df=fetch)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='Bizcard.csv',
                mime='csv')


    with col2:
        if st.button("Click To Store In Database"):
            db = biz(img=uploaded_file.name)
            db.to_sql('bizcardstore', engine, if_exists='append', index=False)
            st.write("### Data is stored ")

            query = ("SELECT DISTINCT * FROM bizcardstore")
            nk.execute(query)
            x = nk.fetchall()
            fetch = pd.DataFrame(x, columns=['Name', 'Designation', 'Emailid', 'Website', 'Pincodes', 'Mobile_number'])
            st.write("### List of Data stored in Database So far")
            container = st.container()
            container.write(fetch)

        st.write("### To delete data in database")
        tab1,tab2 = st.tabs(['CHOOSE TO DELETE',"OUTPUT DATA"])
        with tab1:
            query = ('select distinct "Name" from bizcardstore')
            nk.execute(query)
            x = nk.fetchall()
            fetch = pd.DataFrame(x,columns=["Name"])


            options = st.radio('Choose A Name To Delete From DataBase',fetch)

            if st.button("DELETE"):
                def delete(opt):
                    query = 'DELETE FROM  bizcardstore where  "Name" =\'{choice}\''.format(choice=opt)
                    nk.execute(query)
                    conn.commit()
                    query = ("SELECT DISTINCT * FROM bizcardstore")
                    nk.execute(query)
                    x = nk.fetchall()
                    fetch = pd.DataFrame(x, columns=['Name', 'Designation', 'Emailid', 'Website', 'Pincodes', 'Mobile_number'])
                    st.write("### Data After Deletion")
                    st.write(fetch)


                delete(opt=options)


            with tab2:
                query = ("SELECT DISTINCT * FROM bizcardstore")
                nk.execute(query)
                x = nk.fetchall()
                fetch = pd.DataFrame(x, columns=['Name', 'Designation', 'Emailid', 'Website', 'Pincodes', 'Mobile_number'])
                st.write("### Total No Of  Data Stored In Database")
                st.write(fetch)


                def convert_df(df):
                    return df.to_csv().encode('utf-8')


                csv = convert_df(df=fetch)

                st.download_button(
                    label="Download All data as CSV",
                    data=csv,
                    file_name='TotalBizcards.csv',
                    mime='csv')


if opt == 'WorkFlow':
    st.title("Process Flow")
    st.subheader("Step 1 - Packages Needed")
    st.write("- Install the required packages like esayOCR,re,Psycopg2,PIL, Pandas,Sqlalchemy and Streamlit in python.")
    st.write("- I preferred PostgreSQl DataBase for storing the extracted information.")
    st.subheader("Step 2 - Data Extraction ")
    st.write("- Using easyOCR extract the required information by passing the business card image as input.")
    st.write("- The extracted information should include the  card holder name, designation, mobile number, email address, website URL, address and pin code.")
    st.subheader("Step 3 - Data Processing")

    st.write("- After extracting the text using EasyOCR, we can implement post - processing steps to refine and validate the extracted information. ")
    st.write("- This can involve removing any unnecessary characters, formatting  inconsistencies from the extracted text with the help of re package in python.")

    st.subheader("Step 4 - Data Migration")
    st.write("- Convert the data into dataframe using pandas library which would  in suitable format for data migraion.")
    st.write("- With the help of SQLALCHEMY package ,import the dataframe in sql database.")
    st.subheader("Step 5 - Retrieval Data from SQl")
    st.write("- The psycopg2 library make connection between python and SQL that will be useful for quering required data from python.")
    st.write("- Make our query to  select the records in database and we can do operitations like add/delete and update a particular record ")
    st.write("- We can use SQL queries to create tables, insert data,and retrieve data from the database,")
    st.subheader("Step 6 - Streamlit Deploy")
    st.markdown("- Streamlit deploy our extracted code into Graphical Interface. we can use widgets like tables, text boxes, and labels to present the information.")
    st.write("- Streamlit applictaion should be  carefully design and plan the application structure to ensure that it is scalable, maintainable, and extensible.")


if opt == 'Outcomes':
    # st.header("APPLICATIONS OF THIS PROJECT")
    st.header("Usage Of Business Card Extraction")
    st.write("#### 1.Contact Information")
    st.write("- Business cards typically contain contact details such as names, phone numbers, email addresses, and company information. ")
    st.write("- By using EasyOCR to extract this information, you can automate the process of capturing and storing contact details in a digital format.")
    st.write("#### 2.Customer Relationship Management")
    st.markdown("- In a customer relationship management (CRM) system, the extracted information from business cards can be directly integrated into your CRM database.")
    st.markdown("- This saves time and effort by eliminating the need for manual data entry.However, this manual process can be time - consuming and prone to errors.")

    st.write("#### 3.Networking Efficiency")
    st.markdown("- When attending conferences, meetings, or networking events, you may receive numerous business cards.")
    st.markdown("- By leveraging EasyOCR, you can quickly extract the relevant information and store it digitally, reducing the chances of losing or misplacing important contact details.")


    st.write("#### 4.Data Analysis and Insights")
    st.markdown("- We can analyze the frequency of contact details, identify trends, or perform data-driven decision making based on the extracted information.")


    st.write("#### 5.Accessibility and Searchability")
    st.write("-  Storing business card information digitally makes it easily accessible and searchable. You can use keywords or filters to find specific contacts or perform quick searches within the extracted data.")


    st.write("#### 6.Automation and Integration")
    st.write("- We can build custom automation scripts to automatically extract business card information and perform specific actions based on the extracted data.")

    st.write("### Overall, the result of the project would be a helpful tool for businesses and individuals who need for management, improve data organization, and enhances the networking efficiency to manage business card information efficiently.")
