import React from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm/WorkingTimeForm';
import { weekDays } from '../utils';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';

const formFields = [
  { title: 'name', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'address', type: 'textarea', required: false, helpText: 'This field is not required' },
  { title: 'working_time', weekDays: weekDays },
];

const AddLocation = () => {
  const messageText = 'The location was added!';
  const countOfTimeIntervals = 1;
  const formTitle =  'Add Location';
  return (
      <WorkingFormContext.Provider value={{ countOfTimeIntervals }}>
        <WorkingTimeForm
          formFields={formFields}
          formTitle={formTitle}
          service={ManagerService.addLocation}
          messageText={messageText}
        />
      </WorkingFormContext.Provider>
  );
};

export default AddLocation;
