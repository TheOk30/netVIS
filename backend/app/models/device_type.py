import sqlite3
from app.core.DB_init import DB_PATH

def add_mapping(output_type, device_type):
    """
    Adds a device mapping to the database.

    Args:
        output_type (str): The output_type string to match.
        device_type (str): The corresponding device type.

    Returns:
        str: Success or error message.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO device_type_mappings (output_type, device_type) VALUES (?, ?)", (output_type, device_type))
        conn.commit()
        conn.close()
        return "Mapping added successfully!"
    except sqlite3.IntegrityError:
        return "Error: Mapping already exists."
    except Exception as e:
        return f"Error adding mapping: {e}"


def fetch_mapping_by_output_type(output_type):
    """
    Fetches a device mapping by output_type string.

    Args:
        output_type (str): The output_type string to match.

    Returns:
        tuple: The matching record (id, output_type, device_type) or None if not found.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM device_type_mappings WHERE output_type = ?", (output_type,))
    record = cursor.fetchone()
    conn.close()
    return record


def fetch_all_mappings():
    """
    Fetches all device mappings from the database.

    Returns:
        list[tuple]: List of all mappings (id, output_type, device_type).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM device_type_mappings")
    records = cursor.fetchall()
    conn.close()
    return records

def get_device_type(output_type):
    """
    Fetches the device type from the database based on the output_type string.

    Args:
        output_type (str): The string to match in the database.

    Returns:
        str: The corresponding device type if found, otherwise "unknown".
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT device_type FROM device_type_mappings WHERE output_type = ?", (output_type,))
        result = cursor.fetchone()
        return result[0] if result else "unknown"
    finally:
        conn.close()

def get_all_output_type():
    """
    Fetches all device type from the database.

    Args:
        None.

    Returns:
        str: Device types if found, otherwise "unknown".
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT output_type FROM device_type_mappings")
        result = cursor.fetchall()
        result = [type[0] for type in result]
        return result if result else "unknown"
    finally:
        conn.close()

def update_mapping(output_type, new_device_type):
    """
    Updates the device type for a given output_type string.

    Args:
        output_type (str): The output_type string to match.
        new_device_type (str): The new device type to set.

    Returns:
        str: Success or error message.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE device_type_mappings SET device_type = ? WHERE output_type = ?", (new_device_type, output_type))
    if cursor.rowcount == 0:
        conn.close()
        return "Error: Mapping not found."
    conn.commit()
    conn.close()
    return "Mapping updated successfully!"


def delete_mapping(output_type):
    """
    Deletes a device mapping by output_type string.

    Args:
        output_type (str): The output_type string to match.

    Returns:
        str: Success or error message.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM device_type_mappings WHERE output_type = ?", (output_type,))
    if cursor.rowcount == 0:
        conn.close()
        return "Error: Mapping not found."
    conn.commit()
    conn.close()
    return "Mapping deleted successfully!"
