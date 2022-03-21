# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 16:56:07 2022

@author: MarioPC
"""

import pandas as pd


def clean_comment(comment, dummy_names):
    for name in dummy_names[-20:]:        
        if name in comment and name != "":
            comment = comment.replace(name+" ",'')
            comment = comment.replace(name+",",'')
            comment = comment.replace(name,'')
    return comment


df = pd.read_excel(open('F:/SocialLab/Vacunas/base de datos_vacunas.xlsx', 'rb'),sheet_name='Copia de Respuestas de formular') 
df = df[["comentarios","Fecha"]]

lines_list = list()
cleaned_lines = list() 
dummy_names = list()
comment_date = list()


n_comment_groups = len(df)


for i in range(n_comment_groups):
    comments = df['comentarios'][i].split("\n")    
    for linea in comments:
        if linea=="\n" or linea == " ":
            pass
        else:        
            if len(linea.split(" ")) <= 4:
                dummy_names.append(linea.replace("\n",''))
            else:
                comment = clean_comment(linea,dummy_names)
                cleaned_lines.append(comment)
                comment_date.append(df['Fecha'][i])
                

            lines_list.append(linea)

   

df_nlp =  pd.DataFrame({'date':comment_date,'comments':cleaned_lines})

df_nlp.to_csv('vaccine_comments.csv',index=False,encoding='utf-8')
