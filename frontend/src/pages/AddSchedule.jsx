import React from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm/WorkingTimeForm';
import { weekDays } from '../utils';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';

const formFields = [
  { title: 'specialist', type: 'email', required: true, helpText: 'This field is required. Input specialist email.' },
  { title: 'working_time', weekDays: weekDays },
];

const AddSchedule = () => {
  const messageText = 'The schedule was added!';
  const countOfTimeIntervals = 4;
  const formTitle = 'Add Schedule';
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
