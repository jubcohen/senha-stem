from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)  
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calcular_digito(cpf_parcial):
        soma = sum(int(cpf_parcial[i]) * (10 - i) for i in range(9))
        digito = (soma * 10 % 11) % 10
        return str(digito)

    return cpf[9] == calcular_digito(cpf[:9]) and cpf[10] == calcular_digito(cpf[:10])

def validar_senha(senha, cpf, data_nasc):
    if len(senha) < 8 or len(senha) > 20:
        return "A senha deve ter entre 8 e 20 caracteres"
    if not re.search(r'[A-Z]', senha):
        return "A senha deve conter pelo menos uma letra maiúscula"
    if not re.search(r'[a-z]', senha):
        return "A senha deve conter pelo menos uma letra minúscula"
    if not re.search(r'\d', senha):
        return "A senha deve conter pelo menos um número"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return "A senha deve conter pelo menos um caractere especial"
    if " " in senha:
        return "A senha não pode conter espaços"
    if re.search(r'(.)\1{2,}', senha):  
        return "A senha não pode ter repetições excessivas de caracteres"
    if re.search(r'(123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', senha, re.IGNORECASE):
        return "A senha não pode conter sequências óbvias"
    if cpf and cpf in senha:
        return "A senha não pode conter o CPF"
    if data_nasc:
        data_formatada = data_nasc.replace("-", "")
        if data_formatada in senha:
            return "A senha não pode conter a Data de Nascimento"

    return None  # Senha válida

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    usuario = dados.get("usuario")
    cpf = dados.get("cpf", "")
    data_nasc = dados.get("dataNascimento", "")
    senha = dados.get("senha")

    if not usuario or not senha or not cpf or not data_nasc:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    if not validar_cpf(cpf):
        return jsonify({"erro": "CPF inválido"}), 400

    erro_senha = validar_senha(senha, cpf, data_nasc)
    if erro_senha:
        return jsonify({"erro": erro_senha}), 400

    # Simulando um usuário válido no banco de dados
    #usuario_correto = "usuario123"
    #senha_correta = "Senha@123"

    #if usuario == usuario_correto and senha == senha_correta:
       # return jsonify({"mensagem": "Login bem-sucedido"}), 200
    #else:
        #return jsonify({"erro": "Usuário ou senha incorretos"}), 401

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/validar-senha', methods=['POST'])
def verificar_senha():
    data = request.json  
    senha = data.get("senha")
    cpf = data.get("cpf")
    data_nasc = data.get("data_nasc")

    erro = validar_senha(senha, cpf, data_nasc)

    if erro:
        return jsonify({"valida": False, "erro": erro}), 400
    return jsonify({"valida": True, "mensagem": "Senha válida!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
