import React, { useState, useEffect } from 'react';
import Form from '../components/Form/Form';
import { AdminService } from '../services/auth.service';
import { messageTimeout } from '../utils';
import useFetching from '../hooks/useFetching';
import Loader from '../components/Loader';
import dayjs from 'dayjs';


const AddAppointment = () => {
  const [appointmentData, setAppointmentData] = useState({});
  const [showMessage, setShowMessage] = useState(false);
  const [formFields, setFormFields] = useState([]);
  const [fetching, isLoading, error] = useFetching(async () => {
    await AdminService.addAppointment(appointmentData);
    setShowMessage(true);
    setAppointmentData({});
    messageTimeout(3000, setShowMessage);
  }); 

  // console.log(appointmentData);

  const [fetchingFields, isLoadingFields] = useFetching(async () => {
    const response = await AdminService.appointmentFieldsOption();
    const fields = response.data.fields;
    fields['note']['type'] = 'textarea';
    delete fields.end_time;
    setFormFields(fields);
  });

  useEffect(() => {
    fetchingFields();
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    fetching();
  };

  return (
    <>
      {isLoading || isLoadingFields ? (
        <Loader />
      ) : (
        <Form
          formFields={formFields}
          formTitle="Add Appointment"
          data={appointmentData}
          setData={setAppointmentData}
          handleSubmit={handleSubmit}
          error={error}
          showMessage={showMessage}
          messageText="The appointment was created!"
        />
      )}
    </>
  );
};

export default AddAppointment;
