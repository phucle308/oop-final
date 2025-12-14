class Appointment:
    def __init__(self, day_of_week, start_time_hour):
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0
        self.day_of_week = day_of_week
        self.start_time_hour = start_time_hour

    def get_client_name(self):
        return self.client_name

    def set_client_name(self, name):
        self.client_name = name

    def get_client_phone(self):
        return self.client_phone

    def set_client_phone(self, phone):
        self.client_phone = phone

    def get_appt_type(self):
        return self.appt_type

    def set_appt_type(self, type_code):
        self.appt_type = type_code

    def get_day_of_week(self):
        return self.day_of_week

    def set_day_of_week(self, day_of_week):
        self.day_of_week = day_of_week

    def get_start_time_hour(self):
        return self.start_time_hour

    def set_start_time_hour(self, start_time_hour):
        self.start_time_hour = start_time_hour

    def get_appt_type_desc(self):
        appt_types = {
            0: "Available",
            1: "Mens Cut",
            2: "Ladies Cut",
            3: "Mens Coloring",
            4: "Ladies Coloring"
        }
        return appt_types.get(self.appt_type, "Unknown")

    def get_end_time_hour(self):
        return self.start_time_hour + 1

    def schedule(self, client_name, client_phone, appt_type):
        self.client_name = client_name
        self.client_phone = client_phone
        self.appt_type = appt_type

    def cancel(self):
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0

    def format_record(self):
        return f"{self.client_name},{self.client_phone},{self.appt_type},{self.day_of_week},{self.start_time_hour:02d}"

    def __str__(self):
        start_time = f"{self.start_time_hour:02d}:00"
        end_time = f"{self.get_end_time_hour():02d}:00"

        return (
            f"{self.client_name:<20} "
            f"{self.client_phone:<15} "
            f"{self.day_of_week:<10} "
            f"{start_time} - {end_time}   "
            f"{self.get_appt_type_desc()}"
        )
