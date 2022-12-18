import React from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';

const AddSchedule = () => {
  const countOfTimeIntervals = 3;
  const formTitle = 'Add Schedule';

  return (
    <>
      <WorkingFormContext.Provider value={{ countOfTimeIntervals }}>
        <WorkingTimeForm
          formTitle={formTitle}
          service={ManagerService.addSchedule}
          serviceFields={ManagerService.getScheduleFieldsOption}
          messageText="The schedule was added!"
        />
      </WorkingFormContext.Provider>
    </>
  );
};

export default AddSchedule;
