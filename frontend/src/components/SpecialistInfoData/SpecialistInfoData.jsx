import React from 'react';
import { Grid, Typography } from '@mui/material';
import SpecialistFullName from './SpecialistFullName';
import SpecialistAvatar from './SpecialistAvatar';
import SpecialistSchedule from './SpecialistSchedule';

const SpecialistInfoData = ({ specialist }) => {
  const fullName = `${specialist.first_name} ${specialist.last_name}`;
  return (
    <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
      <Grid item xs display="flex" mt={1} justifyContent="center" alignItems="center">
        <SpecialistFullName fullName={fullName} />
      </Grid>

      <Grid container item spacing={3}>
        <Grid item xs={6} sm={5} md={5}>
          <SpecialistAvatar avatar={specialist.avatar} alt={fullName} />
        </Grid>

        <Grid container item xs={12} spacing={2} sm={7} md={7} direction="column">
          <Grid item>
            <Typography variant="subtitle1" component="p">
              <b>POSITION: </b>
              {`${specialist.position}`.toUpperCase()}
            </Typography>
          </Grid>
          <Grid item>
            <Typography variant="subtitle1" component="p" sx={{ textAlign: 'justify' }}>
              <b>BIO: </b>
              {specialist.bio}
            </Typography>
          </Grid>
          <Grid item container direction="column">
            <Grid item>
              <Typography variant="subtitle1" component="p">
                <b>SCHEDULE: </b>
              </Typography>
            </Grid>
            <SpecialistSchedule specialist={specialist}/>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default SpecialistInfoData;