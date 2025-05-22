
from flask import Flask, render_template, jsonify, request, Response
import psycopg2
import csv
import io
app = Flask(__name__)

def obtener_ultimo_registro():
    conn = psycopg2.connect(
        dbname="estacion",
        user="postgres",
        password="postgres",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensores ORDER BY timestamp DESC LIMIT 1;")
    fila = cur.fetchone()
    conn.close()
    return fila

def obtener_extremos():
    conn = psycopg2.connect(
        dbname="estacion",
        user="postgres",
        password="postgres",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT
            MIN(temperatura), MAX(temperatura),
            MIN(humedad), MAX(humedad),
            MIN(presion), MAX(presion),
            MIN(mq135), MAX(mq135),
            MIN(lluvia), MAX(lluvia)
        FROM sensores
        WHERE timestamp >= NOW() - INTERVAL '12 HOURS';
    """)
    fila = cur.fetchone()
    conn.close()
    return fila


@app.route('/')
def index():
    return render_template("dashboard.html")

@app.route('/api/datos')
def api_datos():
    conn = psycopg2.connect(
        dbname="estacion",
        user="postgres",
        password="postgres",
        host="localhost"
    )
    cur = conn.cursor()

    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    if desde and hasta:
        cur.execute("""
            SELECT timestamp, temperatura, humedad, presion, mq135, lluvia
            FROM sensores
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp
        """, (desde, hasta))
        filas = cur.fetchall()
        conn.close()
        return jsonify([
            {
                "timestamp": f[0],
                "temperatura": f[1],
                "humedad": f[2],
                "presion": f[3],
                "mq135": f[4],
                "lluvia": f[5]
            } for f in filas
        ])
    else:
        actual = obtener_ultimo_registro()
        extremos = obtener_extremos()
        if actual and extremos:
            return jsonify({
                "timestamp": actual[1].isoformat(),
                "temperatura": actual[2],
                "humedad": actual[3],
                "presion": actual[4],
                "mq135": actual[5],
                "lluvia": actual[6],
                "min_max": {
                    "temperatura": [extremos[0], extremos[1]],
                    "humedad": [extremos[2], extremos[3]],
                    "presion": [extremos[4], extremos[5]],
                    "mq135": [extremos[6], extremos[7]],
                    "lluvia": [extremos[8], extremos[9]]
                }
            })
        return jsonify({})

@app.route('/exportar')
def exportar_csv():
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    conn = psycopg2.connect(
        dbname="estacion",
        user="postgres",
        password="postgres",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, temperatura, humedad, presion, mq135, lluvia
        FROM sensores
        WHERE timestamp BETWEEN %s AND %s
        ORDER BY timestamp
    """, (desde, hasta))
    filas = cur.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['timestamp', 'temperatura', 'humedad', 'presion', 'mq135', 'lluvia'])
    for row in filas:
        writer.writerow([
            row[0].strftime('%A, %Y-%m-%d %H:%M:%S.%f UTC'),  
            row[1], row[2], row[3], row[4], row[5]
    ])

    return Response(output.getvalue(), mimetype='text/csv', headers={
        "Content-Disposition": f"attachment; filename=datos_{desde}_{hasta}.csv"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

