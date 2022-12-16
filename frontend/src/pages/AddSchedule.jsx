import React, {useState, useEffect} from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';

const AddSchedule = () => {
  const countOfTimeIntervals = 3;
  const formTitle = 'Add Schedule';
  const [created, setCreated] = useState(false)

  return (
    <WorkingFormContext.Provider value={{ countOfTimeIntervals, created, setCreated }}>
      <WorkingTimeForm
        formTitle={formTitle}
        created={created}
        setCreated={setCreated}
        serviceFields={ManagerService.getScheduleFieldsOption}
        service={ManagerService.addSchedule}
        messageText='The schedule was added!'
      />
    </WorkingFormContext.Provider>
  );
};

export default AddSchedule;
