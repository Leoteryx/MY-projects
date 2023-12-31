# -*- coding: utf-8 -*-
"""BizCardX: Extracting Business Card Data with OCR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bBLgnKMvDj6255561koR6q4_IiBqA7st
"""

!pip install streamlit
!pip install easyOCR

!pip install opencv-python
!pip install pillow

!pip install db-sqlite3
!pip install pyngrok --upgrade

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# from PIL import Image
# import sqlite3
# import io
# from easyocr import Reader
# import cv2
# import numpy as np
# import pandas as pd
# 
# def create_connection():
#     conn = sqlite3.connect("bizcardX.db")
#     return conn
# 
# def create_table(conn):
#     query = """
#     CREATE TABLE IF NOT EXISTS business_cards (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         phone INTEGER,
#         email TEXT NOT NULL,
#         company TEXT NOT NULL,
#         image BLOB NOT NULL
#     )
#     """
#     conn.execute(query)
# 
# def insert_data(conn, name, phone, email, company, image):
#     query = "INSERT INTO business_cards (name, phone, email, company, image) VALUES (?, ?, ?, ?, ?)"
#     conn.execute(query, (name, phone, email, company, image))
#     conn.commit()
# 
# def get_data(conn):
#     query = "SELECT * FROM business_cards"
#     cursor = conn.execute(query)
#     return cursor.fetchall()
# 
# # Main Streamlit app
# def main():
#     st.title("Business Card OCR App")
#     st.write("Upload a business card image and extract its information.")
# 
#     uploaded_file = st.file_uploader("Upload a business card image", type=["jpg", "jpeg", "png"])
# 
#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Uploaded Image", use_column_width=True)
# 
#         # Perform image processing (if necessary)
#         image = image.resize((400, 250))
#         image_array = np.array(image)
#         gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
#         _, threshold_img = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
# 
#         # Perform OCR using easyOCR
#         reader = Reader(['en'])
#         result = reader.readtext(threshold_img)
# 
#         # Extract information from OCR results (assuming the structure of the result is consistent)
#         name = ""
#         phone = ""
#         email = ""
#         company = ""
# 
#         if len(result) >= 1:
#             name = result[0][1]
# 
#         if len(result) >= 2:
#             phone = result[1][1]
# 
#         if len(result) >= 3:
#             email = result[2][1]
# 
#         if len(result) >= 4:
#             company = result[3][1]
# 
#         st.write("Extracted Information:")
#         st.write(f"Name: {name}")
#         st.write(f"Phone: {phone}")
#         st.write(f"Email: {email}")
#         st.write(f"Company: {company}")
# 
#         # Convert the image to bytes to store in the database
#         img_bytes = io.BytesIO()
#         image.save(img_bytes, format="PNG")
# 
#         # Save the extracted information and the image to the database
#         conn = create_connection()
#         create_table(conn)
#         insert_data(conn, name, phone, email, company, img_bytes.getvalue())
#         conn.close()
# 
#  # Display the database table with the stored information
#     st.subheader("Stored Business Cards")
#     conn = create_connection()
#     create_table(conn)
#     data = get_data(conn)
# 
#     # Create a Streamlit table to display the data
#     table_columns = ["ID", "Name", "Phone", "Email", "Company"]
#     rows = [[row[0], row[1], row[2], row[3], row[4]] for row in data]
#     st.table(pd.DataFrame(rows, columns=table_columns))
# 
#     # Allow the user to edit and update the information
#     selected_id = st.number_input("Enter the ID of the business card to edit", min_value=0, value=0, step=1)
#     edit_name = st.text_input("Edit Name:", "")
#     edit_phone = st.text_input("Edit Phone:", "")
#     edit_email = st.text_input("Edit Email:", "")
#     edit_company = st.text_input("Edit Company:", "")
# 
#     if st.button("Update"):
#         # Update the information in the database
#         conn = create_connection()
#         update_query = "UPDATE business_cards SET name=?, phone=?, email=?, company=? WHERE id=?"
#         conn.execute(update_query, (edit_name, edit_phone, edit_email, edit_company, selected_id))
#         conn.commit()
#         conn.close()
#         st.success("Business card information successfully updated!")
#         # Display a success message to the user
#         st.success("Business card information successfully extracted and saved!")
# 
# # Run the Streamlit app
# if __name__ == "__main__":
#     main()

from google.colab import drive
drive.mount('/content/drive')

!ls

!ngrok authtoken 2RSYaDxS4EWqbhfXoNjf1Q5yIUD_6d7nZvZSWupeccbx47GKM

!ngrok

from pyngrok import ngrok

#!nohub streamlit run app.py
!streamlit run app.py&>/dev/null&

!pgrep streamlit

publ_url =ngrok.connect(8501)

publ_url