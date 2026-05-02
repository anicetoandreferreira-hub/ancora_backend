from flask import Blueprint

ping = Blueprint("ping",__name__)

@ping.route("/ping")
def Ping():
  return "ping realizado com sucesso" , 200
  
