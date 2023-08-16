import psycopg2
from psycopg2 import OperationalError


def check_database():
    def try_connection(host):
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host=host,
            port="5432",  # nosec
        )

        # Crear un nuevo cursor
        cursor = connection.cursor()

        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("Estás conectado a - ", record, "\n")
        cursor.close()
        connection.close()
        print("La conexión a la base de datos fue exitosa: HOST %%%", host, "%%% ")

    try:
        try_connection("10.1.0.1")

    except OperationalError as e:
        print(
            f"El error '{e}' ocurrió. Es posible que la base de datos no esté funcionando o que las credenciales sean incorrectas."
        )

        try:
            try_connection("localhost")
        except OperationalError as e:
            print(
                f"El error '{e}' ocurrió. Es posible que la base de datos no esté funcionando o que las credenciales sean incorrectas."
            )
            try_connection("127.0.0.1")


if __name__ == "__main__":
    check_database()
