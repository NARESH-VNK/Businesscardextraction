
# Extracting Business Card Data with OCR
## Description
- The extraction of business cards using EasyOCR is a feature that allows you to scan and extract information from business cards using optical character recognition (OCR) technology.

- EasyOCR is a Python library that provides a simple interface for performing OCR tasks, including text recognition from images

+ The library works by taking an image of a business card as input and then using advanced algorithms to recognize and extract the text from the image.
## Aim

- To develop a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR.
- The extracted information should include the  card holder name, designation, mobile number, email address, website URL, address and pin code.
## Needs For Bizcard Extraction

Some common Usecases and benefits of Bizcard Extraction:
1. Contact Information :
- Automate the process of capturing and storing contact details in a digital format.

2. Customer Relationship Manager Integration:
-  The extracted information from business cards can be directly integrated into your CRM database. This saves time and effort by eliminating the need for manual data entry.

3. Networking Efficiency:
- Quickly extract the relevant information and store it digitally, reducing the chances of losing important contact details.

4. Data Analysis and Insights: 
- Extracted business card data can be further processed and analyzed for generating insights. 

5. Accessibility and Searchability:
-  Storing business card information digitally makes it easily accessible and searchable. You can use keywords or filters to find specific contacts or perform quick searches within the extracted data.

6. Automation and Integration: 
- Buliding automation scripts to automatically extract business card information and perform specific actions based on the extracted data.


## Installation

Install required libraries.

```bash
import easyocr as easyocr
import re
import pandas as pd
import psycopg2 as psycopg2
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine
import streamlit as st
from PIL import Image
```

Install streamlit application run 

```bash
  streamlit run bizcardx.py
```
    
## Demo
A sample video from youtube how extraction process works.

https://www.youtube.com/watch?v=ULjnz2W4t8c


## Process Flow
### 1. Packages Needed
- Install the required packages like esayOCR,re,Psycopg2,PIL, Pandas,Sqlalchemy and Streamlit in python.

- I preferred PostgreSQl DataBase for storing the extracted information.
### 2. Data Extraction
- Using easyOCR extract the required information by passing the business card image as input.
- The extracted information should include the card holder name, designation, mobile number, email address, website URL, address and pin code.
###  3. Data Processing
- After extracting the text using EasyOCR, we can implement post - processing steps to refine and validate the extracted information.

- This can involve removing any unnecessary characters, formatting inconsistencies from the extracted text with the help of re package in python.

###  4. Data Migration
- Convert the data into dataframe using pandas library which would in suitable format for data migraion.

- With the help of SQLALCHEMY package ,import the dataframe in sql database.
###  5. Retrieval Data from SQl
- The psycopg2 library make connection between python and SQL that will be useful for quering required data from python.
- Make our query to select the records in database and we can do operitations like add/delete and update a particular record

- We can use SQL queries to create tables, insert data,and retrieve data from the database,
### 6. Streamlit Deployment
- Streamlit deploy our extracted code into Graphical Interface. we can use widgets like tables, text boxes, and labels to present the information.
- Streamlit applictaion should be carefully design and plan the application structure to ensure that it is scalable, maintainable, and extensible.
- Display the data in a clean and organized manner in the Streamlit GUI.
## Lessons Learned

- The key take aways from this project is about Image processing and extraction of all the data using EasyOCR.

- Quering,Updating and Deleting the extrated data from python. 

- Presenting the data in structural format Streamlit App.

## Sample Dataset Link

#### https://drive.google.com/drive/folders/1FhLOdeeQ4Bfz48JAfHrU_VXvNTRgajhp
## Tools And Packages

1. Python(Libraries) - Pandas,re,psycopg2,EasyOCR,sqlalchemy,Streamlit.
2. Database - PostgreSQL 
## Outcomes

- Overall, the result of the project would be a helpful tool for businesses and individuals who need for management, improve data organization, and enhances the networking efficiency to manage business card information efficiently.