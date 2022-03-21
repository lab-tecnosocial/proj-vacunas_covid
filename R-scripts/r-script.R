library(tidyverse)
library(stringr)
library(stringi)
library(tidytext)
library(stopwords)
library(magrittr)
library(widyr)
library(igraph)
library(ggraph)

# LIMPIEZA DE DATASET
## cargamos los comentarios
comentarios_todo <- read_csv("data/FilteredVaccineComments.csv") %>%
  select(date, comments) %>%
  rename(text = comments) %>%
  mutate(id = row_number())

## acentos y comas
comentarios_todo$text <- stri_trans_general(comentarios_todo$text, "Latin-ASCII")

## separamos cada comentario en palabras sueltas y filtramos palabras vacias
stopwords_es <- tibble(stopwords("spanish")) %>%
  rename(word = `stopwords("spanish")`)

custom_es <- tibble(word = c("si",
                             "mas",
                             "q",
                             "estan",
                             "solo",
                             "ser",
                             "asi",
                             "quieren",
                             "ver",
                             "cada",
                             "van",
                             "aun",
                             "va",
                             "debe",
                             "anos",
                             "tambien",
                             "19",
                             "sera",
                             "igual",
                             "gracias",
                             "todas",
                             "todos",
                             "dias",
                             "pues",
                             "decir",
                             "tan",
                             "vez",
                             "vea"))

stopwords_es <- bind_rows(stopwords_es, custom_es)

coments_vaccine <- comentarios_todo %>%
  unnest_tokens(word, text) %>%
  filter(!word %in% stopwords_es$word)

# stemming
coments_vaccine$word <- str_replace_all(coments_vaccine$word,  c("experimento" = "experimental",
                                                                 "experimentales" = "experimental",
                                                                 "experimentos" = "experimental",
                                                                 "experimentacion" = "experimental",
                                                                 "experimentar" = "experimental",
                                                                 "experimentando" = "experimental"))

coments_vaccine$word <- str_replace_all(coments_vaccine$word,  c("matarnos" = "muerte",
                                                                 "mataron" = "muerte",
                                                                 "matar" = "muerte"))

save(coments_vaccine, file = "outputs/coments_vaccine.RData")

# VISUALIZACIONES
## Histograma palabras
load("outputs/coments_vaccine.RData")

frec_vac <- coments_vaccine %>%
  count(word) %>%
  arrange(desc(n)) %>%
  mutate(id = row_number())

frec_30 <- frec_vac %>%
  filter(!word %in% c("vacunas",
                      "vacuna",
                      "vacunar",
                      "personas",
                      "ahora",
                      "vacunados",
                      "puede",
                      "bien",
                      "poblacion",
                      "vacunacion",
                      "dice",
                      "quiere",
                      "paises",
                      "segunda",
                      "hacer",
                      "pais",
                      "despues",
                      "mejor",
                      "mundo",
                      "menos",
                      "millones",
                      "nadie",
                      "hace",
                      "pueden",
                      "primera",
                      "sabe",
                      "entonces",
                      "3",
                      "primero",
                      "meses",
                      "peor",
                      "2",
                      "tiempo",
                      "rusa",
                      "bolivianos",
                      "favor",
                      "vacunado",
                      "dos",
                      "ademas",
                      "falta",
                      "aqui",
                      "dicen",
                      "tener",
                      "presidente",
                      "v",
                      "usted",
                      "toda",
                      "mal",
                      "creo",
                      "bueno",
                      "1",
                      "vacunaron",
                      "luego",
                      "recibir",
                      "deben",
                      "claro",
                      "vacunarse",
                      "seguro",
                      "deberian",
                      "persona",
                      "haber",
                      "mismo",
                      "da",
                      "hacen",
                      "culpa",
                      "compra",
                      "comprar",
                      "alguien",
                      "cualquier",
                      "ano",
                      "seria",
                      "dia",
                      "argentina",
                      "mientras",
                      "vacunen",
                      "nadie",
                      "sirve",
                      "nunca")) %>%
  head(n=30)


frec_30 %>%
  ggplot(aes(x = fct_reorder(word, n), y = n)) +
  geom_col() +
  coord_flip() +
  theme_minimal()

ggsave("figs/histograma.png")

## Redes de correlaciones de palabras
### encontramos los id de los comentarios con las palabras que nos interesa analizar
id_vacuna <- coments_vaccine %>%
  filter(word %in% c("vacuna", 
                     "vacunas",
                     "vacunacion",
                     "bakuna",
                     "bakunas",
                     "vakuna",
                     "vakunas"))  %>%
  select(id)

### filtramos solo los comentarios con las palabras clave y los correlacionamos
correlaciones <- coments_vaccine %>%
  filter(id %in% id_vacuna$id)

### utilizamos pairwise_cor() para observar correlaciones
correlaciones <- correlaciones %>%
  pairwise_cor(word, id, sort = T) %>%
  filter(item1 %in% c("vacuna", 
                      "vacunas",
                      "vacunacion",
                      "bakuna",
                      "bakunas",
                      "vakuna",
                      "vakunas"))

save(correlaciones, file = "outputs/correlaciones_todo.RData")

### red de correlaciones sobre "vacuna"
red_vacuna <- correlaciones %>%
  filter(!item2 %in% c("partir",
                       "relaciones",
                       "exteriores",
                       "22.04.2021")) %>%
  filter(item1 %in% c("vacuna", "vacunas", "vacunacion")) %>%
  mutate(correlation = round(correlation, 2)) %>%
  head(n=10)

red_vacuna$item1 <- str_replace_all(red_vacuna$item1, c("vacunas" = "vacuna", #stemming
                                                        "vacunacion" = "vacuna"))
write.csv(red_vacuna, "outputs/red_vacuna.csv")

# grafo
red_vacuna %>%
  head(n = 10) %>%
  graph_from_data_frame() %>%
  ggraph(layout = "fr") +
  geom_edge_link(aes(edge_alpha = correlation), show.legend = FALSE) +
  geom_node_point(color = "lightblue", size = 5) +
  geom_node_text(aes(label = name), repel = TRUE) +
  theme_void()

ggsave("figs/vacunas.png")

### red de correlaciones sobre "bakuna"
red_bakuna <- correlaciones %>%
  filter(!item2 %in% c("emita",
                       "veras",
                       "lanzar",
                       "adquirieron",
                       "almeria",
                       "campra",
                       "viales",
                       "sustancia",
                       "pocos",
                       "sabes",
                       "pide",
                       "siguieron",
                       "exactos",
                       "distinto",
                       "importantes",
                       "universidad",
                       "firmo",
                       "observa",
                       "actua",
                       "sabias",
                       "ultimo",
                       "regala",
                       "totalmente",
                       "dr",
                       "adquirir",
                       "sino",
                       "hicieron",
                       "buenas",
                       "quedan",
                       "porcentaje",
                       "ejemplo",
                       "sabias",
                       "4",
                       "traigan",
                       "chile",
                       "culpa",
                       "luego",
                       "toda",
                       "argentina",
                       "escribo",
                       "quedaron")) %>%
  filter(item1 %in% c("bakuna", "bakunas", "vakuna", "vakunas")) %>%
  mutate(correlation = round(correlation, 2)) %>%
  head(n=10)

red_bakuna$item1 <- str_replace_all(red_bakuna$item1, c("bakunas" = "bakuna", #stemming
                                                        "vakuna" = "bakuna",
                                                        "vakunas" = "bakuna"))
write.csv(red_bakuna, "outputs/red_bakuna.csv")

red_bakuna %>%
  head(n = 10) %>%
  graph_from_data_frame() %>%
  ggraph(layout = "fr") +
  geom_edge_link(aes(edge_alpha = correlation), show.legend = FALSE) +
  geom_node_point(color = "lightblue", size = 5) +
  geom_node_text(aes(label = name), repel = TRUE) +
  theme_void()

ggsave("figs/bakunas.png")
