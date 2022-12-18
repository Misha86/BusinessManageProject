import React from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';

const AddLocation = () => {
  const countOfTimeIntervals = 1;
  const formTitle = 'Add Location';

  return (
    <>
      <WorkingFormContext.Provider value={{ countOfTimeIntervals }}>
        <WorkingTimeForm
          formTitle={formTitle}
          service={ManagerService.addLocation}
          serviceFields={ManagerService.getLocationFieldsOption}
          messageText="The location was added!"
        />
      </WorkingFormContext.Provider>
    </>
  );
};

export default AddLocation;
