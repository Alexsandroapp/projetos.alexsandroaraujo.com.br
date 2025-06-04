from flask import Flask, render_template, request

app = Flask(__name__)

# Tabela simplificada (bitola mm² : corrente admissível A)
tabela_condutores = {
    1.5: 15,
    2.5: 21,
    4: 28,
    6: 36,
    10: 50,
    16: 68,
    25: 89,
    35: 110
}

def calcular_corrente(potencia, tensao, tipo_ligacao, fator_potencia, usar_fp):
    if usar_fp and fator_potencia:
        fp = fator_potencia
    else:
        fp = 1.0

    if tipo_ligacao == "monofasica":
        corrente = potencia / (tensao * fp)
    elif tipo_ligacao == "trifasica":
        corrente = potencia / (1.732 * tensao * fp)
    else:
        corrente = 0

    return round(corrente, 2)

def escolher_bitola(corrente_max):
    for bitola, capacidade in tabela_condutores.items():
        if corrente_max <= capacidade:
            return bitola, capacidade
    return "Acima de 35 mm²", ">110 A"

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        potencia = float(request.form["potencia"])
        tensao = float(request.form["tensao"])
        tipo = request.form["tipo"]
        corrente_nom = float(request.form["corrente_nom"])
        corrente_max = float(request.form["corrente_max"])
        usar_fp = request.form.get("usar_fp") == "on"
        fator_potencia = float(request.form["fator_potencia"]) if usar_fp else 1.0

        corrente_calc = calcular_corrente(potencia, tensao, tipo, fator_potencia, usar_fp)
        bitola, capacidade = escolher_bitola(corrente_max)

        faixa_disjuntor = f"{round(corrente_max * 1.1)} A até {round(corrente_max * 1.25)} A"

        resultado = {
            "corrente_calc": corrente_calc,
            "bitola": bitola,
            "capacidade": capacidade,
            "faixa_disjuntor": faixa_disjuntor
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
