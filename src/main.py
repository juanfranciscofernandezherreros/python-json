import mysql.connector
import json
import argparse

def fetch_data_from_db(table_name):
    # Configuración de la conexión a la base de datos
    config = {
        'user': 'root',
        'password': 'admin123',
        'host': 'localhost',
        'port': 6603,
        'database': 'sports'
    }

    # Conexión a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Consulta a la base de datos
    query = f"""
    SHOW COLUMNS FROM {table_name};
    """
    cursor.execute(query)

    # Obtención de los resultados de la consulta
    results = cursor.fetchall()

    # Definición de los nombres de las columnas
    column_names = [column[0] for column in cursor.description]

    # Creación de una lista de diccionarios con los resultados
    data = [dict(zip(column_names, row)) for row in results]

    # Cierre de la conexión
    cursor.close()
    connection.close()

    return data

# Función para convertir el tipo de dato MySQL al tipo de dato Java
def convert_type(mysql_type):
    if mysql_type.startswith("varchar"):
        return "String"
    elif mysql_type.startswith("int"):
        return "int"
    elif mysql_type.startswith("bigint"):
        return "long"
    # Agrega más conversiones de tipos si es necesario
    return "String"

# Función para convertir el JSON de entrada al formato deseado
def convert_json(input_data, table_name):
    # Convertir la primera letra del nombre de la tabla a mayúscula
    name = table_name.capitalize() 
    app_class_name = table_name.capitalize() + "Application"
    repository = table_name.capitalize() + "Repository"
    service = table_name.capitalize() + "Service"
    controller = table_name.capitalize() + "Controller"
    dtos = table_name.capitalize() + "Dto"
    mapper = table_name.capitalize() + "Mapper"

    output_data = {
        "projectName": f"{table_name}-q",
        "targetDirectory": f"{table_name}-q",
        "username": "xxxx",
        "newBranchName": "feature/XXXXX",
        "packageName": f"com.example.{table_name}",
        "appClassName": app_class_name,
        "entityName": name,
        "repositoryName": repository,
        "serviceName": service,
        "controllerName": controller,
        "exceptionName": "ResourceNotFoundException",
        "exceptionNameBadRequest": "BadRequestException",
        "handlerName": "GlobalExceptionHandler",
        "dtoName": dtos,
        "mapperName": mapper,
        "entityFields": [],
        "tableName": table_name.upper(),
        "urlName": table_name,
        "findByKeys": "find",
        "search": "search",
        "databaseConfig": {
            "username": "sa",
            "password": "",
            "host": "jdbc:h2:mem:testdb"
        }
    }

    for field in input_data:
        output_data["entityFields"].append({
            "type": convert_type(field["Type"]),
            "name": field["Field"].replace('_', ''),
            "nameEntity": field["Field"].replace('_', ''),
            "isPrimaryKey": "Y" if field["Key"] == "PRI" else "N",
            "isNotNull": "N" if field["Null"] == "YES" else "Y",
            "columnName": field["Field"]
        })

    return output_data

# Función para guardar JSON en un archivo
def save_to_json(data, filename='resultados.json'):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    # Configurar el analizador de argumentos
    parser = argparse.ArgumentParser(description="Fetch and convert MySQL table columns to JSON.")
    parser.add_argument("table_name", help="The name of the table to fetch columns from")

    args = parser.parse_args()

    # Obtener datos desde la base de datos
    raw_data = fetch_data_from_db(args.table_name)

    # Convertir los datos al nuevo formato
    converted_data = convert_json(raw_data, args.table_name)

    # Guardar el JSON convertido en un archivo
    save_to_json(converted_data, 'output.json')

    print(f"Consulta ejecutada, datos convertidos y JSON guardado en 'output.json' para la tabla {args.table_name}.")
