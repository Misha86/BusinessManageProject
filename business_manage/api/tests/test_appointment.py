"""The module includes tests for Appointment model, serializers and views."""

from django.utils.timezone import datetime, timedelta, get_current_timezone, make_aware
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from ..models import Location, CustomUser, Appointment
from ..services.customuser_services import add_user_to_group_specialist
from ..utils import string_to_time


class AppointmentModelTest(TestCase):
    """Class AppointmentModelTest for testing Appointment model."""

    def setUp(self):
        """This method adds needed info for tests."""
        self.user_data = {
            "email": "specialist@com.ua",
            "first_name": "FN",
            "last_name": "LN"
        }
        specialist = CustomUser.objects.create_user(**self.user_data)
        add_user_to_group_specialist(specialist)

        self.user_data.update(dict(email="user@com.ua"))
        self.user = CustomUser.objects.create_user(**self.user_data)

        location = Location.objects.create(name="office #1", working_time={})

        self.valid_data = {
            "start_time": datetime.combine(datetime.now().date(), string_to_time("09:15"),
                                           tzinfo=get_current_timezone()),
            "duration": timedelta(minutes=20),
            "specialist": specialist,
            "location": location,
            "customer_firstname": "customer_firstname",
            "customer_lastname": "customer_lastname",
            "customer_email": "customer@com.ua",
            "note": "",
        }

        self.appointment = Appointment.objects.create(**self.valid_data)

    def test_create_appointment_valid_data(self):
        """Test for creating appointment with valid data."""
        self.assertEqual(self.appointment.start_time, self.valid_data.get("start_time"))
        self.assertEqual(self.appointment.duration, self.valid_data.get("duration"))
        self.assertEqual(self.appointment.specialist, self.valid_data.get("specialist"))
        self.assertEqual(self.appointment.location, self.valid_data.get("location"))
        self.assertEqual(self.appointment.customer_firstname,
                         self.valid_data.get("customer_firstname"))
        self.assertEqual(self.appointment.customer_lastname,
                         self.valid_data.get("customer_lastname"))
        self.assertEqual(self.appointment.customer_email, self.valid_data.get("customer_email"))

    def test_appointment_end_time(self):
        """Test for appointment end time.

        End time should be more as start time.
        """
        start_time = self.appointment.start_time
        duration = self.appointment.duration
        end_time = start_time + duration
        self.assertEqual(self.appointment.end_time, end_time)
        self.assertGreater(self.appointment.end_time, start_time)

    def test_appointment_user_specialist(self):
        """Test for appointment specialist.

        User should be a specialist.
        """
        self.assertTrue(self.appointment.specialist.groups.filter(name="Specialist"))

    def test_appointment_user_not_specialist_error(self):
        """Test for appointment specialist validator.

        User should be a specialist (check by validator validate_specialist).
        """
        self.valid_data.update(dict(specialist=self.user))
        invalid_data = self.valid_data
        with self.assertRaises(ValidationError) as ex:
            appointment = Appointment(**invalid_data)
            full_name = appointment.specialist.get_full_name().title()
            appointment.full_clean()
        message = ex.exception.args[0]
        self.assertEqual(message, {full_name: f"{full_name} should be specialist."})

    def test_appointment_start_end_times_minutes_error(self):
        """Test for appointment start and end times format.

        Time values must have minutes multiples of 5.
        """
        for i in range(1, 5):
            invalid_minutes = datetime.strptime(f"21/11/2022 11:1{i}:00", "%d/%m/%Y %H:%M:%S")
            for time_value in ["start_time", "end_time"]:
                self.valid_data.update({f"{time_value}": invalid_minutes})

                with self.subTest(time_value=time_value):
                    invalid_data = self.valid_data

                    with self.assertRaises(ValidationError) as ex:
                        appointment = Appointment(**invalid_data)
                        appointment.full_clean()

                    message = ex.exception.args[0]
                    self.assertEqual(message, {
                        invalid_minutes.strftime("%H:%M:%S"):
                            "Time value must have zero seconds and minutes multiples of 5."
                    })

    def test_appointment_start_end_times_seconds_error(self):
        """Test for appointment start and end times format.

        Time values must have zero seconds.
        """
        seconds = datetime.strptime("21/11/2022 11:10:10", "%d/%m/%Y %H:%M:%S")
        for time_value in ["start_time", "end_time"]:
            self.valid_data.update({f"{time_value}": seconds})

            with self.subTest(time_value=time_value):
                invalid_data = self.valid_data

                with self.assertRaises(ValidationError) as ex:
                    appointment = Appointment(**invalid_data)
                    appointment.full_clean()

                message = ex.exception.args[0]
                self.assertEqual(message, {
                    seconds.strftime("%H:%M:%S"):
                        "Time value must have zero seconds and minutes multiples of 5."
                })

    def test_appointment_duration_minutes_error(self):
        """Test for appointment duration format.

        Duration value must have minutes multiples of 5.
        """
        for i in range(1, 5):
            invalid_minutes = timedelta(minutes=int(f"1{i}"))
            with self.subTest(invalid_minutes=invalid_minutes):
                self.valid_data.update({"duration": invalid_minutes})
                invalid_data = self.valid_data

                with self.assertRaises(ValidationError) as ex:
                    appointment = Appointment(**invalid_data)
                    appointment.full_clean()

                message = ex.exception.args[0]
                self.assertEqual(message, {
                    str(invalid_minutes):
                        "Duration value must have zero seconds and minutes multiples of 5."
                })

    def test_appointment_duration_seconds_error(self):
        """Test for appointment duration format.

        Duration value must have zero seconds..
        """
        seconds = timedelta(minutes=10, seconds=10)
        with self.subTest(seconds=seconds):
            self.valid_data.update({"duration": seconds})
            invalid_data = self.valid_data

            with self.assertRaises(ValidationError) as ex:
                appointment = Appointment(**invalid_data)
                appointment.full_clean()

            message = ex.exception.args[0]
            self.assertEqual(message, {
                str(seconds):
                    "Duration value must have zero seconds and minutes multiples of 5."
            })

    def test_appointment_time_range_past_datetime_error(self):
        """Test for appointment start and end times format.

        DateTime values should have current or future date.
        """
        invalid_date = make_aware(datetime.strptime("21/11/1900 11:10:00", "%d/%m/%Y %H:%M:%S"))
        for date_time_value in ["start_time", "end_time"]:
            self.valid_data.update({f"{date_time_value}": invalid_date})

            with self.subTest(date_time_value=date_time_value):
                invalid_data = self.valid_data

                with self.assertRaises(ValidationError) as ex:
                    appointment = Appointment(**invalid_data)
                    appointment.full_clean()

                message = ex.exception.args[0]
                self.assertEqual(message, {
                    invalid_date.strftime("%H:%M:%S"):
                        f"DateTime value {invalid_date} should have future datetime."
                })