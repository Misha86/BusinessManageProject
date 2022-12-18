import React, { useState, useEffect } from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';
import useFetching from '../hooks/useFetching';
import Loading from '../components/Loading';

const AddLocation = () => {
  const countOfTimeIntervals = 1;
  const formTitle = 'Add Location';
  const [formFields, setFormFields] = useState([]);
  const [fetching, isLoading] = useFetching(async () => {
    const response = await ManagerService.getLocationFieldsOption();
    setFormFields(response.data.fields);
  });

  useEffect(() => {
    fetching();
  }, []);

  return (
    <>
      {isLoading ? (
        <Loading />
      ) : (
        <WorkingFormContext.Provider value={{ countOfTimeIntervals }}>
          <WorkingTimeForm
            formTitle={formTitle}
            formFields={formFields}
            service={ManagerService.addLocation}
            messageText="The location was added!"
          />
        </WorkingFormContext.Provider>
      )}
    </>
  );
};

export default AddLocation;
