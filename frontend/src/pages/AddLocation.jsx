import React, { useState } from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';

const AddLocation = () => {
  const countOfTimeIntervals = 1;
  const formTitle = 'Add Location';
  const [created, setCreated] = useState(false);

  return (
    <WorkingFormContext.Provider value={{ countOfTimeIntervals, created, setCreated }}>
      <WorkingTimeForm
        formTitle={formTitle}
        created={created}
        setCreated={setCreated}
        serviceFields={ManagerService.getLocationFieldsOption}
        service={ManagerService.addLocation}
        messageText="The location was added!"
      />
    </WorkingFormContext.Provider>
  );
};

export default AddLocation;
