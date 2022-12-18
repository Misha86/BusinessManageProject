import React, { useState, useEffect } from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';
import useFetching from '../hooks/useFetching';
import Loading from '../components/Loading';

const AddSchedule = () => {
  const countOfTimeIntervals = 3;
  const formTitle = 'Add Schedule';
  const [formFields, setFormFields] = useState([]);
  const [fetching, isLoading] = useFetching(async () => {
    const response = await ManagerService.getScheduleFieldsOption();
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
            service={ManagerService.addSchedule}
            messageText="The schedule was added!"
          />
        </WorkingFormContext.Provider>
      )}
    </>
  );
};

export default AddSchedule;
