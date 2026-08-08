from app.services.tools import (
    get_all_doctors,
    get_doctor_by_name,
    get_patient_appointments,
)


def execute_tool(tool_name, arguments, db):
    if tool_name == "get_all_doctors":
        return get_all_doctors(db)

    elif tool_name == "get_doctor_by_name":
        return get_doctor_by_name(
            db,
            arguments["doctor_name"]
        )

    elif tool_name == "get_patient_appointments":
        return get_patient_appointments(
            db,
            arguments["phone"]
        )

    return {
        "error": "Unknown tool."
    }