# -*- coding: utf-8 -*-


import pandas as pd
import string
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default='browser'

df = pd.read_csv("vaccine_comments_sentiment_analysis.csv")
df2 = df.copy()
datetime_series = pd.to_datetime(df['date'])
df2=df.set_index(datetime_series)
datetime_index = pd.DatetimeIndex(datetime_series.values)
df2=df.set_index(datetime_series)

df2.drop(['date'],axis=1,inplace=True)
df2.sort_index()


vaccine_words = ["vacuna","vacunacion","vacunación","vacunados",
                 "vacunadas","vacunarse","vacunas","vacunado","vacunaron", 
                 "rechazo", "información", "desconfianza", "mentira", "muerte",
                 "experimento", "matar", "engaño","obligar","conspiración", 
                 "decisión", "libertad", "democracia","bakuna", "bakunas",
                 "vakuna", "dictadura", "sanitaria", "dosis", "inmunización", 
                 "inmunizar","ignorantes", "americana", "experimental", 
                 "inmune", "contagio", "responsabilidad", "estudios","bakunas"]



vaccine_list = ["vacuna","vacunacion","vacunación","vacunados",
                 "vacunadas","vacunarse","vacunas","vacunado","vacunaron", 
                 "bakuna", "bakunas",
                 "vakuna", "bakunas"]


stopwords = ['de', 'que', '', 'la', 'no', 'y', 'a', '·', 'el', 'los', 'en', 
             'es', 'se', 'por', 'las', 'para', 'con', 'lo', 'si', 
              'su', 'ya', 'del', 'como', 'q', 'al', 
             'pero', 'o', 'te', 'eso', 'esta','tu', 'ni','le', 'sus', 'este',
             'me', 'nos', 'está', 'esa','les','qué',
             'ese','todo','una','son',"un","más",'d','están', 'hay', 'solo', 
            'porque', 'ser', 'así', 'tiene', 'ahora',
            'tienen', 'mas', 'dicen', 'puede', 'verr', 'sin', 'esas', 'bien',
            'cuando', 'ellos', 'yo', 'hasta', 'hacer', 'sea', 'mi', 'van',
            'cada', 'añoss', 'donde', 'va', 'menos', 'pueden', 'igual', 'muy',
            'sobre', 'esto', 'entonces', 'primero', 'otros', 'tanto',
            'también', 'han', 'estos', 'pues', 'uno', 'estas', 'verz', 'aún',
            'tener', 'decir',  'favor', 'usted', 'fue', 'ha',
            'otra', 'mucho', '3', '2', 'tan', 'estar', 'haber', 'claro', 'dos',
            'otro', 'v', 'años', 'alguien', 'será', 'luego', 'da', 'e',
            'persona', 'gran', 'aquí', 'sean', 'fueron', 'esos', 'poco',
            'cómo', '1', 'desde', 'entre', 'pasa', 'puedes', 'caso', 'días',
            'dar', 'aun','hace']

related_words = list()
mask = list()

valid_index = 0
counter = 0
vacc_counter = 0
for comment in df2["comments"]:
    comment = comment.lower()
    comment = comment.translate(str.maketrans('', '', string.punctuation))

    comment =comment.replace('asi','así')
    comment =comment.replace('año','años')
    comment =comment.replace('coronavirus','covid19')
    comment =comment.replace('covid','covid19')
    comment =comment.replace('debe','deben')
    comment =comment.replace('debería','deben')
    comment =comment.replace('deberían','deben')
    comment =comment.replace('dice','dicen')
    comment =comment.replace('dijo','dicen')
    comment =comment.replace('estan','están')
    comment =comment.replace('boliviana','bolivianos')
    comment =comment.replace('boliviano' ,'bolivianos')
    comment =comment.replace('buena' ,'bueno')
    comment =comment.replace('chinos', 'china')
    comment =comment.replace('chinas', 'china')
    comment =comment.replace('ignorantes' ,'ignorancia')
    comment =comment.replace('ignorante' ,'ignorancia')
    comment =comment.replace('masista' ,'masistas')
    comment =comment.replace('pais','países')
    comment =comment.replace('país' ,'países')
    comment =comment.replace('paises' ,'países')
    comment =comment.replace('prueba' ,'pruebas')
    comment =comment.replace('ve' ,'ver')   
    comment =comment.replace('covid1919','covid19')
    comment =comment.replace('experimental','experimento')
    comment =comment.replace('experimentales','experimento')
    comment =comment.replace('gobiernos','gobierno')
    comment =comment.replace('bolivianoss' ,'bolivianos')
    comment =comment.replace('efectiva' ,'eficacia')
    comment =comment.replace('efectividad' ,'eficacia')
    comment =comment.replace('enfermedades' ,'enfermedad')
    comment =comment.replace('paíseses' ,'países')
    comment =comment.replace('paíseseses' ,'países')
    comment =comment.replace('poblacion' ,'población')
    comment =comment.replace('verrdad' ,'verdad') 
    if any(word in comment for word in vaccine_words):
        related_words.append(comment.split(" "))
        counter = counter +1
        mask.append(valid_index)
    else:
        pass
    valid_index=valid_index+1
    if any(word in comment for word in vaccine_list):        
        vacc_counter = vacc_counter +1
        
    
    # related_words.append(comment.split(" "))

related_words = [item for sublist in related_words for item in sublist]
related_words = [word for word in related_words if word not in stopwords]

related_words = [word for word in related_words if word not in vaccine_list]

from collections import Counter

# counts = Counter(related_words)
# counts = dict(Counter(related_words).most_common(100))

# import matplotlib.pyplot as plt

# from wordcloud import WordCloud

# from PIL import Image
# import numpy as np
# mask = np.array(Image.open("G:/SocialLab/Vacunas/dosis.png"))
# text = " ".join(word for word in counts.keys())
# word_cloud = WordCloud(collocations = False,mask=mask, background_color = 'grey',width=1600, height=800).generate(text)
# plt.imshow(word_cloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()
# # contour_color='#023075',contour_width=10,
# # ,width=1600, height=800
counts = dict(Counter(related_words).most_common(50))
plt.barh(list(counts.keys())[::-1], list(counts.values())[::-1])
plt.show()
df_vc = df2.iloc[mask]
df_vc.to_csv("FilteredVaccineComments.csv")
word_freq_df = pd.DataFrame(counts.values(),index=counts.keys())
# word_freq_df.to_csv("word_freq.csv",encoding='utf-8-sig')

new_words = [word.capitalize() for word in word_freq_df.index.values]
word_freq_df.index = new_words
word_per_df=100*word_freq_df/14279
word_per_df.columns=['Porcentaje[%]']

# import plotly.express as px

# fig = px.bar(word_per_df[:30][::-1], title="Cantidad de palabras en comentarios [%]",labels={"index":"","value":"Porcentaje"}, orientation='h')
# fig.show()

df3=df_vc[df_vc.columns[1:]].resample('1M', label='right', closed='right').mean()
df3 = df3.interpolate(method='polynomial', order=1)


df3 = df3*100

fig = go.Figure()
fig.add_trace(go.Scatter(x=df3.index, y=df3['NEG'],mode='lines',
                    name='Negativos'))
fig.add_trace(go.Scatter(x=df3.index, y=df3['anger'],mode='lines',
                    name='Enojo'))
fig.add_trace(go.Scatter(x=df3.index, y=df3['hateful'],mode='lines',
                    name='Odio'))
fig.update_layout(title='Probabilidad de Sentimientos/Emociones en comentarios',
                   xaxis_title='Fecha',
                   yaxis_title='%')