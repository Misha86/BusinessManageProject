import React, { useEffect, useState } from 'react';
import WorkingTimeForm from '../components/WorkingTimeForm';
import { ManagerService } from '../services/auth.service';
import { WorkingFormContext } from '../context';

const AddLocation = () => {
  const messageText = 'The location was added!';
  const countOfTimeIntervals = 1;
  const formTitle = 'Add Location';
  const [formFields, setFormFields] = useState([]);

  useEffect(() => {
    const getFieldsInfo = async () => {
      await ManagerService.getLocationFieldsOption()
        .then((response) => {
          const fields = response.data.fields;
          fields['address']['type'] = 'textarea';
          setFormFields(fields);
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
        formFields={formFields}
        formTitle={formTitle}
        service={ManagerService.addLocation}
        messageText={messageText}
      />
    </WorkingFormContext.Provider>
  );
};

export default AddLocation;
