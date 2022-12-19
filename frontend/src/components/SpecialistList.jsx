import React from 'react';
import { Grid, Container, Typography} from '@mui/material';
import SpecialistItem from './SpecialistItem';

const SpecialistList = ({ specialists }) => {
  return (
    <Container maxWidth="xl">
      <Grid item xs display="flex" justifyContent="center" alignItems="center">
        <Typography gutterBottom variant="h5" component="h5" color="gray">
          {specialists.length ? 'Specialists' : 'No Specialists yet!!!'}
        </Typography>
      </Grid>
      <Grid container rowSpacing={1} mt={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        {specialists.map((specialist) => (
          <Grid key={specialist.email} item xs={4} sm={3} md={2}>
            <SpecialistItem specialist={specialist} />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default SpecialistList;
