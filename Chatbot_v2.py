import json
import os
from termcolor import colored
from datetime import datetime
import random
import re
import sys
import requests
class Chatbot:
  def __init__(self, name="ChatBot 2.0", claves_url=""):
    self.repetir=0
    self.name=name.title()
    self.tiempo_sesion=[]
    self.tiempo_tema_obj=[]
    self.tiempo_import=[]
    self.tiempo_indicador=[]
    self.tiempo_explorar=[]
    self.tiempo_verif=[]
    self.tiempo_aprend=[]
    self.tema=""
    self.objetivo=""
    self.emocion1=""
    self.emocion2=""
    self.conversacion="Registro de la conversación\n\n"
    self.solucion=""
    self.solucionA=""
    self.solucionB=""
    self.solucionAB=""

    self.Bot(1,"Bienvenido, mi nombre es", self.name)
    self.Bot(0,random.choice(["¿Cuál es tu nombre?", "¿Cómo te llamas?", "¿Con quién tengo el gusto?"]), ":")
    self.usuario=self.mensaje_usuario().title()
    self.Bot(1,"¿Cuáles son tus apellidos?", ":")
    self.usuario_apellido=self.mensaje_usuario().title()

    self.claves=self.Get_Diccionario_Claves(claves_url)

    self.bienvenida()
    
    while True:
      respuesta=self.mensaje_usuario()
      if respuesta.title() in self.claves["Afirmacion"]:
        self.Presentacion()
        break
      elif respuesta.title() in self.claves["Negacion"]:
        self.Despedida()
        break
      else:
        self.repetir+=1
        if self.repetir>3:
          self.No_avanza()
          break
        else:
          self.Respuesta_default()
    self.repetir=0


    # Actividades GROW
    self.titulo_grow=["Conversación", "Tema y Objs ", "Importancia ", "Indicador(s)",
                 "Explorar\t", "Verifica\t", "Aprendizaje "]
    self.Tema_obj()
    self.Importancia()
    self.Indicador()
    self.Explorar()
    self.Verificar()
    self.Aprendizaje()
    self.Despedida()

  ##############################################################################
  def Bot(self, bot=True,*mensaje):
    if bot==True:
      respuesta=self.name,":", *mensaje
    else:
      respuesta="\t", *mensaje
    respuesta=" ".join(respuesta)
    self.conversacion+=respuesta
    self.conversacion+="\n"
    print(colored(respuesta, "red", attrs=["bold"]))
  
  ##############################################################################
  def Presentacion(self):
    self.Bot(1, self.respuesta("Agradecimiento"), self.usuario,
          ", La sesión\n\t estará compuesta de 5 pasos",
          "\n\t * Primero hay que plantear el tema y objetivo de la sesión.",
          "\n\t * Segundo es la importancia que tiene la sesión para ti.",
          "\n\t * Tercero será explorar el tema y los elementos que la componen.",
          "\n\t * Cuarto es la verificación de las ideas propuestas.",
          "\n\t * Por último revisar el aprendizaje de la sesión.",
          "\n\t Comencemos    :-)")

    self.marco("inicio")
  
  ##############################################################################
  def Get_Diccionario_Claves(self, ruta=""):
    resp = requests.get(ruta)
    dictionary = json.loads(resp.text)
    return dictionary

  ##############################################################################
  def mensaje_usuario(self):
    mensaje=input("Usuario : ")
    self.conversacion+="Usuario : "
    self.conversacion+=mensaje
    self.conversacion+="\n"
    print()
    while True:
      if mensaje[-1]=="?" or mensaje=="":
        self.Respuesta_default()
        mensaje=self.mensaje=mensaje_usuario()
      else:
        break
    return mensaje

  ##############################################################################
  def respuesta(self, tema):
    return random.choice(self.claves[tema])

  ##############################################################################
  def bienvenida(self):
    self.Bot(1, self.respuesta("Agradecimiento"),self.usuario, ",\n",
          "\t Te comento, soy un Chatbot diseñado para Coaching estudiantil.",
          "\n\t Mi objetivo es poder ayudarte.\n\t ¿Te parece si comenzamos?")

  ##############################################################################
  def marco(self, concepto):
    if concepto=="inicio":
      self.tiempo_sesion.append(str(datetime.now())[:-7])
    elif concepto=="termino":
      self.tiempo_sesion.append(str(datetime.now())[:-7])
    texto="\n\t Hora de", concepto, ":", str(datetime.now())[:-7]
    print("-"*70)
    print(" ".join(texto))
    print("-"*70)
    self.conversacion+="-"*70
    self.conversacion+=" ".join(texto)
    self.conversacion+="-"*70
  
  
  ##############################################################################
  def Respuesta_default(self):
      self.Bot(1, self.respuesta("Default"))

  ##############################################################################
  def Tema_obj(self):
    self.Bot(1, self.respuesta("Agradecimiento"), self.usuario, ",",
          "\n\t ", self.respuesta("Tema"))
    self.tiempo_tema_obj.append(str(datetime.now())[:-7])

    self.tema=self.Cambiar_pronombres(self.mensaje_usuario())

    if self.tema[-1]=="s": 
      self.Bot(1, self.respuesta("Comprensiva"),",", self.tema.lower(), "te preocupan.")
    else:
      self.Bot(1, self.respuesta("Comprensiva"),",", self.tema.lower(), "te preocupa.")

    self.Bot(1, "Ahora bien, que objetivo te gustaría", self.respuesta("Verbo"), "con respecto a", self.tema.lower())
    self.Bot(0, "Recuerda utilizar un verbo en infinitivo para que yo pueda identificar el objetivo:")
    
    while True:
      respuesta_usuario=self.Cambiar_pronombres(self.mensaje_usuario())
      for palabra in respuesta_usuario.split(" "):
        if palabra[-2:] in ["ar", "er", "ir"]:
          i=respuesta_usuario.index(palabra)
          self.objetivo=respuesta_usuario[i:]
          break
        else:
          no_infinitivo=1
          self.repetir+=1
          if self.repetir>3:
            self.No_avanza()
            continue
      if self.objetivo!="":
        break
      else:
        self.Bot(1, self.respuesta("Default"))
        self.Bot(0, "A lo mejor no usaste un verbo en infinitivo")
        self.Bot(0, "Por favor vuelve a intentarlo")
    self.Bot(1 , self.respuesta("Comprensiva"))
    
    self.Bot(1, "Para esta sesión se abordará el tema de", self.tema.lower())
    if len(self.objetivo)==0:
      self.Bot(0, "Sin ningún objetivo en particular")

    else:
      self.Bot(0, "Con el siguiente objetivo en mente:")
      self.Bot(0, "\t *",self.objetivo)
    
    self.Bot(0)
    self.Bot(1, "Solo para saber como te sientes,")
    self.Bot(0, "¿Qué emoción o sentimiento estás experimentando actualmente al hablar de {0}?".format(self.tema.lower()))
    self.emocion1=self.Cambiar_pronombres(self.mensaje_usuario())

    self.tiempo_tema_obj.append(str(datetime.now())[:-7])
    
  ##############################################################################
  def Importancia(self):
    self.tiempo_import.append(str(datetime.now())[:-7])
    self.Bot(1, self.respuesta("Comprensiva"), self.usuario, ";")
    self.Bot(0, self.respuesta("Cambio"), ",")
    self.Bot(1, self.respuesta("Importancia"))
    respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
    self.Bot(0, self.respuesta("Rebotar"))
    respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
    self.Bot(1, self.respuesta("Comprensiva"))
    self.Bot(0, self.respuesta("Rebotar0").format(self.objetivo))
    respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
    self.tiempo_import.append(str(datetime.now())[:-7])

  ##############################################################################
  def Indicador(self):
    self.tiempo_indicador.append(str(datetime.now())[:-7])
    self.Bot(1, self.respuesta("Agradecimiento"), self.usuario)
    self.Bot(1, "Ya que estamos hablando sobre {0}".format(self.tema))
    self.Bot(0, "y que se ha establecido el objetivo para la sesión,")
    self.Bot(0, self.respuesta("Cambio"), self.usuario, ",")
    self.Bot(0, self.respuesta("Indicador"))
    respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
    while True:
      self.Bot(1, self.respuesta("Comprensiva"))
      self.Bot(0, self.respuesta("Indagar"))
      self.Bot(0, "O si ya estás conforme, solo dime 'No'")
      respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
      if self.Negativa(respuesta):
        break
    self.tiempo_indicador.append(str(datetime.now())[:-7])

  ##############################################################################
  def Explorar(self):
    self.tiempo_explorar.append(str(datetime.now())[:-7])
    self.Bot(1, self.respuesta("Agradecimiento"), self.usuario, ",")
    self.Bot(0, "Ahora exploremos los posibles resultados de poder", self.respuesta("Verbo"))
    self.Bot(0, "de forma exitosa ", self.tema, ".")
    explorar=["Explorar1","Explorar2","Explorar3"]
    for exp in explorar:
      self.Bot(1, self.respuesta(exp))
      respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
      if exp=="Explorar2" and self.solucionA=="":
        self.solucionA=respuesta.title()
      if exp=="Explorar3" and self.solucionB=="":
        self.solucionB=respuesta.title()
      self.Bot(1, self.respuesta("Comprensiva"))
    self.Bot(0)
    self.Bot(1, self.respuesta("Agradecimiento"), self.usuario, ",")
    self.Bot(0)
    self.Bot(1, "Si tuvieras que escoger entre:")
    self.Bot(0, "\tA)", self.solucionA)
    self.Bot(0, "\tB)", self.solucionB)
    self.Bot(0, "¿Cuál consideras mas viable? Indica el inciso,")
    self.solucionAB=self.Cambiar_pronombres(self.mensaje_usuario())[-1].upper()
    if self.solucionAB =="A":
      self.Bot(0)
      self.Bot(1, "Excelente selección, continuemos.")
      self.solucion=self.solucionA
    elif self.solucionAB =="B":
      self.Bot(0)
      self.Bot(1, "Muy bien, creo que es una buena opción.")
      self.solucion=self.solucionB
    else:
      self.Bot(0)
      self.Bot(1, "No seleccionaste un inciso valido, creo que andas distraido.")
      self.Bot(0, "Pero en mi opinión deberías escoger la A")
      self.solucion=self.solucionA
    self.tiempo_explorar.append(str(datetime.now())[:-7])

  ##############################################################################
  def Verificar(self):
    self.tiempo_verif.append(str(datetime.now())[:-7])
    self.Bot(1, self.respuesta("Agradecimiento"), self.usuario)
    self.Bot(0)
    self.Bot(0, "Ahora exploremos los posibles resultados de poder", self.respuesta("Verbo"))
    self.Bot(0, "de forma exitosa ", self.tema, ".")
    verificar=["Verificar1","Verificar2"]
    for verif in verificar:
      self.Bot(1, self.respuesta(verif).format(self.solucion))
      respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
    self.tiempo_verif.append(str(datetime.now())[:-7])

  ##############################################################################
  def Aprendizaje(self):
    self.tiempo_aprend.append(str(datetime.now())[:-7])
    self.Bot(1, self.respuesta("Agradecimiento"), self.usuario)
    self.Bot(0)
    self.Bot(1, self.respuesta("Afirmacion") , self.respuesta("Aprendizaje").format(self.usuario))
    respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
    self.Bot(1, self.respuesta("Comprensiva"))
    self.Bot(0, "¿Algún comentario final para agregar a la sesión de hoy?")
    respuesta=self.Cambiar_pronombres(self.mensaje_usuario())
    if respuesta.title() in self.claves["Afirmacion"]:
      self.Bot(1, self.respuesta("Comprensiva"), ", Te leo...")
      self.Cambiar_pronombres(self.mensaje_usuario())

    self.Bot(1, "Ya para casi terminar,")
    self.Bot(0, "¿Qué emoción o sentimiento estás experimentando actualmente?")
    self.emocion2=self.Cambiar_pronombres(self.mensaje_usuario())
    self.tiempo_aprend.append(str(datetime.now())[:-7])
    
  ##############################################################################
  def Despedida(self, corta=False):
    self.tiempo_sesion.append(str(datetime.now())[:-7])
    if corta:
      self.Bot(0, "Por mi parte es todo,", self.respuesta("Despedida"), self.usuario)
      self.marco("termino")
    else:
      self.Bot(1, self.respuesta("Agradecimiento"), self.usuario, ", espero que la sesión")
      self.Bot(0, "te haya sido de utilidad. Por mi parte es todo")
      self.Bot(0, self.respuesta("Despedida"))
      self.Resumen_final()
      self.marco("termino")
    input("Si quieres iniciar una nueva conversación, ejecuta la celda nuevamente.\n\nPresiona Enter para terminar la applicación.")
    sys.exit(0)
  
  ##############################################################################
  def No_avanza(self):
    self.Bot(1, "Disculpa, esta conversación no avanza, será mejor que intentemos en otra ocasión")
    self.Despedida(1)
  
  ##############################################################################
  def Negativa(self, respuesta):
    if respuesta.title() in self.claves["Negacion"]:
      self.Bot(1, self.respuesta("Comprensiva"), ", No te preocupes, sigamos avanzando")
      return True
    else:
      return False

  ##############################################################################
  def Cambiar_pronombres(self, texto):
    pron_usuario=["yo", "mi", "mio", "mis", "tu", "tuyo", "ti", "tus"]
    cambio=["tu", "tu", "tuyo", "tus", "yo", "mio", "mi", "mis"]
    lista=texto.split(" ")
    texto_cambio=[]
    for palabra in lista:
      for n, pron in enumerate(pron_usuario):
        if palabra.lower() == pron:
          palabra = cambio[n]
          break
      texto_cambio.append(palabra)
    texto_cambio[0]=texto_cambio[0].title()
    return " ".join(texto_cambio)

  ##############################################################################
  def Resumen_final(self):
    path=os.getcwd()
    with open(path + "Resumen " + self.usuario, "w+") as file:
      file.write("ChatBot name: {} \n\n".format(self.name))
      file.write("User name: {} \n\n".format(self.usuario))
      file.write("Chat tópico: {} \n".format(self.tema))
      file.write("Chat objectivo: \t * {} \n".format(self.objetivo))

      file.write("\n")
      file.write("\t\tTiempos GROW\n\n")
      tiempos=[self.tiempo_sesion, self.tiempo_tema_obj, self.tiempo_import, 
             self.tiempo_indicador, self.tiempo_explorar, self.tiempo_verif,
             self.tiempo_aprend]
      i=0
      print(self.titulo_grow)
      print(tiempos)
      print(i)
      for tiempo in tiempos:
        file.write(self.titulo_grow[i] + " : " + tiempo[0] + " hasta " + tiempo[1] + "\n")
        i+=1
      file.write("\n\n")
      file.write(self.conversacion)
