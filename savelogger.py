import requests
import mysql.connector
from mysql.connector import Error

def get_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        response.raise_for_status()  
        ip_address = response.json()['origin']
        return ip_address
    except requests.exceptions.RequestException as e:
        print(f"Fout bij het ophalen van IP-adres: {e}")
        return None

def save_ip_to_db(ip_address):
    try:
        connection = mysql.connector.connect(
            host='localhost',         
            database='logger',     
            user='root',               
            password=''       
        )
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = "INSERT INTO ip_addresses (ip_address) VALUES (%s)"
            cursor.execute(insert_query, (ip_address,))
            connection.commit()
            print(f"[+] Het IP-adres {ip_address} is opgeslagen in de database.")
            
            cursor.close()

    except Error as e:
        print(f"Fout bij verbinding maken met MySQL: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()

def main():
    print("IP Adres Tracker")
    print("=================")
    

    ip_address = get_ip()
    
    if ip_address:
        print(f"Je publieke IP-adres is: {ip_address}")
        
       
        save_ip_to_db(ip_address)
    else:
        print("Kan je IP-adres niet ophalen.")

if __name__ == "__main__":
    main()
