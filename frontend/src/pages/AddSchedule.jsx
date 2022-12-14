import React, { useState, useEffect } from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm/WorkingTimeForm';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';

const AddSchedule = () => {
  const messageText = 'The schedule was added!';
  const countOfTimeIntervals = 3;
  const formTitle = 'Add Schedule';
  const [formFields, setFormFields] = useState([]);

  useEffect(() => {
    const getFieldsInfo = async () => {
      await ManagerService.getScheduleFieldsOption()
        .then((response) => {
          setFormFields(response.data.fields);
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    };
    getFieldsInfo();
  }, []);

  return (
    <WorkingFormContext.Provider value={{ countOfTimeIntervals }}>
      <WorkingTimeForm
        formTitle={formTitle}
        formFields={formFields}
        service={ManagerService.addSchedule}
        messageText={messageText}
      />
    </WorkingFormContext.Provider>
  );
};

export default AddSchedule;
