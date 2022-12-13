import React, { useState, useEffect } from 'react';
import { Grid, Container, Card, CardActionArea, CardMedia, CardContent, Typography, Box } from '@mui/material';
import UserService from '../services/user.service';

const Home = () => {
  const [specialists, setSpecialists] = useState([]);

  useEffect(() => {
    const getSpecialists = async () => {
      await UserService.getSpecialists()
        .then((response) => {
          setSpecialists(response.data.results);
        })
        .catch((error) => {
          console.log(error.data);
        });
    };
    getSpecialists();
  }, []);

  return (
    <Container maxWidth="xl">
      <Grid container rowSpacing={1} mt={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        {specialists.length ? (
          specialists.map((specialist) => (
            <Grid key={specialist.email} item xs={4} sm={3} md={2}>
              <Card>
                <CardActionArea>
                  <CardMedia component="img" height="auto" image={specialist.avatar} alt={specialist.email} />
                  <CardContent>
                    <Typography gutterBottom variant="subtitle1" component="div">
                      {`${specialist.first_name} ${specialist.last_name}`}
                    </Typography>
                    <Box component="p" sx={{ fontWeight: 900 }}>
                      {specialist.position}
                    </Box>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))
        ) : (
          <Grid item xs display="flex" justifyContent="center" alignItems="center">
            <Typography gutterBottom variant="h5" component="h5">
              No Specialists yet!!!
            </Typography>
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

export default Home;
