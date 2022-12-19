import React from 'react';
import { Grid, Container, Typography } from '@mui/material';
import SpecialistItem from './SpecialistItem';


const SpecialistList = ({ specialists }) => {
  return (
    <>
      <Grid item xs display="flex" mt={2} justifyContent="center" alignItems="center">
        <Typography gutterBottom variant="h5" component="h5" color="gray">
          {specialists.length ? 'Specialists' : 'No Specialists yet!!!'}
        </Typography>
      </Grid>
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
