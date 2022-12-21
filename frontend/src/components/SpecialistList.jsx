import React from 'react';
import { Grid, Container, Typography } from '@mui/material';
import SpecialistItem from './SpecialistItem';


const SpecialistList = ({ specialists }) => {
  return (
    <>
      <Grid container item rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        {specialists.map((specialist) => (
          <Grid key={specialist.email} item xs={4} sm={3} md={2}>
            <SpecialistItem specialist={specialist} />
          </Grid>
        ))}
      </Grid>
    </>
  );
};

export default SpecialistList;
